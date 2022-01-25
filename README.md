# argparse-codegen

Python package for creating a parser (using the argparse module of python) of input arguments and the corresponding .sh file for running the python script.
The arguments are provided as a json file.

## Install

```
cd conda-recipe
conda build . --output-folder path/to/build/folder
# in the build directory will be create the tar file: gen-parser-0.1-py38_1.tar.bz2
conda install --use-local gen-parser-0.1-py38_1.tar.bz2
```

## Usage

```
from genparser.codegen import parser_codegen
json_path = "path/to/arg.json"

parser_codgen(json_path, "path/to/output/argparser.py", "path/to/output/run.sh")
```

where arg.json:
```
[
    {
        "name": "--name",
        "help": "name of the model",
        "required": true
    },
    {
        "name": "--seed",
        "help": "seed for the rng",
        "default": 0
    }
]
```

### output: argparser.py and run.sh

argparser.py: 

```
import argparse

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('--name', help='name of the model', required=True)
	parser.add_argument('--seed', help='seed for the rng', default=0)

```

run.sh:

```
#!/bin/bash

name=
seed=

python3 train.py --name ${name} --seed ${seed} 
```
