import sys
import os
import xmltodict
# import json  # for debugging

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
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=

VERSION = 0.01

IGNORE_SYMBOL = "tt_ignore"
IGNORE_VALUE = 1
TMX = ".tmx"
MAP = ".map"

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

	xml = ""\
		+'<?xml version="1.0" encoding="UTF-8"?>\n'\
		+'<map version="1.8" tiledversion="1.8.4" orientation="orthogonal" renderorder="right-down" width="240" height="136" tilewidth="8" tileheight="8" infinite="0" nextlayerid="2" nextobjectid="1">\n'\
		+' <tileset firstgid="1" source="tiles.tsx"/>\n'\
		+' <layer id="1" name="Tile Layer 1" width="240" height="136">\n'\
		+'   <data encoding="csv">\n'\
		+ ', '.join(map_data) + '\n'\
		+'   </data>\n'\
		+' </layer>\n'\
		+'</map>'

	with open(dest_fname, 'w') as file:
		file.write(xml)


def no_args():
	print(f"\n\tTicTiled {VERSION}\n\nUsage:\n    tictiled <source_file[{MAP}|{TMX}]> <dest_file[{TMX}|{MAP}]>")



def main(argc, argv):
	if argc == 1:
		no_args()
		return

	src_fname  = None # argv[1]
	dest_fname = None # argv[2]

	for i in range(1, argc):
		a = argv[i]
		if a.startswith('-'):
			if a == "-v":
				print(f"\n\tTicTiled {VERSION}\n")
				return
		else:
			if   not src_fname: src_fname = a
			elif not dest_fname: dest_fname = a

	# print(src_fname, dest_fname)

	(sname, sext) = os.path.splitext(src_fname)
	if not dest_fname: dest_fname = sname

	# print(sname, sext)
	(dname, dext) = os.path.splitext(dest_fname)
	if not dext:
		if sext == TMX:
			dest_fname += MAP
			dext = MAP
		elif sext == MAP:
			dest_fname += TMX
			dext = TMX

	# print(src_fname, dest_fname)

	if not ((sext == MAP and dext == TMX) or (sext == TMX and dext == MAP)):
		__ERROR("invalid file extensions \n")

	if not file_exists(src_fname):
		__ERROR(f"couldn't load file '{src_fname}'. \n")

	print(f"converting from '{src_fname}' to '{dest_fname}'...")

	if   sext == TMX: tmx_to_map(src_fname, dest_fname)
	elif sext == MAP: map_to_tmx(src_fname, dest_fname)

	print(f"\n'{dest_fname}' done.")


#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=
if __name__ == '__main__':
	main(len(sys.argv), sys.argv)
