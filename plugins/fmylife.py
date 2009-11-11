#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    import elementtree.ElementTree as et
except ImportError:
    import xml.etree.ElementTree as et

import urllib

class FMyLife:
    """Show random message from http://fmylife.com"""

    def __init__(self):
        print 'fmylife init'

    def run(self, contact, msg):
        rand = urllib.urlopen('http://api.betacie.com/view/random?language=en&key=readonly')
        tree = et.fromstring(rand.read())
        message = tree.find('items/item/text').text
        contact.send(message)

    def exit(self):
        pass

provides = {'fml' : FMyLife}

