import sys
import numpy as np 
import os

from Image import Image
import Galaxy
from Model import Model

RECOGNIZED = ["-GETREDSHIFT", "-TRAIN", "-GET2DFRAMES", "-GETNPY", "-GETRGBCOMPOSITE",
				"-FINETUNE", "-VISUALIZEMODEL", "-VISUALIZELAYER", "--cdnts", "--files",
				"--data", "--model", "--epochs", "--batch_size", "--csv", "--folder"]

def GET2DFRAMES(parsed):

	valid_commands = [RECOGNIZED[8], RECOGNIZED[9]]

	if parsed[2][:2] != "--":
		raise ValueError("Misplaced or incorrect command, " + parsed[2])

	cmd_stack = []
	values = {"cdnts": [], "filenames": []}

	for i in range(2, len(parsed)):
		if parsed[i] not in valid_commands:

			if len(cmd_stack) > 0:

				if cmd_stack[-1][0] == valid_commands[0] and 0 <= cmd_stack[-1][1] < 2: # if cdnts has been invoked and cannot be more than 2 cdnts
					values["cdnts"].append(parsed[i])
					cmd_stack[-1][1] += 1

				elif cmd_stack[-1][0] == valid_commands[1] and 0 <= cmd_stack[-1][1] < 5: # if files has been invoked and less 
					values["filenames"].append(parsed[i])
					cmd_stack[-1][1] += 1

				else:
					raise ValueError("Misplaced or incorrect command for GET2DFRAMES, " + parsed[i]) 	

			else: # raise error if neither of the recognized commands have been invoked
				raise ValueError("Misplaced or incorrect command for GET2DFRAMES, " + parsed[i]) 

		elif parsed[i].lower() == valid_commands[0].lower(): # for cdnts
			cmd_stack.append([valid_commands[0], 0])

		elif parsed[i].lower() == valid_commands[1].lower(): # for files
			cmd_stack.append([valid_commands[1], 0])

	return values

def GETNPY(parsed):
	valid_commands = [RECOGNIZED[8], RECOGNIZED[9]]
	
	if parsed[2][:2] != "--":
		raise ValueError("Misplaced or incorrect command, " + parsed[2])
	
	cmd_stack = []
	values = {"cdnts": [], "filenames": []}
	
	for i in range(2, len(parsed)):
		if parsed[i] not in valid_commands:
		
			if len(cmd_stack) > 0:
			
				if cmd_stack[-1][0] == valid_commands[0] and 0 <= cmd_stack[-1][1] < 2: # if cdnts has been invoked and cannot be more than 2 cdnts
					values["cdnts"].append(parsed[i])
					cmd_stack[-1][1] += 1
					
				elif cmd_stack[-1][0] == valid_commands[1] and 0 <= cmd_stack[-1][1] < 5: # if files has been invoked and less 
					values["filenames"].append(parsed[i])
					cmd_stack[-1][1] += 1
				else:
					raise ValueError("Misplaced or incorrect command for GET2DFRAMES, " + parsed[i]) 
					
			else: # raise error if neither of the recognized commands have been invoked
				raise ValueError("Misplaced or incorrect command for GET2DFRAMES, " + parsed[i]) 
					
		elif parsed[i].lower() == valid_commands[0].lower(): # for cdnts
			cmd_stack.append([valid_commands[0], 0])

		elif parsed[i].lower() == valid_commands[1].lower(): # for files
			cmd_stack.append([valid_commands[1], 0])
	
	if cmd_stack[-1][0] == valid_commands[1] and cmd_stack[-1][1] < 5:
		raise ValueError("All five files must be given as input in the order u, g, r, i, z.") 
		
	return values
	
def GETRGBCOMPOSITE(parsed):
	valid_commands = [RECOGNIZED[8], RECOGNIZED[9]]
	
	if parsed[2][:2] != "--":
		raise ValueError("Misplaced or incorrect command, " + parsed[2])
	
	cmd_stack = []
	values = {"cdnts": [], "filenames": []}
	
	for i in range(2, len(parsed)):
		if parsed[i] not in valid_commands:
		
			if len(cmd_stack) > 0:
			
				if cmd_stack[-1][0] == valid_commands[0] and 0 <= cmd_stack[-1][1] < 2: # if cdnts has been invoked and cannot be more than 2 cdnts
					values["cdnts"].append(parsed[i])
					cmd_stack[-1][1] += 1
					
				elif cmd_stack[-1][0] == valid_commands[1] and 0 <= cmd_stack[-1][1] < 3: # if files has been invoked and less: g, r, i
					values["filenames"].append(parsed[i])
					cmd_stack[-1][1] += 1
				else:
					raise ValueError("Misplaced or incorrect command for GET2DFRAMES, " + parsed[i]) 
					
			else: # raise error if neither of the recognized commands have been invoked
				raise ValueError("Misplaced or incorrect command for GET2DFRAMES, " + parsed[i]) 
					
		elif parsed[i].lower() == valid_commands[0].lower(): # for cdnts
			cmd_stack.append([valid_commands[0], 0])

		elif parsed[i].lower() == valid_commands[1].lower(): # for files
			cmd_stack.append([valid_commands[1], 0])
	
	if cmd_stack[-1][1] < 3:
		raise ValueError("All five files must be given as input in the order u, g, r, i, z.") 
		
	return values

