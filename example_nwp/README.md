## ROCM in Numerical Weather Prediction (NWP)

Code to replicate the CPA plots for the numerical weather prediction example in the paper "ROC movies — a new generalization to a popular classic. 

### Data
HRES forecast and ERA reanalysis product downloaded from European Centre for Medium-Range Weather Forecasts (ECMWF) from https://confluence.ecmwf.int/display/TIGGE and https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-single-levels?tab=overview at initial time 00:00 UTC for the years 2007-2018. Note that for precipitation summation over hourly rainfall from ERA5 is necessary. Both wind speed and 2m Temperature are instantaneous. 

### Processing the data
The data is stored in netCDF-format. Before computing the CPA plots the netCDF-files are modified by using CDO to perform standard operations on climate and forecast model data. After applying these operations (see tigge.sh) the data output is of the following form:
- regional data that covers Europe (25W, 44.5E, 74.5N, 25N)
- ranging from 2007-2018 (In Reanalysis also 27.12.2006-31.12.2006 included to compute persistence forecast)
- a single value of 2 meter temperature (wind speed, total precipitation) per day
- thus each file consists of 279 x 199 grid points and 365x9+366x3 = 4383 days

### Files
1. **RetrieveTiggeData.py**

download tigge data from ECMWF for 2m temperature, precipitation and wind speed for different lead times

2. **RetrieveERA5Data.py**

download ERA5 data from Copernicus Climate Change Service (C3S) Climate Date Store for 2m temperature, precipitation and wind speed

2. **tigge.sh**:

performs CDO operations on tigge data set

3. **nwp_cpa_plot.py**:

uses preprocessed netCDF files to compute cpa plots.



