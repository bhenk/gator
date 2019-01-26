#!/usr/bin/env bash

# working with Qt Installer Framework from
# https://download.qt.io/official_releases/qt-installer-framework/2.0.3/QtInstallerFramework-mac-x64.dmg

current_gator_version="Gator.app"

qt_bin=~/Qt/Tools/QtInstallerFramework/3.0/bin/binarycreator
qt_archivegen=~/Qt/Tools/QtInstallerFramework/3.0/bin/archivegen

if [ -e "$qt_bin" ]; then
    echo "Found $qt_bin"
else
    echo "No Qt Installer Framework found at $qt_bin"
    exit 1
fi

cd dist
echo "Archiving $current_gator_version"
$qt_archivegen ../installer/packages/bhenk.gator/data/gator_mac.7z $current_gator_version
echo "Archived $current_gator_version as installer/packages/bhenk.gator/data/gator_mac.7z"
cd ../

echo "Creating installer..."
$qt_bin -c installer/config/config.xml -p installer/packages --offline-only gator_mac_installer
echo "Created gator_mac_installer.app"

echo "Code signing gator_mac_installer.app..."
codesign -s "Code Signing Cerificate" gator_mac_installer.app --deep


# Q: How to create a disk image?
# http://www.wikihow.com/Make-a-DMG-File-on-a-Mac

echo "Creating disk image..."
hdiutil create gator_mac_installer.dmg -volname "gator_mac_installer" \
    -srcfolder gator_mac_installer.app


# Q: How to make a disk image window open automatically?
# A: https://discussions.apple.com/thread/3851123?tstart=0
# bless --openfolder /Volumes/MPT_mac_installer


mkdir dist_installer
rm -Rf dist_installer/*
echo "Moving files"
mv gator_mac_installer.app dist_installer/
mv gator_mac_installer.dmg dist_installer/
echo "Finished creating installer"

mkdir ../../z_dist
cp dist_installer/gator_mac_installer.dmg ../../z_dist

