#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib, urllib2, re, BeautifulSoup

class IDOS:
    u"""Zjišťuje informace o dopravních spojeních.
    Formát: idos from odkud to kam [at čas [datum]]"""

    def __init__(self):
        print "idos init"
        self.regex = re.compile("from (.+) to (.+?)(?: at (\d\d:\d\d)( \d{1,2}.\d{1,2}.\d{4})?)?$")

    def run(self, contact, msg):
        msg = msg.encode('utf-8')
        found = self.regex.findall(msg)
        if found:
            connection = self.find_connection(found[0])
            contact.send(connection)
        else:
            contact.send("I don't understand, read help.")

    def find_connection(self, args):
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', \
            'Opera/8.01 (J2ME/MIDP; Opera Mini/3.0.6306/1528; en; U; ssr)'), \
            ('Referer', 'http://ttwap.chaps.cz')]
        url = "http://ttwap.chaps.cz/conn.aspx?%s&jr=C&OP=&Lang=C&Format=3&cmd=search"
        
        data = urllib.urlencode([('odkud',args[0]),('kam',args[1]),
            ('cas',args[2]),('datum',args[3])])
        page = opener.open(url % data)

        soup = BeautifulSoup.BeautifulSoup(page.read())

        return self.format_output(soup)

    def convert(self, str):
        return unicode(BeautifulSoup.BeautifulStoneSoup(str,
                  convertEntities=BeautifulSoup.BeautifulStoneSoup.HTML_ENTITIES))

    def format_output(self, soup):
        response = soup.findAll('p')
        caption = response[0].firstText().string
        caption = self.convert(caption)

        return_string = caption
        if u'Upřesnit zadání' in caption:
            for s in soup.findAll('select'):
                return_string += u'\nSpecifikujte blíže, které místo jste měli na mysli:\n'
                for o in s.findAll('option'):
                    return_string += self.convert(o.string) + '\n'

        else:
            informations = response[1].contents
            while len(informations) > 7:
                odkud = self.convert(informations[0].string)
                cas_odjezdu = self.convert(informations[1].string)
                kam = self.convert(informations[3].string)
                cas_prijezdu = self.convert(informations[4].string)
                spoj = self.convert(informations[6].string)
                return_string += "\nFrom: %s %s\nTo: %s %s\n%s\n" % \
                (odkud, cas_odjezdu, kam, cas_prijezdu, spoj)
                informations = informations[8:] 

            return_string += "\n" + self.convert(informations[0].string)

        return return_string

    def exit(self):
        pass

