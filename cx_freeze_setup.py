# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
# Contact: 01101011@tuta.io
import sys
from cx_Freeze import setup, Executable
sys.path.insert(0, "hunters_and_rabbits")

"""Alternate setup file for freezing to EXE via cx_Freeze"""

build_exe_options = {"packages": ["jinja2.ext"], "excludes": []}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
# BUT... on Windows, it causes this crash:
# https://github.com/pallets/flask/issues/3447
# With base left None, we get a cmd.exe window and the program works.
# if sys.platform == "win32":
#     base = "Win32GUI"

setup(
    name="hunters_and_rabbits",
    version="1.1.1",
    install_requires=[
        "networkx>=2.4",
        "flask>=1.1.1",
        "plotly>=4.4.1",
        "dash>=1.7.0",
        "dash-core-components>=1.6.0",
        "dash-html-components>=1.0.2",
        "numpy>=1.18.0",
    ],
    python_requires='>=3.8',

    options = {"build_exe": build_exe_options},
    executables = [
        Executable("hunters_and_rabbits/hunters_and_rabbits.py", base=base)
    ],

    # PyPI metadata
    author="Krotera",
    author_email="01101011@tuta.io",
    description="A Dash implementation of the Hunters and Rabbits graph game",
    long_description_content_type="text/markdown",
    url="https://github.com/Krotera/hunters_and_rabbits",
    classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
    "Operating System :: OS Independent",
    ]
)
