import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "excludes": ['Tkconstants', 'Tkinter'],
    "includes": ['email.mime.multipart', 'email.mime.image']
}

# if there is no version, an error occurs.
setup(
    name="Puffadder",
    options={"build_exe": build_exe_options},
    version="0.01",
    executables=[Executable("Puffader.py", base="WIN32GUI")]
)
