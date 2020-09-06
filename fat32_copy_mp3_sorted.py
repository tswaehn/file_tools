import argparse
import os
from shutil import copyfile
import pathlib


parser = argparse.ArgumentParser(description='Copy mp3 files in alphabetical order (needed by some mp3 players to play songs in correct order).', prefix_chars='-')
parser.add_argument('source_dir', metavar='SRC', type=str, help='source path of mp3 (recursive folder structure)')
parser.add_argument('destination_dir', metavar='DST', type=str, help='destination path where all files incl. structure are copied in alphabetical order')

args = parser.parse_args()

args_src = args.source_dir.encode("UTF-8")
args_dst = args.destination_dir.encode("UTF-8")

print(b'searching mp3 in [' + args_src + b']')
print(b'writing m3u files to [' + args_dst + b']')

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
    all_mp3 = dict()

    for root, dirs, files in os.walk(root_dir, topdown=True):
        for name in files:
            filename, file_extension = os.path.splitext(name)
            if file_extension.lower() == b'.mp3':
                fullname = os.path.relpath(os.path.join(root, name), root_dir)
                # playlist = os.path.basename(os.path.dirname(fullname))
                split_dir = split_path(fullname)
                mp3_folder = b'__'.join(split_dir[0:-1])
                if mp3_folder not in all_mp3:
                    all_mp3[mp3_folder] = list()

                all_mp3[mp3_folder].append(fullname)

        for name in dirs:
            print(os.path.join(root, name))

    return all_mp3


def sort_mp3_by_name(all_mp3):
    for key, mp3_folder in all_mp3.items():
        playlist = sorted(mp3_folder)
        all_mp3[key] = playlist

    return all_mp3


def copy_to_dst(src_dir, dst_dir, all_mp3):
    if not os.path.exists(dst_dir):
        print(b"err - path [" + dst_dir + b'] does not exist')
        return

    for name, mp3s in all_mp3.items():
        for mp3 in mp3s:
            src_fullname = os.path.join(src_dir, mp3)
            dst_fullname = os.path.join(dst_dir, mp3)

            print(b"src>" + src_fullname)
            print(b"dst>" + dst_fullname)

            dst_dir_rec = os.path.dirname(dst_fullname).decode("UTF-8")
            pathlib.Path(dst_dir_rec).mkdir(parents=True, exist_ok=True)

            copyfile(src_fullname, dst_fullname)
            print("... done")

    return


all_mp3 = dir_walk(args_src)
all_mp3 = sort_mp3_by_name(all_mp3)

copy_to_dst(args_src, args_dst, all_mp3)

exit(0)
