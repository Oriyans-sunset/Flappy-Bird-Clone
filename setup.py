from setuptools import setup

APP=['Flappy-Bird-Clone.py']

OPTIONS = {
    'argv_emulation': True,
}

setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app']
)

'''
Use the terminal to make .app file for the game:
type 'python3 setup.py py2app'
'''