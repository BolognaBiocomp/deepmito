import numpy
from Bio import SeqIO
import logging

from time import localtime, strftime

from . import deepmitoconfig as dmcfg
import copy
import json

def annotToText(annotation, outfile):
  ofs = open(outfile, 'w')
  for acc in sorted(annotation.keys()):
    ofs.write("%s\t%s\t%.2f\n" % (acc, annotation[acc]['goa'][0], annotation[acc]['score']))
  ofs.close()

def printDate(msg):
  print ("[%s] %s" % (strftime("%a, %d %b %Y %H:%M:%S", localtime()), msg))

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
        print("Error while open/reading checkpoint file.")
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
    return numpy.array(pssm)

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
  mtx = numpy.concatenate((pssm, numpy.array(propencoding)), axis=1)
  mtx = mtx.reshape((1, mtx.shape[0], mtx.shape[1]))
  return acc, mtx

def check_sequence_pssm_match(sequence, psiblast_pssm):
    try:
        pssm_mat = BlastCheckPointPSSM(psiblast_pssm)
    except:
        logging.error("Failed reading/parsing PSSM file")
        raise
    else:
        try:
            assert(len(sequence) == pssm_mat.shape[0])
        except:
            logging.error("Sequence and PSSM have different lengths")
            raise

    return True

def write_gff_output(annotation, output_file):
    print("##gff-version 3", file = output_file)
    for acc in annotation:
        sequence = annotation[acc]['sequence']
        score = annotation[acc]['score']
        c = dmcfg.locmap[annotation[acc]['loc']]
        l = len(sequence)
        print(acc, "DeepMito", c[0], 1, l, score, ".", ".",
        "Ontology_term=%s;evidence=ECO:0000256" % c[1], file = output_file, sep = "\t")

def write_json_output(annotation, output_file):
    protein_jsons = []
    for acc in annotation:
        sequence = annotation[acc]['sequence']
        c = dmcfg.locmap[annotation[acc]['loc']]
        go_info = dmcfg.GOINFO[c[1]]

        acc_json = {'accession': acc, 'dbReferences': [], 'comments': []}
        acc_json['sequence'] = {
                                  "length": len(sequence),
                                  "sequence": sequence
                               }
        acc_json['dbReferences'].append({
            "id": c[1],
            "type": "GO",
            "properties": {
              "term": go_info['GO']['properties']['term'],
              "source": "IEA:DeepMito"
            },
            "evidences": [
              {
                "code": "ECO:0000256",
                "source": {
                  "name": "SAM",
                  "id": "DeepMito",
                  "url": "https://busca.biocomp.unibo.it/deepmito",
                }
              }
            ]
        })
        acc_json['comments'].append({
            "type": "SUBCELLULAR_LOCATION",
            "locations": [
              {
                "location": {
                  "value": go_info["uniprot"]["location"]["value"],
                  "evidences": [
                    {
                      "code": "ECO:0000256",
                      "source": {
                        "name": "SAM",
                        "id": "DeepMito",
                        "url": "https://busca.biocomp.unibo.it/deepmito",
                      }
                    }
                  ]
                }
              }
            ]
        })
        protein_jsons.append(acc_json)
    json.dump(protein_jsons, output_file, indent=5)
