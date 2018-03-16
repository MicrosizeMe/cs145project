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
    df[attrib] = label_encoders[attrib].fit_transform(df[attrib])
    print 'done with %s' % attrib

print 'creating label_encoders pickle'
for attrib in attributes_to_encode:
    with open('./models/'+attrib+'label_encoder_params.bin', 'wb') as f:
        cPickle.dump(label_encoders[attrib].get_params(), f)

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