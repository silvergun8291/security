#!/bin/bash
git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git $HOME/depot_tools
export PATH=$PATH:$HOME/depot_tools
mkdir chromium && cd chromium
fetch --nohooks chromium
cd src
git checkout 105.0.5195.125
./build/install-build-deps.sh
gclient runhooks
mkdir -p out/Chrome
cp ../../args.gn out/Chrome/args.gn
cd v8
patch -p1 < ../../../patch.diff
cd ..
autoninja -C out/Chrome chrome
