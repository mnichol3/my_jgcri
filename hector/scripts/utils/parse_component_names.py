import pandas as pd
from os.path import join

component_defs = {}

f_path = r"C:\Users\nich980\code\hector\inst\include"
f_name = "component_names.hpp"

f_abs = join(f_path, f_name)

with open(f_abs, 'r') as fh:
    for line_idx, line in enumerate(fh):
        line_strs = line.split(' ')
        
        if (line_strs[0] == '#define' and len(line_strs) > 2):
            curr_key = line_strs[1]
            curr_vals = line_strs[2:]
            
            # Strip any double quotation marks & newlines from the values
            curr_vals = [x.replace('"', '').replace('\n', '') for x in curr_vals if x != '']
            
            for idx, val in enumerate(curr_vals):
                if (val in component_defs.keys() and len(component_defs[val]) == 1):
                    curr_vals[idx] = component_defs[val][0]
                    
            component_defs[curr_key] = curr_vals

for key, val in component_defs.items():
    # print(key, val)
    val_str = ''.join(component_defs[key])
    
    component_defs[key] = val_str
    
    print('{} --> {}'.format(key, val_str))

# Read the dictionary of macro defs into a Pandas DataFrame & write it to csv
col_names = ['Macro', 'Definition']
df = pd.from_dict(component_defs, orient='columns', dtype=str, columns=col_names)

out_path = r"C:\Users\nich980\Documents\Docs\Hector\coding-notes"
f_name_out = "component_names.csv"

out_abs = join(out_path, f_name_out)

df.to_csv(out_abs, sep = ',', header=True, index=False)

