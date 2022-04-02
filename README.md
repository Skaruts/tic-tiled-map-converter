# TicTiled map converter

A simple python script for converting maps between Tiled and TIC-80.

```
tictiled source_file.tmx dest_file.map
```
There are some limitations (for now):

- it only supports conversion from `.tmx` to `.map`
- it only supports `CSV` Tile Layer Format (you can set it in the map properties in Tiled)


Empty tiles are set to `0` when converting from `.tmx` to `.map`.

You can use layers in Tiled. The script will merge down all layers when converting from `.tmx` to `.map`.

If you need a layer to be ignored by Tictiled, you can do it in two ways:
 - add a custom property (string or int) to the layer: `tt_ignore = 1` 
 - put the layer in a group (groups are ignored by Tictiled)






