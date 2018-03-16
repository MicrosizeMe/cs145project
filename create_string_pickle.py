import feather
import pandas as pd

print 'reading feather'
df = feather.read_dataframe('./data/final_feathers/total_df.feather')

print 'creating series'
str_column = 'user_id=' + df.user_id.astype('str') + ' ' \
+ 'ip_address=' + df.ip_address + ' ' \
+ 'ip_prefix=' + df.ip_prefix + ' ' \
+ 'country=' + df.USER_COUNTRY_CODE + ' ' \
+ 'continent=' + df.USER_CONTINENT_CODE + ' ' \
+ 'timezone=' + df.USER_TIME_ZONE + ' ' \
+ 'region=' + df.USER_REGION_CODE + ' ' \
+ 'city=' + df.USER_CITY_NAME + ' ' \
+ 'county=' + df.USER_COUNTY_NAME + ' ' \
+ 'tags=' + df.REVISION_TAGS + ' ' \
+ 'cat=' + df.revision_comment_category + ' ' \
+ 'prop=' + df.revision_comment_property

'saving pickle'
str_column.to_pickle('./data/final_feathers/string_pickle.bin')