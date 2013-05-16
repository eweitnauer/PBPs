# converts all svg-files in the current directory to pdf-files
output_dir=${1-.} # set to second parameter or, if not given, set to "."
shopt -s nullglob # let *.svg be empty if there are not svg files
for s in *.svg
do
	mkdir -p "$output_dir"
	echo $s && /Applications/Inkscape.app/Contents/Resources/bin/inkscape --export-area-drawing $s --export-pdf "$output_dir/`echo $s | sed -e 's/svg$/pdf/'`"
done
