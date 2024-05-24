import tkinter as tk
from tkinter import filedialog
from tqdm import tqdm
import os
import chardet
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor, as_completed


class FileHandling:
    def __init__(self):
        pass

    @staticmethod
    def detect_file_encoding(file_path):
        with open(file_path, 'rb') as f:
            raw_data = f.read()
        result = chardet.detect(raw_data)
        return result['encoding']

    @staticmethod
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


class UniqueLines:
    def __init__(self, folder_path=None):
        valid_folder = False
        if folder_path is not None:
            if os.path.exists(folder_path):
                valid_folder = True

        if valid_folder:
            self.collect_unique_lines(folder_path)
        else:
            print("Please use collect_unique_lines for reading lines")
            self.Lines = []

    @staticmethod
    def collect_unique_lines_of_file_encoding(
            fname=None,
            encoding="utf-8",
            ignore_err=False):
        if fname is None:
            fname = FileHandling.file_choose()
        if ignore_err:
            err = "ignore"
        else:
            err = None
        with open(fname, 'r', encoding=encoding, errors=err) as f:
            unique_lines = {ln.rstrip('\n') for ln in f}
        return unique_lines

    @staticmethod
    @lru_cache(maxsize=None)
    def collect_unique_lines_of_file(fname=None):
        try:
            ul = UniqueLines.collect_unique_lines_of_file_encoding(fname)
        except UnicodeDecodeError:
            enc = FileHandling.detect_file_encoding(fname)
            ul = UniqueLines.collect_unique_lines_of_file_encoding(
                fname,
                encoding=enc,
                ignore_err=True
            )
        return ul

    def collect_unique_lines(self, folder_path=None, on_multi_thread=True):
        """
        Reads and collects unique lines from all R-scripts

        :param folder_path: folder containing R-scripts
                            (if missed you'll be prompted)
        :param on_multi_thread: if set to true files will be read in parallel
                                threads (may not be ideal for SSD, if HDD you may
                                set to True, by default it's set to ``True``)
        :return: a list containing unique lines from the
        """
        if folder_path is None:
            folder_path = FileHandling.file_choose(is_folder=True)
        unique_lines = set()
        filenames = [os.path.join(folder_path, f)
                     for f in os.listdir(folder_path)
                     if f.upper().endswith(".R")]

        def single_file(fn):
            try:
                ul = UniqueLines.collect_unique_lines_of_file(fn)
            except Exception as e:
                print(f"Issue in file: {fn} \nDetails: {type(e).__name__}:{e}")
                ul = set()
            return ul

        if on_multi_thread:
            with ThreadPoolExecutor() as exe:
                ftrs = [exe.submit(single_file, fn) for fn in filenames]
                for ftr in tqdm(
                        as_completed(ftrs),
                        desc="Processing file:", unit="files",
                        total=len(filenames)):
                    unique_lines.update(ftr.result())
        else:
            for fn in tqdm(filenames, desc="Processing file:", unit="files"):
                unique_lines.update(single_file(fn))
        self.Lines = list(unique_lines)
        return self.Lines
