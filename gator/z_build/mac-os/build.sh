#!/bin/bash --


# APPNAME should equal > app = BUNDLE(exe, name=xxx < in gator.spec
APPNAME="Gator.app"

rm -Rf build dist

pyinstaller --onefile -w gator.spec

# pyinstaller is lazy: Mac oss app still missing files
cp -R dist/gator/* "dist/$APPNAME/Contents/MacOs"

# codesign has problems with these two:
# rm -Rf "dist/$APPNAME/Contents/MacOs/include"
# rm -Rf "dist/$APPNAME/Contents/MacOs/lib"
# they can be missed.

#echo "This step will probably not work on your machine!"
#cd dist/
#codesign -s "Code Signing Cerificate" "$APPNAME" --deep
#cd ../

echo "Finished"
echo " --> dist/Gator.app/Contents/Info.plist may have LSBackgroundOnly set to true."
echo " --> Set to false"