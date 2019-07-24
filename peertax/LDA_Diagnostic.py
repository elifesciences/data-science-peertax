import glob
import re
import numpy as np


def LDA_Scores(base_pth):
    # Compute arrays of model scores from logs in folder "base_pth"
    cv_arr = []
    um_arr = []
    # Fields to look for
    p = re.compile(r"\(C_V\): (\d+\.\d+)")
    q = re.compile(r"\(UMass\): (-*\d+\.\d+)")
    if not glob.glob(base_pth+"*.log"):
        raise Exception('No file found.')

    # Loop over log files in folder & grab relevant scores
    for file in glob.glob(base_pth+"*.log"):
        log_file = open(file)
        num_topics = file.split('_')[-1].split('.')[0]
        matches = [p.findall(l) for l in log_file]
        matches = [m for m in matches if len(m) > 0]
        if matches:
            cv_arr.append([num_topics, matches[0][0]])
        log_file.close()
        log_file = open(file)
        matches = [q.findall(l) for l in log_file]
        matches = [m for m in matches if len(m) > 0]
        if matches:
            um_arr.append([num_topics, matches[0][0]])
        log_file.close()

    # Convert to numpy
    cv_arr = np.asarray(cv_arr, dtype=np.float64)
    um_arr = np.asarray(um_arr, dtype=np.float64)

    # Sort per first column
    cv_arr = cv_arr[cv_arr[:, 0].argsort()]
    um_arr = um_arr[um_arr[:, 0].argsort()]

    return cv_arr, um_arr


def LDA_Conv(base_pth, num_topics='5'):
    # Compute model "num_topics" convergence curve from log in folder "base_pth"
    filename = base_pth + 'gensim_' + num_topics + '.log'

    # Field to look for
    p = re.compile(r"(-*\d+\.\d+) per-word .* (\d+\.\d+) perplexity")

    # Scan log file & grab relevant fields
    log_file = open(filename)
    matches = [p.findall(l) for l in log_file]
    matches = [m for m in matches if len(m) > 0]
    tuples = [t[0] for t in matches]
    perplexity = [float(t[1]) for t in tuples]
    likelihood = [float(t[0]) for t in tuples]
    iter_no = list(range(0, len(tuples), 1))
    log_file.close()

    return iter_no, perplexity, likelihood
