import argparse
import os
import hashlib

parser = argparse.ArgumentParser(description='Try to find all SRC files SOMEWHERE in DEST - report differences.', prefix_chars='-')
parser.add_argument('root_A', metavar='SRC', type=str, help='path A')
parser.add_argument('root_B', metavar='DST', type=str, help='path B')


args = parser.parse_args()

args_root_A = args.root_A.encode("UTF-8")
args_root_B = args.root_B.encode("UTF-8")

print(b'source [' + args_root_A + b']')
print(b'destination [' + args_root_B + b']')


class FileItem:

    def __init__(self, name):
        self.name = name


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

def get_file_fingerprint(filename, fingerprint_len):
    fingerprint = b'none'
    with open(filename, "rb") as f:
        bytes = f.read(fingerprint_len)
        m = hashlib.md5()
        m.update(bytes)
        # return bytearray
        fingerprint = m.hexdigest().encode('UTF-8')

    return fingerprint

def dir_walk(root_dir):
    all_files = dict()

    for root, dirs, files in os.walk(root_dir, topdown=True):
        for name in files:
            filename, file_extension = os.path.splitext(name)

            fullname = os.path.relpath(os.path.join(root, name), root_dir)

            full_file_name = os.path.join(root_dir, fullname)
            if not os.path.isfile(full_file_name):
                print(b"ERR: cannot open file:" + full_file_name)
                continue

            # get file size
            file_size = os.stat(full_file_name).st_size

            # get file fingerprint (max. 100kb)
            fingerprint_len = min(file_size, 100000)
            finger_print = get_file_fingerprint(full_file_name, fingerprint_len)

            # create key
            key_file_id = b'__' + str(file_size).encode("UTF-8") + b'_' + finger_print + b'_' + name
            if key_file_id not in all_files:
                all_files[key_file_id] = FileItem(fullname)
            else:
                print(b'NOTE: found duplicate:' + full_file_name)
                print(b' --> ' + os.path.join(root_dir, all_files[key_file_id].name))

        for name in dirs:
            print(os.path.join(root, name))

    return all_files


def find_files_A_somewhere_in_B(A, B):
    print("> cecking for new files <")
    count_A = 0

    for key, file_item in A.items():
        if key not in B:
            count_A += 1
            print(b'new in [SRC]:' + file_item.name)

    print("- - - S U M M A R Y - - -")
    if count_A == 0:
        print("all files of SRC are somewhere in DST")
    else:
        print("new files present in SRC only: " + str(count_A))

    return


files_A = dir_walk(args_root_A)
files_B = dir_walk(args_root_B)

find_files_A_somewhere_in_B(files_A, files_B)


exit(0)
