import pandas as pd
import numpy as np
import cv2
import math
from scipy import ndimage

import astropy
from astropy.io import fits
from astropy.wcs import WCS
from astropy.visualization import make_lupton_rgb

from subprocess import call
import sys
import os
import shutil
import glob
import time

from Galaxy import Galaxy

class Image(Galaxy):
	def __init__(self, ra=0, dec=0, files=[]):
		self.ra, self.dec = ra, dec
		self.u, self.g, self.r, self.i, self.z = None, None, None, None, None
		self.datacube = None
		
		if len(files) == 5:
			self.u, self.g, self.r, self.i, self.z = files
		elif len(files) == 4:
			self.u, self.g, self.r, self.i = files
		elif len(files) == 3:
			self.u, self.g, self.r = files
		elif len(files) == 2:
			self.u, self.g = files
		else:
			self.u = files[0]
			
		self.u_processed = None
		self.g_processed = None
		self.r_processed = None
		self.i_processed = None
		self.z_processed = None

		self.mapping = {"u": self.u, "g": self.g, "r": self.r, "i":self.i, "z": self.z}

	def GetRGBComposite(self):
		if self.i == None or self.r == None or self.g == None:
			raise ValueError("Please define all i, r, and g frames.")

		self.i_processed = self.Get2DFrame(self.i) if self.i_processed == None else self.i_processed
		self.r_processed = self.Get2DFrame(self.r) if self.r_processed == None else self.r_processed
		self.g_processed = self.Get2DFrame(self.g) if self.g_processed == None else self.g_processed

		return make_lupton_rgb(self.i_processed, self.r_processed, self.g_processed, stretch=1.0, Q=5)

	def GetDataCube(self):
		if self.u == None or self.z == None or self.i == None or self.r == None or self.g == None:
			raise ValueError("Please define all u, g, r, i, z frames.")

		call(["mkdir", "processed"])

		self.u_processed = Get2DFrame(self.u, self.ra, self.dec) if self.u_processed != None else self.u_processed
		self.g_processed = Get2DFrame(self.g, self.ra, self.dec) if self.g_processed != None else self.g_processed
		self.r_processed = Get2DFrame(self.r, self.ra, self.dec) if self.r_processed != None else self.r_processed
		self.i_processed = Get2DFrame(self.i, self.ra, self.dec) if self.i_processed != None else self.i_processed
		self.z_processed = Get2DFrame(self.z, self.ra, self.dec) if self.z_processed != None else self.z_processed

		data = np.ones((64, 64, 5))
		data[:,:,0] = self.u_processed
		data[:,:,1] = self.g_processed
		data[:,:,2] = self.r_processed
		data[:,:,3] = self.i_processed
		data[:,:,4] = self.z_processed

		self.datacube = data

		return self.datacube

	def Get2DFrame(self, filename):
		'''
		string: channel name
		'''
		# create a directory to save processed files
		call(["mkdir", "processed"])
		# run swarp     
		
		call(["swarp", filename + "[0]", "-SUBTRACT_BACK", "N", "-RESAMPLING_TYPE", "LANCZOS3", "-IMAGEOUT_NAME", "processed/" + filename])
		
		img = self.crop_and_center("processed/" + filename, self.ra, self.dec)
		
		os.remove("processed/" + filename)
		return img

	def crop_and_center(self, frame_path, ra, dec, scale=32, rotate=False):
	    hdu = fits.open(frame_path)[0]
	    img = hdu.data
	    wcs = WCS(hdu.header)
	    
	    x, y = wcs.wcs_world2pix(float(ra), float(dec), 1)
	    x, y = int(x), int(y)
	    img_ = img[y - scale:y + scale, x - scale:x + scale]
	    
	    if rotate:
	        hdr = astropy.io.fits.getheader(frame_path)
	        cd1_1,cd1_2,cd2_1,cd2_2 = hdr['CD1_1'],hdr['CD1_2'],hdr['CD2_1'],hdr['CD2_2'] 
	        rot = math.degrees(math.atan2(math.radians(cd2_1), math.radians(cd1_1))) 
	        img_ = ndimage.rotate(img_, rot)
	    
	    return img_ 
