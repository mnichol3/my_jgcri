import os

def rename(dir, target_str, replace_str):
    print("\n...Changing working directory to {}...\n".format(dir))
    orig_wd = os.getcwd()
    os.chdir(dir)
    
    print("...Renaming files...")
    
    for f in os.listdir():
        if (target_str) in f:
            src = f
            dest = src.replace(target_str, replace_str)
            print("...{} --> {}".format(src, dest))
            os.rename(src, dest)
    print("\n...Finished!\n...Changing working directory back to {}".format(orig_wd))
    os.chdir(orig_wd)
    

def main():
    base_dir = r"C:\Users\nich980\code\CEDS\final-emissions\previous-versions"
    target_str = "2019_08_25"
    replace_str = "frozen"
    
    rename(base_dir, target_str, replace_str)
    
    
if __name__ == '__main__':
    main()