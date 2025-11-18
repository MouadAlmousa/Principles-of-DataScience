import pandas as pd
import numpy as np

pd.options.display.max_columns = None
pd.options.display.expand_frame_repr =False

# Read in the raw data using pandas

raw_yield_data = pd.read_csv('../data_raw/raw_yield_data.csv')

df=raw_yield_data.copy()

num_cols = df.select_dtypes(include=np.number) # Get all numeric columns
df = df.drop(df[(num_cols == 0).any(axis=1)].index) # Drop rows where value=0 (Missing values) in a numeric column
df["overall_avg"] = num_cols.mean(axis=1).round(2) # Find Overall Avgaverage and add it to the dataframe

# Write clean dataframe to disk
df.to_csv('../data_clean/clean_yield_data.csv',index=False)



