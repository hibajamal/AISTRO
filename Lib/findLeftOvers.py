import glob
import sys
import os

n1, n2 = sys.argv[1], sys.argv[2]

nums = n1 + '-' + n2
print(nums)

origin = open(nums + "/" + nums + ".txt", "r")

if os.path.isfile(nums + "/" + "leftovers-" + nums + ".txt"):
	os.remove(nums + "/" + "leftovers-" + nums + ".txt")

write_to = open(nums + "/" + "leftovers-" + nums + ".txt", "x")

ogs = []

for line in origin.readlines():
	ogs.append(line.strip())

origin.close()

opath = nums + '/'
#path_get = "dr9/"
path_get = "collected/"

files = glob.glob( opath + path_get + '**/*.bz2', recursive=True)
print(len(files))

# compare which are missing

# if we are to retrieve from collected/
#'''
ogs_comp = [i[32:] for i in ogs]
files_comp = [i[24:] for i in files]

for i in range(len(ogs_comp)):
	if ogs_comp[i] not in files_comp:
		write_to.write(ogs[i] + "\n")
#'''

write_to.close()