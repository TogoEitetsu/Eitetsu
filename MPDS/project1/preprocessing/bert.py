import os
import random
import collections

from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.metrics import f1_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from tqdm.notebook import tqdm
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

from transformers import AutoTokenizer, AutoModel, AdamW
import nlp


def seed_everything(seed):
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
        

class Classifier(nn.Module):
    def __init__(self, model_name, num_classes=2):
        super().__init__()

        self.bert = AutoModel.from_pretrained(model_name)
        self.dropout = nn.Dropout(0.1)
        self.linear = nn.Linear(768, num_classes)
        nn.init.normal_(self.linear.weight, std=self.bert.config.initializer_range)
        nn.init.zeros_(self.linear.bias)
    
    def forward(self, **inputs):
        outputs = self.bert(**inputs)
        output = outputs.last_hidden_state
        output = output[:, 0, :]
        output = self.dropout(output)
        output = self.linear(output)
        return output


if __name__ == "__main__":
    SEED = 21
    seed_everything(SEED)
    TRAIN