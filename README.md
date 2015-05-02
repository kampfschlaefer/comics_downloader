# comics_downloader

Badges: [![Build Status](https://travis-ci.org/kampfschlaefer/comics_downloader.svg?branch=master)](https://travis-ci.org/kampfschlaefer/comics_downloader)

One of my little helpers: Given a json-file of a humblebundle.com comics/ebooks bundle, it extracts md5 sums and download urls for the formats. Also it downloads the files.

All because I am too lazy to click on all the links individually.


## TODO list

- [x] publish on github
- [x] complete test-coverage for current code
- [ ] save books each into their directory (better for calibre import)
- [ ] search for existing files by md5sum/sha1sum in calibre store
- [ ] prepare download lists based on type preference and existing files in calibre-store
- [ ] fetch new json from humblebundle
