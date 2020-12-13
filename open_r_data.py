# script to open R files in python, and save the resultant pandas dataframe as a pickle file.
import pyreadr
import pandas as pd

# read file and save as pickled data.
# read_R_file = pyreadr.read_r('Data/1365 Cattle Activity Isis Downs data merge CLEAN data v0.19 14-09-2020.Rdata')
# print(read_R_file.keys)
# cattle_df = read_R_file[None]
# cattle_df.to_pickle("Data/cattle_pickle.pkl")

# import pickled data
cattle_df = pd.read_pickle("Data/cattle_pickle.pkl")
print(cattle_df)

