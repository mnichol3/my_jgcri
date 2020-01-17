library(hector)

cum_vars_input <- function(core, dates, lib_funcs) {

    # Use regex to find the indices of EMISSIONS_* function names
    func_idx <- grep("^EMISSIONS_+", lib_funcs)

    # Get the variable closures and execute them to get the capabililty strings
    var_funcs <- sapply(lib_funcs[func_idx], get)

    # Don't really know what this does exactly but it makes the sendmessage()
    # call work
    vars_em <- getOption('hector.vars.emissions',
                         default=sapply(var_funcs, function(f){f()}))

    # Repeat the above process for PREINDUSTRIAL_* functions
    func_idx <- grep("^PREINDUSTRIAL_+", lib_funcs)
    var_funcs <- sapply(lib_funcs[func_idx], get)
    vars_conc <- getOption('hector.vars.preindustrial',
                           default=sapply(var_funcs, function(f){f()}))


    # Get model output for variables that use date arg
    rslt_em <- do.call(rbind,
                       lapply(vars_em, function(v) {
                           sendmessage(core, GETDATA(), v, dates, NA, '')
                       }))

    # Get model output for variables that DO NOT use date arg
    rslt_conc <- do.call(rbind,
                         lapply(vars_conc, function(v) {
                             sendmessage(core, GETDATA(), v, NA, NA, '')
                         }))

    rslt_tot <- rbind(rslt_em, rslt_conc)

    invisible(rslt_em)
}


#' Cumulate Hector parameters
#'
#' This function cumulates all available Hector parameters, such as BETA, ESC,
#' and Volcanic Scale
#'
#' @param core Hector object
#' @return rslt_tot Dataframe containing the parameters/variables
#' @family fetchvars_all helper function
cum_vars_params <- function(core) {

    # These variables don't follow a common naming rule (i.e., EMISSIONS_*),
    # so the best option is to hardcode
    vars <- c(AERO_SCALE(), BETA(), DIFFUSIVITY(), ECS(), F_NPPV(), F_NPPD(),
              F_LITTERD(), F_LUCV(), Q10_RH(), VOLCANIC_SCALE(), WARMINGFACTOR()
    )

    # Get the data for the given list of variables
    rslt_tot <- do.call(rbind,
                        lapply(vars, function(v) {
                            sendmessage(core, GETDATA(), v, NA, NA, '')
                        }))

    invisible(rslt_tot)
}


#' Cumulate Hector output variables
#'
#' This function cumulates all available output variables from an active Hector
#' core (e.g.,  Concentrations, Forcings, etc.)
#'
#' @param core Hector core object
#' @param dates Vector of dates
#' @return rslt_tot Dataframe containing the variables
#' @family fetchvars_all helper function
cum_vars_output <- function(core, dates, lib_funcs) {

    # Atmospheric concentrationvars. Take date arg
    func_idx <- grep("^ATMOSPHERIC_+", lib_funcs)
    var_funcs <- sapply(lib_funcs[func_idx], get)
    vars_conc_d <- getOption('hector.vars.atmospheric',
                             default=sapply(var_funcs, function(f){f()}))


    # Various concenctration, temperature, & flux parameters that
    # DO NOT take a date arg
    func_idx <- grep("^OCEAN_C(_\\w{2})?$|^ATM_OCEAN_+|\\w{1,5}_[HL]L$", lib_funcs)
    var_funcs <- sapply(lib_funcs[func_idx], get)
    vars_ocn_nd <- getOption('hector.vars.ocean',
                             default=sapply(var_funcs, function(f){f()}))

    # Various CFLUX and Natural emission variables. DO NOT take date arg
    func_idx <- grep("^\\w{4,5}_CFLUX$|^NATURAL_+", lib_funcs)
    var_funcs <- sapply(lib_funcs[func_idx], get)
    vars_cflux_nd <- getOption('hector.vars.cflux',
                               default=sapply(var_funcs, function(f){f()}))

    # Temperature and flux variabels. Take date arg
    func_idx <- grep("+_TEMP(\\w{2})?$|+_FLUX$", lib_funcs)
    var_funcs <- sapply(lib_funcs[func_idx], get)
    vars_temps_d <- getOption('hector.vars.oceantemps',
                              default=sapply(var_funcs, function(f){f()}))

    # Radiative forcing variables. Date arg OK
    func_idx <- grep("PREINDUSTRIAL_+", lib_funcs)
    var_funcs <- sapply(lib_funcs[func_idx], get)
    vars_rf <- getOption('hector.vars.radforcing',
                         default=sapply(var_funcs, function(f){f()}))

    # Concat the lists of vars that do & do not use date arg, respectively
    vars_d <- c(vars_conc_d, vars_temps_d)
    vars_nd <- c(vars_ocn_nd, vars_cflux_nd)

    # Get variables that DO NOT use date arg
    rslt_nd <- do.call(rbind,
                       lapply(vars_nd, function(v) {
                           sendmessage(core, GETDATA(), v, NA, NA, '')
                       }))

    # Get variables that use date arg
    rslt_d <- do.call(rbind,
                      lapply(vars_d, function(v) {
                          sendmessage(core, GETDATA(), v, dates, NA, '')
                      }))

    # Combine the results of the sendmessage calls into one dataframe
    rslt_tot <- rbind(rslt_nd, rslt_d)

    invisible(rslt_tot)
}



