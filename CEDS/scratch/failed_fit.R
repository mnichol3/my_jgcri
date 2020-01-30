# Script to test solution to the problem of reporting out ISOs of failed fits
# in the CEDS Uncertainty package
#
# Matt Nicholson
# 1-28-2020


# Create an environment to hold the failed fitting objects. See documentation
# for add.failed.fit() for further details
#
# MN 1-28-2020
failed_fits <- new.env()
failed_fits$count <- 0
failed_fits$rslt <- list(NULL)
failed_fits$size <- 1


# Add a failed.fit object to the failed_fits environment
#
# In the worst case, there could be over 24,420 failed fits. The most efficient
# way to gather the failed fits would be to pre-allocate an empty list of size 25,000
# and iteratively add the failed fits to it, however the worst case represents
# a very small number of actual cases.
#
# To balance efficiency and memory usage, we can create an environment containing
# a list that doubles in size every time it becomes full. Using this method,
# 2e4 items can be added to a list that starts at size = 1 in 0.22 seconds.
#
# Modified from Ferdinand.kraft's answer here:
# https://stackoverflow.com/questions/17046336/here-we-go-again-append-an-element-to-a-list-in-r
#
# Params
#   failed_fit - failed.fit object
#
# MN 1-28-2020
add.failed.fit <- function(failed_fit) {
    # When the list is full, double its size
    if( failed_fits$count == failed_fits$size )
    {
        # Double the variable tracking the list's size, then double the size of the list.
        # New list elements get initialized to NULL
        failed_fits$size <- failed_fits$size * 2
        length(failed_fits$rslt) <- failed_fits$size
    }

    failed_fits$count <- failed_fits$count + 1

    failed_fits$rslt[[failed_fits$count]] <- failed_fit
}


# Class for a failed fitting from CEDS Uncertainty, fitting_funcs.R
#
# Params
#   fit_type - Character; Type of fit attempted
#   b_iso - Character; ISO that failed the fit
#   b_sector - Character; Sector associated with the failed fit
#   b_fuel - Character; Fuel associated with the failed fit
#   err - Character; Error message associated with the fitting failure
#
# Return
#   failed.fit object
failed.fit <- function(fit_type, b_iso, b_sector, b_fuel, err) {

    attr_list <- list(type = fit_type,
                      iso = b_iso,
                      sector = b_sector,
                      fuel = b_fuel,
                      error = err)

    s <- structure(attr_list, class = "failed.fit")

    s

}


# Print function for the failed.fit objects
#
# Params
#   obj - failed.fit object
report.failed.fits <- function(obj) {
    # NULL check since the last m objects in the list could be NULL
    if (!is.null(obj)) {
        cat('Could not apply logistic fit for', obj$iso, obj$sector, obj$fuel, '(reason:', obj$error, '\b)\n')
    }
}



# ================================= Setup & Run ================================

bad_fits <- list(
    list(iso = 'sgp', sector = '1A3b_Road', fuel = 'diesel_oil', err = 'number of iterations exceeded maximum of 50'),
    list(iso = 'tgo', sector = '1A3b_Road', fuel = 'diesel_oil', err = 'number of iterations exceeded maximum of 50'),
    list(iso = 'tha', sector = '1A3b_Road', fuel = 'diesel_oil', err = 'number of iterations exceeded maximum of 50'),
    list(iso = 'tjk', sector = '1A3b_Road', fuel = 'light_oil', err = 'step factor 0.000488281 reduced below minFactor of 0.000976562'),
    list(iso = 'tls', sector = '1A3b_Road', fuel = 'diesel_oil', err = 'step factor 0.000488281 reduced below minFactor of 0.000976562'),
    list(iso = 'tls', sector = '1A3b_Road', fuel = 'light_oil', err = 'step factor 0.000488281 reduced below minFactor of 0.000976562'),
    list(iso = 'tto', sector = '1A3b_Road', fuel = 'diesel_oil', err = 'number of iterations exceeded maximum of 50')
)

# Create new failed.fit objects and add them to the failed_fits env
lapply(bad_fits, function(x) {
    f <- failed.fit('logistic', x$iso, x$sector, x$fuel, x$err)
    add.failed.fit(f)
})

# Print the failed.fit objects
lapply(failed_fits$rslt, report.failed.fit)

