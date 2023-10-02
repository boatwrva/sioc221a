% SIOC 221 Data Analysis: HW1 

% problem1: Statistics of sea surface temperature. Download the 2021 sea surface temperature data for the Scripps Pier from the SCCOOS web site:

url = 'http://thredds.sccoos.org/thredds/dodsC/autoss/scripps_pier-2021.nc'; 
ncdisp(url)

lon = ncread(url,'lon');
lat = ncread(url,'lat');