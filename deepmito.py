#!/usr/bin/env python
import sys
import os
sys.path.append(os.environ['DEEPMITO_ROOT'])
import argparse
import numpy
import logging
from Bio import SeqIO

import deepmitolib.deepmitoconfig as cfg
from deepmitolib.cnn import MultiCNNWrapper
from deepmitolib.utils import encode, annotToText, check_sequence_pssm_match
from deepmitolib.workenv import TemporaryEnv
from deepmitolib.blast import runPsiBlast

def run_multifasta(ns):
  workEnv = TemporaryEnv()
  multiModel = MultiCNNWrapper(cfg.MODELS)
  annotation = {}
  try:
    for record in SeqIO.parse(ns.fasta, 'fasta'):
      record.id = record.id.replace("|","_")
      fastaSeq  = workEnv.createFile(record.id+".", ".fasta")
      SeqIO.write([record], fastaSeq, 'fasta')
      pssmFile, _ = runPsiBlast(record.id, ns.dbfile, fastaSeq, workEnv)
      acc, X = encode(fastaSeq, cfg.AAIDX10, pssmFile)
      pred   = multiModel.predict(X)
      cc = cfg.GOMAP[numpy.argmax(pred)]
      score = round(numpy.max(pred),2)
      annotation[record.id] = {'sequence': {'len': len(str(record.seq)), 'sequence': str(record.seq)},
                                   'goa': [cc], 'features': [], 'score': score, 'second': '-', 'alt_score': 0.0}
    annotToText(annotation, ns.outf)
  except:
    logging.exception("Errors occurred:")
    sys.exit(1)
  else:
    workEnv.destroy()
    sys.exit(0)

def run_pssm(ns):
  workEnv = TemporaryEnv()
  multiModel = MultiCNNWrapper(cfg.MODELS)
  annotation = {}
  try:
    record = SeqIO.read(ns.fasta, "fasta")
  except:
    logging.exception("Error reading FASTA: file is not FASTA or more than one sequence is present")
    sys.exit(1)
  else:
    pssmFile = ns.psiblast_pssm
    try:
      check_sequence_pssm_match(str(record.seq), pssmFile)
    except:
      logging.exception("Error in PSSM: sequence and provided PSSM do not match.")
      sys.exit(1)
    else:
      try:
        record.id = record.id.replace("|","_")
        fastaSeq  = workEnv.createFile(record.id+".", ".fasta")
        SeqIO.write([record], fastaSeq, 'fasta')
        acc, X = encode(fastaSeq, cfg.AAIDX10, pssmFile)
        pred   = multiModel.predict(X)
        cc = cfg.GOMAP[numpy.argmax(pred)]
        score = round(numpy.max(pred),2)
        annotation[record.id] = {'sequence': {'len': len(str(record.seq)), 'sequence': str(record.seq)},
                                   'goa': [cc], 'features': [], 'score': score, 'second': '-', 'alt_score': 0.0}
        annotToText(annotation, ns.outf)
      except:
        logging.exception("Errors occurred:")
        sys.exit(1)
      else:
        workEnv.destroy()
        sys.exit(0)

def main():
  DESC = "DeepMito: Predictor of protein submitochondrial localization"
  parser = argparse.ArgumentParser(description=DESC)

  subparsers   = parser.add_subparsers(title = "subcommands",
                                       description = "valid subcommands",
                                       help = "additional help",
                                       required = True)
  multifasta  = subparsers.add_parser("multi-fasta",
                                        help = "Multi-FASTA input module",
                                        description = "DeepMito: Multi-FASTA input module.")
  pssm  = subparsers.add_parser("pssm", help = "PSSM input module (one sequence at a time)",
                                  description = "DeepMito: PSSM input module.")
  multifasta.add_argument("-f", "--fasta",
                            help = "The input multi-FASTA file name",
                            dest = "fasta", required = True)
  multifasta.add_argument("-d", "--dbfile",
                            help = "The PSIBLAST DB file",
                            dest = "dbfile", required= True)
  multifasta.add_argument("-o", "--outf",
                        help = "The output GFF3 file",
                        dest = "outf", required = True)
  multifasta.set_defaults(func=run_multifasta)

  pssm.add_argument("-f", "--fasta",
                        help = "The input FASTA file name (one sequence)",
                        dest = "fasta", required = True)
  pssm.add_argument("-p", "--pssm",
                        help = "The PSIBLAST PSSM file",
                        dest = "psiblast_pssm", required= True)
  pssm.add_argument("-o", "--outf",
                        help = "The output GFF3 file",
                        dest = "outf", required = True)
  pssm.set_defaults(func=run_pssm)
  if len(sys.argv) == 1:
    parser.print_help()
  else:
    ns = parser.parse_args()
    ns.func(ns)

if __name__ == "__main__":
  main()
