# cleans up all svg files in the currect directory and subdirectories
find . -name '*.svg' -print0 | xargs -0 /Applications/Inkscape.app/Contents/Resources/bin/inkscape --vacuum-defs