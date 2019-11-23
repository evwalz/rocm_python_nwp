# CPA example - Numerical weather prediction

Code to replicate the CPA plots for the numerical weather prediction example in the paper ROC movies, universal ROC curves and coefficient of predictive ability (CPA). 

### Data
HRES forecast and ERA reanalysis product downloaded from European Centre for Medium-Range Weather Forecasts (ECMWF) from https://confluence.ecmwf.int/display/TIGGE and https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-single-levels?tab=overview at initial time 00:00 UTC for the years 2007-2018. Note that for precipitation summation over hourly rainfall from ERA5 is necessary. Both wind speed and 2m Temperature are instantaneous. 

### Processing the data
The data is stored in a netCDF-format. Before computing the CPA plots the netCDF-files are modified by using CDO to perform standard operations on climate and forecast model data. After performing some CDO operations the data output is of the following form:
- regional data that covers Europe (25W, 44.5E, 74.5N, 25N)
- ranging from 2007-2018 (In Reanalysis also 27.12.2006-31.12.2006 included to compute persistence forecast)
- a single value of 2 meter temperature (wind speed, total precipitation) per day
- thus each file consists of 279 x 199 grid points and 365*9+366*3 = 4383 days

### Code
A python routine can be used to compute the value of the CPA. To compute the uroc curve and the rocm the R package uroc provides the required functionalities. An implementation of these functions in python will soon be available. 

