from setuptools import setup

APP = ['HomePage.py']
DATA_FILES = ['chromedriver']
OPTIONS = {
    'argv_emulation': True,
    'packages': ['selenium'],
    'includes': ['PyQt6'],
    'iconfile': 'logo.png'
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
