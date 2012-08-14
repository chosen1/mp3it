#!/usr/bin/python
#
# Authors:
# ==============================================================================
# Author: Sundar Srinivasan (krishna.sun@gmail.com) Twitter: @krishnasun
# Author: Chosen1 (chosen1x@gmail.com) Twitter: @chosen1x
#
# Copyright [2011] Sundar Srinivasan
# Fork Copyright [2012] Chosen1
#
# Purpose:
# ==============================================================================
# Reasoning: This was almost identical to code I was authoring so I forked
# it to save time.
#
# Purpose of Fork: I often like to look up lectures or information on youtube
# when I am unable to attend a conference in person or am reasearching something
# new. In the interest of making the content as portable as possible for my own
# use this fork will download the video infromation and convert it into the
# ultraportable mp3 format for use in audo playback devices.
#
# Note: -- I am _NOT_ an attorney. --
# I beleive that making a copy in mp3 format is covered under "Fair Use"
# as you could access the information at any time online and in this case you
# are making a copy for personal use, which is no different than recording
# music off the radio onto audio cassette which had been common place for
# many years.
#
# Edits:
# ==============================================================================
# 08/13/2012 - Edited file to reflect the fork and add documention of purpose.
#
# 08/14/2012 - Download function returning error. Workingto fix this before
# adding new mp3 functions.
#
# License Info
# ==============================================================================
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


__author__ = ('Chosen1')

import re
import sys
import urllib2

def getVideoUrl(content):
    fmtre = re.search('(?<=fmt_url_map=).*', content)
    grps = fmtre.group(0).split('&amp;')
    vurls = urllib2.unquote(grps[0])
    videoUrl = None
    for vurl in vurls.split('|'):
        if vurl.find('itag=5') > 0:
            return vurl
    return None

def getTitle(content):
    title = content.split('</title>', 1)[0].split('<title>')[1]
    return sanitizeTitle(title)

def sanitizeTitle(rawtitle):
    rawtitle = urllib2.unquote(rawtitle)
    lines = rawtitle.split('\n')
    title = ''
    for line in lines:
        san = unicode(re.sub('[^\w\s-]', '', line).strip())
        san = re.sub('[-\s]+', '_', san)
        title = title + san
    ffr = title[:4]
    title = title[5:].split(ffr, 1)[0]
    return title

def downloadVideo(f, resp):
    totalSize = int(resp.info().getheader('Content-Length').strip())
    currentSize = 0
    CHUNK_SIZE = 32768

    while True:
        data = resp.read(CHUNK_SIZE)

        if not data:
            break
        currentSize += len(data)
        f.write(data)

        print('============> ' + \
                  str(round(float(currentSize*100)/totalSize, 2)) + \
                  '% of ' + str(totalSize) + ' bytes')
        if currentSize >= totalSize:
            break
    return

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python youtap.py \"<youtube-url>\"")
        exit(1)
    urlname = sys.argv[1].split('&', 1)[0]
    print('Downloading: ' + urlname)
    try:
        resp = urllib2.urlopen(urlname)
    except urllib2.HTTPError:
        print('Bad URL: 404')
        exit(1)
    content = resp.read()
    videoUrl = getVideoUrl(content)
    if not videoUrl:
        print('Video URL cannot be found')
        exit(1)
    title = getTitle(content)
    filename = title + '.flv'
    print('Creating file: ' + filename)
    f = open(filename, 'wb')
    print('Download begins...')

    ## Download video
    video = urllib2.urlopen(videoUrl)
    downloadVideo(f, video)
    f.flush()
    f.close()
    exit(0)