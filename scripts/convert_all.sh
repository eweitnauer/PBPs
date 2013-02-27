# descends into all pbp* subdirectories and converts the svg-files to png-files of the width=height=$1 (first parameter)
if [ -z "$1" ]; then
  echo "usage: convert.sh png_size [output_dir]"
else
	output_dir=${2-.}
	shopt -s nullglob # let pbp* and *.svg be empty if there are not svg files
	for i in pbp*
	do
		mkdir -p "$output_dir/$i"
		cd $i
		for s in *.svg
		do
			echo $s && /Applications/Inkscape.app/Contents/Resources/bin/inkscape --export-area-drawing -h=$1 -b=white $s --export-png "../$output_dir/$i/`echo $s | sed -e 's/svg$/png/'`"
		done
		cd ..
	done
fi
