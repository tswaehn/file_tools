import argparse
import os


parser = argparse.ArgumentParser(description='Compare two directories based on defined criteria - report differences.', prefix_chars='-')
parser.add_argument('root_A', metavar='A', type=str, help='path A')
parser.add_argument('root_B', metavar='B', type=str, help='path B')
parser.add_argument('-f', help='compare filesize', default=False, dest='boolean_switch', action='store_true')

args = parser.parse_args()

args_root_A = args.root_A.encode("UTF-8")
args_root_B = args.root_B.encode("UTF-8")
args_comp_filesize = args.boolean_switch

print(b'compare [' + args_root_A + b']')
print(b'compare [' + args_root_B + b']')


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


def dir_walk(root_dir):
    all_files = dict()

    for root, dirs, files in os.walk(root_dir, topdown=True):
        for name in files:
            filename, file_extension = os.path.splitext(name)

            fullname = os.path.relpath(os.path.join(root, name), root_dir)
            split_dir = split_path(fullname)
            key_file_id = b'__'.join(split_dir)
            if key_file_id not in all_files:
                all_files[key_file_id] = FileItem(fullname)
            else:
                xx
                all_files[key_file_id].append(fullname)

        for name in dirs:
            print(os.path.join(root, name))

    return all_files


def find_new_files(A, B):
    print("> cecking for new files <")
    count_A = 0
    count_B = 0

    for key, file_item in A.items():
        if key not in B:
            count_A += 1
            print(b'new in [A]:' + file_item.name)

    for key, file_item in B.items():
        if key not in A:
            count_B += 1
            print(b'new in [B]:' + file_item.name)

    print("- - - S U M M A R Y - - -")
    if count_A == 0 and count_B == 0:
        print("folders identical")
    else:
        print("new files present in A only: " + str(count_A))
        print("new files present in B only: " + str(count_B))

    return


def compare_file_size(root_A, root_B, A, B):

    print("- - - cecking for same file sizes - - -")
    count = 0
    for key, file_item in A.items():
        if key in B:
            full_file_A = os.path.join(root_A, file_item.name)
            full_file_B = os.path.join(root_B, file_item.name)
            if not os.path.isfile(full_file_A):
                print(b"ERROR - cannot open: " + full_file_A)
                continue
            if not os.path.isfile(full_file_B):
                print(b"ERROR - cannot open: " + full_file_B)
                continue
            size_A = os.stat(full_file_A).st_size
            size_B = os.stat(full_file_B).st_size
            if size_A != size_B:
                count += 1
                print(b"filesize different:" + file_item.name)

    print("- - - S U M M A R Y - - -")

    if count == 0:
        print("folders identical")
    else:
        print("total count of filesize differences: " + str(count))

    return


files_A = dir_walk(args_root_A)
files_B = dir_walk(args_root_B)

find_new_files(files_A, files_B)

if args_comp_filesize:
    compare_file_size(args_root_A, args_root_B, files_A, files_B)

exit(0)
