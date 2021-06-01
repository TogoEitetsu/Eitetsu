import re
import glob
import json
import numpy as np
import pandas as pd

DATA_DIR = '/Users/togoeitetsu/Documents/k-lab/data/名大会話コーパス/nucc/'

def input_text(path):
    f = open(path, 'r')
    data = f.read()
    f.close()
    return data


if __name__ == "__main__":
    filepath = glob.glob(DATA_DIR + '*.txt')
    test_file = filepath[0]
    data = input_text(test_file)
    print(data)