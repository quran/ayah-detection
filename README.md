# Quran Utilities

بسم الله الرحمن الرحيم

Quran utils is a set of scripts for detecting ayat in quran images. it's very rough, but it definitely works (tested on 3 sets of images - shamerly, qaloon, and warsh images).

## Files

* `ayat.py` - detects ayah images in a particular image.
* `lines.py` - "detects" lines in a particular image
* `loop.py` - a verification utility.
* `main.py` - main loop for generating a database from images
* `make_transparent.py` - make an image with a white background transparent
* `make_white.py` - make an image with a transparent background white

## Setup

ideally, run something like this:

```sh
python3 -m venv virtualenv
source virtualenv/bin/activate
pip install -r requirements.txt
```

## Suggested Workflow

- crop the images first (if necessary).
- assuming images with a white background, make the images transparent.
- if the images were already transparent, make a copy with white backgrounds.
- using an image editor, cut out an ayah marker from any page.
- while in the image editor, figure out the approximate height of each line.
- run ayah detection on a few pages, validating by looking at `res.png`.
- run line detection on a few pages, validating by looking at `temp.png`.
- run the loop script across all images to validate the data (search for pages
  with no images found, for example).

```sh
# -u so it's unbuffered
python -u loop.py /path/ template.png | tee output.txt
```

- when done, validate output.txt using the error checking script. this is
  really important since it helps find errors (ex missed pages, not enough
  ayahs parsed on a page, etc).
- when everything looks fine, run main.py after tweaking values.
- revalidate the output using the error checking script.
- note: if main.py breaks due to index out of bounds, etc, double check the
  values. chances are something is off (check to ensure that the correct start
  sura, end sura, and number of ayahs per sura are set).
- in some cases, having multiple ayah templates helps (or otherwise reducing
  the accuracy, but this could lead to false positives).
- note: reading the sql output can also help pinpoint issues - ex if you
  expect page 50 to be the start of sura Al-i-'Imran and it's actually writing
  sql that indicates its for an ayah in sura Baqarah, then you know that an
  ayah might not have been detected in sura Baqarah for example.


## Scripts

### make_transparent.py

`make_transparent.py` takes in an image with a white background and attempts
to make the background transparent. there are some tweakable parameters within
the script, and it can theoretically be used with other background colors
given the correct amount of tweaking.


### make_white.py

`make_white.py` takes in a transparent image and makes all the transparent
pixels white. this is helpful when images with white backgrounds are needed
for better accuraccy while running `ayat.py` or `lines.py`.


### ayat.py

`ayat.py` is responsible for detecting ayah images inside a page image. note that it works best on images with a white background (see `make_white.py` if your image has a transparent background).

requirements:

* opencv and python bindings (`brew install homebrew/science/opencv`)
* matplotlib (`pip install matplotlib`)
* numpy (`pip install numpy`)

you also need a template image. you make one by cutting out an ayah marker image from one of your pages. the threshold is set low enough such that it will match all of the marker images despite the different numbers. some examples exist under `images/templates`.

### lines.py

`lines.py` attempts to figure out where the lines are in a certain image. it does this by searching for white space between the images. consequently, it's the least accurate of the scripts. i typically verify it by running it across all images and making sure i get 15 lines for each page. run this on pages with white backgrounds for better results.

requirements:

* pillow (`pip install pillow`)

there are 3 numbers you'll find configured in the main - line height (approximate height of each line), max pixels (a threshold - how many pixels in a line make the line a quran line vs a line of tashkeel between two lines), and mode (0 or 1 - i think this is used for how to handle the very first line - pass 0 for most cases).

### main.py

`main.py` is what outputs sql from a set of images. before running it, you want to make sure you can run `ayat.py` and validate its output, along with `lines.py` and validate its output. `main.py` is just a wrapper that combines the results from the above scripts to generate sql, which it prints to the command line.

to run it:
`python main.py images/shamerly images/template/shamerly.png > shamerly.out`

### loop.py

`loop.py` is used in conjunction with things like `find_errors.pl` to do some basic validation. i was using it to figure out where each sura starts/ends, so i could then
check that particular page and verify.

### Quran Android

in order to be compatible with Quran Android, just generate a database file with similar structure to the existing ayahinfo database files.

```sql
    CREATE TABLE glyphs(
      glyph_id int primary key,
      page_number int not null,
      line_number int not null,
      sura_number int not null,
      ayah_number int not null,
      position int not null,
      min_x int not null,
      max_x int not null,
      min_y int not null,
      max_y int not null
    );
    CREATE INDEX sura_ayah_idx on glyphs(sura_number, ayah_number);
    CREATE INDEX page_idx on glyphs(page_number);
```

note: currently, `glyph_id` is set to `NULL` in the script, which is problematic. we can just put a number and increase it as need be, since using `AUTOINCREMENT` in sqlite has performance implications.


### Experimental Scripts

#### marker_remover.py

`marker_remover.py` is an experimental script to remove markers. it uses the template marker as a "blueprint" by which it tries to remove existing markers. it figures out how amny pixels there are in each row of the template. it then tries to use that as an input to figure out how many pixels to remove from that particular row of the actual image. this is experimental and pretty dangerous, since it can eat pieces of touching ayahs, especially when things are really close together. really recommend using a tool like [kaleidoscope](https://www.kaleidoscopeapp.com) to overlay the image without the ayahs on top of the ones with the ayahs and see that nothing extra is cut out, etc. configure its values at the top of the script.


#### header_remover.py

`header_remover.py` experimentally removes headers. it's safer than `marker_remover.py` and easier to validate, but still pretty experimental. configure its values in the top of the script.


#### find_ayat_v2.py

`find_ayat_v2.py` is a simpler version of `ayat.py` that uses OpenCV to find contours instead. consequently, this script doesn't need a template image. the downside of this approach, however, is that it can have many false positives since certain letters can still be detected as contours. this can greatly be reduced if the ayah markers have colors, which most do - simply checking for colors in a certain range greatly reduces (if not completely eliminates) these false positives. this is the recommended approach moving forward in sha' Allah. the old `ayat.py` will stay around since, in some cases, `ayat.py` works better than `find_ayat_v2.py` (also, `ayat.py` powers the `header_remover.py` script). whenever possible, use `find_ayat_v2.py`, but if it doesn't work well for the particular type of image, use `ayat.py`.


#### marker_remover_v2.py

`marker_remover_v2.py` is an updated version of `marker_remover.py` that uses `find_ayat_v2.py` to find and remove markers from pages. initial tests are very promising al7amdulillah. whenever v2 works, this is the recommended approach. fallback to v1 only when v2 doesn't work.
