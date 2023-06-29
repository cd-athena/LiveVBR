# Command Line Options

## Input/Output

- `--input <filename>`

	Input filename. Raw YUV or Y4M supported.

- `--inputres <wxh>`

	Source picture size [w x h].
	
- `--output <filename>`

	Input filename. CSV supported. 

## Bitrate ladder generator Configuration

- `--minbr <integer>` 

	Minimum bitrate supported by the streaming service provider.
	
- `--codec <codec-name>` 

	Name of the encoder/codec employed.

- `--maxbr <integer>` 

	Maximum bitrate supported by the streaming service provider.

- `--jnd <integer>`
 
	Target average VMAF difference between the bitrate ladder representations.
