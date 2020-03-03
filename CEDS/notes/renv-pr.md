This PR introduces the reproducible enrironment package [renv](https://rstudio.github.io/renv/index.html) as a means of managing CEDS R package dependencies. I think the addition of `renv` will make the installation of CEDS much easier and user-friendly.

### Brief Overview
`renv` is a package that allows users to create isolated, reproducible, project-specific R libraries. It is cross-platform and allows for the installation of older package versions. 

### Structure
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
### User Installation
Upon cloning the repository and navigating to the root CEDS directory, the user can install all the packages needed to run CEDS in one of two ways:
* From the command line: `Rscript -e 'renv::restore()'`
* From an R session: `renv::::restore()`

The `renv::restore()` function retrieves the library package metadata from `renv.lock` and installs the packages to the project's own library located in `CEDS/renv/library/<subdirs>/`. As an example, here is the full `renv` path from my CEDS-dev frozen emissions branch renv library: `CEDS-dev/renv/library/R-3.4/x86_64-pc-linux-gnu/`. The [renv docs](https://rstudio.github.io/renv/reference/restore.html) describe restoring a project in further detail.



**Note**: The following packages were not discovered by renv's dependency scan (may not be required) but were installed anyway due to the package check in `parameters/global_settings.R`:
  * reshape v0.8.6
  * XML v3.98-1.5
    * Installation of XML v3.98-1.5 failed; using v3.99-0.3 instead
