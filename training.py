import feather
import pandas as pd
from sklearn.svm import LinearSVC

df = feather.read_dataframe('./data/final_feathers/total_df.feather')
print 'read df'

train_y = df[df.fold==0].truth.values
test_y = df[df.fold==2].truth.values

train_X = df[df.fold==0]
test_X = df[df.fold==2]

del train_X['truth']
del train_X['fold']

del test_X['truth']
del test_X['fold']

del df

svc = LinearSVC(dual=False,penalty='l1',C=0.5,random_state=1)

print 'starting fit'

svc.fit(train_X, train_y)

print 'finished fit'

print 'starting score'

score = svc.score(test_X, test_y)

print 'finished score'
print score