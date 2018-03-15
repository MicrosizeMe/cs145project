from glob import glob
import pandas as pd
import feather
import numpy as np

def main():
    # get validation & 2015+2016 training data march15 onwards
    feather_file_paths = sorted(glob('./data/merged_feathers/*2015*.feather')
        + glob('./data/merged_feathers/*2016*.feather')
        + glob('./data/merged_feathers/validation/*.feather'))
    feather_file_paths.remove('./data/merged_feathers/wdvc16_2015_01.feather')

    # collect all the dataframes
    all_dfs = []
    for feather_file_path in feather_file_paths:
        df = feather.read_dataframe(feather_file_path)
        print 'read %s' % feather_file_path
        all_dfs.append(df)

    # join the dataframes into one
    total_df = pd.concat(all_dfs)
    total_df.reset_index(drop=True, inplace=True)

    # free this memory
    del all_dfs, df

    print 'joined dfs'

    # mark rows with their split category

    # train=0, validation=1, test=2
    total_df['fold'] = 0
    total_df['fold'] = total_df['fold'].astype('uint8')

    # validate on january16 - march16 data
    total_df.loc[(total_df.revision_timestamp > pd.to_datetime('2016-01-01')) & 
        (total_df.revision_timestamp <= pd.to_datetime('2016-03-01')), 'fold'] = 1

    # test on march16 onwards
    total_df.loc[total_df.revision_timestamp > pd.to_datetime('2016-03-01'), 'fold'] = 2

    print 'split done'

    # put user features into df

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
    total_df['revision_comment_category'] = total_df.revision_comment.str.extract('/\*(.+):[0-9]', expand=False).fillna('')
    total_df['revision_comment_property'] = total_df.revision_comment.str.extract('\[\[Property:(.+)\]\]:', expand=False).fillna('')

    print 'comment features done'

    # save final feather
    del total_df['page_id']
    del total_df['revision_timestamp']
    del total_df['revision_comment']
    del total_df['username']

    feather.write_dataframe(total_df, './data/final_feathers/total_df.feather')
    print 'all done'

def mine_sub_ips(ip_address):
    if ip_address is None:
        return ''
    elif '.' in ip_address:
        split_ip = ip_address.split('.')
        return split_ip[0] + '.' + split_ip[1]
    elif ':' in ip_address:
        split_ip = ip_address.split(':')
        return split_ip[0] + ':' + split_ip[1]

if __name__ == '__main__':
    main()