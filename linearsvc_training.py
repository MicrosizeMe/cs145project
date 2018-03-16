import feather
import pandas as pd
import numpy as np
from sklearn.svm import LinearSVC
from sklearn.metrics import roc_auc_score
import cPickle

print 'reading feather'
df = feather.read_dataframe('./data/final_feathers/encoded_training.feather')

print 'getting ys'
y_train = df[df.fold==0].truth.values
y_test = df[df.fold==2].truth.values

print 'creating Xs'
X_train = df[df.fold==0].copy()
del X_train['truth']
del X_train['fold']
print 'X_train done'
X_test = df[df.fold==2].copy()
del X_test['truth']
del X_test['fold']
print 'Xs done'

print y_train.shape
print X_train.shape

del df

lvc = LinearSVC(penalty='l1', dual=False, random_state=1)

print 'fitting lvc'
lvc.fit(X_train, y_train)

print 'creating lvc pickle'
with open('./models/default_c_lvc_model.bin', 'wb') as f:
    cPickle.dump(lvc, f)

print 'predict proba on y_test'
y_pred = rfc.predict(X_test)

print 'getting roc'
auc = roc_auc_score(y_test, y_pred)

print auc