import feather
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from collections import defaultdict
from tqdm import tqdm

tqdm.pandas(desc="my bar!")

df = feather.read_dataframe('./data/final_feathers/total_df.feather')
d = defaultdict(LabelEncoder)
fit = df.progress_apply(lambda x: d[x.name].fit_transform(x))
df.progress_apply(lambda x: d[x.name].transform(x))
feather.write_dataframe(df, './data/final_feathers/label_encoded_df.feather')