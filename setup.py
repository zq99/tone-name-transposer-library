from setuptools import setup

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: GNU General Public License v2.0 only (GPL-2.0-only)',
    'Programming Language :: Python :: 3'
]

setup(
    name='tonetransposer',
    version='0.0.2',
    packages=['tonetranspose'],
    url='',
    classifiers=classifiers,
    license='GPL2',
    author='Zaid Qureshi',
    author_email='zq99@hotmail.com',
    keywords=['MUSIC THEORY', 'PIANO', 'TRANSPOSITION','KEYBOARD','CHORDS','SCALES'],
    long_description=open('README.md').read(),
    description='Transposes a series of tones into all 12 keys and classifies them by their shape on a piano keyboard',
)
