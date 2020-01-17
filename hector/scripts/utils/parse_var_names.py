import pandas as pd
import re

from os.path import join

re_desc = re.compile(r"(?:\//' @describeIn\s(\w+)\s([^\n]+)\n)")
re_func_name = re.compile(r"\n*\w+\s(\w+)\(\)\s\{\n*")
re_func_val = re.compile(r"\n*return\s(\w+);\n*")

re_list = [re_desc, re_func_name, re_func_val]

dir_path = r'C:\Users\nich980\code\hector\src'
f_name = 'rcpp_constants.cpp'

f_out = 'rcpp_consant_names.csv'

abs_path = join(dir_path, f_name)

# Dictionary to hold the variable/constant definitions
var_defs = {}

# Open & read the file line-by-line
with open(abs_path, 'r') as fh:
    block_component = ''
    block_desc = ''
    func_name = ''
    func_val = ''
    
    # for line_idx, line in enumerate(fh):
    file_str = fh.read()
    block_arr = file_str.split("\n\n")
    for block in block_arr:
    
        match = re.search(re_desc, block)
        if (match):
            block_component = match.group(1)
            block_desc = match.group(2)
                
        match = re.search(re_func_name, block)
        if (match):
            func_name = match.group(1)

        match = re.search(re_func_val, block)
        if (match):
            func_val = match.group(1)
        
        if (func_val != ''):
            var_defs[func_val] = [func_name, block_component, block_desc]
            
            
            

# Create a Pandas DataFrame from the dictionary we just created
df = pd.DataFrame.from_dict(var_defs, orient='index')

# The DataFrame is initialized with the 'Constant' column as the index,
# so here we copy the index column to a new column named 'Constant'
df['Constant'] = df.index

# Specify the desired order of the DataFrame colummns
cols_rearr = ['Constant', 0, 1, 2]

# Rearrange the columns
df = df[cols_rearr]

# Rename the columns as the DataFrame is initialized with integer column names
df = df.rename(columns={0: "Function", 1: "Type", 2: "Desc"})

# change the DataFrame index column from the function constant values to the
# default integer index values 
df = df.reset_index(drop=True)

print(df)

print('\nWriting DataFrame to {}...'.format(f_out))
df.to_csv(f_out, sep=',', header=True, index=False)
        