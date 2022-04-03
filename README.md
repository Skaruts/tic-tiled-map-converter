# Tic-Tiled Map Converter

A simple python script for converting maps between Tiled and TIC-80. 

Depends on [xmltodict](https://github.com/martinblech/xmltodict#ok-how-do-i-get-it).

Current version: `0.02`





## Usage


### Converting

Call the script with the file names in the appropriate order, to convert from TIC-80 to Tiled or from Tiled to TIC-80. 

```
python3 ttmc foo.map derp.tmx

python3 ttmc derp.tmx foo.map
```
(On some systems you may be able to omit `python3` and call scripts directly, as in `ttmc derp.tmx foo.map`.)

The output file name and extension are optional. If a file name isn't provided, then it will be given the same name as the source file. 
If the extension is omitted, it will be inferred. 


### Tilesets

When converting to `.tmx`, a default tileset `tiles.tsx` will be attached to the resulting `.tmx` file. If you want to specify your own tileset, you can use the `-ts` parameter (cannot contain spaces):

`-ts:<tileset_name>`

Example:

```
python3 ttmc -ts:my_tileset.tsx foo.map derp.tmx
```

The tileset file extension can be omitted. 

If the tileset doesn't exist, a new one will be created, and it will be given a `.png` image with the same name (won't check if the image exists). 

It doesn't matter if the `-ts` parameter comes before or after the filenames. This will work too:

```
python3 ttmc foo.map derp.tmx -ts:my_tileset
```





## Notes

- You can use `Tile Layers` in your maps. They are merged down when converting to TIC-80. All other layer types and groups are ignored.
- The `Tile Layer Format` must be set to `CSV` (you can set it in the map properties). 
- Empty tiles are converted to `0` (from `.map` to `.tmx`).
- If you need a layer to be ignored during the conversion process, you can do it either by adding the layer to a group, or by adding a custom property (string or int) to the layer: `tt_ignore = 1`.




