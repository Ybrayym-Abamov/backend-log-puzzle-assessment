#!/usr/bin/env python2
"""
Logpuzzle exercise

Copyright 2010 Google Inc.
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0

Google's Python Class
http://code.google.com/edu/languages/google-python-class/

Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"

"""

__author__ = """ Ybrayym Abamov, Mustafa Prodhan, Mike Alnakhale """

import os
import re
import sys
import urllib.request
import argparse


def read_urls(filename):
    """Returns a list of the puzzle urls from the given log file,
    extracting the hostname from the filename itself.
    Screens out duplicate urls and returns the urls sorted into
    increasing order."""
    with open(filename, 'r') as f:
        file_ = f.read()
    correct_URLs = []
    exracted_URLs = list(set(re.findall(r"\S+puzzle\S+", file_, re.DOTALL)))
    for url in exracted_URLs:
        correct_URLs.append("https://code.google.com" + url)
    correct_URLs = sorted(correct_URLs, key=lambda url: url[-8:])
    return correct_URLs


def download_images(img_urls, dest_dir):
    """Given the urls already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory
    with an img tag to show each local image file.
    Creates the directory if necessary.
    """
    print('Downloading images into {}...'.format(dest_dir))
    images = []
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        # os.chdir(dest_dir)
    for idx, url in enumerate(img_urls):
        image_f = f"img{idx}.jpg"
        print('Downloading ' + image_f)
        returl = urllib.request.urlretrieve(url, f"{dest_dir}/{image_f}") # downloading the image URLs
        images.append(image_f)
    with open(f'{dest_dir}/index.html', 'w') as f:
        f.write("""
        <html>
            <title>Code Cracked</title>
            <body>
                <h1>TADAAAAA!</h1>
        """)
        for image in images:
            f.write(f'<img src="{image}" />')
        f.write("""
            </body>
        </html>""")


def create_parser():
    """Create an argument parser object"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d', '--todir',  help='destination directory for downloaded images')
    parser.add_argument('logfile', help='apache logfile to extract urls from')

    return parser


def main(args):
    """Parse args, scan for urls, get images from urls"""
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)

    img_urls = read_urls(parsed_args.logfile)

    if parsed_args.todir:
        download_images(img_urls, parsed_args.todir)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main(sys.argv[1:])
