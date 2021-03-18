import os
import subprocess
from . import deepmitoconfig as dmcfg
from . import utils

def check_db_index(dbfile):
  for ext in ['phr', 'pin', 'psq']:
      if not os.path.isfile(dbfile + ".%s" % ext):
          return False
  return True

def runPsiBlast(acc, dbfile, fastaFile, workEnv, data_cache=None):
  psiblastStdOut   = workEnv.createFile(acc+".psiblast_stdout.", ".log")
  psiblastStdErr   = workEnv.createFile(acc+".psiblast_stderr.", ".log")
  psiblastOutPssm  = workEnv.createFile(acc+".psiblast.", ".pssm")
  psiblastOutAln   = workEnv.createFile(acc+".psiblast.", ".aln")
  psial2HSSPStdErr = workEnv.createFile(acc+".psial_stderr.", ".log")

  sequence = "".join([x.strip() for x in open(fastaFile).readlines()[1:]])
  exec_blast = True
  if data_cache is not None:
    if data_cache.lookup(sequence, "psiblast.pssm"):
      exec_blast = False
  if exec_blast:
    if not check_db_index(dbfile):
      makeblastdb(dbfile)
    subprocess.call(['psiblast', '-query', fastaFile,
                     '-db', dbfile,
                     '-out', psiblastOutAln,
                     '-out_ascii_pssm', psiblastOutPssm,
                     '-num_iterations', '3',
                     '-evalue', '1e-3'],
                     stdout=open(psiblastStdOut, 'w'),
                     stderr=open(psiblastStdErr, 'w'))
    if data_cache is not None:
      data_cache.store(psiblastOutPssm, sequence, 'psiblast.pssm')
  else:
    data_cache.retrieve(sequence, 'psiblast.pssm', psiblastOutPssm)
  return psiblastOutPssm

def makeblastdb(dbfile):
  subprocess.call(['makeblastdb', '-in', dbfile, '-dbtype', 'prot'])
