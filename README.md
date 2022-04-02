# TicTiled map converter

A simple python script for converting maps between Tiled and TIC-80. Requires [xmltodict](https://github.com/martinblech/xmltodict).

### Usage

To convert from TIC-80 to Tiled

```
tictiled source_file.map dest_file.tmx
```

To convert from Tiled to TIC-80

```
tictiled source_file.tmx dest_file.map
```
### Notes

The `Tile Layer Format` must be set to `CSV` (you can set it in the map properties). 

Empty tiles will be converted to `0`.

Tile Layers can be used, and will be merged down when converting. TicTiled ignores all other layer types and groups.

If you need a layer to be ignored by TicTiled, you can do it either by adding the layer to a group, or by adding a custom property (string or int) to the layer: `tt_ignore = 1`.




