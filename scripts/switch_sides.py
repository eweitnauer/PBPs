import shutil, argparse

parser = argparse.ArgumentParser(description="switch left side with right side for PBP scenes in given path")
parser.add_argument("problem", nargs='*', help="Path that contains the PBP scenes. If no path is given, the scenes are rendered empty.")
args = parser.parse_args()

for path in args.problem:
	for ext in ['svg', 'png']:
		for y in [1,2,3,4,5]:
			for x in [1,2]:
				shutil.move('%s/%d-%d.%s' % (path, y, x, ext), '/tmp/img.tmp')
				shutil.move('%s/%d-%d.%s' % (path, y, x+2, ext),
									  '%s/%d-%d.%s' % (path, y, x, ext))
				shutil.move('/tmp/img.tmp', '%s/%d-%d.%s' % (path, y, x+2, ext))