class MHD(IDOS):
    u"""Hledá spojení v MHD 76 českých měst.
    Formát: mhd město from odkud to kam [at čas [datum]] | mhd list"""

    cities = {u'Turnov': u'Turnov', u'Trutnov': u'TUCz', 
            u'\u010cesk\xe9 Bud\u011bjovice': u'CBCz', u'Jihlava': u'JICz', 
            u'T\u0159inec': u'TRICz', u'Znojmo': u'ZNCz', u'Zl\xedn': u'ZLCz',
            u'Chrudim': u'CRCz', u'Fr\xfddek-M\xedstek': u'FMCz',
            u'P\u0159\xedbram': u'PBCz', u'\u017d\u010f\xe1r nad S\xe1zavou':
            u'ZRCz', u'Velk\xe9 Mezi\u0159\xed\u010d\xed': u'VELMCz', 
            u'Hradec Kr\xe1lov\xe9': u'HKCz', u'Klatovy': u'KTCz', 
            u'Beroun': u'BECz', u'Orlov\xe1': u'ORCz', u'Kutn\xe1 Hora': u'KHCz',
            u'P\u0159e\u0161tice': u'PRECz', u'Vset\xedn': u'VSCz', u'Karlovy Vary': u'KVCz', u'T\xe1bor': u'TACz', u'Doma\u017elice': u'DOCz',
            u'Havl\xed\u010dk\u016fv Brod': u'HBCz', u'Mlad\xe1 Boleslav':
            u'MBCz', u'M\u011bln\xedk': u'MECz', u'D\u011b\u010d\xedn':
            u'DCCz', u'P\u0159erov': u'PRCz', u'Poli\u010dka': u'POLCz',
            u'Pelh\u0159imov': u'PECz', u'Hranice': u'HRACz', u'\xdast\xed nad Labem': u'ULCz', u'Brno': u'IDSJMK', u'Mikulov': u'MIKCz',
            u'Olomouc': u'OLCz', u'Plze\u0148': u'PMCz', u'Chomutov': u'CVCz',
            u'Jind\u0159ich\u016fv Hradec': u'JHCz', u'Bene\u0161ov': u'BNCz',
            u'Pardubice': u'PACz', u'Dv\u016fr Kr\xe1lov\xe9 nad Labem':
            u'DKCz', u'\u010cesk\xfd T\u011b\u0161\xedn': u'CTECz',
            u'\u010c\xe1slav': u'Caslav', u'Kladno': u'KDCz', u'Hodon\xedn':
            u'HOCz', u'Jablonec nad Nisou': u'JNCz', u'J\xe1chymov': u'JachCz',
            u'Teplice': u'TPCz', u'Kol\xedn': u'KOCz', u'Blansko': u'BKCz',
            u'\u010cesk\xe1 L\xedpa': u'CLCz', u'Krom\u011b\u0159\xed\u017e':
            u'KROMCz', u'Prost\u011bjov': u'PVCz', u'Vla\u0161im': u'VlasimCz',
            u'A\u0161': u'ASCz', u'Ostrava': u'OVCz', u'Vala\u0161sk\xe9 Mezi\u0159\xed\u010d\xed': u'VACz', u'B\u0159eclav': u'BVCz',
            u'Nymburk': u'NBCz', u'Z\xe1b\u0159eh': u'ZACz', u'Vy\u0161kov':
            u'VYCz', u'Liberec': u'LICz', u'Kyjov': u'KYJCz', u'Tachov':
            u'TCCz', u'Most a Litv\xednov': u'MOCz', u'Brunt\xe1l': u'BRCz',
            u'Sokolov': u'SOCz', u'Strakonice': u'STCz', u'Hav\xed\u0159ov':
            u'HAVCz', u'Krnov': u'KRNCz', u'Praha': u'PID', u'Cheb': u'CHCz',
            u'P\xedsek': u'PICz', u'\u0160umperk': u'SUCz', u'Karvin\xe1':
            u'KACz', u'St\u0159\xedbro': u'SBCz', u'Stud\xe9nka': u'SDCz'} 

    def __init__(self):
        print "mhd init"
        self.regex = re.compile("(?:(.+) from (.+) to (.+?)(?: at (\d\d:\d\d)( \d{1,2}.\d{1,2}.\d{4})?)?$)|(list)")

    def find_connection(self, args):
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', \
            'Opera/8.01 (J2ME/MIDP; Opera Mini/3.0.6306/1528; en; U; ssr)'), \
            ('Referer', 'http://ttwap.chaps.cz')]
        url = 'http://ttwap.chaps.cz/ConnMHD.aspx?%s&linka=&OP=&Lang=C&Format=3&cmd=search'
        
        if not self.convert(args[0]) in self.cities.keys():
            if args[5] == 'list':
                c = self.cities.keys()
                c.sort()
                return ", ".join(c)
            return "Město nenalezeno"

        city = self.cities[self.convert(args[0])]
        data = urllib.urlencode([('JR',city),('odkud',args[1]),
            ('kam',args[2]),('cas',args[3]),('datum',args[4])])
        page = opener.open(url % data)

        soup = BeautifulSoup.BeautifulSoup(page.read())

        return self.format_output(soup)

provides = {'idos' : IDOS, 'mhd' : MHD}

