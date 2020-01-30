#!/bin/bash

end=".nc"
end2="*.nc"
years="2007 2008 2009 2010 2011 2012 2013 2014 2015 2016 2017 2018"
months="01 02 03 04 05 06 07 08 09 10 11 12"
sep="-"

echo input file directory with file name 
read filedir1
echo output file directory with file name
read filedir2

echo The area 25W, 44.5E, 74.5N, 25N is selected

for year in $years
do

        for month in $months
        do
                filein1="$filedir1$year$sep$month$end"
                fileout1="$filedir2$year$sep$month$end"
                if test -f "$filein1"; then
                        cdo sellonlatbox,335,44.5,25,74.5 $filein1 $fileout1
                fi
        done
done

echo Files are merged by year from 2007 to 2018 

for year in $years
do 
       	filein2="$filedir2$year$end2"
	fileout2="$filedir2$year$end"
	cdo mergetime $filein2 $fileout2
        rm $filein2
done


