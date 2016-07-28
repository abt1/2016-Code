'''Before using this code, here is how the input file should be made:
1) Start with a GZ2 classification table, and a MaNGA data table
2) Remove columns until all that are left are:
MaNGA: RA, DEC, IAUNAME, MANGAID, MANGA_TILEID, Z, IFUTARGETSIZE, NSAID, PETHROTH50,
SERSIC_TH50
GZ: specobjid, dr8objid, dr7objid, ra, dec, t01_smooth_or_features_a02_features_or_disk_weighted_fraction,
t02_edgeon_a05_no_weighted_fraction, t03_bar_a06_bar_weighted_fraction, t04_spiral_a08_spiral_weighted_fraction

3) Sky match the tables by RA and DEC in topcat, with the MaNGA data as table 1, and GZ as table 2.
4) Remove the second set of RA and DEC columns, and name the first ones 'RA' and 'DEC'
5) Save this file as a csv
'''

import numpy as np
from panoptes_client import SubjectSet, Subject, Project, Panoptes
import os
myusername = os.environ['PANOPTES_USERNAME']
mypassword = os.environ['PANOPTES_PASSWORD']
Panoptes.connect(username= myusername, password=mypassword)

project = Project.find(id='73')

fullsample = SubjectSet.find(5326)
spirals = SubjectSet.find(5324)
bars = SubjectSet.find(5325)

data = np.genfromtxt('MatchedData.csv', delimiter = ',', names=True, 
                      dtype=[('DEC', float), ('IAUNAME', '|S30'),('IFUTARGETSIZE',int),
                             ('MANGAID', '|S10'),('MANGA_TILEID',int),('NSAID', int),
                             ('PETROTH50',float),('RA',float),('SERSIC_TH50',float),
                             ('Z',float),('specobjid', int),('dr8objid', int),
                             ('dr7objid', int),('t01_smooth_or_features_a02_features_or_disk_weighted_fraction', float),
                             ('t02_edgeon_a05_no_weighted_fraction', float),
                             ('t03_bar_a06_bar_weighted_fraction', float),
                             ('t04_spiral_a08_spiral_weighted_fraction', float)])
counter = 0
nancounter = 0
spiralcount = 0
summer = 0
failfile = open('FailedUploads.txt','a')
failfile.write('###########################\n')
log = open('UploadLog.txt','a')
log.write('###########################\n')
for row in data:
    if os.path.isfile('./manga_mpl4_cutouts/cutouts/{0}.jpg'.format(row['MANGAID'].decode('utf-8'))):
        if counter < 75:
            if np.isnan(row['t01_smooth_or_features_a02_features_or_disk_weighted_fraction']):
                pbar = 'NaN'
                pspiral = 'NaN'
                dr8id = 'NaN'
                dr7id = 'NaN'
                specid = 'NaN'
            else:
                pbar = row['t01_smooth_or_features_a02_features_or_disk_weighted_fraction']*row['t02_edgeon_a05_no_weighted_fraction']*row['t03_bar_a06_bar_weighted_fraction']
                pspiral = row['t01_smooth_or_features_a02_features_or_disk_weighted_fraction']*row['t02_edgeon_a05_no_weighted_fraction']*row['t04_spiral_a08_spiral_weighted_fraction']
                dr8id = row['dr8objid']
                dr7id = row['dr7objid']
                specid = row['specobjid']
            summer += 1
            if summer > 313:
                subject = Subject()
                subject.links.project = project
                subject.add_location('./manga_mpl4_cutouts/cutouts/{0}.jpg'.format(row['MANGAID'].decode('utf-8')))
                subject.metadata['RA'] = row['RA']
                subject.metadata['DEC'] = row['DEC']
                subject.metadata['MANGAID'] = row['MANGAID'].decode('utf-8')
                subject.metadata['Z'] = row['Z']
                subject.metadata['PETROTH50'] = row['PETROTH50']
                subject.metadata['#MANGA_TILEID'] = row['MANGA_TILEID']
                subject.metadata['#NSAID'] = row['NSAID']
                subject.metadata['#SERSIC_TH50'] = row['SERSIC_TH50']
                subject.metadata['#P(Bar)'] = pbar
                subject.metadata['#P(Spiral)'] = pspiral
                subject.metadata['#specobjid'] = specid
                subject.metadata['#dr8objid'] = dr8id
                subject.metadata['#dr7objid'] = dr7id
                try:
                    subject.save()
                
                    fullsample.add(subject)
                    if pspiral == 'NaN':
                        try:
                            spirals.add(subject)
                            bars.add(subject)
                            nancounter += 1
                        except:
                            print subject.metadata
                            raise Exception('stop the upload at NaN')
                    else:
                        if pspiral > 0.5:
                            try:
                                spirals.add(subject)
                                spiralcount += 1
                            except:
                                print subject.metadata
                                raise Exception('stop the upload at spiral')
                        if pbar > 0.5:
                            try:
                                bars.add(subject)
                                counter += 1
                            except:
                                print subject.metadata
                                raise Exception('stop the upload at bar')
                except:
                    failfile.write(row['MANGAID'].decode('utf-8') + '\n')
                    
                log.write(row['MANGAID'].decode('utf-8') + '\n')