# -*- coding: utf-8 -*-
"""
Created on Wed Feb 07 16:11:14 2018

@author: u56903
"""

# do Gardner & Knopoff (1974 declustering)
def decluster_GK74(catalogue, filename):
    from os import remove
    from copy import deepcopy
    from hmtk.seismicity.declusterer.dec_gardner_knopoff import GardnerKnopoffType1
    from hmtk.seismicity.declusterer.distance_time_windows import GardnerKnopoffWindow
    from hmtk.parsers.catalogue.csv_catalogue_parser import CsvCatalogueWriter
    
    decluster_config = {'time_distance_window': GardnerKnopoffWindow(),
                        'fs_time_prop': 1.0}
    
    #####################################################
    # decluster here
    #####################################################
    
    print 'Running GK declustering...'
    decluster_method = GardnerKnopoffType1()
    
    #---------------------------------------------
    # declustering
    cluster_index_gk, cluster_flags_gk = decluster_method.decluster(catalogue, decluster_config)
    #---------------------------------------------
    
    # adding to the catalog
    # The cluster flag (main shock or after/foreshock) and cluster index to the catalogue keys
    catalogue.data['cluster_index_gk'] = cluster_index_gk
    catalogue.data['cluster_flags_gk'] = cluster_flags_gk
    
    #####################################################
    # purge remove non-poissonian events
    #####################################################
    
    # create a copy from the catalogue object to preserve it
    catalogue_gk = deepcopy(catalogue)
    
    catalogue_gk.purge_catalogue(cluster_flags_gk == 0) # cluster_flags == 0: mainshocks
    
    print 'Gardner-Knopoff\tbefore: ', catalogue.get_number_events(), " after: ", catalogue_gk.get_number_events()
    
    #####################################################
    # write declustered catalogue
    #####################################################
    
    # setup the writer
    #declustered_catalog_file = filename.split('.')[0]+'_GK74_declustered.csv'
    declustered_catalog_file = filename[0:-9] + '_GK74_declustered.csv'
    
    # if it exists, delete previous file
    try:
        remove(declustered_catalog_file)
    except:
        print declustered_catalog_file, 'does not exist'
    
    # set-up writer
    writer = CsvCatalogueWriter(declustered_catalog_file) 
    
    # write
    writer.write_file(catalogue_gk)
    #writer.write_file(catalogue_af)
    print 'Declustered catalogue: ok\n'

# decluster ISC-GEM catalogue using Gardner & Knopoff method
def decluster_iscgem_gk74(hmtk_csv):
    from hmtk.parsers.catalogue.csv_catalogue_parser import CsvCatalogueParser
    
    # parse isc-gem hmtk
    #hmtk_csv = path.join('data', 'ISC-GEM_V4_hmtk_full.csv')
    
    # parse HMTK csv
    parser = CsvCatalogueParser(hmtk_csv)
    cat = parser.read_file()
    
    decluster_GK74(cat, hmtk_csv)

# Convert native ISC-GEM catalogue download to HMTK
def convert_iscgem2hmtk(iscgemcsv):   
    from parsers import parse_iscgem
    from writers import iscgem2hmtk_csv
    from os import path
    
    # parse catalogue
    #iscgemcsv = 'data/isc-gem-cat.csv'
    iscgemDict = parse_iscgem(iscgemcsv)
    
    # convert to hmtk
    iscgem2hmtk_csv(iscgemDict, path.join('data', 'ISC-GEM_V4_hmtk_full.csv'))
    
# clip declustered global GEM-ISC catalogue to local region
def clip_declustered_iscgem_hmtk(hmtkcsv):
    from hmtk.parsers.catalogue.csv_catalogue_parser import CsvCatalogueParser, CsvCatalogueWriter
    from copy import deepcopy
    
    print '\nNOTE: this code is incomplete\n'
    
    minlat = -55.
    maxlat = 5.
    minlon = 95.
    maxlon = 166.
    
    # parse HMTK csv
    parser = CsvCatalogueParser(hmtk_csv)
    cat = parser.read_file()
    
    # create a copy from the catalogue object to preserve it
    catalogue_gk = deepcopy(cat)
    
    catalogue_gk.purge_catalogue(cluster_flags_gk == 0) # cluster_flags == 0: mainshocks
    
    # set-up writer
    writer = CsvCatalogueWriter(declustered_catalog_file) 
    
    # write
    writer.write_file(catalogue_gk)