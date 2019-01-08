import subprocess
import deepmitoconfig as dmcfg
from utils import printDate

def runPsiBlast(acc, dbfile, fastaFile, workEnv):
  psiblastStdOut   = workEnv.createFile(acc+".psiblast_stdout.", ".log")
  psiblastStdErr   = workEnv.createFile(acc+".psiblast_stderr.", ".log")
  psiblastOutPssm  = workEnv.createFile(acc+".psiblast.", ".pssm")
  psiblastOutAln   = workEnv.createFile(acc+".psiblast.", ".aln")
  psial2HSSPStdErr = workEnv.createFile(acc+".psial_stderr.", ".log")

  sequence = "".join([x.strip() for x in open(fastaFile).readlines()[1:]])
  printDate("%s: Running PsiBlast" % acc)
  subprocess.call(['psiblast', '-query', fastaFile,
                   '-db', dbfile,
                   '-out', psiblastOutAln,
                   '-out_ascii_pssm', psiblastOutPssm,
                   '-num_iterations', '3',
                   '-evalue', '1e-3'],
                   stdout=open(psiblastStdOut, 'w'),
                   stderr=open(psiblastStdErr, 'w'))
  return psiblastOutPssm, psiblastOutAln
