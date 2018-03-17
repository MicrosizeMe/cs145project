import pandas as pd
from glob import glob
import feather
from multiprocessing import Pool

def main():
    meta_pool = Pool(2)
    meta_files = ['./data/wdvc16_meta.csv', './data/validation/wdvc16_2016_03_meta.csv']

    truth_pool = Pool(2)
    truth_files = ['./data/wdvc16_truth.csv', './data/validation/wdvc16_2016_03_truth.csv']

    meta_dfs = meta_pool.map(process_meta_files, meta_files)
    meta_pool.close()

    # df representing all meta csv's
    meta_df = pd.concat(meta_dfs)
    meta_df.reset_index(inplace=True, drop=True)
    meta_df.set_index('REVISION_ID', inplace=True)

    truth_dfs = truth_pool.map(process_truth_files, truth_files)
    truth_pool.close()

    # df representing all truth csv's
    truth_df = pd.concat(truth_dfs)
    truth_df.reset_index(inplace=True, drop=True)
    truth_df.set_index('REVISION_ID', inplace=True)

    csv_files = sorted(glob('./data/converted_wdvc16_*.csv') + glob('./data/validation/converted_wdvc16_*.csv'))
    for csv_file in csv_files:
        create_feather(csv_file, meta_df, truth_df)

def process_meta_files(meta_file):
    print('processing %s' % meta_file)
    df = pd.read_csv(meta_file)
    
    # create frame of sum of null entries in df rows
    null_entry_counts = df.isnull().sum(axis=1)

    # drop all entries with 7 null entries (not useful row)
    df = df[null_entry_counts != 7].reset_index(drop=True)

    # cast revision ids to uint32
    df.REVISION_ID = df.REVISION_ID.astype('uint32')

    # replace na's with empty str
    df.fillna('', inplace=True)

    # remove session ID column - not using this
    del df['REVISION_SESSION_ID']

    # index by revision_id
    df.set_index('REVISION_ID', inplace=True)

    # turn each row into a string representation
    stringified = df.apply(row_to_string, axis='columns')

    final_df = stringified.reset_index()
    final_df.columns = ['REVISION_ID', 'meta_string']
    return final_df

# take a row of meta-df and return a string representation of it
def row_to_string(row):
    row_dict = row.to_dict()
    # format: 'col=value col=value col=value ...'
    return ' '.join('%s=%s' % (key, value.replace(' ', '_')) for (key, value) in row_dict.items() if value)

def process_truth_files(truth_file):
    print('processing %s' % truth_file)
    df = pd.read_csv(truth_file)
    
    # not useful for us
    del df['UNDO_RESTORE_REVERTED']

    # convert to 0s and 1s
    df.ROLLBACK_REVERTED = (df.ROLLBACK_REVERTED == 'T').astype('uint8')

    # cast ID's to uint32
    df.REVISION_ID = df.REVISION_ID.astype('uint32')
    return df

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

    new_file_path = './data/merged_feathers/' + csv_file[len('./data/converted_'):-4] + '.feather'
    feather.write_dataframe(csv_df, new_file_path)
    print('%s done' % new_file_path)

if __name__ == '__main__':
    main()