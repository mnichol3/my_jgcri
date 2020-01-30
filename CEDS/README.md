# diff_csv.py

This python script serves as a way to quickly check if two `.csv` files are identical. It will not, however, identify the differences between the two files.

### Usage
Though the only way to execute `diff_csv.py` is from the command line, there are a few different ways to specify which files you would live to compare:

* **Passing file paths as arguments**
  The most direct way to use the script is to pass the absolute paths of the two `.csv` files you wish to compare as command line arguments via the `-f` flag:
  ```
  python diff_csv.py -f /path/to/first.csv /path/to/second.csv
  ```
  
  If the two files are in the same directory (which isn't your current working directory), you can pass the path of the directory that holds the two files as the `common directory` argument:
  ```
  python diff_csv.py -d /path/to/parent/dir -f first.csv second.csv
  ```
  
* **Passing files via yaml file**
  Another way to specify which `.csv` files you wish to diff is by creating a `.yml` file and passing its path as an argument, along with the `-i` flag:
  ```
  python diff_csv.py -i input/uncertainty/diff-fullEmissions-BC-Pshift.yml
  ```
  
  The yaml input file is structured as such:
  ```
  # diff-FullEmissions-BC-Pshift.yaml

  - file: fullEmissions-BC-Pshift-ACTUAL.csv
    path: C:\Users\nich980\data\CEDS\CEDS-uncertainty\output
    needs_clean: !!bool false
  - file: fullEmissions-BC-Pshift.csv
    path: C:\Users\nich980\code\CEDS-dev\input
    needs_clean: !!bool true
  ```
  
  
  
### Output
If the two `.csv` files are identical, the following messge will be displayed:
```
--- csv_1 & csv_2 are identical ---
```

However, if the two files are **not** identical, their shapes will be printed and a `ValueError` will be raised:
```
csv_1 shape: (11124, 59)
csv_2 shape: (4449, 59)

Traceback (most recent call last):
  File "diff_csv.py", line 157, in <module>
    raise ValueError('csv_1 & csv_2 are not identical')
ValueError: csv_1 & csv_2 are not identical
```
