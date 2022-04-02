import sys
import os
import xmltodict
import json

# TODO:
#   optionally care about layer visibility
#   convert map -> tmx
#   consider asking about overwriting 'dest_file'?

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=
#       OS / helper stuff
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=
CWD = os.getcwd()
def file_exists(fname): return os.path.exists(os.path.join(CWD, fname))
def path_exists(path): return os.path.exists(path)
def __ERROR(msg):
	print(f'error: {msg}')
	sys.exit(1)
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=

IGNORE_SYMBOL = "tt_ignore"
IGNORE_VALUE = 1

def check_ignored_flag(layer):
	if not "properties" in layer: return False
	props = layer["properties"]["property"]
	if not isinstance(props, list):
		if props["@name"] == IGNORE_SYMBOL:
			return int(props["@value"]) == IGNORE_VALUE
	else:
		for p in props:
			if p["@name"] == IGNORE_SYMBOL:
				return int(p["@value"]) == IGNORE_VALUE
	return False


def convert(src_file, dest_file):
	print(f"converting '{src_file}' to '{dest_file}'...")

	src_ext  = os.path.splitext(src_file)[1]
	dest_ext = os.path.splitext(dest_file)[1]

	if src_ext == ".tmx":
		map_data = [0 for i in range(240*136)]

		with open(src_file, 'r') as f:
			layers = []
			xml = xmltodict.parse(f.read())
			# print(json.dumps(xml, indent=4))

			# print( isinstance(xml["map"]["layer"], list) )
			if not isinstance(xml["map"]["layer"], list):
				layers.append(xml["map"]["layer"])
			else:
				for l in xml["map"]["layer"]:
					layers.append(l)

			# collect tile data from layers
			layer_data = []
			for l in layers:
				ignored = check_ignored_flag(l)
				if not ignored:
					data = l["data"]
					encoding = data["@encoding"]
					if encoding != "csv":
						__ERROR(f"invalid Tile Layer Format: '{encoding}' (only 'CSV' is supported for now) \n")
					# print("ignored: ", ignored)
					layer_data.append(data["#text"].replace('\n', '').split(','))

			# merge down layers
			for ld in layer_data:
				for i in range(len(ld)):
					val = int(ld[i])-1
					if val >= 0:
						map_data[i] = val

		with open(dest_file, 'wb') as file:
			for n in map_data:
				file.write(n.to_bytes(1, byteorder='big', signed=False))
	# elif src_ext == ".map"
		# TODO

	print(f"\n'{dest_file}' done.")

def main(argc, argv):
	# print("argv[0]: ", argv[0])

	if argc <= 2:
		__ERROR("invalid file names\n\n    Usage: tictiled <source_file[.map|.tmx]> <dest_file[.tmx|.map]>\n")

	src_fname = argv[1]
	dest_fname = argv[2]

	if not (
	           ( src_fname.endswith(".map") and dest_fname.endswith(".tmx") )\
	        or ( src_fname.endswith(".tmx") and dest_fname.endswith(".map") )\
	       ):
		__ERROR("invalid file extensions \n")

	if not file_exists(src_fname):
		__ERROR(f"couldn't load file '{src_fname}'. \n")

	# if file_exists(dest_fname):
		# TODO: bother asking about overwriting? (add '-y' parameter for skipping it)

	convert(src_fname, dest_fname)




#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=
if __name__ == '__main__':
	main(len(sys.argv), sys.argv)
