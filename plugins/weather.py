#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib, BeautifulSoup, re

class Weather:
    u"""zobrazí aktuální počasí ve městě
    Formát: weather Město"""

    meteo = {
        u'Karlovy Vary':'11414', u'Přimda':'11423', u'Tušimice':'11438', u'Plzeň':'11450',
        u'Churáňov':'11457', u'Milešovka':'11464', u'Kocelovice':'11487', u'Ústí nad Labem':'11502',
        u'Doksany':'11509', u'Praha':'11518', u'Praha Libuš':'11520', u'Temelín':'11538',
        u'České Budějovice':'11546', u'Liberec':'11603', u'Čáslav':'11624', u'Košetice':'11628',
        u'Kostelní Myslová':'11636', u'Pec pod Sněžkou':'11643', u'Pardubice':'11652', 
        u'Přibyslav':'11659', u'Polom':'11669', u'Ústí nad Orlicí':'11679', u'Svratouch':'11683',
        u'Dukovany':'11693', u'Kuchařovice':'11698', u'Luká':'11710', u'Brno':'11723',
        u'Šerák':'11730', u'Přerov':'11748', u'Červená u Libavé':'11766', u'Holešov':'11774',
        u'Ostrava':'11782', u'Lysá hora':'11787'
    } 

    def convert(self, str):
        return unicode(BeautifulSoup.BeautifulStoneSoup(str,
                  convertEntities=BeautifulSoup.BeautifulStoneSoup.HTML_ENTITIES))

    def __init__(self):
        print "weather init"

    def run(self, contact, msg):
        url = "http://www.chmi.cz/meteo/opss/pocasi/pocasina.php?%s"
        if msg in self.meteo.keys():
            data = urllib.urlencode([('indstanice',self.meteo[msg])])
            page = urllib.urlopen(url % data)
            soup = BeautifulSoup.BeautifulSoup(page.read())            

            response = u""
            for radek in soup.findAll('tr'):
                info = radek.findAll('td')
                if not re.match('^(\s*(&nbsp;)*)*$', info[1].string):
                    response += self.convert(info[0].string) + self.convert(info[1].string) + '\n'
            contact.send(response)

        else:
            l = self.meteo.keys()
            l.sort()
            contact.send(u"Dostupná města: "+", ".join(l))

    def exit(self):
        pass

provides = {'weather':Weather}
