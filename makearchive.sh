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

cd "$SOURCE_DIR" || exit 1

7z a "../codrivers-v$VERSION.7z" codrivers
7z a -spf2 "../zendrive-v$VERSION.7z" -i@../filelist.txt
