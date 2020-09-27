# file tools

### content
* `dir_comp` ... compares 2 directories and reports any difference (new files, modified files)
* `find_any` ... find all files of directory __A__ in files of folder __B__ - report any files that are in __A__ but not __B__)
* `fat32_copy_mp3_sorted` ... copy all __*.mp3__ files from folder __A__ to folder __B__ in alphabetical order (some MP3-Players play their files in FAT order, because they cannot sort internally -- this is my workaround)
* `m3u_gen` ... create playlist files __*.m3u__ for all folders given. sort files in each playlist in alphabetical order

#### required python packages
* argparse
* hashlib
* pathlib

#### usage: dir_comp
```
$ python dir_comp.py -h
usage: dir_comp.py [-h] [-f] A B

Compare two directories based on defined criteria - report differences.

positional arguments:
  A           path A
  B           path B

optional arguments:
  -h, --help  show this help message and exit
  -f          compare filesize
```
#### usage: find_any
```
$ python find_any.py -h
usage: find_any.py [-h] SRC DST

Try to find all SRC files SOMEWHERE in DEST - report differences.

positional arguments:
  SRC         path A
  DST         path B

optional arguments:
  -h, --help  show this help message and exit

```
#### usage: fat32_copy_mp3_sorted

T.B.D

#### usage: m3u_gen

```
$ python m3u_gen.py -h
usage: m3u_gen.py [-h] FOLDER OUTPUT

Create m3u playlists from mp3 folders.

positional arguments:
  FOLDER      root folder for searching mp3s
  OUTPUT      folder for output m3u files

optional arguments:
  -h, --help  show this help message and exit
```
