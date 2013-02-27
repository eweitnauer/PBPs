# descends into all pbp* subdirectories and converts the svg-files to png-files of the width=height=$1 (first parameter)
if [ -z "$1" ]; then
  echo "pass target size of pngs as argument"
else
	for i in pbp*
	do
		cd $i
		for s in *.svg
		do
			echo $s && /Applications/Inkscape.app/Contents/Resources/bin/inkscape --export-area-drawing -h=$1 -b=white $s --export-png `echo $s | sed -e 's/svg$/png/'`
		done
		cd ..
	done
fi
