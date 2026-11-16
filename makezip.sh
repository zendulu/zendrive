#!/bin/bash

if [ -z "$1" ]; then
  echo "Usage: $0 <version>"
  exit 1
fi

VERSION=$1
SOURCE_DIR="$(pwd)/zendrive-v$VERSION"

if [ ! -d "$SOURCE_DIR" ]; then
  echo "Error: release directory zendrive-v$VERSION/ not found"
  exit 1
fi

# Archives land next to the release directory; zip contents stay flat
# (rooted at pacenotes/, README.md, ...) the way users expect to unpack.
cd "$SOURCE_DIR" || exit 1

# Voice packs ship separately so a codriver update doesn't force a full
# mod redownload.
zip -qr "../codrivers-v$VERSION.zip" codrivers

# Mod archive: everything in filelist.txt, which excludes the voices.
zip -qr "../zendrive-v$VERSION.zip" -@ < ../filelist.txt
