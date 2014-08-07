import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read().replace('#','')

setup(
    name = "crdown",
    version = "0.3",
    author = "Thiago Kenji Okada",
    author_email = "thiago.mast3r@gmail.com",
    description = ("Crunchyroll video downloader."),
    license = "Creative Commons Attribution-ShareAlike 3.0 Unported",
    keywords = "video crunchyroll downloader",
    url = 'https://github.com/m45t3r/crdown',
    packages=["utils", "crunchy"],
    package_dir={"":"src"},
    scripts=['src/crdown'],
    install_requires=("Unidecode", "appdirs", "beautifulsoup4", "pycrypto", "lxml"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "Environment :: Console",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Multimedia :: Video",
        "Topic :: Utilities",
    ],
)
