# santoryu.py
A tool to splice one or multiple spritesheets into multiple single sprites

## How to use
First, git clone of course
Then, just launch the script like
```shell
py ./santoryu.py [filename | dirname] [parameters] [filename2 | dirname] [parameters2] ...
```
Each `filename` or `dirname` should have its `parameters` attached to it right after.

The `filename` or `dirname` is the path to the spritesheet. The `parameters` are the numbers of rows and columns of this specific spritesheet. It's formatted such: `x.y`. So for a spritesheet with 10 columns and 3 rows, the `parameters` will be: `10.3`

## Flags
You can use the `--help` flag to understand how this script works
```shell
py ./santoryu.py --help
```

Folders of your spliced sprites are created recursively: the created directory will be named like this: `santoryued_[filename]`.

If a folder `santoryued_[filename]` already exists, another one called `santoryued_[filename]_[index]` will be created.
