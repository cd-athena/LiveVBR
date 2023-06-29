# Command Line Options

## Input/Output

- `--input <filename>`

	Input filename. Raw YUV or Y4M supported.

- `--input-res <wxh>`

	Source picture size [w x h].

## Bitrate ladder generator Configuration

- `--min-br <integer>` 

	Minimum bitrate supported by the streaming service provider.

- `--max-br <integer>` 

	Maximum bitrate supported by the streaming service provider.

- `--jnd <integer>`
 
	Target average VMAF difference between the bitrate ladder representations.
