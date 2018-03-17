import feather
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
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

#hyperparameter tuning
depths = [10, 20, 40, 80, 100, 120, 180, 250]

for depth in depths:
	rfc = RandomForestClassifier(n_jobs=7, verbose=2, n_estimators=20, max_depth=depth)
	print 'fitting rfc %s' % depth
	rfc.fit(X_train, y_train)
	y_pred = rfc.predict(X_test)
	auc = roc_auc_score(y_test, y_pred)
	print 'depth=%s auc=%s' % (depth, auc)

print 'creating rfc pickle'
with open('./models/default_rfc_model.bin', 'wb') as f:
    cPickle.dump(rfc, f)


print 'predict on X_test'
y_pred = rfc.predict(X_test)

print 'getting roc'
auc = roc_auc_score(y_test, y_pred)

print auc