#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re, threading, datetime

class At:
    """show message at specified time."""

    def __init__(self):
        self.exact_time = re.compile('^(?:(\d{1,2}:\d{2})|(\d+)([msh])) (.*)$')
        self.list_of_times = []
        self.timer = None

    def __send_message(self, contact, msg):
        contact.send(msg)

    def run(self, contact, msg):
        match = self.exact_time.match(msg)
        if match:
            now = datetime.datetime.now()
            spec = match.groups()
            if spec[0]:
                start_time = datetime.datetime.combine(datetime.date.today(),
                        datetime.time(*map(int, spec[0].split(':'))))
            else:
                if spec[2] == 'h':
                    start_time = now + datetime.timedelta(0,int(spec[1])*3600)
                elif spec[2] == 'm':
                    start_time = now + datetime.timedelta(0, int(spec[1])*60)
                else:
                    start_time = now + datetime.timedelta(0, int(spec[1]))

            if self.timer:
                self.timer.cancel()
            self.list_of_times.append((start_time, contact, spec[3]))
            self.list_of_times.sort()
            first = self.list_of_times[0]
            now = datetime.datetime.now()
            self.timer = threading.Timer((first[0]-now).seconds, self.__send_message, [first[1], first[2]])
            self.timer.start()

        else:
            contact.send('Wrong format of message, see help.')

    def exit(self):
        pass

provides = {'at' : At}
