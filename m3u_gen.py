import argparse
import os
import unicodedata
import codecs
import io
#import importlib

# we are expecting a folder struct like
#
# root / artist / album / track xx.mp3
#
# then playlist name will be: "[artist] - album"
#
# sorting of playlist will be by track name
#
#

parser = argparse.ArgumentParser(description='Create m3u playlists from mp3 folders.', prefix_chars='-')
parser.add_argument('folder', metavar='FOLDER', type=str, help='root folder for searching mp3s')
parser.add_argument('output', metavar='OUTPUT', type=str, help='folder for output m3u files')

args = parser.parse_args()

#
#reload(sys)
#sys.setdefaultencoding('ISO_8859-1')

# we treat all folders as byte sequences - seems more complicated however is needed to have m3u encoding exactly same
# like folder structure
args_folder = args.folder.encode("UTF-8")
args_output = args.output.encode("UTF-8")

print(b'searching mp3 in [' + args_folder + b']')
print(b'writing m3u files to [' + args_output + b']')


def split_path(path):
    folders = []
    while 1:
        path, folder = os.path.split(path)

        if len(folder) != 0:
            folders.append(folder)
        else:
            if len(path) != 0:
                folders.append(path)

            break

    folders.reverse()
    return folders


def dir_walk(root_dir):
    all_playlists = dict()

    for root, dirs, files in os.walk(root_dir, topdown=True):
        for name in files:
            filename, file_extension = os.path.splitext(name)
            if file_extension.lower() == b'.mp3':
                fullname = os.path.relpath(os.path.join(root, name), root_dir)
                # playlist = os.path.basename(os.path.dirname(fullname))
                split = split_path(fullname)
                playlist = b'[' + split[-3] + b'] - ' + split[-2]
                if playlist not in all_playlists:
                    all_playlists[playlist] = list()

                all_playlists[playlist].append(fullname)

        for name in dirs:
            print(os.path.join(root, name))

    return all_playlists


def sort_playlists_by_name(playlists):
    for key, playlist in playlists.items():
        playlist = sorted(playlist)
        playlists[key] = playlist

    return playlists


def make_windows_format(playlists):
    for key, playlist in playlists.items():
        # replace forward with backward slashes
        for idx, filename in enumerate(playlist):
            # create all back slashes
            playlist[idx] = playlist[idx].replace(b"/", b"\\")
            # windows line endings
            playlist[idx] += b'\r\n'
            # unicode
            #playlist[idx] = unicodedata.normalize('NFC', playlist[idx]).encode('iso_8859_1', 'replace')
            #playlist[idx] = playlist[idx].encode("ISO-8859-1")
            # store back to dict
        playlists[key] = playlist

    return playlists


def write_output(output_dir, playlists):
    if not os.path.exists(output_dir):
        print(b"err - path [" + output_dir + b'] does not exist')
        return

    for name, playlist in playlists.items():
        fullname = os.path.join(output_dir, name + b'.m3u')
        #fullname = os.path.join(output_dir, name + b'.m3u')
        #fullname = ''.join([i if i < 128 else ' ' for i in fullname])
        print(b"writing [" + fullname + b']')
        f = open(fullname, "wb")
        for line in playlist:
            test2 = line.decode("UTF-8")
            test3 = test2.encode("ISO-8859-1", "xmlcharrefreplace")
            f.write(test3)
            #f.write(line)
        f.close()

    return


playlists = dir_walk(args_folder)

playlists = sort_playlists_by_name(playlists)

playlists = make_windows_format(playlists)

write_output(args_output, playlists)


