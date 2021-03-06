#!/usr/bin/env python
import sys
import logging
import os
if 'DEEPMITO_ROOT' in os.environ:
    sys.path.append(os.environ['DEEPMITO_ROOT'])
else:
    logging.error("DEEPMITO_ROOT environment varible is not set")
    logging.error("Please, set and export DEEPMITO_ROOT to point to deepmito root folder")
    sys.exit(1)

import argparse
import numpy

from Bio import SeqIO

import deepmitolib.deepmitoconfig as cfg
from deepmitolib.cnn import MultiCNNWrapper
from deepmitolib.utils import encode, annotToText, check_sequence_pssm_match, printDate, write_gff_output
from deepmitolib.workenv import TemporaryEnv
from deepmitolib.blast import runPsiBlast

def run_multifasta(ns):
  workEnv = TemporaryEnv()
  multiModel = MultiCNNWrapper(cfg.MODELS)
  annotation = {}
  try:
    for record in SeqIO.parse(ns.fasta, 'fasta'):
      prefix = record.id.replace("|","_")
      fastaSeq  = workEnv.createFile(prefix+".", ".fasta")
      printDate("Processing sequence %s" % record.id)
      SeqIO.write([record], fastaSeq, 'fasta')
      printDate("Running PSIBLAST")
      pssmFile, _ = runPsiBlast(prefix, ns.dbfile, fastaSeq, workEnv)
      printDate("Predicting sumbitochondrial localization")
      acc, X = encode(fastaSeq, cfg.AAIDX10, pssmFile)
      pred   = multiModel.predict(X)
      cc = numpy.argmax(pred)
      score = round(numpy.max(pred),2)
      annotation[record.id] = {'sequence': str(record.seq), 'loc': cc, 'score': score}
    #annotToText(annotation, ns.outf)
    ofs = open(ns.outf, 'w')
    write_gff_output(annotation, ofs)
    ofs.close()
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
    printDate("Processing sequence %s" % record.id)
    printDate("Using user-provided PSSM file, skipping PSIBLAST")
    pssmFile = ns.psiblast_pssm
    try:
      check_sequence_pssm_match(str(record.seq), pssmFile)
    except:
      logging.exception("Error in PSSM: sequence and provided PSSM do not match.")
      sys.exit(1)
    else:
      try:
        prefix = record.id.replace("|","_")
        fastaSeq  = workEnv.createFile(prefix+".", ".fasta")
        SeqIO.write([record], fastaSeq, 'fasta')
        printDate("Predicting sumbitochondrial localization")
        acc, X = encode(fastaSeq, cfg.AAIDX10, pssmFile)
        pred   = multiModel.predict(X)
        cc = numpy.argmax(pred)
        score = round(numpy.max(pred),2)
        annotation[record.id] = {'sequence': str(record.seq), 'loc': cc, 'score': score}
        ofs = open(ns.outf, 'w')
        write_gff_output(annotation, ofs)
        ofs.close()
      except:
        logging.exception("Errors occurred:")
        sys.exit(1)
      else:
        workEnv.destroy()
        sys.exit(0)

def main():
  DESC = "DeepMito: Predictor of protein submitochondrial localization"
  parser = argparse.ArgumentParser(description=DESC, prog="deepmito.py")

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
