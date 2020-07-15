#!/usr/bin/env python
"""
Download precipitation from ERA5
Daily amount of precipitation is obtained by summation over hourly data

For 2m temperature use 'time' : '00:00' and 'variable' : '2m_temperature'
For windspeed use 'time' : '00:00' and 'variable': ['10m_u_component_of_wind', '10m_v_component_of_wind']
"""
import cdsapi
years = ['2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018']
var_name  = 'tp'
for year in years: 
    name = var_name + '_%s.nc' % (year)
    c = cdsapi.Client()
    r = c.retrieve(
        'reanalysis-era5-single-levels', {
                'variable'    : 'total_precipitation',
                'product_type': 'reanalysis',
                'year'        : year,
                'month'       : ['01','02','03','04','05','06','07','08','09','10','11','12'],
                'day'         : ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31'],
                'time'        : [
                    '00:00','01:00','02:00',
                    '03:00','04:00','05:00',
                    '06:00','07:00','08:00',
                    '09:00','10:00','11:00',
                    '12:00','13:00','14:00',
                    '15:00','16:00','17:00',
                    '18:00','19:00','20:00',
                    '21:00','22:00','23:00'
                ],
                'format'      : 'netcdf'
        })
    r.download(name)
