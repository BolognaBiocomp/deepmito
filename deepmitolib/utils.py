import numpy
from Bio import SeqIO

from time import localtime, strftime

import deepmitoconfig as dmcfg
import copy

def annotToText(annotation, outfile):
  ofs = open(outfile, 'w')
  for acc in sorted(annotation.keys()):
    ofs.write("%s\t%s\t%.2f\n" % (acc, annotation[acc]['goa'][0], annotation[acc]['score']))
  ofs.close()

def printDate(msg):
  print "[%s] %s" % (strftime("%a, %d %b %Y %H:%M:%S", localtime()), msg)

def _check(line):
    import re
    if not re.search('Last position-specific scoring matrix computed', line):
        raise InvalidCheckpointFileError

def logistic(x):
    # return math.tanh(x)
    return 1 / (1 + numpy.exp(-x))

class InvalidCheckpointFileError(Exception):
    def __init__(self):
        pass


def BlastCheckPointPSSM(checkpointFile, newFormat = True, transform = True):
    try:
        checkpointFile = open(checkpointFile).readlines()
    except IOError:
        print "Error while open/reading checkpoint file."
        raise
    pssm = None
    if newFormat:
        try:
            pssm = _pssmParseNew(checkpointFile, transform)
        except:
            raise
    return pssm

def _pssmParseNew(checkpoint, transform):
    headerSize = 3
    footerSize = -6

    try:
        _check(checkpoint[1])
    except:
        raise

    pssm = []

    for line in checkpoint[headerSize:footerSize]:
        line = line.split()[2:22]
        pos = numpy.zeros(20)
        for j in range(20):
            if transform:
                pos[j] = logistic(float(line[j]))  # 1.0 / (1.0 + math.exp(-1 * float(line[j + shift])))
            else:
                pos[j] = float(line[j])
        pssm.append(pos)
    return pssm

def readfasta(fastafile):
  record = next(SeqIO.parse(fastafile, "fasta"))
  return record.id, str(record.seq)

def seq_to_pssm(sequence):
  aaOrder = "ARNDCQEGHILKMFPSTWYV"
  X = []
  for aa in sequence:
    x = [0.0]*len(aaOrder)
    try:
      x[aaOrder.index(aa)]=1.0
    except:
      pass
    X.append(x)
  return numpy.array(X)

def encode(fasta, properties, blastpssm):
  acc, sequence = readfasta(fasta)
  try:
    pssm = BlastCheckPointPSSM(blastpssm)
  except:
    pssm = seq_to_pssm(sequence)
  assert(len(sequence)==len(pssm))
  propencoding = []
  for aa in sequence:
    propencoding.append(properties.get(aa, [0.0]*len(properties['A'])))
  mtx = numpy.concatenate((numpy.array(pssm), numpy.array(propencoding)), axis=1)
  mtx = mtx.reshape((1, mtx.shape[0], mtx.shape[1]))
  return acc, mtx










