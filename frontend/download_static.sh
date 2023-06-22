#!/bin/bash

FONTS=(  
  "https://static.frag-den-staat.de/static/fonts/fontawesome-webfont.eot"
  "https://static.frag-den-staat.de/static/fonts/fontawesome-webfont.woff2"
  "https://static.frag-den-staat.de/static/fonts/fontawesome-webfont.woff"
  "https://static.frag-den-staat.de/static/fonts/fontawesome-webfont.ttf"
  "https://static.frag-den-staat.de/static/fonts/Inter-Bold-latin.woff2"
  "https://static.frag-den-staat.de/static/fonts/Inter-Bold-latin.woff"
  "https://static.frag-den-staat.de/static/fonts/Inter-Regular-latin-ext.woff2"
  "https://static.frag-den-staat.de/static/fonts/Inter-Regular-latin-ext.woff"
  "https://static.frag-den-staat.de/static/fonts/Inter-Regular-latin.woff"
  "https://static.frag-den-staat.de/static/fonts/Inter-Regular-latin.woff2"
  "https://static.frag-den-staat.de/static/fonts/Inter-SemiBold-latin-ext.woff2"
  "https://static.frag-den-staat.de/static/fonts/Inter-SemiBold-latin.woff"
  "https://static.frag-den-staat.de/static/fonts/Inter-SemiBold-latin-ext.woff"
  "https://static.frag-den-staat.de/static/fonts/Inter-SemiBold-latin-ext.woff"
  "https://static.frag-den-staat.de/static/fonts/Inter-SemiBold-latin.woff2"
)

mkdir -p static/css/fds
mkdir -p static/fonts/
mkdir -p static/js/d3/

cd static/css/fds
curl "https://static.frag-den-staat.de/static/css/main.css" | sed "s/https:\/\/static.frag-den-staat.de//g" > main.css



cd ../../fonts/
for font in "${FONTS[@]}"
do
  wget "$font"
done

cd ../js/d3/
curl https://d3js.org/d3.v7.min.js > d3.v7.min.js


# source https://github.com/okfde/frontex-assets/blob/main/fds-assets.sh