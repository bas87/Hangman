#!/usr/bin/python
# -*- coding: utf-8 -*-
 
import os, sys
import random,re

class WordReader:
    builtin_words = u"albatros  banan"

    def __init__(self, filename, min_length = 5):
        self.min_length = min_length
        filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), filename)

        print "Trying to open file %s" % (filename,)
        try:
            f = open(filename, "r")
        except:
            print "Couldn't open dictionary file %s, using builtins" % (filename,)
            self.words = self.builtin_words
            self.filename = None
            return
        self.words = f.read()
        self.filename = filename
        print "Got %d bytes." % (len(self.words),)

    def SetMinLength(min_length):
        self.min_length = min_length

    def Get(self):
    	print self.words
        reg = re.compile('\s+([a-zA-Z]+)\s+')
        n = 50 # safety valve; maximum number of tries to find a suitable word
        while n:
            index = int(random.random()*len(self.words))
            m = reg.search(self.words[index:])
            if m and len(m.groups()[0]) >= self.min_length: break
            n = n - 1
        if n: return m.groups()[0].lower()
        return "error"

def stdprint(x):
    print x