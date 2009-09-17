#!/usr/bin/env python
# -*- coding: utf-8 -*-

import BeautifulSoup as bs
import urllib

class MDT:
    """Show random message from http://mydrunktexts.com"""

    def __init__(self):
        print 'mdt init'

    def run(self, contact, msg):
        web_page = urllib.urlopen('http://mydrunktexts.com/random').read()
        soup = bs.BeautifulSoup(web_page)
        txt = soup.find(attrs={'class':'fmllink'}).string
        txt = txt.replace('&quot;','"')
        contact.send(txt)

    def exit(self):
        pass

provides = {'mdt': MDT}

