from PIL import Image, ImageDraw, ImageFont
import math
import re
import argparse
parser = argparse.ArgumentParser(description="v1.1: Generate png-image for a PBP by composing its scenes (compatible to mturk experiment 3.2 or 4.0)")
parser.add_argument("problem", nargs='*', help="Path that contains the PBP scenes. If no path is given, the scenes are rendered empty.")
parser.add_argument("-s", "--with-solution", help="print solution above the problem", action="store_true", dest="with_sol")
parser.add_argument("-n", "--with-number", help="print the problem number as title above the problem", action="store_true", dest="with_title")
parser.add_argument("-t", "--with-tests", help="include the test scenes in the problem", action="store_true", dest="with_tests")
parser.add_argument("--no-test-gap", help="show no vertical gap between training and test scenes", action="store_true", dest="no_test_gap")
parser.add_argument("-c", "--condition", help="{interleaved,blocked,simultaneous}-{sim,dis}-{sim,dis}, default is 'interleaved-sim-sim'.\
 The similarities are category similarities.", default="interleaved-sim-sim", dest="mapping", metavar="VAL")
parser.add_argument("-f", "--frame-file", help="Png image file containing an empty frame, used when no problem paths are given. Default: frame.png", default="frame.png", metavar="FILE", dest="frame_file")
parser.add_argument("-a", "--annotate", help="write scene names (A1, A2, ...) into each scene", action="store_true")
parser.add_argument("-o", "--output-path", help="output path to which the pngs are written (default: '.')", default=".", dest="out_dir", metavar="PATH")
parser.add_argument("-e", "--experiment-version", help="3.2 (default) or 4.0", default="3.2", dest="exp_ver", metavar="EXP_VER")

args = parser.parse_args()

font_size_title = 28
font_size_sol = 16
gutter = 5
gap = -2
middle_gap = 40
test_gap = 18
if args.no_test_gap: test_gap = gap

sol_font = ImageFont.truetype("/Users/erik/Library/Fonts/Ubuntu-R.ttf", font_size_sol)
title_font = ImageFont.truetype("/Users/erik/Library/Fonts/Ubuntu-R.ttf", font_size_title)
annotate_font = ImageFont.truetype("/Users/erik/Library/Fonts/Ubuntu-B.ttf", 35)

solutions = {
  '02': ["one object", "two objects"]
 ,'03': ["big objects", "small objects"]
 ,'04': ["squares", "circles"]
 ,'05': ["objects move", "objects don't move"]
 ,'06': ["objects move to the left", "objects move to the right"]
 ,'07': ["fast movement", "slow movement"]
 ,'08': ["unstable situation", "stable situation"]
 ,'09': ["objects move in opposite directions", "objects move in same direction"]
 ,'10': ["rotation", "no rotation"]
 ,'11': ["the objects will eventually be close to each other", "the objects are far from each other"]
 ,'11b': ["objects close to each other", "objects far from each other"]
 ,'12': ["small object falls off", "small object stays on top"]
 ,'13': ["objects form a tower", "objects form an arc"]
 ,'14': ["vertical construction", "horizontal construction"]
 ,'15': ["circle does not hit right between the other objects", "circle hits right between the other objects"]
 ,'16': ["the circle is left of the square", "the square is left of the circle"]
 ,'17': ["objects touch", "objects don't touch"]
 ,'18': ["object touch eventually", "objects don't touch eventually"]
 ,'18b': ["object touch eventually", "objects don't touch eventually"]
 ,'19': ["at least one object flies through the air", "all object always touch something"]
 ,'20': ["eventually, the square supports other objects", "eventually, the square does not support other objects"]
 ,'21': ["strong collision", "weak or no collision"]
 ,'22': ["objects collide with each other", "objects don't collide with each other"]
 ,'23': ["collision", "no collision"]
 ,'24': ["several possible outcomes", "one possible outcome"]
 ,'25': ["objects do not topple over", "the object topples over"]
 ,'26': ["circle moves right", "circle moves left"]
 ,'27': ["(potential) chain reaction","no chain reaction"]
 ,'28': ["rolls well", "does not roll well"]
 ,'29': ["circle could move to one side", "circle could move to both sides"]
 ,'30': ["less stable situation", "stable situation"]
 ,'31': ["circle can be picked up directly", "circle cannot be picked up directly"]
 ,'32': ["objects rotate a lot", "objects rotate little or no at all"]
 ,'33': ["construction gets destroyed", "construction stays intact"]
 ,'34': ["object falls to the left", "object falls to the right"]
 ,'__empty__': ["solution left", "solution right"]
}

def pos2AB(y, x):
  return ("A" if x < 2 else "B") + str(1+y*2+(x%2))

def AB2pos(side, number):
  x = (number-1)%2+1
  if side=='B': x+=2
  y = int(math.floor((number-1)/2)+1)
  return [y,x]

