#!/usr/bin/env python3
"""Train simple model (MaxEnt-style via logistic regression on engineered features)."""
import os
import joblib
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
FEAT_DIR = os.path.join(DATA_DIR, 'features')
MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'model')
os.makedirs(MODEL_DIR, exist_ok=True)

def train():
    df = pd.read_csv(os.path.join(FEAT_DIR, 'training.csv'))
    X = df[['lat','lon']]
    y = df['presence']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
    clf = LogisticRegression(max_iter=1000)
    clf.fit(X_train, y_train)
    pred = clf.predict_proba(X_test)[:,1]
    print('AUC:', roc_auc_score(y_test, pred))
    joblib.dump(clf, os.path.join(MODEL_DIR, 'model.joblib'))
    print('Saved model')

if __name__ == '__main__':
    train()