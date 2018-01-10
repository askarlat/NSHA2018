# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 09:42:50 2017

@author: u56903
"""
def checkstr(num):
    '''
    check if number is nan.  If True, return blank ('')
    '''
    from numpy import isnan
    
    if  isinstance(num, basestring):
        return num
    else:
        if isnan(num):
            return ''
        else:
            return str(num)


def ggcat2ascii(ggcat_dict, outfile):    
    '''
    # takes event dictionary format as parsed by catalogues.parsers.parse_ggcat
    
    # exports to outfile
    '''
    # make file for writing
    cattxt = ''
    
    for ev in ggcat_dict:
        # set string constant width
        datestr = '{0.year:4d} {0.month:02d} {0.day:02d} {0.hour:02d}{0.minute:02d}'.format(ev['datetime'])
        
        # make line        
        line = ' '.join((datestr, str("%0.3f" % ev['lon']), str("%0.3f" % ev['lat']), \
                         str("%0.1f" % ev['dep']), str("%0.1f" % ev['prefmag']), \
                         ev['prefmagtype'], ev['auth']))
                       
        cattxt = cattxt + line + '\n'
                
    #f = open(path.join(outfolder, outfile), 'wb')
    f = open(outfile, 'wb')
    f.write(cattxt)
    f.close()
    
def ggcat2hmtk_csv(ggcat_dict, hmtkfile, prefmag):
    '''
    prefmag = 'orig' or 'mw'
    '''
    
    '''
    takes catalogue dictionary format as parsed by catalogues.parsers.parse_ggcat
    
    returns OQ compliant catalogue in csv fmt
    '''
    
    # make oq cat dict
    header = ','.join(('eventID','year', 'month', 'day', 'hour', 'minute', 'second', \
                       'longitude', 'latitude','depth','magnitude','magnitudeType', \
                       'Agency', 'flag', 'mx_origML', 'mx_origType', 'mx_revML', 'pref_mw'))
    oq_dat = header + '\n'
    
    '''
    tmpdict = {'auth':line[7], 'place':line[30],'year':evdt.year, 'month':evdt.month, 'day':evdt.day, \
                   'hour':evdt.hour, 'min':evdt.minute, 'sec':evdt.second, 'lon':float(line[4]), 'lat':float(line[5]), 'dep':float(line[6]), \
                   'prefmag':float(line[28]), 'prefmagtype':line[29], 'ml':float(line[14]), 'mb':float(line[12]), 'ms':float(line[10]), \
                   'mw':float(line[8]), 'mp':float(line[17]), 'fixdep':0, 'datetime':evdt, 'dependence':str(line[3]), 'mx_orig':float(line[20]), \
                   'mx_origType':omt, 'mx_rev_ml':float(line[21]), 'mx_rev_src':line[22], 'mw_src':line[-2]}
    '''
                   
                   
    # loop thru eqs
    for ggc in ggcat_dict:
        # make datstr - strftime does not work for dats < 1900!
        datestr = '{0.year:4d}{0.month:02d}{0.day:02d}{0.hour:02d}{0.minute:02d}'.format(ggc['datetime'])
        
        # flag dependent or man-made events
        '''
        # for 2012 catalogue
        if ggc['dependence'] == 'Aftershock' or ggc['dependence'] == 'Foreshock':
            flag = '1'
        elif  ggc['ev_type'] == 'blast' or ggc['ev_type'] == 'coal':
            flag = '2'
        else:
            flag = '0'
        '''
        # for 2018 catalogue
        
        if ggc['dependence'] == 0:
            flag = '1'
        else:
            flag = '0'
            
        # set Original magnitude as main magnitude for declustering (mx_orig) and add additional columns
        if prefmag == 'orig':
            line = ','.join((datestr, checkstr(ggc['year']), checkstr(ggc['month']),checkstr(ggc['day']), \
                             checkstr(ggc['hour']).zfill(2),checkstr(ggc['min']).zfill(2),checkstr(ggc['sec']),checkstr(ggc['lon']),checkstr(ggc['lat']), \
                             checkstr(ggc['dep']),checkstr(ggc['mx_orig']),checkstr(ggc['mx_origType']),ggc['auth'], flag, \
                             checkstr(ggc['mx_orig']), checkstr(ggc['mx_origType']), checkstr(ggc['mx_rev_ml']), checkstr(ggc['prefmag'])))
        
        # else use pref mw
        else:
            line = ','.join((datestr, checkstr(ggc['year']), checkstr(ggc['month']),checkstr(ggc['day']), \
                             checkstr(ggc['hour']).zfill(2),checkstr(ggc['min']).zfill(2),checkstr(ggc['sec']),checkstr(ggc['lon']),checkstr(ggc['lat']), \
                             checkstr(ggc['dep']),checkstr(ggc['prefmag']),checkstr(ggc['mx_origType']),ggc['auth'], flag, \
                             checkstr(ggc['mx_orig']), checkstr(ggc['mx_origType']), checkstr(ggc['mx_rev_ml']), checkstr(ggc['prefmag'])))     
        '''
        # for making MX_REV_ML file        
        line = ','.join((datestr, checkstr(ggc['year']), checkstr(ggc['month']),checkstr(ggc['day']), \
                         checkstr(ggc['hour']).zfill(2),checkstr(ggc['min']).zfill(2),checkstr(ggc['sec']),checkstr(ggc['lon']),checkstr(ggc['lat']), \
                         checkstr(ggc['dep']),checkstr(ggc['mx_rev_ml']),checkstr(ggc['mx_rev_src']),ggc['auth'], flag))
        '''                 
        oq_dat += line + '\n'
        
    #write to OQ out
    print 'Writing HMTK csv...'
    f = open(hmtkfile, 'wb')
    f.write(oq_dat)
    f.close()
    
# writes htmk dict to shapefile
def htmk2shp(cat, outshp):
    '''
    cat = htmk dictionory
    outshp = output shapefile
    '''
    import shapefile
    from numpy import isnan
    
    print 'Making shapefile...'
    w = shapefile.Writer(shapefile.POINT)
    w.field('EVID','C','15')
    w.field('AGENCY','C','15')
    w.field('YEAR','F', 4, 0)
    w.field('MONTH','F', 2, 0)
    w.field('DAY','F', 2, 0)
    w.field('HOUR','F', 2, 0)
    w.field('MIN','F', 2, 0)
    w.field('SEC','F', 2, 0)
    w.field('LON','F', 10, 4)
    w.field('LAT','F', 10, 4)    
    w.field('DEP','F', 10, 2)
    w.field('PREF_MW','F', 13, 6)
    w.field('PREF_MAG_TYPE','C','100')
    w.field('ORIG_MAG','F', 13, 6)
    w.field('ORIG_MAG_TYPE','C','100')
    
    # now loop thru records
    for i in range(0, len(cat.data)):
        if isnan(cat.data[i]['lon']) | isnan(cat.data[i]['lat']):
            lon = 0.0
            lat = 0.0
        else:
            lon = cat.data[i]['lonitude']
            lat = cat.data[i]['latitude']
    
        w.point(lon, lat)
        w.record(cat.data[i]['eventID'],cat.data[i]['Agency'], \
                 cat.data[i]['year'],cat.data[i]['month'], \
                 cat.data[i]['day'],cat.data[i]['hour'], \
                 cat.data[i]['minute'],cat.data[i]['second'], \
                 cat.data[i]['lonitude'],cat.data[i]['latitude'], \
                 cat.data[i]['dep'],cat.data[i]['pref_mw'],\
                 cat.data[i]['mx_origML'],cat.data[i]['mx_origType'])
    
    print 'Writing shapefile...'
    w.save(outshp)
    
    # write projection file
    prjfile = outshp.strip().split('.shp')[0]+'.prj'
    f = open(prjfile, 'wb')
    f.write('GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]')
    f.close()

    
    
    
    
    
    
    
    
    
    
    
    
    