# Run multiple Hector scenarios
#
# Author: Matt Nicholson
# 18 Dec 19

library(hector)
library(ggplot2)

# scenarios <- c("gas_paris_med",
#                "gas_paris_plus_med",
#                "gas_no_paris_med",
#                "gas_ref_med")

scenarios <- c("gas_paris_med", "gas_ref_med")

#                   Ca              Ftot        Tgav
out_vars <- c(ATMOSPHERIC_CO2(), RF_TOTAL(), GLOBAL_TEMP(), PH_HL(), PH_LL())

out_path <- "C:/Users/nich980/data/hector/output"

### First scenario
scen = scenarios[1]
print( paste0( "Running scenario ", scen) )

f_out = file.path( out_path, paste0( scen, ".csv" ) )
f_ini = file.path( "input", paste0( scen, ".ini" ) )

ini_file <- system.file(f_ini, package = "hector")

core <- newcore(ini_file, name=scen)

run(core)

results <- fetchvars(core, 1745:2300, vars=out_vars)

for ( idx in 2:length(scenarios)) {

    scen <- scenarios[idx]
    print( paste0( "Running scenario ", scen) )

    f_out = file.path( out_path, paste0( scen, ".csv" ) )
    f_ini = file.path( "input", paste0( scen, ".ini" ) )

    ini_file <- system.file(f_ini, package = "hector")

    core <- newcore(ini_file, name=scen)

    run(core)

    curr_results <- fetchvars(core, 1745:2300, vars=out_vars)
    results <- rbind(results, curr_results)
    # results_rs <- reshape(results, idvar=c("year", "scenario"), timevar="variable", direction="wide")

    # write.csv(results, f_out, row.names = FALSE)
}

p <- ggplot(results) +
        aes(x = year, y = value, color = factor(scenario)) +
        geom_line() +
        facet_wrap(~variable, scales = "free_y") +
        guides(color = guide_legend(title = expression(scenario)))


print(p)
