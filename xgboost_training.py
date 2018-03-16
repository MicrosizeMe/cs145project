import xgboost as xgb
import feather
import pandas as pd
import numpy as np
import scipy.sparse as sp
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.metrics import roc_auc_score
import cPickle

print 'reading feather'
df = feather.read_dataframe('./data/final_feathers/total_df.feather')

print 'reading pickle'
str_column = pd.read_pickle('./data/final_feathers/string_pickle.bin')

vec = HashingVectorizer(dtype=np.uint8, n_features=500000,
    norm=None, lowercase=False, binary=True, token_pattern='\S+', 
    non_negative=True)

print 'getting ys'
y_train = df[df.fold<=1].truth.values
y_test = df[df.fold==2].truth.values

print 'creating Xs'
X_train = vec.transform(str_column[df.fold<=1])
print 'X_train done'
X_test = vec.transform(str_column[df.fold==2])
print 'Xs done'

del df
del str_column

print 'creating DMatrix'
dtrain = xgb.DMatrix(X_train, label=y_train)

print 'creating dtrain pickle'
with open('./data/final_feathers/xgb_dtrain.bin', 'wb') as f:
    cPickle.dump(rfc, f)

print 'training'
param = {'n_jobs': 7}
bst = xgb.train(param, dtrain, verbose_eval=True)

print 'done training'

print 'saving model'
bst.save_model('./models/xgb.model')

print 'predicting y_test'
y_pred = bst.predict(y_test)

print 'getting roc'
auc = roc_auc_score(y_test, y_pred)

print auc