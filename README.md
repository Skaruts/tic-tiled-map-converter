# TicTiled map converter

A simple python script for converting maps between Tiled and TIC-80. 

Depends on [xmltodict](https://github.com/martinblech/xmltodict#ok-how-do-i-get-it).

Current version: `0.02`





## Usage


### Converting

Call the script with the file names in the appropriate order, to convert from TIC-80 to Tiled or from Tiled to TIC-80. 

```
tictiled foo.map derp.tmx

tictiled derp.tmx foo.map
```

The output file name and extension are optional. If a file name isn't given, then TicTiled will use the same name as the source file. 
If the extension is omitted, it will be inferred. 


### Tilesets

When converting to `.tmx`, TicTiled will use a default tileset `tiles.tsx`. If you want to specify your own tileset, you can use the `-ts` parameter (cannot contain spaces):

`-ts:<tileset_name>`

Example:

```
tictiled -ts:my_tileset.tsx foo.map derp.tmx
```

The tileset file extension can be omitted. If the tileset doesn't exist, TicTiled will create a new one, and it will attach the tileset to a `.png` image with the same name (it won't check if the image exists). 

It doesn't matter if the `-ts` parameter comes before or after the filenames. This will work too:

```
tictiled foo.map derp.tmx -ts:my_tileset
```





## Notes

The `Tile Layer Format` must be set to `CSV` (you can set it in the map properties). 

Empty tiles are converted to `0`.

You can use `Tile Layers` in your maps. They are merged down when converting to TIC-80. All other layer types and groups are ignored.

If you need a layer to be ignored by TicTiled, you can do it either by adding the layer to a group, or by adding a custom property (string or int) to the layer: `tt_ignore = 1`.




