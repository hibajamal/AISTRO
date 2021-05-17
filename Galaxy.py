class Galaxy:
	def __init__(self, ra=0, dec=0, reddening=None, data=None, redshift=None):
		self.ra = ra
		self.dec = dec
		self.reddening = reddening
		self.datacube = data
		self.redshift = redshift

	

	def GetRedshift(self):
		return self.redshift