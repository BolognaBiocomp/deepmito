# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 15:58:18 2017

@author: cas
"""

import os
import hashlib
import shutil
import errno

class DataCache():
    def __init__(self, cacheDir, forceRebuild=False, levels=2, dir_name_chars=2):
        self.cacheDir = cacheDir
        self.forceRebuild = forceRebuild
        self.levels = levels
        self.dir_name_chars = dir_name_chars

    def _create_path(self, digest):
        path = self.cacheDir
        for i in range(self.levels):
            s = i * self.dir_name_chars
            e = s + self.dir_name_chars
            path = os.path.join(path, digest[s:e])
            try:
                os.mkdir(path)
            except FileExistsError:
                pass
            except:
                raise

    def _get_path(self, digest):
        path = self.cacheDir
        for i in range(self.levels):
            s = i * self.dir_name_chars
            e = s + self.dir_name_chars
            path = os.path.join(path, digest[s:e])
        return path

    def lookup(self, sequence, ext):
        digest = hashlib.sha512(sequence.encode("utf-8")).hexdigest()
        name = os.path.join(self._get_path(digest), '%s.%s' % (digest, ext))
        try:
            f=open(name)
        except:
            return False
        else:
            f.close()
            return (True and (not self.forceRebuild))

    def store(self, filename, sequence, ext):
        if not self.lookup(sequence, ext) or self.forceRebuild:
            digest = hashlib.sha512(sequence.encode("utf-8")).hexdigest()
            self._create_path(digest)
            dest = os.path.join(self._get_path(digest), '%s.%s' % (digest, ext))
            shutil.copyfile(filename, dest)

    def retrieve(self, sequence, ext, outfile):
        if self.lookup(sequence, ext):
            digest = hashlib.sha512(sequence.encode("utf-8")).hexdigest()
            name = os.path.join(self._get_path(digest), '%s.%s' % (digest, ext))
            shutil.copyfile(name, outfile)

    def get_handle(self, sequence, ext):
        fh = None
        if self.lookup(sequence, ext):
            digest = hashlib.sha512(sequence.encode("utf-8")).hexdigest()
            name = os.path.join(self._get_path(digest), '%s.%s' % (digest, ext))
            fh = open(name)
        return fh
