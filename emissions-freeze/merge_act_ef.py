import pandas as pd

fname_ef = r"C:\Users\nich980\data\e-freeze\CMIP6-emissions\intermediate-output\H.SO2_total_EFs_extended.csv"
fname_act = r"C:\Users\nich980\data\e-freeze\CMIP6-emissions\intermediate-output\H.SO2_total_activity_extended.csv"


df_act = pd.read_csv(fname_act, sep=',', header=0)
df_ef = pd.read_csv(fname_ef, sep=',', header=0)

# Compare the first three columns of the two dataframes, i.e. the columns
# 'iso', 'sector', & 'fuel'
merged = pd.merge(df_act.iloc[:, : 3], df_ef.iloc[:, : 3], on=['iso', 'sector', 'fuel'], how='inner')

shape_act = df_act.shape
shape_ef = df_ef.shape
shape_merged = merged.shape

equal_lens = (shape_act[0] == shape_ef[0] == shape_merged[0])

