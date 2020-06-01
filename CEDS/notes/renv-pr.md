This PR introduces the reproducible enrironment package [renv](https://rstudio.github.io/renv/index.html) as a means of managing CEDS R package dependencies. I think the addition of `renv` will make the installation of CEDS much easier and user-friendly.

## Brief Overview
`renv` is a package that allows users to create isolated, reproducible, project-specific R libraries. It is cross-platform and allows for the installation of older package versions. 

## Structure
`renv` is extremely lightweight and only adds four files the the repo with a total size of 32 KB. It also automatically adds its installed package directories to the project's `.gitignore` file, so we don't have to worry about accidentally committing hundreds of MB of R packages to the repo. An example of the `renv` file structure as it would appear in the CEDS repo is below:
```
CEDS/
 |- renv/
 |   |- .gitignore
 |   |- activate.R
 |   |- settings.dcf
 |
 |- renv.lock
```
Once initialized, a `library/` sub-directory would be added to `renv/`, which is where R packages would be installed.

## Lockfiles
`renv` utilizes [lockfiles](https://rstudio.github.io/renv/reference/lockfiles.html) to record the state of a project's library at some point in time. They contain package metadata, such as package names, versions, and sources, as well as the R version that was used to initialize the project. While normally generated with the [`snapshot()`](https://rstudio.github.io/renv/reference/snapshot.html)/[`restore()`](https://rstudio.github.io/renv/reference/restore.html) functions, lockfiles are written as `.json` which allows them to be edited by hand. The CEDS lockfile, `renv.lock`, is located in the root CEDS project directory. 

## User Installation
Upon cloning the repository and navigating to the root CEDS directory, users can activate their `renv` library and install CEDS R dependencies. 

### 1. Initialize a CEDS-specific Library
Although some `renv` files ship with the CEDS repository, it is still necesarry initialize the project. This can be accomplished with the [`renv::init()`](https://rstudio.github.io/renv/reference/init.html) function. 

To initialize a `renv` library for CEDS, open an R session in your CEDS root directory. Then:
1. Install the `renv` package: `install.packages("renv")`
2. Initialize the project library: `renv::init(bare=TRUE)`

By default, the `init` function will scan the project's source code for R dependency packages to download, but this can take a while to run and won't necessarily install the package versions CEDS needs to run. Using the `bare = TRUE` argument will tell `renv` to install an empty R library for CEDS that we can populate with packages defined in the lockfile.

`renv::init()` calls [`renv::activate()`](https://rstudio.github.io/renv/reference/activate.html), which writes the infrastructure needed to ensure that R will load the CEDS R library on launch, among other things.

### 2. Install R Packages in CEDS-specific Library
After initializing the library, users can install CEDS R dependencies defined in the lockfile via the [`renv::restore()`](https://rstudio.github.io/renv/reference/restore.html) function. 

From an R session in your CEDS project root directory, run the following command: `renv::restore()`.

This command will retrieve the library package metadata from `renv.lock` and install the packages to the project's private library located in `CEDS/renv/library/.../...`. 


## Global Package Cache
A defining feature of `renv` is the use of a [global package cache](https://rstudio.github.io/renv/articles/renv.html#cache), which is shared across all projects using `renv` on a machine. The cache saves time and disk space by allowing various projects to access the same packages, rather than installing the same packages and versions into separate projects. 

When using the global package cache, the project library is formed as a directory of symlinks rather than a directory of installed R packages. Each `renv` project is isolated from other projects on a machine, but they can still re-use the same installed packages as needed. 

The global package cache is enabled by default, however it can be disabled by setting `renv::settings$use.cache(FALSE)`. This will ensure that packages are then installed to project libraries directly, without attempting to link to the `renv` cache. 

## Troubleshooting
### R package `farver` fails to compile on pic HPC cluster
The installation of the `farcer` package may fail when attempting to compile, resulting in an error message that looks something like this:
  ```
  * installing *source* package 'farver' ...
  ** package 'farver' successfully unpacked and MD5 sums checked
  ** libs
  g++ -std=gnu++0x -I"/share/apps/R/3.5.1/lib64/R/include" -DNDEBUG   -I/usr/local/include   -fpic  -I/share/apps/R/3.5.1/include -c     ColorSpace.cpp -o ColorSpace.o
  In file included from ColorSpace.cpp:1:
  ColorSpace.h:19: error: ISO C++ forbids initialization of member 'valid'
  ColorSpace.h:19: error: making 'valid' static
  ColorSpace.h:19: error: ISO C++ forbids in-class initialization of non-const static member 'valid'
  make: *** [ColorSpace.o] Error 1
  ERROR: compilation failed for package 'farver'
  ```

This is due to the package's C++ backend using features that the default `gcc` complier on `pic` is unaware of due to it being an older version (`gcc 4.4.7` is still default as of 12 May 2020). 

#### Solution
Load a newer version (6.1.0 works as of 13 May 2020) of the `gcc` compiler via `module load gcc/6.1.0`.
  
  ---
  
### R package `ncdf4` fails to install on pic HPC cluster
CEDS only uses the `ncdf4` package within the gridding module to produce gridded emissions files. The package is not required to produce CEDS emissions CSV files.
  
`ncdf4` depends on an `nc-config` file that ships with the [Unidata NetCDF library](https://www.unidata.ucar.edu/software/netcdf/). The Unidata NetCDF library is a [documented system requirement](https://cran.r-project.org/web/packages/ncdf4/index.html) for the R ncdf4 package. The NetCDF C library is installed on pic, but is not loaded as a module at the beginning of a remote session. Attempting to install the R `ncdf4` package without the `netcdf` module loaded into your session can result in the following error:
  ```
  Installing ncdf4 [1.16] ...
          FAILED
  Error installing package 'ncdf4':
  =================================
  * installing *source* package 'ncdf4' ...
  ** package 'ncdf4' successfully unpacked and MD5 sums checked
  configure.ac: starting
  checking for nc-config... no
  -----------------------------------------------------------------------------------
  Error, nc-config not found or not executable.  This is a script that comes with the
  netcdf library, version 4.1-beta2 or later, and must be present for configuration
  to succeed.
  ```
  
#### Solution
Load the `netcdf` library into your session via the command `module load netcdf`.

---

### Unable to locate ICU4C library
[ICU](http://userguide.icu-project.org/intro) is a cross-platform Unicode based globalization library. It includes support for locale-sensitive string comparison, date/time/number/currency/message formatting, text boundary detection, character set conversion and so on. 
When attempting the install some R packages, such as `stringi v1.2.2`, the `ICU4C` library is unable to be located and the installation fails:
```
checking for pkg-config... /usr/bin/pkg-config
checking with pkg-config for the system ICU4C... no
*** pkg-config did not detect ICU4C-devel libraries installed
*** Trying with "standard" fallback flags
checking whether we may build an ICU4C-based project... no
*** The available ICU4C cannot be used
checking whether we may compile src/icu61/common/putil.cpp... no
checking whether we may compile src/icu61/common/putil.cpp with -D_XPG6... no
*** The ICU4C bundle could not be build. Upgrade your compiler flags.
ERROR: configuration failed for package 'stringi'
* removing '/pic/projects/GCAM/mnichol/ceds/CEDS-dev/renv/staging/1/stringi'
Error: install of package 'stringi' failed
```
#### Solution 1
Load a newer compiler into your remote session: `module load gcc/7.3.0` (`gcc/7.3.0` works as of 15 May 2020).

#### Solution 2
Use the `install.packages` function to modify the compiler flags used in the installation process:
```R
install.packages(c("stringi"),configure.args=c("--disable-cxx11"), lib=lib)
```
Use the `lib` argument to install the package into your project's `renv` library (can be found using `.libPaths()`). 

**NOTE** This solution is fine for only installing `stringi`, however it may not completely resolve the problem when `stringi` is being installed as a dependency for another R package through `renv`.

---

### R/renv unable to load shared object
`renv` has the ability to link packages from a user's global R library to their project-specific `renv` library, saving the time and space that re-downloading the same package and version a second time. However, once this cache link is established, removing the package from the global R library will break the link, causing errors in the `renv` library.

his error message below resulted from the cache link between the CEDS `renv` library and global R library being broken for the `stringi` package when attempting to load the `stringr` package, which depends on `stringi`:
```
Error in dyn.load(file, DLLpath = DLLpath, ...) :
  unable to load shared object '/qfs/people/nich980/.local/share/renv/cache/v5/R-3.3/x86_64-pc-linux-gnu/stringi/1.2.2/e99d8d656980d2dd416a962ae55aec90/stringi/libs/stringi.so':
  /usr/lib64/libstdc++.so.6: version `CXXABI_1.3.8' not found (required by /qfs/people/nich980/.local/share/renv/cache/v5/R-3.3/x86_64-pc-linux-gnu/stringi/1.2.2/e99d8d656980d2dd416a962ae55aec90/stringi/libs/stringi.so)
Couldn't load 'stringr'. Please Install.
```
#### Solution
Manually install the package dependency in question into the project `renv` library, using the [`library`](https://rstudio.github.io/renv/reference/install.html#arguments) and [`rebuild`](https://rstudio.github.io/renv/reference/install.html#arguments) arguments:
```R
> .libPaths()
[1] "/pic/projects/GCAM/mnichol/ceds/CEDS-dev/renv/library/R-3.3/x86_64-pc-linux-gnu"
[2] "/tmp/RtmpofmJy0/renv-system-library"
> lib <- .libPaths()[1]  # CEDS renv library
> renv::install("stringi@1.2.2", library=lib, rebuild=TRUE)
```
This forces `renv` to install the package in the local library, rather than attempting to create another cache link.
