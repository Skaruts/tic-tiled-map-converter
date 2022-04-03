# TicTiled map converter

A simple python script for converting maps between Tiled and TIC-80. 

Depends on [xmltodict](https://github.com/martinblech/xmltodict#ok-how-do-i-get-it).

### Usage

Call the script with the file names in the appropriate order, to convert from TIC-80 to Tiled or from Tiled to TIC-80. 

```
tictiled foo.map derp.tmx

tictiled derp.tmx foo.map
```

The output file name is optional. If one isn't given, then TicTiled will use the name of the source file. 
You can also omit the file extension for the output file. 


### Notes

The `Tile Layer Format` must be set to `CSV` (you can set it in the map properties). 

Empty tiles are converted to `0`.

You can use `Tile Layers` in your maps. They are merged down when converting to TIC-80. All other layer types and groups are ignored.

If you need a layer to be ignored by TicTiled, you can do it either by adding the layer to a group, or by adding a custom property (string or int) to the layer: `tt_ignore = 1`.




