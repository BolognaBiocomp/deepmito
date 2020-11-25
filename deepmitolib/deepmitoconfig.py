import os

DEEPMITOROOT=os.environ['DEEPMITO_ROOT']

MODELS=[os.path.join(DEEPMITOROOT, "models", "model.0.no-opt.h5"),
        os.path.join(DEEPMITOROOT, "models", "model.1.no-opt.h5"),
        os.path.join(DEEPMITOROOT, "models", "model.2.no-opt.h5"),
        os.path.join(DEEPMITOROOT, "models", "model.3.no-opt.h5"),
        os.path.join(DEEPMITOROOT, "models", "model.4.no-opt.h5"),
        os.path.join(DEEPMITOROOT, "models", "model.5.no-opt.h5"),
        os.path.join(DEEPMITOROOT, "models", "model.6.no-opt.h5"),
        os.path.join(DEEPMITOROOT, "models", "model.7.no-opt.h5"),
        os.path.join(DEEPMITOROOT, "models", "model.8.no-opt.h5"),
        os.path.join(DEEPMITOROOT, "models", "model.9.no-opt.h5")]


AAIDX10 = {'A': [0.00,0.07,0.18,0.38,0.21,0.28,0.50,0.48,0.63,0.47],
'R': [0.49,0.80,0.82,1.00,0.00,0.56,0.82,0.41,0.63,0.82],
'N': [0.75,0.47,0.41,0.69,0.51,0.54,0.53,0.76,0.85,0.15],
'D': [0.59,0.43,0.01,0.69,0.21,0.49,0.11,0.59,0.76,0.77],
'C': [0.46,0.26,0.56,0.15,0.27,1.00,1.00,0.35,0.86,0.87],
'Q': [0.30,0.54,0.46,0.78,0.76,0.59,0.80,0.34,0.57,0.00],
'E': [0.03,0.53,0.00,0.80,0.11,0.55,0.57,0.58,0.49,0.56],
'G': [0.83,0.00,0.38,0.41,0.49,0.43,0.94,1.00,0.16,0.70],
'H': [0.32,0.61,0.36,0.54,0.89,0.69,0.01,0.59,0.86,1.00],
'I': [0.23,0.44,0.93,0.23,0.31,0.47,0.31,0.60,0.74,0.14],
'L': [0.14,0.48,0.38,0.14,0.31,0.00,0.84,0.33,0.69,0.82],
'K': [0.34,0.68,0.38,0.95,0.88,0.10,0.89,0.48,0.45,0.74],
'M': [0.04,0.53,0.33,0.24,1.00,0.80,0.63,0.52,0.26,0.66],
'F': [0.37,0.72,0.34,0.04,0.52,0.28,0.75,0.73,1.00,0.48],
'P': [1.00,0.40,0.13,0.24,0.70,0.36,0.64,0.00,0.76,0.52],
'S': [0.65,0.22,0.48,0.58,0.40,0.36,0.00,0.25,0.33,0.53],
'T': [0.50,0.31,0.77,0.64,0.43,0.51,0.62,0.25,0.43,0.64],
'W': [0.51,1.00,0.24,0.00,0.15,0.59,0.41,0.41,0.00,0.44],
'Y': [0.81,0.85,0.66,0.29,0.46,0.31,0.46,0.71,0.56,0.72],
'V': [0.23,0.31,1.00,0.34,0.59,0.28,0.24,0.51,0.46,0.75],
'X': [0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00],
'U': [0.46,0.26,0.56,0.15,0.27,1.00,1.00,0.35,0.86,0.87],
'B': [0.75,0.47,0.41,0.69,0.51,0.54,0.53,0.76,0.85,0.15],
'Z': [0.30,0.54,0.46,0.78,0.76,0.59,0.80,0.34,0.57,0.00],
'J': [0.23,0.44,0.93,0.23,0.31,0.47,0.31,0.60,0.74,0.14]}

GOMAP = {0: "GO:0005741", 1: "GO:0005743", 2: "GO:0005758", 3: "GO:0005759"}
GOINFO        = {"GO:0005741": {"uniprot": {"location": {"value": "Mitochondrion outer membrane"}},
                                "GO": {"type": "GO", "id": "GO:0005741",
                                       "properties": {"term": "C:mitochondrial outer membrane"},
                                       "evidences": [{"code": "ECO:0000256|SAM:DeepMito"}]}},
                "GO:0005743": {"uniprot": {"location": {"value": "Mitochondrion inner membrane"}},
                               "GO": {"type": "GO", "id": "GO:0005743",
                                      "properties": {"term": "C:mitochondrial inner membrane"},
                                      "evidences": [{"code": "ECO:0000256|SAM:DeepMito"}]}},
                "GO:0005758": {"uniprot": {"location": {"value": "Mitochondrion intermembrane space"}},
                               "GO": {"type": "GO", "id": "GO:0005758",
                                      "properties": {"term": "C:mitochondrial intermembrane space"},
                                      "evidences": [{"code": "ECO:0000256|SAM:DeepMito"}]}},
                "GO:0005759": {"uniprot": {"location": {"value": "Mitochondrion matrix"}},
                               "GO": {"type": "GO", "id": "GO:0005759",
                                      "properties": {"term": "C:mitochondrial matrix"},
                                      "evidences": [{"code": "ECO:0000256|SAM:DeepMito"}]}}}

DOCKER_PSIBLAST_DBDIR = "/seqdb"
