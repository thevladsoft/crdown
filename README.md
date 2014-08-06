# Crunchyroll Downloader
## Download your favorite anime from Crunchyroll

### Introduction

This is somewhat both a port and cleanup of [Crunchyroll Downloader Toolkit DX][1] for Unix systems. Actually, it still should work on Windows too, but since compiling things using pip is not the easiest thing on Windows, if you do want to use this on Windows it's easier to just use [Crunchyroll Downloader Toolkit DX][1].

It's really simple to use. First you need to (optionally but recommended) login on your account, using the following command:
```
$ python2 login.py
```

This will generate a 'cookies.txt' file, containing you account information. After that, you should go to [Crunchyroll website][2], copy any Anime link you want (for example (this one)[http://www.crunchyroll.com/fatekaleid-liner-prisma-illya/episode-1-illya-grow-up-657285]) and use the following command to start the download:
```
$ python2 crdown.py http://www.crunchyroll.com/fatekaleid-liner-prisma-illya/episode-1-illya-grow-up-657285
```

That's it. You will see .flv and .ass files (if the subtitle is available) in the 'export/' directoy if all goes well. You can change the quality and language subtitle if you want editing the 'settings.ini' file.

### How to install

You need to have 'rtmpdump' installed and added somewhere on your PATH. Probably the best way is to use your distribution packages to install this program. Some distribution commands to install 'rtmpdump':
```
$ sudo apt-get install rtmpdump # Debian/Ubuntu and derivates
$ sudo pacman -S rtmpdump # Arch Linux
```

After that, you will need to install the Python requirements. They're listed on 'requirements.txt' file, that is compatible with Python's 'pip' package manager. But since cryptopy is not available on PyPi, you'll need to install it separately. Just run the following commands:
```
$ sudo pip install http://sourceforge.net/projects/cryptopy/files/latest/download
$ sudo pip install -r requirements.txt
$ python crdown.py URL
```

**Optional but recommended**: instead of running the pip commands as root it's better to create a isolated virtual environment so you don't mess with your system Python. To do so, install the python2-virtualenv package and do the following:
```
$ virtualenv2 crdown
$ cd crdown
$ source bin/activate # You should run this command after every new terminal you open
$ pip install http://sourceforge.net/projects/cryptopy/files/latest/download
$ pip install -r requirements.txt
$ python crdown.py URL
```

[1]: http://www.darkztar.com/forum/showthread.php?219034-Ripping-videos-amp-subtitles-from-Crunchyroll-(noob-friendly)
[2]: http://www.crunchyroll.com/