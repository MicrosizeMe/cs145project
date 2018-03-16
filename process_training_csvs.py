import merge_csvs as mc
import create_final_features as cff
import pandas as pd
import feather
from multiprocessing import Pool

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