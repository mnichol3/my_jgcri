# Installing CEDS Dependencies with renv
[renv](https://rstudio.github.io/renv/articles/renv.html) is a project-local R dependency management package that allows users to isolate their project’s R dependencies. Since CEDS depends on package versions that are much older than their current versions, `renv` enables the installation of CEDS dependency packages without downgrading the versions of those packages in the user's global R library.


## Prerequisites
Some CEDS dependencies have dependencies of their own, and not all of these dependencies are R packages. For example, the R package `readr` depends on the R package `curl`, which depends on the `libcurl` software library. During testing, two software libraries were identified as needing to be installed before beginning the renv installation process: `libcurl` and `openssl`.

The prerequisite software libraries can be downloaded via the system-specific instructions below.
* Linux
  * deb (Debian, Ubuntu, etc):
    ```
    sudo apt-get install libcurl4-openssl-dev
    sudo apt-get install libssl-dev
    ```
  * rmp (Fedora, CentOS, RHEL):
    ```
    yum install libcurl-devel
    yum install openssl-devel
    ```
* Windows
  * TODO
* Mac
  * TODO
  
## Activating renv and downloading packages
After installing the prerequisite libraries detailed above, activating the revn environment will begin the download and installation of CEDS dependency packages. 

There are two ways to activate the CEDS renv environment:
* Via RStudio: `renv::restore()`
* Via command line: `Rscript -e "renv::restore()"`

Note: renv *should* install itself if not already installed, but if this fails, renv can be installed manually with `install.packages("renv")`
