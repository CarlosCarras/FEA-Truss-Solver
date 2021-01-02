import tkinter as tk
from tkinter import filedialog
import subprocess
import webbrowser
import os

EXT = ".eml5526"

ELEMENT_TRUSS = 'truss'

def request_input():
    print("...Initializng the EML5526 Solver...")
    print("Options: \n\t 1) Solve a Mesh \n\t 2) Create a Mesh \n\t 3) Support the Creator!\n")
    return input(">> ")


def get_filename():
    root = tk.Tk()
    root.withdraw()
    filename = filedialog.askopenfilename(initialdir=".",
                                          title="Select an FEA Solver File",
                                          filetypes=(("fea files", "*"+EXT), ("all files", "*.*")))
    return filename


def get_filedata(filename):
    file = open(filename, "r")

    element_type = file.readline().split(' ')[1]
    element_type = element_type.strip('\n')
    units = file.readline().split(' ')[1]
    units = units.strip('\n')

    file.close()
    return element_type, units


def launch_editor():
    filename = input("Please enter a filename: ")
    filename += EXT
    open(filename, "w")

    if os.name == "posix":
        subprocess.call(['open', '-a', 'TextEdit', filename])


def launch_website():
    url = 'http://carloscarras.tech/Home'
    webbrowser.open_new(url)


def handle_startup():
    command = request_input()

    if command == "1":
        filename = get_filename()
        return filename
    elif command == "2":
        launch_editor()
    elif command == "3":
        launch_website()

    exit()