def GETREDSHIFT(parsed):
	valid_commands = [RECOGNIZED[10], RECOGNIZED[11]]

	if parsed[2][:2] != "--":
		raise ValueError("Misplaced or incorrect command, " + parsed[2])

	cmd_stack = []
	values = {"data": [], "model": []}
	
	for i in range(2, len(parsed)):
		if parsed[i] not in valid_commands:
		
			if len(cmd_stack) > 0:
			
				if cmd_stack[-1][0] == valid_commands[1] and 0 <= cmd_stack[-1][1] < 1: # if model has been invoked and cannot be more than once
					values["model"].append(parsed[i])
					cmd_stack[-1][1] += 1
					
				elif cmd_stack[-1][0] == valid_commands[0] and 0 <= cmd_stack[-1][1] < 1: # if data has been invoked and cannot be more than once
					values["data"].append(parsed[i])
					cmd_stack[-1][1] += 1
				else:
					raise ValueError("Misplaced or incorrect command for GETREDSHIFT, " + parsed[i]) 
					
			else: # raise error if neither of the recognized commands have been invoked
				raise ValueError("Misplaced or incorrect command for GETREDSHIFT, " + parsed[i]) 
					
		elif parsed[i].lower() == valid_commands[0].lower(): # for data
			cmd_stack.append([valid_commands[0], 0])

		elif parsed[i].lower() == valid_commands[1].lower(): # for model
			cmd_stack.append([valid_commands[1], 0])
		
	return values

def FINETUNE(parsed):
	# AISTRO -FINETUNE --model model.h5, --epochs 50, -batch\_size 16
	# "--data", "--model", "--epochs", "--batch_size", "--csv" 10, 11, 12, 13, 14
	valid_commands = [RECOGNIZED[10], RECOGNIZED[11], RECOGNIZED[12], RECOGNIZED[13], RECOGNIZED[14]]

	if parsed[2][:2] != "--":
		raise ValueError("Misplaced or incorrect command, " + parsed[2])

	cmd_stack = []
	values = {"model": [], "epochs": [], "batch_size": [], "data": [], "csv": []}

	for i in range(2, len(parsed)):
		if parsed[i] not in valid_commands:
		
			if len(cmd_stack) > 0:
			
				if cmd_stack[-1][0] == valid_commands[0] and 0 <= cmd_stack[-1][1] < 1: # if data has been invoked and cannot be more than once
					values["data"].append(parsed[i])
					cmd_stack[-1][1] += 1
					
				elif cmd_stack[-1][0] == valid_commands[1] and 0 <= cmd_stack[-1][1] < 1: # if model has been invoked and cannot be more than once
					values["model"].append(parsed[i])
					cmd_stack[-1][1] += 1

				elif cmd_stack[-1][0] == valid_commands[2] and 0 <= cmd_stack[-1][1] < 1: # if epochs has been invoked and cannot be more than once
					values["epochs"].append(parsed[i])
					cmd_stack[-1][1] += 1

				elif cmd_stack[-1][0] == valid_commands[3] and 0 <= cmd_stack[-1][1] < 1: # if batch_size has been invoked and cannot be more than once
					values["batch_size"].append(parsed[i])
					cmd_stack[-1][1] += 1

				elif cmd_stack[-1][0] == valid_commands[4] and 0 <= cmd_stack[-1][1] < 1: # if csv has been invoked and cannot be more than once
					values["csv"].append(parsed[i])
					cmd_stack[-1][1] += 1

				else:
					raise ValueError("Misplaced or incorrect command for FINETUNE, " + parsed[i]) 
					
			else: # raise error if neither of the recognized commands have been invoked
				raise ValueError("Misplaced or incorrect command for FINETUNE, " + parsed[i]) 
					
		elif parsed[i].lower() == valid_commands[0].lower(): # for data
			cmd_stack.append([valid_commands[0], 0])

		elif parsed[i].lower() == valid_commands[1].lower(): # for model
			cmd_stack.append([valid_commands[1], 0])

		elif parsed[i].lower() == valid_commands[2].lower(): # for epochs size
			cmd_stack.append([valid_commands[2], 0])

		elif parsed[i].lower() == valid_commands[3].lower(): # for batch_size size
			cmd_stack.append([valid_commands[3], 0])

		elif parsed[i].lower() == valid_commands[4].lower(): # for csv size
			cmd_stack.append([valid_commands[4], 0])
		
	return values