#' Fetch all the available Hector variables
#'
#' This function is similar to fetchvars, except it fetches all available
#' Hector variables, including exogenous inputs (e.g., emissions & pre-industrial
#' concentrations), parameters (e.g., alpha, beta, ECS), and output
#' variables (e.g., concentrations & forcings).
#'
#' @param core Hector core object
#' @param dates ector of dates, optional
#' @param scenario Scenario name, optional str
#' @param write If TRUE, write the resulting dataframe to a csv file, optional bool
#' @param outpath Absolute path of the output csv. Must be given if 'write' is true
#' @return vars_all    Dataframe containing all Hector variables
#' @family main user interface functions
#' @export
fetchvars_all <- function(core, dates=NULL, scenario=NULL, outpath=NULL) {

    if (is.null(scenario)) {
        scenario <- core$name
    }

    strt <- startdate(core)
    end <- getdate(core)

    if (is.null(dates)) {
        dates <- strt:end
    } else {
        valid <- dates >= strt & dates <= end
        dates <- dates[valid]
    }

    # Ocean variables. Not all can take date arg
    vars_ocean <- c(ATM_OCEAN_FLUX_HL(), ATM_OCEAN_FLUX_LL(),
                    CO3_HL(), CO3_LL(),
                    DIC_HL(), DIC_LL(),
                    OCEAN_AIR_TEMP(), OCEAN_C(),
                    OCEAN_C_DO(), OCEAN_C_HL(),
                    OCEAN_C_IO(), OCEAN_C_LL(),
                    OCEAN_CFLUX(), OCEAN_SURFACE_TEMP(),
                    PCO2_HL(), PCO2_LL(),
                    PH_HL(), PH_LL(),
                    TEMP_HL(), TEMP_LL())


    # Variables that cannot take date parameter
    vars_nodate <- c(AERO_SCALE(), BETA(), DIFFUSIVITY(), ECS(), F_NPPV(), F_NPPD(),
                     F_LITTERD(), F_LUCV(), Q10_RH(), VOLCANIC_SCALE(), WARMINGFACTOR())

    vars_all <- rbind(vars_inpt, vars_param, vars_outpt)

    # If 'outpath' is given, reshape the resulting data frame to a wide format
    # and write csv to the specified path
    if (outpath) {

        # Pivot the dataframe "wide" so years run along the x axis
        # Catch warning from reshape()
        suppressWarnings(vars_all <- reshape(vars_all, direction="wide",
                                             idvar=c("variable", "units"), timevar="year"))

        # Clean up the column names (value.YYYY --> YYYY)
        col_names <- colnames(vars_all)[-1:-2]
        col_names <- sapply(col_names, function(x) sub("value.", "", x), USE.NAMES=F)
        col_names <- col_names[-length(col_names)]

        col_names <- c("variable", "units", "initial value", col_names)

        num_cols <- length(col_names)

        # Move last column into 3rd col position
        vars_all <- vars_all[, c(1, 2, num_cols, 4:num_cols-1)]

        # Set the column names for the re-ordered dataframe
        colnames(vars_all) <- col_names

        # Construct output filename and absolute path
        f_name <- "fetchvars_all.csv"
        abs_path <- file.path(outpath, f_name)

        write.table(vars_all, abs_path, col.names=col_names, row.names=F, sep=',')

        message("Output written to ", abs_path)
    }

    invisible(vars_all)
}




################## Simple Hector run from Alexey's vignette ####################
ini_file <- system.file("input/hector_rcp45.ini", package = "hector")

core <- newcore(ini_file)

run(core)

# vars_all <- fetchvars_all(core, 2100:2200, write=T, outpath="C:/Users/nich980/data/hector/test/fetchvars_all.csv")
vars_all <- fetchvars_all(core, 2100:2200)

# print(vars_all)


