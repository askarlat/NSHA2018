"""Code for building a source model for plate boundary regions
to the north of Australia
Jonnathan Griffin
Geoscience Australia, November 2017
"""

import os, sys
from glob import glob
import numpy as np
from NSHA2018.source_models.faults.shapefile2nrml import shapefile_2_complexfault, \
    shp2nrml
try:
    import netCDF4
except ImportError:
    print 'NetCDF4 not installed/loaded, be sure to run module load netcdf on NCI'

contour_dir = './shp'
contour_shapefiles = glob(os.path.join(contour_dir, '*.shp'))
rate_dir = './source_rates'
source_model_name = 'banda_sources'
tectonic_region = 'banda'
magnitude_scale_rel = 'Leonard2014_Interplate'
rupture_aspect_ratio = 1.5
rake = 90 # Fix for normal sources!
#min_mag = 6.0 # currently 7.2 based on PTHA curves
bin_width = 0.1
# Store output xml strings here
output_xml = []

# Add xml headers
shp2nrml.append_xml_header(output_xml, source_model_name)

# Now add each fault source
id_base = 'banda_'
i = 0
for shapefile in contour_shapefiles:
    sourcename = shapefile.split('/')[-1][:-4]
    print 'Adding source %s' % sourcename
    contours = shapefile_2_complexfault.parse_line_shapefile(
        shapefile, 'level')
    ID = id_base + str(i)
    i+=1
    shapefile_2_complexfault.append_fault_source_header(output_xml,
                                                        ID,
                                                        sourcename,
                                                        tectonic_region)
    shapefile_2_complexfault.append_rupture_geometry(output_xml, 
                                                     contours)

    # Now we want to read and sum the rates from the PTHA data
    ratefilename = 'all_uniform_slip_earthquake_events_%s.nc' % sourcename
    ratefile = os.path.join(rate_dir, ratefilename)
    ratedata = netCDF4.Dataset(ratefile, 'r')
    magnitudes = ratedata.variables['Mw'][:]
    rates = ratedata.variables['rate_annual'][:]
    mw_rates = np.vstack([magnitudes, rates])
    print mw_rates
    # These should be sorted by magnitude, but best not to assume
    mw_rates = mw_rates[mw_rates[:,1].argsort()]
    mw_rates = np.fliplr(mw_rates) # Descending order for cum-sum calcs
    print mw_rates

    mw_list = []
    cum_rates = []
    rate_cumsum = 0
    mag = mw_rates[1][0]
    print mag
    j=0
    for mw in mw_rates[1][:]:
        if mw == mag:
            rate_cumsum += mw_rates[0][j]
        else:
            cum_rates.append(rate_cumsum)
            mw_list.append(mag)
            mag = mw_rates[1][j] # Update to next magnitude increment
            rate_cumsum += mw_rates[0][j]
        j+=1
    # Append final rates
    mw_list.append(mag)
    cum_rates.append(rate_cumsum)
    print mw_list
    print cum_rates
    min_mag = min(mw_list)
#    sys.exit()
    shp2nrml.append_incremental_mfd(output_xml, magnitude_scale_rel,
                                    rupture_aspect_ratio, rake,
                                    min_mag, bin_width, rates)
    
