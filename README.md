# TJA Toolbox

### What's inside
* TJA to OSU Taiko Converter 
* OSU Taiko to TJA Converter (Forked from the original repo and needs testing)
* TJA Player Auto Performer

### TJA to OSU Taiko Converter
It takes the TJA file path as an argument, and print out the converted result.

`python .\tja2osu.py [TJA File Path]`

#### Test Results

| Song Name            | Notes                        | Result           |
|:--------------------:|:----------------------------:|:----------------:|
| 旋風ノ舞【地】       | Measure changes              | Passed           |
| 天妖ノ舞             | No change in BPM nor measure | Passed           |
| めたるぽりす         | Measure changes              | Pending for test |
| Purple Rose Fusion   | BPM changes                  | Pending for test |

#### Notes
1. The output OSU Taiko file will be in format v14;
2. TJA file with "#BRANCH" tag is not supported;
3. Website version of this converter will be implemented later.


### Reference
1. <a href="https://osu.ppy.sh/wiki/en/Client/File_formats/Osu_(file_format)" target="_blank">.osu (file format)</a> 
