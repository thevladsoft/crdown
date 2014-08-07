#!/usr/bin/env python2

import argparse
import os
import sys
from getpass import getpass
from distutils.util import strtobool

from appdirs import user_config_dir

from crunchy.downloader import config,getVideo
from crunchy.login import CrunchyLogin

__author__ = 'Thiago Kenji Okada'
__appname__ = 'crdown'
__version__ = '0.1'


def argparser():
    parser = argparse.ArgumentParser(
        description='Crunchyroll video downloader')
    parser.add_argument(
        dest='url', nargs='?', action='store', metavar='URL',
        help='Video url from Crunchyroll to download')
    parser.add_argument(
        '-l', '--login', action='store_true', default=0,
        help='Login to your Crunchyroll account')
    version_info = '%(prog)s {}'.format(__version__)
    parser.add_argument(
        '-v', '--version', action='version',
        version=version_info)
    return parser


def yes_no_query(question):
    print('{} (y/n)'.format(question))
    while True:
        try:
            return strtobool(raw_input().lower())
        except ValueError:
            print("Please respond with 'y' or 'n'.")


def main():
    # If no option is given, show help and exit
    parser = argparser()
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(2)
    # Parse the user choices
    args = parser.parse_args()

    config_path = user_config_dir(__appname__)
    if not os.path.exists(config_path):
        os.mkdir(config_path)
    login = CrunchyLogin(config_path)

    if args.login:
        if yes_no_query('Do you have a Crunchyroll login?'):
            username = raw_input('Crunchyroll username: ')
            password = getpass('Crunchyroll password: ')
            login.create_cookies()
            result = login.try_login(username, password)
            if result:
                print 'Login successful!'
            else:
                sys.exit('Login failure!')
        else:
            login.create_cookies()
            print 'Cookies created successfuly!'

    if args.url:
        config(config_path)
        getVideo(args.url)

if __name__ == '__main__':
    main()
