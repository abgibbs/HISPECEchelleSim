import datetime
import os
from glob import glob
from astropy.io import fits
import astropy.units as u
import numpy as np

class ObsEnvironment():
    '''
    A wrapper class to generate realistic headers on simulation data
    '''
    def __init__(self, instrument, path, inTime=None, inDate=None):
        '''
        This class needs the psisim instrument (hopefully with an associated telescope).
        Inputs:
        instrument: typically will just be the HISPEC instrument from psisim, but it could work with others
        path: the data output path, where fits files will be saved
        inTime: (optional) a string of the simulated time of observation
        inDate: (optional) a string of the simulated date of observation
        '''
        self.instrument = instrument
        self.telescope = self.instrument.telescope
           
        self.outpath = path
        
        if inTime is not None:
            if isinstance(intime, str):
                self.timeUT = intime
            else:
                print('intime should be a string of UT time. {} given'.format(type(intime)))
                raise ValueError
        
        if inDate is not None:
            if isinstance(indate, str):
                self.date = indate
            else:
                print('indate should be a string of UT time. {} given'.format(type(indate)))
                raise ValueError
    
    def get_time(self):
        '''
        When making an observation, need to record the time. 
        Returns the UT time unless specified
        
        UT_time: should be a string
        '''
        if hasattr(self, 'timeUT'): #If the time is specified in the environment
            return self.timeUT
        else: #otherwise give the current time in UT
            daytime = datetime.datetime.utcnow()
            return str(daytime.time())
        
    def get_date(self):
        '''
        Returns today's date unless specified
        DATE-OBS: should be a string
        '''
        if hasattr(self, 'date'): #If the time is specified in the environment
            return self.date
        else: #otherwise give the current time in UT
            daytime = datetime.datetime.utcnow()
            return str(daytime.date())
        
    
        
    def generate_header(self, start_header, fnum = 1, targ = 'test', sep=0.0):
        '''
        fnum gets passed in from the function that is doing the file saving
        
        The KPIC pipeline works with keywords in the data headers. We need the keys:
        'FRAMENUM': frame number that gets turned into 'FILENUM' in KPIC dataframes
        'DATE-OBS': observation UT date, gets turned into 'UTDATE' in KPIC dataframes
        'UT': observation time, gets turned into 'UTTIME'
        'TRUITIME': exposure time
        'EL': elevation on the sky of the observation
        'FIUGNM': the science frame number (for here, same as fnum)?, gets turned into 'SFNUM'
        'FIUDSEP': amount offset from the central star
        'FIUDAR': differential atmospheric refraction, gets turned into 'DAR'
        'AIRMASS': airmass at observation. Can be found from elevation
        'FILTER': filter used for observation
        'FIUGCNAM': gets turned into 'CORONAGRAPH', either VFN, MDA, or none
        'ECHLPOS': echelle position? isn't needed for HISPEC
        'DISPPOS': disperser position? isn't needed for HISPEC
        'TARGNAME': name of the planet, star, disk that is observed. 
        
        Inputs:
        
        dataout: a fits object that was only made with data, no other real header to speak of
        telescope: a psisim (or similar) telescope object, will get folded into env
        '''
        new_header = start_header.__deepcopy__() #use a deep copy to make sure no accidents
        new_header['UT'] = self.get_time()
        new_header['DATE-OBS'] = self.get_date()
        
        # The instrument should have these parameters
        new_header['TRUITIME'] = self.instrument.exposure_time.to(u.s).to_string()[:-2] #exposure time is astropy
        new_header['FILTER'] = self.instrument.current_filter
        new_header['FIUCGNAM'] = self.instrument.mode #Is supposed to be coronagraph, just a placeholder for now
        
        # The function calling this should know the file naming situation
        new_header['FRAMENUM'] = fnum 
        new_header['FIUGNM'] = fnum
        new_header['TARGNAME'] = targ
        new_header['FIUDSEP'] = sep #placeholder, need to decide on separation
        #new_header['FIUDSEP'] = self.instrument.separation #for future closer to real implementation
        
        # Set of things to pull from the state of the telescope
        loc_am = self.telescope.airmass
        new_header['AIRMASS'] = loc_am
        
        #TODO: I'm just using airmass = sec(zenith_angle). Not great approximation for high airmass
        zen_ang = 180*np.arccos(1/loc_am)/np.pi #Give it in degrees
        new_header['EL'] = 90 - zen_ang #elevation is angle from ground
        
        #Something about DAR, differential atmospheric refraction
        new_header['FIUDAR'] = zen_ang #I'm not sure, but when it's airmass=1.2, DAR is about 30
        
        
        
        # Needed for the KPIC Pipeline that won't be relevant to HISPEC
        new_header['ECHLPOS'] = 65 #looking for a number but it doesn't matter
        new_header['DISPPOS'] = 35
        
        # Info not needed for the KPIC pipeline, but I'm including because I think it'll be nice
        new_header['INST'] = self.instrument.name
        new_header['OBSMODE'] = self.instrument.mode
        #new_header['PYDICHROIC'] = self.instrument.pywfs_pickoff #for the future, in the FEI
        #new_header['TCDICHROIC'] = self.instrument.tc_pickoff
        
        return new_header
    
    def save_with_header(self, data, save_name='Headed_data.fits'):
        '''
        data: 2D ndarray of the data to be saved
        env: variable/class that keeps track of the
        save_name: string of the filename to get saved to. Must change environment outpath to change directory
                    '.fits' isn't Necessary in save_name, but it's nice to be explicit
        '''
        dataout = fits.PrimaryHDU(data) #primaryHDU is not an HDUList
        
        #Need to find the file the number and tack it on
        numberer = 0
        target = save_name.split('.')[0] #please for the love of god only have one '.' in the save_name
        for fullname in glob(os.path.join(self.outpath, "*.fits")):
            if target == os.path.basename(fullname).split('.')[0][:-4]:
                numberer+=1
        
        fnumber = str(int(numberer))
        numzeros = 3-len(fnumber) #BEWARE if you save more than 1000 of the same filename
        real_save = target+'_'+'0'*numzeros+fnumber+'.fits'
        
        dataout.header = self.generate_header(dataout.header, fnum=int(fnumber), 
                                              targ = target, sep=0.0)
        dataout.writeto(os.path.join(self.outpath, real_save), overwrite = True)
