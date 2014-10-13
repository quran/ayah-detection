import sys
from PIL import Image, ImageDraw

"""
algorithm for determining rows
- find out the number of non-white pixels in each row
- rows with low pixel count (20 and below, for example) are break points
- combine them into ranges, such that we have line+1 groups
- if midpoint[i+1] - height is within range, use it - otherwise, start at
  either low[i] and end at low[i] + height or at high[i] and end after height
  depending on where we are relative to the range at i

then, for each line's ys, find the min x and max across them.
we then have the bounding box for each line
"""

def is_not_blank(pt):
   return sum(pt) < 200 * len(pt)

def find_lines(image, line_height, max_pixels, mode):
   ranges = []
   range_end = -1
   range_start = -1
   restrict_lines = True
   if mode == 1:
      restrict_lines = False

   data = image.getdata()
   width, height = image.size
   for y in range(0, height):
      filled_pixels = 0
      for x in range(0, width):
         pt = data[y * width + x]
         if is_not_blank(pt):
            filled_pixels = filled_pixels + 1
      # print "line " + str(y) + " has " + str(filled_pixels)
      if filled_pixels < max_pixels:
         if range_start == -1:
            if restrict_lines and filled_pixels == 0 and len(ranges) == 0:
               continue
            range_start = y
            range_end = y
         elif y - range_end < 20:
            range_end = y
         else:
            # print "adding range " + str(range_start) + "," + str(range_end)
            ranges.append((range_start, range_end))
            range_start = -1
            range_end = -1
   if range_start > -1:
     ranges.append((range_start, range_end))

   line_ys = []
   should_skip = False
   for i in range(0, len(ranges) - 1):
      if should_skip:
         should_skip = False
         continue
      top = ranges[i]
      bottom = ranges[i + 1]
      midpoint = (bottom[0] + bottom[1]) / 2
      
      if bottom[1] - top[0] < line_height:
         top_midpoint = ((top[0] + top[1]) / 2)
         top = (top_midpoint, midpoint)
         bottom = ranges[i + 2]
         midpoint = (bottom[0] + bottom[1]) / 2
         should_skip = True

      top_y = midpoint - line_height
      if top_y >= top[0] and top_y <= top[1]:
         # within range, we keep it
         line_ys.append((top_y, midpoint))
      elif top_y < top[0]:
         if top[0] + line_height < height:
            line_ys.append((top[0], top[0] + line_height))
      else:
         if top[1] + line_height < height:
            line_ys.append((top[1], top[1] + line_height))

   lines = []
   for yrange in line_ys:
      first_x = width
      last_x = 0
      for y in range(yrange[0], yrange[1]):
         for x in range(0, width):
            pt = data[y * width + x]
            if is_not_blank(pt):
               if first_x > x:
                  first_x = x - 1
               break
         for x in reversed(range(0, width)):
            pt = data[y * width + x]
            if is_not_blank(pt):
               if x > last_x:
                  last_x = x
               break
      lines.append(((first_x, yrange[0]), (last_x, yrange[1])))
   return lines

# for debugging, this method draws boxes around each line
def draw(image, lines, output):
   draw = ImageDraw.Draw(image)
   for line in lines:
      draw.rectangle([line[0], line[1]], None, (255, 0, 0))
   del draw
   image.save(output)

if __name__ == "__main__":
   if len(sys.argv) < 2:
      print "usage: " + sys.argv[0] + " [image]"
      sys.exit(1)
   image = Image.open(sys.argv[1]).convert('RGBA')

   # 100/35/0 for warsh
   # 110/87/0 for shamerly
   # 175/75/1 for qaloon
   lines = find_lines(image, 175, 75, 1)
   for line in lines:
      print line
   draw(image, lines, 'test.png')
   print "lines: %d" % len(lines)
