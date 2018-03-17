import merge_csvs as mc
from create_final_features import mine_sub_ips
import pandas as pd
import feather
import bisect
from sklearn.preprocessing import LabelEncoder
import numpy as np
import cPickle

def create_feather(csv_file, meta_df, truth_df):
    print('creating feather for %s' % csv_file)
    csv_df = pd.read_csv(csv_file)

    # these are all uniform
    del csv_df['page_ns']
    del csv_df['revision_model']
    del csv_df['revision_format']

    csv_df.username.fillna('', inplace=True)
    csv_df.revision_comment.fillna('', inplace=True)
    csv_df.user_id.fillna(-1, inplace=True)
    csv_df.ip_address.fillna('', inplace=True)
    csv_df.revision_timestamp = pd.to_datetime(csv_df.revision_timestamp)
    csv_df.user_id = csv_df.user_id.astype('int32')

    # add meta strings
    meta_string_column = meta_df.meta_string.loc[csv_df.revision_id].fillna('')
    csv_df['meta'] = meta_string_column.reset_index(drop=True)
    
    # add labels
    truth_column = truth_df.ROLLBACK_REVERTED.loc[csv_df.revision_id]
    csv_df['truth'] = truth_column.reset_index(drop=True)

    new_file_path = './data/merged_feathers/wdvc16_2016_05.feather'
    feather.write_dataframe(csv_df, new_file_path)
    print('%s done' % new_file_path)

# xml -> csv done
# merge csv's

print 'merging csvs'
meta_file = './data/test/wdvc16_2016_05_meta.csv'
truth_file = './data/test/wdvc16_2016_05_truth.csv'

meta_df = mc.process_meta_files(meta_file)
meta_df.reset_index(inplace=True, drop=True)
meta_df.set_index('REVISION_ID', inplace=True)

truth_df = mc.process_truth_files(truth_file)
truth_df.reset_index(inplace=True, drop=True)
truth_df.set_index('REVISION_ID', inplace=True)

csv_file = './data/test/converted_wdvc16_2016_05.csv'
create_feather(csv_file, meta_df, truth_df)

del meta_file
del truth_file
del meta_df
del truth_df
del csv_file

# create final features
print 'creating final features'
total_df = feather.read_dataframe('./data/merged_feathers/wdvc16_2016_05.feather')
total_df.reset_index(drop=True, inplace=True)

# ip address prefixes
total_df['ip_prefix'] = total_df.ip_address.apply(mine_sub_ips).fillna('')

# meta data
total_df['REVISION_SESSION_ID'] = total_df.meta.str.extract('REVISION_SESSION_ID=([^\s]+)', expand=False).fillna('')
total_df['USER_COUNTRY_CODE'] = total_df.meta.str.extract('USER_COUNTRY_CODE=([^\s]+)', expand=False).fillna('')
total_df['USER_CONTINENT_CODE'] = total_df.meta.str.extract('USER_CONTINENT_CODE=([^\s]+)', expand=False).fillna('')
total_df['USER_TIME_ZONE'] = total_df.meta.str.extract('USER_TIME_ZONE=([^\s]+)', expand=False).fillna('')
total_df['USER_REGION_CODE'] = total_df.meta.str.extract('USER_REGION_CODE=([^\s]+)', expand=False).fillna('')
total_df['USER_CITY_NAME'] = total_df.meta.str.extract('USER_CITY_NAME=([^\s]+)', expand=False).fillna('')
total_df['USER_COUNTY_NAME'] = total_df.meta.str.extract('USER_COUNTY_NAME=([^\s]+)', expand=False).fillna('')
total_df['REVISION_TAGS'] = total_df.meta.str.extract('REVISION_TAGS=([^\s]+)', expand=False).fillna('')
del total_df['meta']

print 'user features done'

# put comment features into df
total_df['revision_comment_category'] = total_df.revision_comment.str.extract('/\*(.+?):[0-9]', expand=False).fillna('')
total_df['revision_comment_property'] = total_df.revision_comment.str.extract('\[\[Property:(.+?)\]\]:', expand=False).fillna('')

print 'comment features done'

# save feather
del total_df['page_id']
del total_df['revision_timestamp']
del total_df['revision_comment']
del total_df['username']

feather.write_dataframe(total_df, './data/final_feathers/test_df.feather')


# create encoded feather
df = feather.read_dataframe('./data/final_feathers/test_df.feather')
print 'adding anon feature'
df['anon'] = np.where(df['user_id']==-1, 1, -1).astype('int8')

attributes_to_encode = [
'USER_COUNTY_NAME','USER_COUNTRY_CODE','USER_CONTINENT_CODE',
'USER_TIME_ZONE','USER_REGION_CODE','USER_CITY_NAME',
'REVISION_TAGS', 'ip_prefix', 'revision_comment_category', 
'revision_comment_property'
]

label_encoders = {}
for attrib in attributes_to_encode:
    print 'loading %s encoder' % attrib
    with open('./models/'+attrib+'_label_encoder.bin', 'rb') as f:
        label_encoders[attrib] = cPickle.load(f)

for attrib in attributes_to_encode:
    le = label_encoders[attrib]
    classes = le.classes_.tolist()
    bisect.insort_left(classes, 'other')
    le.classes_ = classes

print 'mapping'
for attrib in attributes_to_encode:
    classes = label_encoders[attrib].classes_
    df[attrib] = df[attrib].map(lambda s: 'other' if s not in classes else s)

print 'encoding attributes'
for attrib in attributes_to_encode:
    print 'encoding %s' % attrib
    le = label_encoders[attrib]
    df[attrib] = le.transform(df[attrib])
    print 'done with %s' % attrib

print 'creating new df'
new_df = pd.DataFrame()
for attrib in attributes_to_encode:
    new_df[attrib] = df[attrib]
new_df['user_id'] = df['user_id']
new_df['anon'] = df['anon']
new_df['truth'] = df['truth']

print 'creating df feather'
feather.write_dataframe(new_df, './data/final_feathers/encoded_test.feather')
