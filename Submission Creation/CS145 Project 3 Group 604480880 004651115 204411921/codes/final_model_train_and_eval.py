import feather
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
import cPickle

print 'reading feathers'
df = feather.read_dataframe('./data/final_feathers/encoded_training.feather')
df_test = feather.read_dataframe('./data/final_feathers/encoded_test.feather')

print 'getting ys'
y_train = df.truth.values
y_test = df_test.truth.values

print 'creating Xs'
X_train = df
X_test = df_test

print X_train.shape
print X_test.shape

del X_train['truth']
del X_train['fold']
del X_test['truth']
print 'Xs done'

print X_train.shape
print X_test.shape
print y_train.shape
print y_test.shape

rfc = RandomForestClassifier(n_jobs=7, verbose=2, n_estimators=500, max_depth=100)
rfc.fit(X_train, y_train)

print 'creating rfc pickle'
with open('./models/final_rfc_model.bin', 'wb') as f:
    cPickle.dump(rfc, f)

print 'predict on X_test'
y_pred = rfc.predict(X_test)

print 'getting roc'
auc = roc_auc_score(y_test, y_pred)

print auc