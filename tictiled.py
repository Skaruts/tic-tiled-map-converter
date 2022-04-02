import sys
import os
import xmltodict
# import json  # for debugging

# TODO:
#   optionally care about layer visibility in order to ignore layers
#   account for when no tileset file exists yet
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


def tmx_to_map(src_fname, dest_fname):
	print(f"converting from '{src_fname}' to '{dest_fname}'...")
	map_data = [0 for i in range(240*136)]

	with open(src_fname, 'r') as f:
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

	with open(dest_fname, 'wb') as file:
		for n in map_data:
			file.write(n.to_bytes(1, byteorder='big', signed=False))

	print(f"\n'{dest_fname}' done.")


def map_to_tmx(src_fname, dest_fname):
	print(f"converting from '{src_fname}' to '{dest_fname}'...")
	map_data = []
	with open(src_fname, 'rb') as f:
		map_str = f.read()
		map_data = list(map_str)

	for i in range(len(map_data)):
		map_data[i] = str(map_data[i]+1)

	xml = ""\
		+'<?xml version="1.0" encoding="UTF-8"?>\n'\
		+'<map version="1.8" tiledversion="1.8.4" orientation="orthogonal" renderorder="right-down" width="240" height="136" tilewidth="8" tileheight="8" infinite="0" nextlayerid="4" nextobjectid="1">\n'\
		+' <tileset firstgid="1" source="mini_tiles.tsx"/>\n'\
		+' <layer id="1" name="Tile Layer 1" width="240" height="136">\n'\
		+'   <data encoding="csv">\n'\
		+ ', '.join(map_data) + '\n'\
		+'   </data>\n'\
		+' </layer>\n'\
		+'</map>'

	with open(dest_fname, 'w') as file:
		file.write(xml)

	print(f"\n'{dest_fname}' done.")


def ask_user(msg):
	while True:
		inpt = input(msg)
		if inpt in ['y', 'Y', 'yes', 'yup', 'yoh', 'yeah', 'yea', 'da', 'ya', 'si', 'sim', 'hai', 'yeah yeah yeah', 'sure', 'of course']:
			return True
		if inpt in ['n', 'N', 'no', 'nope', 'nah', 'nop', 'newp', 'NO', 'niet', 'nein', 'não', 'nao', 'bo', 'wait no!', 'fu', 'under my dead body!', ]:
			return False


def main(argc, argv):
	# print("argv[0]: ", argv[0])

	if argc == 1:
		__ERROR("invalid file names\n\n    Usage: tictiled <source_file[.map|.tmx]> <dest_file[.tmx|.map]>\n")

	src_fname = argv[1]
	dest_fname = argv[2]

	if not (   (src_fname.endswith(".map") and dest_fname.endswith(".tmx"))\
	        or (src_fname.endswith(".tmx") and dest_fname.endswith(".map"))  ):
		__ERROR("invalid file extensions \n")

	if not file_exists(src_fname):
		__ERROR(f"couldn't load file '{src_fname}'. \n")

	if file_exists(dest_fname):
		# TODO: bother asking about overwriting? (add '-y' parameter for skipping it)
		if not ask_user(f"file {dest_fname} exists: you want to overwrite it? "):
			return

	src_ext  = os.path.splitext(src_fname)[1]
	dest_ext = os.path.splitext(dest_fname)[1]

	if src_ext == ".tmx":
		tmx_to_map(src_fname, dest_fname)
	elif src_ext == ".map":
		map_to_tmx(src_fname, dest_fname)




#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=
if __name__ == '__main__':
	main(len(sys.argv), sys.argv)
