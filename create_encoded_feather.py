import feather
import pandas as pd
import numpy as np
import cPickle
from sklearn.preprocessing import LabelEncoder

print 'reading df'
df = feather.read_dataframe('./data/final_feathers/total_df.feather')

print 'adding anon feature'
df['anon'] = np.where(df['user_id']==-1, 1, -1).astype('int8')

attributes_to_encode = [
'USER_COUNTY_NAME','USER_COUNTRY_CODE','USER_CONTINENT_CODE',
'USER_TIME_ZONE','USER_REGION_CODE','USER_CITY_NAME',
'REVISION_TAGS', 'ip_prefix', 'revision_comment_category', 
'revision_comment_property'
]

label_encoders = {
    attribute: LabelEncoder() for attribute in attributes_to_encode
}

print 'encoding attributes'
for attrib in attributes_to_encode:
    print 'encoding %s' % attrib
    le = label_encoders[attrib]
    df[attrib] = le.fit_transform(df[attrib])
    print 'creating pickle'
    with open('./models/'+attrib+'_label_encoder.bin', 'wb') as f:
        cPickle.dump(le, f)
    print 'done with %s' % attrib

print 'creating new df'
new_df = pd.DataFrame()
for attrib in attributes_to_encode:
    new_df[attrib] = df[attrib]
new_df['user_id'] = df['user_id']
new_df['anon'] = df['anon']
new_df['fold'] = df['fold']
new_df['truth'] = df['truth']

print 'creating df feather'
feather.write_dataframe(new_df, './data/final_feathers/encoded_training.feather')