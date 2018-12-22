Quran Utilities
=========

بسم الله الرحمن الرحيم

Quran utils is a set of scripts for detecting ayat in quran images. it's very rough, but it definitely works (tested on 3 sets of images - shamerly, qaloon, and warsh images).

Files
------
* `ayat.py` - detects ayah images in a particular image.
* `lines.py` - "detects" lines in a particular image
* `loop.py` - a verification utility.
* `main.py` - main loop for generating a database from images
* `make_transparent.py` - make an image with a white background transparent
* `make_white.py` - make an image with a transparent background white

ayat.py
---------
`ayat.py` is responsible for detecting ayah images inside a page image. note that it works best on images with a white background (see `make_white.py` if your image has a transparent background).

requirements:
* opencv and python bindings (`brew install homebrew/science/opencv`)
* matplotlib (`pip install matplotlib`)
* numpy (`pip install numpy`)

ideally, run something like this:

```
python -m virtualenv virtualenv
pip install -r requirements.txt
source virtualenv/bin/activate
```

you also need a template image. you make one by cutting out an ayah marker image from one of your pages. the threshold is set low enough such that it will match all of the marker images despite the different numbers. some examples exist under `images/templates`.

lines.py
---------
`lines.py` attempts to figure out where the lines are in a certain image. it does this by searching for white space between the images. consequently, it's the least accurate of the scripts. i typically verify it by running it across all images and making sure i get 15 lines for each page.

requirements:
* pillow (`pip install pillow`)

there are 3 numbers you'll find configured in the main - line height (approximate height of each line), max pixels (a threshold - how many pixels in a line make the line a quran line vs a line of tashkeel between two lines), and mode (0 or 1 - i think this is used for how to handle the very first line - pass 0 for most cases).

main.py
-----------
`main.py` is what outputs sql from a set of images. before running it, you want to make sure you can run `ayat.py` and validate its output, along with `lines.py` and validate its output. `main.py` is just a wrapper that combines the results from the above scripts to generate sql, which it prints to the command line.

to run it:
`python main.py images/shamerly images/template/shamerly.png > shamerly.out`

loop.py
---------
`loop.py` is used in conjunction with things like `find_errors.pl` to do some basic validation. i was using it to figure out where each sura starts/ends, so i could then
check that particular page and verify.

Quran Android
-------------
in order to be compatible with Quran Android, just generate a database file with similar structure to the existing ayahinfo database files.

    CREATE TABLE glyphs(
      glyph_id int not null,
      page_number int not null,
      line_number int not null,
      sura_number int not null,
      ayah_number int not null,
      position int not null,
      min_x int not null,
      max_x int not null,
      min_y int not null,
      max_y int not null,
      primary key(glyph_id)
    );
    CREATE INDEX sura_ayah_idx on glyphs(sura_number, ayah_number);
    CREATE INDEX page_idx on glyphs(page_number);

note: currently, `glyph_id` is set to `NULL` in the script, which is problematic. we can just put a number and increase it as need be, since using `AUTOINCREMENT` in sqlite has performance implications.
