# generate_anthro_1850.R
#
# Generate final figures for the emissions_gridding paper.
#
# Read instructions in gridding_paper_figures.R, then run this file.
#
# Matt Nicholson
# 12/17/19
source('code/gridding-paper-figures/gridding_paper_figures.R')

CH4_1850 <- file.path(HISTORICAL_EMS_DIR, 'CH4-em-anthro_input4MIPs_emissions_CMIP_CEDS-2017-05-18-supplemental-data_gn_185001-196012.nc')
CH4_1980 <- file.path(HISTORICAL_EMS_DIR, 'CH4-em-anthro_input4MIPs_emissions_CMIP_CEDS-2017-05-18_gn_197001-201412.nc')
stopifnot(all(file.exists(c(CH4_1850, CH4_1980))))

# Get breaks for consistent scale across all years ------------------------
#
# In order to have all plots show emissions with the same scale, we need to
# provide the same scale breaks for each year we are plotting. To do this, we
# first load all of the grids that need the same scale, then call the function
# `calculate_em_cuts` to get the scale breaks for each species.
#
# Note that the grids are cached when loaded here, so that plotting does not
# have to re-load them.

# Historical gridding file names
print("Gathering historical gridded file names")
nc_files_hist_1850 <- get_nc_filenames(EM_LIST, 'anthro', '1850', HISTORICAL_EMS_DIR, nc_files = c(CH4=CH4_1850))
nc_files_hist_1950 <- get_nc_filenames(EM_LIST, 'anthro', '1950', HISTORICAL_EMS_DIR, nc_files = c(CH4=CH4_1980))

# Special arguments for loading each type of file
hist_1850_args   <- list(years = 1850, nc_years = list(CH4 = seq(1850, 1960, 10), default = 1850))
hist_1980_args   <- list(years = 1980, nc_years = HIST_YEAR_LIST)

# Create lists of emissions grids, where each element is an array with year in
# the third dimension
em_grids_hist_1850 <- Map(load_emissions_grid, nc_files_hist_1850, EM_LIST, MoreArgs = hist_1850_args)
em_grids_hist_1950 <- Map(load_emissions_grid, nc_files_hist_1950, EM_LIST, MoreArgs = hist_1980_args)

# Combine emissions for each species across all years and types
em_grids_all <- Map(c, em_grids_hist_1850[NON_CO2], em_grids_hist_1950[NON_CO2])

# Future open burning emissions do not include CO2, so add it separately
em_grids_all['CO2'] <- Map(c, em_grids_hist_1950['CO2'], em_grids_hist_1850['CO2'])

# Calculate the breaks
breaks <- lapply(em_grids_all, calculate_em_cuts, get_breaks = TRUE)


# Create plots ------------------------------------------------------------

# 1850 anthro figure
print("Plotting 1850 anthro figure")
plot_em_grids(EM_LIST, 'anthro', 1850, '1850',
              indir = HISTORICAL_EMS_DIR,
              outdir = 'output/gridding-paper-figures',
              nc_years = list(CH4=seq(1850, 1960, 10), default = 1850),
              nc_files = c(CH4=CH4_1850),
              breaks = breaks)