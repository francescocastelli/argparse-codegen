codegen for creating a parser (using the argparse module of python) of input arguments and the corresponding sh file for running the python script
The arguments are provided as a json file.

example: 

```
python3 main.py arg.json 
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

output: two files, argparser.py and run.sh

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
