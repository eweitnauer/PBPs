from PIL import Image, ImageDraw, ImageFont

import argparse
parser = argparse.ArgumentParser(description="v1.0: Generate png-image for a PBP by composing its scenes, with 12 training scenes (compatible to pbp3).")
parser.add_argument("problem", nargs='*', help="Path that contains the PBP scenes. If no path is given, the scenes are rendered empty.")
parser.add_argument("-s", "--with-solution", help="print solution above the problem", action="store_true", dest="with_sol")
parser.add_argument("-n", "--with-number", help="print the problem number as title above the problem", action="store_true", dest="with_title")
parser.add_argument("-t", "--with-tests", help="include the test scenes in the problem", action="store_true", dest="with_tests")
parser.add_argument("-p", "--scene-positioning", help="is either 'sim' for similar scenes in one row, 'dis' for mixed up scenes (default: 'sim')", default="sim", dest="mapping", metavar="VAL")
parser.add_argument("-f", "--frame-file", help="Png image file containing an empty frame, used when no problem paths are given. Default: frame.png", default="frame.png", metavar="FILE", dest="frame_file")
parser.add_argument("-o", "--output-path", help="output path to which the pngs are written (default: 'complete')", default="complete", dest="out_dir", metavar="PATH")
parser.add_argument("-a", "--annotate", help="write scene names (A1, A2, ...) into each scene", action="store_true")
parser.add_argument("--no-gaps", help="there are no gaps between the scenes", action="store_true", dest="no_gaps")
args = parser.parse_args()

font_size_title = 24
font_size_sol = 16
gutter = 5
gap = -3 if args.no_gaps else 10
middle_gap = 40
test_gap = 30

sol_font = ImageFont.truetype("/Users/erik/Library/Fonts/Ubuntu-R.ttf", font_size_sol)
title_font = ImageFont.truetype("/Users/erik/Library/Fonts/Ubuntu-R.ttf", font_size_title)
annotate_font = ImageFont.truetype("/Users/erik/Library/Fonts/Ubuntu-B.ttf", 35)

solutions = {
  '02': ["one object", "two objects"]
 ,'04': ["squares", "circles"]
 ,'08': ["unstable situation", "stable situation"]
 ,'09': ["objects move in opposite directions", "objects move in same direction"]
 ,'11b': ["objects close to each other", "objects far from each other"]
 ,'12': ["small object falls off", "small object stays on top"]
 ,'13': ["objects form a tower", "objects form an arc"]
 ,'16': ["the circle is left of the square", "the square is left of the circle"]
 ,'18': ["object touch eventually", "objects don't touch eventually"]
 ,'18b': ["object touch eventually", "objects don't touch eventually"]
 ,'19': ["at least one object flies through the air", "all object always touch something"]
 ,'20': ["eventually, the square supports other objects", "eventually, the square does not support other objects"]
 ,'21': ["strong collision", "weak or no collision"]
 ,'22': ["objects collide with each other", "objects don't collide with each other"]
 ,'23': ["collision", "no collision"]
 ,'24': ["several possible outcomes", "one possible outcome"]
 ,'26': ["circle moves right", "circle moves left"]
 ,'27': ["(potential) chain reaction","no chain reaction"]
 ,'28': ["rolls well", "does not roll well"]
 ,'30': ["less stable situation", "stable situation"]
 ,'31': ["circle can be picked up directly", "circle cannot be picked up directly"]
 ,'32': ["objects rotate a lot", "objects rotate little or no at all"]
 ,'33': ["construction gets destroyed", "construction stays intact"]
 ,'__empty__': ["solution left", "solution right"]
}

# as in pbp3
dis_maps = {
  'dis': [[[1,1],[3,2],[2,3],[1,4]],
          [[2,1],[1,2],[3,3],[2,4]],
          [[3,1],[2,2],[1,3],[3,4]],
          [[4,1],[4,2],[4,3],[4,4]],
          [[5,1],[5,2],[5,3],[5,4]]]
 ,'sim': [[[1,1],[1,2],[1,3],[1,4]],
          [[2,1],[2,2],[2,3],[2,4]],
          [[3,1],[3,2],[3,3],[3,4]],
          [[4,1],[4,2],[4,3],[4,4]],
          [[5,1],[5,2],[5,3],[5,4]]]
}

if (len(args.problem) == 0): args.problem.append("__empty__")

def pos2AB(y, x):
  return ("A" if ix < 2 else "B") + str(1+y*2+(x%2))

for pbp_path in args.problem:
  if (pbp_path == "__empty__"):
    scene_img = Image.open(args.frame_file)
  else:
    scene_img = Image.open("%s/1-1.png" % pbp_path)
  sw, sh = scene_img.size
  pbp_name = pbp_path[pbp_path.rfind('pbp'):]

  xs = [gutter]; xs.append(xs[-1] + sh+gap); xs.append(xs[-1] + sh+middle_gap)
  xs.append(xs[-1] + sh+gap); xs.append(xs[-1] + sh+gutter)
  ys = [gutter]
  if args.with_sol: ys[0] += 2*font_size_sol
  if args.with_title: ys[0] += 2*font_size_title
  ys.append(ys[-1] + sh+gap); ys.append(ys[-1] + sh+gap);
  if args.with_tests:
    ys.append(ys[-1] + sh+test_gap); ys.append(ys[-1] + sh+gap);
  ys.append(ys[-1] + sh+gutter);

  img = Image.new("RGB", (xs[-1],ys[-1]), "white")
  draw = ImageDraw.Draw(img)

  for iy in range(len(ys)-1):
      for ix in range(len(xs)-1):
        scene_idx = dis_maps[args.mapping][iy][ix];
        if (pbp_path != "__empty__"):
          scene_img = Image.open("%s/%d-%d.png" % (pbp_path, scene_idx[0], scene_idx[1]))
        img.paste(scene_img, (xs[ix],ys[iy]))
        if args.annotate:
          text = " " + pos2AB(scene_idx[0]-1, scene_idx[1]-1)
          size = annotate_font.getsize(text)
          draw.text((xs[ix], ys[iy]), text, (200,200,200), font=annotate_font)

  draw.rectangle((round(xs[-1]/2-6),ys[0],round(xs[-1]/2+6),ys[-1]-gutter-1), fill='black')
  draw.rectangle((round(xs[-1]/2-4),ys[0]+2,round(xs[-1]/2+4),ys[-1]-gutter-3), fill='#aaa')
  if args.with_title:
    title = "Physical Bongard Problem %s" % pbp_name[3:]
    size = title_font.getsize(title)
    draw.text((round(xs[-1]/2-size[0]/2), gutter), title, (0,0,0), font=title_font)
  if args.with_sol:
    solution = solutions[pbp_name[3:]]
    bbox = [sol_font.getsize(solution[0]), sol_font.getsize(solution[1])]
    y = gutter if not args.with_title else gutter + 2*font_size_title
    draw.text((round(xs[-1]/4)-bbox[0][0]/2, y), solution[0], (0,0,0), font=sol_font)
    draw.text((round(3*xs[-1]/4)-bbox[1][0]/2, y), solution[1], (0,0,0), font=sol_font)
  del draw

  if (pbp_path == "__empty__"):
    name = "%s/empty_grid.png" % (args.out_dir)
  else:
    name = "%s/%s.png" % (args.out_dir, pbp_name)
  print("writing %s" % name)
  img.save(name)