Crunchyroll video downloader
============================

Download your favorite anime from Crunchyroll
---------------------------------------------

Introduction
~~~~~~~~~~~~

This is somewhat both a port and cleanup of `Crunchyroll Downloader Toolkit DX`_ for Unix systems. Actually, it still should work on Windows too, but since compiling things using pip is not the easiest thing on Windows, if you do want to use this on Windows it's easier to just use `Crunchyroll Downloader Toolkit DX`_.

It's really simple to use. First you need to login to your account, using the following command:

::

    $ crdown -l

This will generate a 'cookies.txt' file in your configuration directory (generally ``~/.config/crdown``), containing you account information. Even if you don't have a account you need to run this command at least once to generate a valid 'cookies.txt' file.

After that, you should go to `Crunchyroll website`_, copy any Anime link you want (for example `this one`_) and use the following command to start the download:

::

    $ crdown http://www.crunchyroll.com/fatekaleid-liner-prisma-illya/episode-1-illya-grow-up-657285

You can change some settings (like video quality, subtitle language, etc.) creating a 'settings.ini' in your configuration directory. See ``misc/settings.ini`` file for an example.

That's it. You will see .flv and .ass files (if the subtitle is available) in the ``./export/`` directoy if all goes well. If you want to convert the .flv/.ass files in a nicer .mkv container, you will need some additional tools (see "How to install" section) to do the job. See ``misc/convert.sh`` script for an example on how to convert files.

**WARNING**: for now this script will delete the original .flv/.ass files. You can comment the line on 'convert.sh' script that do it if you don't want this behavior.

How to install
~~~~~~~~~~~~~~

You need to have 'rtmpdump' installed and added somewhere on your PATH. Probably the best way is to use your distribution packages to install this program. Some distribution commands to install 'rtmpdump':

::

    $ sudo apt-get install rtmpdump # Debian/Ubuntu and derivates
    $ sudo pacman -S rtmpdump # Arch Linux

After that you need to install 'crdown' per se. The easiest way to do it is using 'pip'. This downloads and installs this project from PyPi, completely automagically (excluding for system dependencies). The only problem it's not always up-to-date. Just run the following command:

::

    $ sudo pip install crdown

If you do want to install manually, you will first need to install the Python requirements. They're listed on 'requirements.txt' file, that is compatible with Python's 'pip' package manager. Just run the following commands:

::

    $ sudo pip install -r requirements.txt
    $ git clone https://github.com/m45t3r/crdown.git

**Optional but recommended**: instead of running the pip commands as root (using sudo) it's better to create a isolated virtual environment so you don't mess with your system Python. To do so, install the ``python2-virtualenv`` package and do the following:

::

    $ virtualenv2 crdown
    $ cd crdown
    $ source bin/activate # You should run this command after every new terminal you open
    $ pip install crdown

**Aditional dependencies to 'convert.sh' script**: you will need 'ffmpeg' and 'mkvtoolnix' installed to run the MKV conversion script. Some distribution commands to install both:

::

    $ sudo apt-get install ffmpeg mkvtoolnix # Debian/Ubuntu and derivates
    $ sudo pacman -S ffmpeg mkvtoolnix # Arch Linux

Copy ``misc/convert.sh`` somewhere and make the changes to adapt to your case. The script serves as an example only, **do not** run it without studying what it does.

Disclaimer
~~~~~~~~~~

This work is licensed under the Creative Commons Attribution-ShareAlike 3.0 Unported License. To view a copy of this license, visit `this
page`_ or see the included LICENSE.txt file.

The software is provided "AS IS", without any warranty, either expressed or implied, including, but not limited to, the implied warranties of merchantability and fitness for a particular purpose. The author(s) will not be liable for any special, incidental, consequential or indirect damages due to loss of data or any other reason. This is a free tool for educational (yes, educational >.>) use only.

.. _`Crunchyroll Downloader Toolkit DX`: http://www.darkztar.com/forum/showthread.php?219034-Ripping-videos-amp-subtitles-from-Crunchyroll-(noob-friendly)
.. _`Crunchyroll website`: http://www.crunchyroll.com/
.. _`this one`: http://www.crunchyroll.com/fatekaleid-liner-prisma-illya/episode-1-illya-grow-up-657285
.. _`this page`: http://creativecommons.org/licenses/by-sa/3.0/deed.en_US
