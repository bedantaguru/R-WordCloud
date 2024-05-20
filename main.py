import tkinter as tk
from tkinter import filedialog
from tqdm import tqdm
import os
import chardet
from functools import lru_cache


def detect_file_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
    result = chardet.detect(raw_data)
    return result['encoding']


def file_choose(is_folder=False):
    """
    Opens file/folder selection window in windows.
    :param is_folder: If set true will choose a folder (default is 'False')
    :return: The selected file/folder path
    """
    root = tk.Tk()
    root.lift()
    root.attributes('-topmost', True)
    root.withdraw()
    # take user home
    u_home = os.path.expanduser("~")
    if is_folder:
        fp = filedialog.askdirectory(initialdir=u_home)
    else:
        fp = filedialog.askopenfilename(initialdir=u_home)
    root.destroy()
    if not fp:
        raise Exception("No file or folder selected.")
    return fp


def collect_unique_lines_of_file_encoding(
        fname=None,
        encoding="utf-8",
        ignore_err=False):
    if fname is None:
        fname = file_choose()
    if ignore_err:
        err = "ignore"
    else:
        err = None
    with open(fname, 'r', encoding=encoding, errors=err) as f:
        unique_lines = {ln.rstrip('\n') for ln in f}
    return unique_lines


@lru_cache
def collect_unique_lines_of_file(fname=None):
    try:
        ul = collect_unique_lines_of_file_encoding(fname)
    except UnicodeDecodeError:
        enc = detect_file_encoding(fname)
        ul = collect_unique_lines_of_file_encoding(
            fname,
            encoding=enc,
            ignore_err=True
        )
    return ul


def collect_unique_lines(folder_path=None):
    """
    Reads and collects unique lines from all R-scripts
    :param folder_path: folder containing R-scripts (if missed you'll be prompted)
    :return: a list containing unique lines from the
    """
    if folder_path is None:
        folder_path = file_choose(is_folder=True)
    unique_lines = set()
    filenames = [f for f in os.listdir(folder_path) if f.upper().endswith(".R")]
    for fn in tqdm(filenames, desc="Processing file:", unit="file"):
        file_path = os.path.join(folder_path, fn)
        try:
            ul = collect_unique_lines_of_file(file_path)
        except Exception as e:
            print(f"Issue in file: {file_path} \nDetails: {type(e).__name__}:{e}")
            ul = set()
        unique_lines.update(ul)
    return list(unique_lines)


all_lines = collect_unique_lines("C:/Users/Nil/Downloads/R")

