import argparse
import json
import re

param_list = ['name', 'action', 'nargs', 'const', 'default',
              'type', 'choices', 'required', 'help', 'metavar', 
              'dest']

def filter_variable_name(arg_name):
    filter_regex = '-'
    return re.sub(filter_regex, '', arg_name)

def codegen_arg(arg):
    if not isinstance(arg, dict):
       raise TypeError('each argument should be a json object ({})') 

    arg_name = arg['name']
    parser_arg_str = f"parser.add_argument('{arg_name}'"
    for k, v in arg.items():
        if k == 'name': continue

        if k not in param_list:
            raise ValueError(f"argument {k} is not valid! Should be one of: "
                             f"{param_list}")

        if isinstance(v, str):
            parser_arg_str += f", {k}='{v}'"
        else: 
            parser_arg_str += f", {k}={v}"

    parser_arg_str += ')'

    # for now just create a variable assignment
    run_arg_str = f"{filter_variable_name(arg_name)}="
    return parser_arg_str, run_arg_str, arg_name

def codegen(arguments):
    # file initialization
    parser_code_str = "import argparse\n\ndef parse_args():\n"
    parser_code_str += "\tparser = argparse.ArgumentParser()\n"

    run_code_str = "#!/bin/bash\n\n"

    # file bodies
    name_list = []
    for arg in arguments:
        parser_arg_str, run_arg_str, name = codegen_arg(arg)
        name_list.append(name)

        parser_code_str += f"\t{parser_arg_str}\n"
        run_code_str += f"{run_arg_str}\n"

    run_code_str += "\npython3 train.py"
    for name in name_list:
        run_code_str += f" {name} ${{{filter_variable_name(name)}}}"
    return parser_code_str, run_code_str 

def main(args):
    json_path = args.json[0]

    with open(json_path) as h:
        arguments = json.loads(h.read())

    if not isinstance(arguments, list):
       raise TypeError('json file should contain a list of args ([])') 
    
    parser_code, run_code = codegen(arguments)
    with open(args.out_name, "w") as out_file:
        out_file.write(parser_code)

    with open("run.sh", "w") as out_file:
        out_file.write(run_code)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('json', nargs=1,
                        help='path to json file with all the args')
    parser.add_argument('--out_name', default='argparse.py',
                        help='path to the output file')
    args = parser.parse_args()
    main(args)
