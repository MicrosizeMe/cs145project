import feather
import pandas as pd
import numpy as np
import scipy.sparse as sp
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
import cPickle

print 'reading feather'
df = feather.read_dataframe('./data/final_feathers/total_df.feather')

print 'reading pickle'
str_column = pd.read_pickle('./string_pickle.bin')

print 'getting ys'
y_train = df[df.fold==0].truth.values
y_test = df[df.fold==2].truth.values

vec = HashingVectorizer(dtype=np.uint8, n_features=1000000,
    norm=None, lowercase=False, binary=True, token_pattern='\S+', 
    non_negative=True)


print 'creating Xs'
X_train = vec.transform(str_column[df.fold==0])
print 'X_train done'
X_test = vec.transform(str_column[df.fold==2])
print 'Xs done'

del df
del str_column

rfc = RandomForestClassifier(n_jobs=-1, verbose=1)

print 'fitting rfc'
rfc.fit(X_train, y_train)

print 'creating hashvec pickle'
with open('./models/hashvectorizer.bin', 'wb') as f:
    cPickle.dump(vec, f)

print 'creating rfc pickle'
with open('./models/default_rfc_model.bin', 'wb') as f:
    cPickle.dump(rfc, f)

print 'predict proba on y_test'
y_pred = rfc.predict_proba(X_test)

print 'getting roc'
auc = roc_auc_score(y_test, y_pred)

print auc