def BUNDLENPYS(parsed):
	# only the folder parameter
	valid_commands = [RECOGNIZED[15]]

	if parsed[2][:2] != "--":
		raise ValueError("Misplaced or incorrect command, " + parsed[2])

	cmd_stack = []
	values = {"folder": []}

	for i in range(2, len(parsed)):
		if parsed[i] not in valid_commands:
		
			if len(cmd_stack) > 0:
			
				if cmd_stack[-1][0] == valid_commands[0] and 0 <= cmd_stack[-1][1] < 1: # if folder has been invoked and cannot be more than once
					values["folder"].append(parsed[i])
					cmd_stack[-1][1] += 1

				else:
					raise ValueError("Misplaced or incorrect command for BUNDLENPYS, " + parsed[i]) 
					
			else: # raise error if neither of the recognized commands have been invoked
				raise ValueError("Misplaced or incorrect command for BUNDLENPYS, " + parsed[i]) 
					
		elif parsed[i].lower() == valid_commands[0].lower(): # for model
			cmd_stack.append([valid_commands[0], 0])

	# create the NPY:
	bundle = []
	folder = values["folder"][0]
	if folder[-1] != "/":
		folder += "/"

	for filename in os.listdir(folder):
		if filename[-4:] == ".npy":
			x = np.load(folder + filename)
			bundle = np.concatenate([bundle, [x]]) if len(bundle) > 0 else np.array([x])
		
	return bundle


def parse(string):
	''' purpose of this is to parse the command and separate all the elements 
	    separate criteria: space or comma: '''

	lst = [i if i.find(",")==0 else i.split(",") for i in string]
	lst1 = np.array([])

	for i in lst:
		lst1 = np.concatenate([lst1, i])

	return lst1[lst1 != ""] # removing all empty elements


if __name__ == "__main__":
	inp = sys.argv
	command = parse(inp)
	
	token = 0
	values = None
	
	if inp[1] == "-GET2DFRAMES":
		values = GET2DFRAMES(command)
		
	elif inp[1] == "-GETNPY":
		values = GETNPY(command)
		token = 1
		
	elif inp[1] == "-GETRGBCOMPOSITE":
		values = GETRGBCOMPOSITE(command)
		token = 2

	elif inp[1] == "-GETREDSHIFT":
		values = GETREDSHIFT(command)
		values["cdnts"] = (0, 0) # they are not needed so just adding for sake of non-repititive code
		token = 3

	elif inp[1] == "-BUNDLENPYS":
		bundle = BUNDLENPYS(command)
		np.save("data_bundle.npy", bundle)
		# no need to go further in the program:
		sys.exit("File for data created.")

	elif inp[1] == "-FINETUNE":
		# values = {"model": [], "epochs": [], "batch_size": [], "data": [], "csv": []}
		values = FINETUNE(command)
		model = Model()
		model.FineTune(X=values["data"], y_csv=values["csv"], model=values["model"], epochs=values["epochs"], batch_size=values["batch_size"])
		# no need to go further in the program:
		sys.exit("Finetuned model saved.")

	ra, dec = values["cdnts"]
	files = values["filenames"]
	
	if token == 2:
		# create fake u and z
		files = ["u"] + list(files) + ["z"]

	# does not matter if we assign a u filename to variable that is not u
	# we just need seperate frames to be saved
	image_obj = Image(ra=ra, dec=dec, files=files)
	
	if token == 0:
		for i in files:
			np.save("processed/" + i, image_obj.Get2DFrame(i))
			print("File saved at", "processed/" + i)
	
	elif token == 1:
		np.save("processed/DataCube", image_obj.GetDataCube())

	elif token == 2:
		np.save("processed/rgb_composite", image_obj.GetRGBComposite())

	elif token == 3:
		# read datacube first
		datacube = np.load(values["data"][0])
		if not datacube:
			raise ValueError("Please provide a valid NumPy file.")

		# if default model is to be invoked:
		if values["model"][0] == "default":
			model = Model()
			redshift = model.GetRedshift(datacube)
		else:
			model = Model(filename=values["model"][0])
			redshift = model.GetRedshift(datacube, "set")

		print("Redshift of given Galaxy is", redshift)
		
		
