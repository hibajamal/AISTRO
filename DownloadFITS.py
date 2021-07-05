import glob
import os
import shutil
from subprocess import call
import sys

#####################################################

n1, n2 = sys.argv[1], sys.argv[2]

try:
	getLefts = sys.argv[3]
	assert getLefts == "i", "Parameter to specify downloading of interrupted files is \'i\'"

	# run find left overs:
	call("python Lib/findLeftOvers.py" + n1 + " " + n2)
	getLefts = True
except:
	getLefts = False


nums = n1 + '-' + n2
print(nums)

if not getLefts:
	# DOWNLOAD THE FILES
	FILENAME = nums + '/' + nums + '.txt'
else:
	# incase of exception
	FILENAME = nums + "/" + "leftovers-" + nums + ".txt"

call(["mkdir", nums + "/collected"])

call(["rsync", "-avzL", "--files-from="+ FILENAME, "rsync://data.sdss.org/dr9", nums + "/dr9"])


##########################################################
# MOVE ALL FILES FROM dr9 FOLDER TO ONE LOCATION

original = nums + '/'

files = glob.glob(original + 'dr9/**/*.bz2', recursive=True)
print(len(files))
destination = original + 'collected/'

for opath in files:
	try:
	    shutil.move(opath, destination)
	except:
		print("File already exists. Deleting...")
		os.remove(opath)

##########################################################
# extract all the .bz2 files

'''for filename in os.listdir(original+'collected/'):
	# this will delete initial bz2 file and only keep extracted versions
	call(["bzip2", "-d", original+"collected/"+filename]) '''