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
## User Installation
Upon cloning the repository and navigating to the root CEDS directory, users can activate their `renv` library and install CEDS R dependencies. 

### Initialize a CEDS-specific Library
Although some `renv` files ship with the CEDS repository, it is still necesarry initialize the project. This can be accomplished with the [`renv::init()`](https://rstudio.github.io/renv/reference/init.html) function. 

To initialize a `renv` library for CEDS, open an R session in your CEDS root directory. Then:
1. Install the `renv` package: `install.packages("renv")`
2. Initialize the project library: `renv::init(bare=TRUE)`

By default, the `init` function will scan the project's source code for R dependency packages to download, but this can take a while to run and won't necessarily install the package versions CEDS needs to run. Using the `bare = TRUE` argument will tell `renv` to install an empty R library for CEDS that we can populate with packages defined in the lockfile.

`renv::init()` calls [`renv::activate()`](https://rstudio.github.io/renv/reference/activate.html), which writes the infrastructure needed to ensure that R will load the CEDS R library on launch, among other things.

### Install R Packages in CEDS-specific Library
After initializing the library, users can install CEDS R dependencies defined in the lockfile via the [`renv::restore()`](https://rstudio.github.io/renv/reference/restore.html) function. 

From an R session in your CEDS project root directory, run the following command: `renv::::restore()`.

This command will retrieve the library package metadata from `renv.lock` and install the packages to the project's private library located in `CEDS/renv/library/.../...`. 


## Cache
A defining feature of `renv` is the use of a global package cache, which is shared across all projects using `renv` on a machine. The cache saves time and disk space by allowing various projects to access the same packages, rather than installing the same packages and versions into separate projects. 

When using the global package cache, the project library is formed as a directory of symlinks rather than a directory of installed R packages. Each `renv` project is isolated from other projects on a machine, but they can still re-use the same installed packages as needed. 

The global package cache is enabled by default, however it can be disabled by setting `renv::settings$use.cache(FALSE)`. This will ensure that packages are then installed to project libraries directly, without attempting to link to the `renv` cache. 
