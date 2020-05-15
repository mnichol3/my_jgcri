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

---

**Note**: The following packages were not discovered by renv's dependency scan (may not be required) but were installed anyway due to the package check in `parameters/global_settings.R`:
  * reshape v0.8.6
  * XML v3.98-1.5
    * Installation of XML v3.98-1.5 failed; using v3.99-0.3 instead