def f(pair_str):
  m = re.search('([AB])(\d+)([AB])(\d+)', pair_str)
  return [AB2pos(m.group(1), int(m.group(2))), AB2pos(m.group(3), int(m.group(4)))]

# positions scenes as in pbp3.2 an pbp4
# we use category similarities here, so int-sim-dis and int-dis-sim are swapped.
if args.exp_ver == '3.2':
  positions = {
     'interleaved-sim-sim': [f(pair) for pair in ['A1B1', 'A2B2', 'A3B3', 'A4B4', 'A5B5', 'A6B6', 'A7B7', 'A8B8', 'A9B9', 'A10B10']]  # wi: 8 bw: 4
    ,'interleaved-sim-dis': [f(pair) for pair in ['A1B3', 'A2B4', 'A3B5', 'A4B6', 'A5B7', 'A6B8', 'A7B1', 'A8B2', 'A9B9', 'A10B10']]  # wi: 8 bw: 0
    ,'interleaved-dis-sim': [f(pair) for pair in ['A1B1', 'A3B3', 'A5B5', 'A7B7', 'A2B2', 'A4B4', 'A6B6', 'A8B8', 'A9B9', 'A10B10']]  # wi: 0 bw: 4
    ,'interleaved-dis-dis': [f(pair) for pair in ['A1B3', 'A5B7', 'A4B2', 'A8B6', 'A3B1', 'A7B5', 'A2B4', 'A6B8', 'A9B9', 'A10B10']]  # wi: 0 bw: 0
    ,'blocked-sim-sim':     [f(pair) for pair in ['A1A2', 'B1B2', 'A3A4', 'B3B4', 'A5A6', 'B5B6', 'A7A8', 'B7B8', 'A9A10', 'B9B10']]  # wi: 8 bw: 4
    ,'blocked-sim-dis':     [f(pair) for pair in ['A1A2', 'B3B4', 'A5A6', 'B7B8', 'A3A4', 'B1B2', 'A7A8', 'B5B6', 'A9A10', 'B9B10']]  # wi: 8 bw: 0
    ,'blocked-dis-sim':     [f(pair) for pair in ['A1A3', 'B1B3', 'A2A4', 'B2B4', 'A5A7', 'B5B7', 'A6A8', 'B6B8', 'A9A10', 'B9B10']]  # wi: 0 bw: 6
    ,'blocked-dis-dis':     [f(pair) for pair in ['A1A5', 'B3B7', 'A6A2', 'B8B4', 'A7A3', 'B5B1', 'A4A8', 'B2B6', 'A9A10', 'B9B10']]} # wi: 0 bw: 2
elif args.exp_ver == '4' or args.exp_ver == '4.0':
  positions = {
     'interleaved-sim-sim':  [f(pair) for pair in ['A1B1', 'A2B2', 'A3B3', 'A4B4', 'A5B5', 'A6B6', 'A7B7', 'A8B8', 'A9B9', 'A10B10']]
    ,'simultaneous-sim-sim': [f(pair) for pair in ['A1A2', 'B1B2', 'A3A4', 'B3B4', 'A5A6', 'B5B6', 'A7A8', 'B7B8', 'A9A10', 'B9B10']]
    ,'simultaneous-sim-dis': [f(pair) for pair in ['A1A2', 'B3B4', 'A5A6', 'B7B8', 'A3A4', 'B1B2', 'A7A8', 'B5B6', 'A9A10', 'B9B10']]
    ,'simultaneous-dis-sim': [f(pair) for pair in ['A1A3', 'B1B3', 'A5A7', 'B5B7', 'A4A2', 'B4B2', 'A8A6', 'B8B6', 'A9A10', 'B9B10']]
    ,'simultaneous-dis-dis': [f(pair) for pair in ['A1A5', 'B3B7', 'A3A7', 'B1B5', 'A6A2', 'B8B4', 'A8A4', 'B6B2', 'A9A10', 'B9B10']]}


if (len(args.problem) == 0): args.problem.append("__empty__")

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
  ys.append(ys[-1] + sh+gap); ys.append(ys[-1] + sh+gap); ys.append(ys[-1] + sh+gap);
  if args.with_tests: ys.append(ys[-1] + sh+test_gap);
  ys.append(ys[-1] + sh+gutter);

  img = Image.new("RGB", (xs[-1],ys[-1]), "white")
  draw = ImageDraw.Draw(img)
  for iy in range(len(ys)-1):
      for ix in range(len(xs)-1):
        if (pbp_path != "__empty__"):
          if args.mapping.startswith('blocked') or args.mapping.startswith('simultaneous'):
            scene_idx = positions[args.mapping][2*iy+int(ix/2)][ix%2];
          else:
            scene_idx = positions[args.mapping][2*iy+ix%2][int(ix/2)];
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
