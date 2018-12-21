# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 11:40:53 2017

@author: cas
"""

import tempfile
import shutil
import os

class TemporaryEnv():
  def __init__(self):
    tempfile.tempdir = os.path.abspath(tempfile.mkdtemp(prefix="job.tmpd.", dir="."))
  
  def destroy(self):
    if not tempfile.tempdir == None:
      shutil.rmtree(tempfile.tempdir)
      
  def createFile(self, prefix, suffix):
    outTmpFile = tempfile.NamedTemporaryFile(mode   = 'write',
                                             prefix = prefix,
                                             suffix = suffix,
                                             delete = False)
    outTmpFileName = outTmpFile.name
    outTmpFile.close()
    return outTmpFileName
  
  def createDir(self, prefix):
    outTmpDir = tempfile.mkdtemp(prefix=prefix)
    return outTmpDir
