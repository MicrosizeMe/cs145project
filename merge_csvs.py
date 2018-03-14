import pandas as pd
from glob import glob
import feather
from multiprocessing import Pool

# used for creating feathers
global_meta_df = None
global_truth_df = None

def main():
    global global_meta_df
    global global_truth_df
    meta_pool = Pool(2)
    meta_files = ['./data/wdvc16_meta.csv', './data/validation/wdvc16_2016_03_meta.csv']

    truth_pool = Pool(2)
    truth_files = ['./data/wdvc16_truth.csv', './data/validation/wdvc16_2016_03_truth.csv']

    meta_dfs = meta_pool.map(process_meta_files, meta_files)
    meta_pool.close()

    # df representing all meta csv's
    meta_df = pd.concat(meta_dfs)
    meta_df.reset_index(inplace=1, drop=1)
    meta_df.set_index('REVISION_ID', inplace=1)

    # set global meta
    global_meta_df = meta_df

    truth_dfs = truth_pool.map(process_truth_files, truth_files)
    truth_pool.close()

    # df representing all truth csv's
    truth_df = pd.concat(truth_dfs)
    truth_df.reset_index(inplace=1, drop=1)
    truth_df.set_index('REVISION_ID', inplace=1)

    # set global meta
    global_truth_df = truth_df

    feather_pool = Pool(6)
    csv_files = sorted(glob('./data/converted_wdvc16_*.csv') + glob('./data/validation/converted_wdvc16_*.csv'))
    feather_pool.map(create_feather, csv_files)

def process_meta_files(meta_file):
    df = pd.read_csv(meta_file)
    
    # create frame of sum of null entries in df rows
    null_entry_counts = df.isnull().sum(axis=1)

    # drop all entries with 7 null entries (not useful row)
    df = df[null_entry_counts != 7]
    df.reset_index(drop=True)

    # cast revision ids to uint32
    df.REVISION_ID = df.REVISION_ID.astype('uint32')

    # remove session ID column - not using this
    del df['REVISION_SESSION_ID']

    # replace na's with empty str
    df.fillna('', inplace=True)

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
    df = pd.read_csv(truth_file)
    
    # not useful for us
    del df['UNDO_RESTORE_REVERTED']

    # convert to 0s and 1s
    df.ROLLBACK_REVERTED = (df.ROLLBACK_REVERTED == 'T').astype('uint8')

    # cast ID's to uint32
    df.REVISION_ID = df.REVISION_ID.astype('uint32')
    return df

def create_feather(csv_file):
    csv_df = pd.read_csv(csv_file)

    # these are all 0
    del csv_df['page_ns']

    csv_df.username.fillna('', inplace=1)
    csv_df.revision_comment.fillna('', inplace=1)
    csv_df.user_id.fillna(-1, inplace=1)
    csv_df.ip_address.fillna('', inplace=1)
    csv_df.revision_timestamp = pd.to_datetime(df.revision_timestamp)
    csv_df.user_id = df.user_id.astype('int32')

    # add meta strings
    meta_string_column = global_meta_df.meta_string.reindex(csv_df.revision_id)
    meta_string_column.fillna('')
    meta_string_column.reset_index(drop=1)
    csv_df['meta'] = meta_string_column
    
    # add labels
    truth_column = global_truth_df.ROLLBACK_REVERTED.reindex(csv_df.revision_id)
    truth_column.reset_index(drop=1)
    csv_df['truth'] = truth_column

    new_file_path = './data/merged_feathers/' + csv_file[len('./data/converted_'):-4] + '.feather'
    feather.write_dataframe(csv_df, new_file_path)

if __name__ == '__main__':
    main()