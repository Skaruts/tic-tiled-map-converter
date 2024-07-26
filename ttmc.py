#!/usr/bin/env python3

import sys
import os
import xmltodict
# import json  # for debugging

VERSION = "0.02b"

# TODO:
#   optionally care about layer visibility in order to ignore layers
#   account for when no tileset file exists yet


#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=
#       OS / helper stuff
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=
CWD = os.getcwd()
def file_exists(fname): return os.path.exists(os.path.join(CWD, fname))
def path_exists(path): return os.path.exists(path)
def __ERROR(msg):
	print(f'error: {msg}')
	sys.exit(1)
def check_file(filename):
	if not file_exists(filename):
		__ERROR(f"couldn't find file '{filename}'. \n")
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=

IGNORE_SYMBOL = "tt_ignore"
IGNORE_VALUE = 1
TMX = ".tmx"
MAP = ".map"
TSX = ".tsx"
TILESET="tiles.tsx"



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
	map_data = [0 for i in range(240*136)]

	with open(src_fname, 'r') as f:
		layers = []
		xml = xmltodict.parse(f.read())
		# print(json.dumps(xml, indent=4))

		if not isinstance(xml["map"]["layer"], list):
			layers.append(xml["map"]["layer"])
		else:
			for l in xml["map"]["layer"]:
				layers.append(l)

		# collect tile data from layers
		layer_data = []
		for l in layers:
			if check_ignored_flag(l): continue
			data = l["data"]
			encoding = data["@encoding"]
			if encoding != "csv":
				__ERROR(f"invalid Tile Layer Format: '{encoding}' (only 'CSV' is supported for now) \n")
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


def map_to_tmx(src_fname, dest_fname):
	map_data = []
	with open(src_fname, 'rb') as f:
		map_str = f.read()
		map_data = list(map_str)

	for i in range(len(map_data)):
		map_data[i] = str(map_data[i]+1)

	with open(dest_fname, 'w') as file:
		file.write(""\
			+  '<?xml version="1.0" encoding="UTF-8"?>\n'\
			+  '<map version="1.8" tiledversion="1.8.4" orientation="orthogonal" renderorder="right-down" width="240" height="136" tilewidth="8" tileheight="8" infinite="0" nextlayerid="2" nextobjectid="1">\n'\
			+ f' <tileset firstgid="1" source="{TILESET}"/>\n'\
			+  ' <layer id="1" name="Tile Layer 1" width="240" height="136">\n'\
			+  '   <data encoding="csv">\n'\
			+ ", ".join(map_data) + '\n'\
			+  '   </data>\n'\
			+  ' </layer>\n'\
			+  '</map>'
		)


USAGE = f"Usage:\n    ttmc [-ts:<tileset[{TSX}]>] <source_file[{MAP}|{TMX}]> <dest_file[{TMX}|{MAP}]>"
def no_args():
	print(f"\n\tTic-Tiled Map Converter {VERSION}\n\n{USAGE}")


def handle_tileset(arg):
	global TILESET
	filename = arg[arg.find(':')+1:]
	basename, ext = os.path.splitext(filename)

	if not ext:
		filename += TSX
	elif ext != TSX:
		__ERROR(f"invalid tileset extension '{ext}' \n")

	# create tileset if it doesn't exist
	if not file_exists(filename):
		with open(filename, 'w') as file:
			file.write(""\
				+  '<?xml version="1.0" encoding="UTF-8"?>\n'\
				+ f'<tileset version="1.8" tiledversion="1.8.4" name="{basename}" tilewidth="8" tileheight="8" tilecount="256" columns="16">\n'\
				+ f' <image source="{basename}.png" width="128" height="128"/>\n'\
				+  '</tileset>\n'
			)
		print(f"created tileset: '{filename}'")

	TILESET = filename


def convert(ext, src_fname, dest_fname):
	print(f"converting from '{src_fname}' to '{dest_fname}'...")
	if   ext == TMX: tmx_to_map(src_fname, dest_fname)
	elif ext == MAP: map_to_tmx(src_fname, dest_fname)
	print(f"\n'{dest_fname}' done.")


def main(argc, argv):
	if argc == 1:
		return no_args()

	src_filename  = None # argv[1]
	dest_filename = None # argv[2]

	for i in range(1, argc):
		arg = argv[i]
		if arg.startswith('-'):
			if arg == "-v":
				print(f"\n\tTic-Tiled Map Converter {VERSION}\n")
				return
			elif arg.startswith("-ts"):
				handle_tileset(arg)
		else:
			if   not src_filename:  src_filename  = arg
			elif not dest_filename: dest_filename = arg

	src_basename, src_ext = os.path.splitext(src_filename)
	if not dest_filename:
		dest_filename = src_basename

	dest_ext = os.path.splitext(dest_filename)[1]
	if not dest_ext:
		if src_ext == TMX:
			dest_filename += MAP
			dest_ext = MAP
		elif src_ext == MAP:
			dest_filename += TMX
			dest_ext = TMX

	if not ((src_ext == MAP and dest_ext == TMX) or (src_ext == TMX and dest_ext == MAP)):
		__ERROR("invalid file extensions \n")

	check_file(src_filename)
	convert(src_ext, src_filename, dest_filename)



#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=
if __name__ == '__main__':
	main(len(sys.argv), sys.argv)
