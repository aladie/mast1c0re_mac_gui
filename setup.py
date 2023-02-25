"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['mast1c0re-file-loader-mac.py']
APP_NAME = "Mast1c0re File Loader"
DATA_FILES = []
OPTIONS = {'iconfile':'mast1c0re-file-loader.ico', 'plist': {
        'CFBundleName': APP_NAME,
        'CFBundleDisplayName': APP_NAME,
        'CFBundleGetInfoString': "Send files to Mast1c0re running on PS4/PS5",
        'CFBundleIdentifier': "com.aladie.osx.mast1c0re",
        'CFBundleVersion': "0.0.2",
        'CFBundleShortVersionString': "0.0.2",
        'NSHumanReadableCopyright': u"Copyright © 2023, Aladie, Feel free to modify this software"
    }}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)