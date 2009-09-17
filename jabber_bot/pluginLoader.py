#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, os.path, glob, helper, sys, imp

class PluginLoaderException(Exception):
    pass

class PluginLoader:

    def __init__(self, path):
        self.change_path(path)

    def __load_plugins(self):
        for plugin_filename in glob.glob(os.path.sep.join([self.path,'*.py'])):
            try:
                plugin = imp.load_source(os.path.split(plugin_filename)[1][:-3], plugin_filename)
                #plugin = __import__(plugin_filename[:-3]) # Get rid of .py
                for keyword in plugin.provides.keys():
                    if keyword in self.commands.keys():
                        raise PluginLoaderException('Keyword already used.')
                    self.commands[keyword] = plugin.provides[keyword]()
            except ImportError, err:
                print err
                raise PluginLoaderException('Cannot import %s.' % plugin_filename)
            except AttributeError:
                pass
                #raise PluginLoaderException('File %s is not correct plugin.' % plugin_filename)
            except NameError:
                pass
                #raise PluginLoaderException('File %s is not correct plugin.' % plugin_filename)

    def load(self):
        self.commands = {}
        self.__load_plugins()

    def change_path(self, path):
        self.path = path
        self.load()
    
    def get_plugin(self, keyword):
        if keyword == 'help':
            return helper.Helper(self.commands)
        return self.commands[keyword]

    def exit(self):
        for (key, obj) in self.commands.iteritems():
            obj.exit()
