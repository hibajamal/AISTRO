import numpy as np 
import tensorflow as tf 
from Image import Image
from Galaxy import Galaxy

class Model:
	def __init__(self, filename=""):
		self.filename = filename
		self.model = tf.keras.models.load_model(self.filename) if len(filename) > 0 else None
		self.PhotoNet = tf.keras.models.load_model('FakeModel.h5')

	def GetRedshift(self, datacube, model="default"): # model can be default or set
		# if no model is specified, use default model
		model = self.AistroNet if model == "default" else self.model

		redshift = model.predict(datacube.reshape(1, 64, 64, 5))[0,0]

		return redshift 

	def Train(self, X, y_csv, epochs, batch_size, redshifts):
		# number of epochs, batch size, an npy file for training data, and a csv file of redshifts as labels for training data
		return 

	def FineTune(self, X, y_csv, model, epochs, batch_size):
		# "--data", "--model", "--epochs", "--batch_size", "--csv"

		new_model = tf.keras.models.load_model(model)
		y = csv2y(y_csv)
		x = np.load(X)

		new_model.fit(x, y, batch_size=batch_size, epochs=epochs)
		new_model.save(model[:-3] + "_fine_tuned.h5")

	def csv2y(self, csv):
		df = pd.read_csv(csv)
		v = list(df)[0] # assuming this is a csv with one column of only redshifts

		redshifts = []

		for i in range(len(df[v])):
			redshifts.append(df[v][i])

		return np.array(redshifts)