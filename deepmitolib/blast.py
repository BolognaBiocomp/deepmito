import subprocess
import deepmitoconfig as dmcfg
from utils import printDate

def runPsiBlast(acc, fastaFile, workEnv, dataCache):
  psiblastStdOut   = workEnv.createFile(acc+".psiblast_stdout.", ".log")
  psiblastStdErr   = workEnv.createFile(acc+".psiblast_stderr.", ".log")
  psiblastOutPssm  = workEnv.createFile(acc+".psiblast.", ".pssm")
  psiblastOutAln   = workEnv.createFile(acc+".psiblast.", ".aln")
  psial2HSSPStdErr = workEnv.createFile(acc+".psial_stderr.", ".log")

  sequence = "".join([x.strip() for x in open(fastaFile).readlines()[1:]])
  printDate("%s: Running PsiBlast" % acc)
  if not dataCache.lookup(sequence, 'psiblast.pssm'):
    subprocess.call([dmcfg.PSIBLASTBIN, '-query', fastaFile,
                     '-db', dmcfg.PSIBLASTDB,
                     '-out', psiblastOutAln,
                     '-out_ascii_pssm', psiblastOutPssm,
                     '-num_iterations', '3',
                     '-evalue', '1e-3'],
                     stdout=open(psiblastStdOut, 'w'),
                     stderr=open(psiblastStdErr, 'w'))

    #dataCache.store(psiblastOutAln, sequence, 'psiblast.aln')

    dataCache.store(psiblastOutPssm, sequence, 'psiblast.pssm')
  else:
    dataCache.retrieve(sequence, 'psiblast.pssm', psiblastOutPssm)

  return psiblastOutPssm, psiblastOutAln
