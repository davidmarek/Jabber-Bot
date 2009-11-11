#!/usr/bin/env python
# -*- coding: utf-8 -*-

import BeautifulSoup as bs
import urllib

class MDT:
    """Show random message from http://mydrunktexts.com"""

    def __init__(self):
        print 'mdt init'

    def __filter_source(self, text):
        start = 0
        end = text.find("<script", start) 
        novy = ""
        while end != -1:
            novy += text[start:end]
            start = text.find("</script>", end) + len("</script>")
            end = text.find("<script", start) 
        novy += text[start:]
        return novy

    def run(self, contact, msg):
        web_page = self.__filter_source(urllib.urlopen('http://mydrunktexts.com/random').read())
        soup = bs.BeautifulSoup(web_page)
        txt = soup.find(attrs={'class':'fmllink'}).string
        txt = txt.replace('&quot;','"')
        contact.send(txt)

    def exit(self):
        pass

provides = {'mdt': MDT}

