#!/usr/bin/env python
import sys
import os
sys.path.append(os.environ['DEEPMITOROOT'])
import argparse

from deepmitolib.blast import makeblastdb

def main():
  DESC = "DeepMito: Prepare sequence database"
  parser = argparse.ArgumentParser(description=DESC)
  parser.add_argument("-f", "--fasta",
                      help = "The input FASTA file name",
                      dest = "fasta", required = True)
  ns = parser.parse_args()

  makeblastdb(ns.fasta)

if __name__ == "__main__":
  main()  
