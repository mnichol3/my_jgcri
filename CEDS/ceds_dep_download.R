### This script attempts to download the specific versions of R packages that
### CEDS depends on
### 
### Author: Matt Nicholson
### 23 Dec 2019


### Function to handle the actual package downloads
###
### @param pckg         Name of package to download
### @param vers_nums    List of version number to try
### @param repo_url     CRAN repo URL to download the package files from
### @return outcome     1 if package downloads successfully, else 0
downloadPackage <- function( pckg, vers_num ) {
    repo_url <- "https://cran.us.r-project.org"
    outcome <- 0

    dl_error <- tryCatch( devtools::install_version( pckg, version=vers_num,
                                                     repo=repo_url, dependencies=c("Depends", "Imports"),
                                                     upgrade="never" ),
                          error = function( e ) e   # Leave as-is or else inherits() call fails
    )

    # Check if an error was caught
    if ( inherits( dl_error, "error" ) ) {
        print( glue( "--- Error downloading {pckg} v{vers_num} ---" ) )
    } else {
        outcome <- 1
    }

    return( outcome )
}




### Try to load devtools & glue packages, install them if loading raises an error
### (e.i., they aren't already installed)
if ( !require("usethis", character.only=T ) ) {
    print( "Installing package usethis..." )
    install.packages( "usethis", dependencies=TRUE )
}

if ( !require( "glue", character.only=T ) ) {
    print( "Installing package glue..." )
    install.packages( "glue", dependencies=TRUE )
}

if ( !require( "devtools", character.only=T ) ) {
    print( "Installing packages devtools & magrittr..." )
    install.packages( c( "devtools", "magrittr" ), dependencies=TRUE )
    # devtools will fail to load if magrittr is not also installed here
}

library( usethis )
library( glue )     # <-- Might not be necessary due to above require() call
library( devtools )

lib_matrix <- installed.packages()

repo_url <- "https://cran.us.r-project.org"

failed_pckgs <- vector()

### Packages & their acceptable versions. Optimal version numbers are the first
### element in the package's version list
packages <- c(
                dplyr     = "0.7.6",
                ggplot2   = "3.0.0" ,
                gridExtra = "2.2.1" ,
                magrittr  = "1.5" ,
                plyr      = "1.8.4" ,
                readxl    = "1.0.0" ,
                reshape   = "0.8.6" ,
                stringr   = "1.1.0" ,
                tidyr     = "0.8.1" ,
                zoo       = "1.7-14",
                openxlsx  = "4.0.0" ,
                XML       = "3.98-1.20"
                )

### Loops through the packages & their respective versions and pass them to
### devtools.install_version() if necessary
for ( pckg in names( packages ) ){

    print( glue( "Checking {pckg}..." ) )
    
    vers_num <- packages[[pckg]]

    if ( pckg %in% rownames( lib_matrix ) == FALSE ){
        ### No version of the package is currently installed

        print( glue( "     {pckg} not found! Installing..." ) )

        ### Download the package
        result <- downloadPackage( pckg, vers_num )
        if ( result != 1 ) {
            failed_pckgs <- c( failed_pckgs, pckg )
        }

    } else {
        ### A version of the package is already installed

        print( glue( "     {pckg} found!" ) )

        curr_vers <- lib_matrix[pckg, 3]

        if ( curr_vers != vers_num ) {
            ### Installed package version is not acceptable

            print( glue( "     Current version: {curr_vers}" ) )
            print( glue( "     Required:        {vers_num}" ) )

            ### Download the package
            result <- downloadPackage( pckg, vers_num )
            if ( result != 1 ) {
                failed_pckgs <- c( failed_pckgs, pckg )
            }

        } else {
            print( glue( "     Version {curr_vers} OK" ) )
        }
    }
    writeLines( "\n" )
}


if ( length( failed_pckgs ) > 0 ) {
    for ( i in 1:length( failed_pckgs ) ) {
        print( glue( "--- Package {failed_pckgs[i]} failed to download! ---" ) )
    }
}
