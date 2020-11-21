import argparse
import os
from datetime import datetime
from shutil import copyfile
import subprocess

parser = argparse.ArgumentParser(description='Backup SOURCE into TARGET.', prefix_chars='-')
parser.add_argument('root', metavar='SOURCE', type=str, help='source directory for all files')
parser.add_argument('target', metavar='TARGET', type=str, help='target directory for backup')

args = parser.parse_args()

args_root = args.root.encode("UTF-8")
args_target = args.target.encode("UTF-8")

print(b'Source directory is ' + args_root)
print(b'Target backup directory is ' + args_target)


if not os.path.exists(args_root):
    print(b'error: path does not exist ' + args_root)
    exit(-1)

if not os.path.exists(args_target):
    print(b'error: path does not exist ' + args_target)
    exit(-1)


def run_backup(src, target, incremental=1):

    # prepare filename string
    src_dir_str = str(src.decode("UTF-8")).replace("/", "_").encode("UTF-8")

    # prepare date and time strings for backup
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d").encode("UTF-8")
    time_str = now.strftime("%H-%M-%S").encode("UTF-8")

    # prepare target folder and base file names
    backup_dir = os.path.join(target, date_str)
    backup_file = os.path.join(backup_dir, time_str + src_dir_str)

    # prepare file names
    log_file = backup_file + b".log"
    err_file = backup_file + b".error.log"
    incremental_file = backup_dir + src_dir_str + b".incremental.txt"
    incremental_file_cp = backup_file + b".incremental.copy.txt"
    archive_file = backup_file + b".tar.gz"
    file_list = backup_file + b".filelist.txt"

    if incremental:
        level_0 = b''
        print(b"doing incremental backup")
    else:
        level_0 = b"--level=0"
        print(b"doing full backup")

    #
    cmd_line = [b"tar"]
    cmd_line += [b"--verbose", b"--create", b"--preserve-permissions", b"--gzip"]
    cmd_line += [b"--listed-incremental=" + incremental_file]
    cmd_line += [b"--file=" + archive_file]
    cmd_line += [level_0]
    cmd_line += [src]

    print(cmd_line)

    # create target path
    os.makedirs(backup_dir, exist_ok=True)

    # create archive
    print("START Archive")
    with open(log_file, "wb") as log_out, open(err_file, "wb") as err_log:
        output = subprocess.run(cmd_line, stdout=log_out, stderr=err_log)
    if not output.returncode == 0:
        print("error: create archive failed")
        return
    print("DONE Archive")

    # create a copy of incremental file
    copyfile(incremental_file, incremental_file_cp)

    # get tar content
    cmd_line = [b"tar", b"-tvf", archive_file]
    with open(file_list, "wb") as file_out:
        output = subprocess.run(cmd_line, stdout=file_out, stderr=subprocess.PIPE)
    if not output.returncode == 0:
        print("error: archive is invalid or file list command failed")
        return

    return


run_backup(args_root, args_target, incremental=0)

print("BYE")
exit(0)
