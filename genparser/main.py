import argparse
import json
import re

param_list = ['name', 'action', 'nargs', 'const', 'default',
              'type', 'choices', 'required', 'help', 'metavar', 
              'dest']

header = "'''\n\nCode auto-generated using https://github.com/francescocastelli/argparse-codegen\n\n'''\n\n"

def filter_variable_name(arg_name):
    filter_regex = '-'
    return re.sub(filter_regex, '', arg_name)

def codegen_arg(arg):
    if not isinstance(arg, dict):
       raise TypeError('each argument should be a json object ({})') 

    arg_name = arg['name']
    parser_arg_str = f"parser.add_argument('{arg_name}'"
    for k, v in arg.items():
        if k not in param_list:
            raise ValueError(f"argument {k} is not valid! Should be one of: "
                             f"{param_list}")

        if k == 'name': continue

        # type for now doesn't work
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
    parser_code_str = header
    parser_code_str += "import argparse\n\ndef parse_args():\n"
    parser_code_str += "\tparser = argparse.ArgumentParser()\n"

    run_code_str = "#!/bin/bash\n\n"
    run_code_str += header

    # file bodies
    name_list = []
    for arg in arguments:
        parser_arg_str, run_arg_str, name = codegen_arg(arg)
        name_list.append(name)

        parser_code_str += f"\t{parser_arg_str}\n"
        run_code_str += f"{run_arg_str}\n"

    # file end
    run_code_str += "\npython3 train.py"
    for i, name in enumerate(name_list, 1):
        run_code_str += f" {name} ${{{filter_variable_name(name)}}}"
        if not i % 3: 
            run_code_str += " \\\n"
            run_code_str += "\t"*8


    return parser_code_str, run_code_str 

def main(args):
    json_path = args.json[0]

    with open(json_path) as h:
        arguments = json.loads(h.read())

    if not isinstance(arguments, list):
       raise TypeError('json file should contain a list of args ([])') 
    
    # codegen of the output files
    parser_code, run_code = codegen(arguments)

    with open(args.parser_name, "w") as out_file:
        out_file.write(parser_code)

    with open(args.run_name, "w") as out_file:
        out_file.write(run_code)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('json', nargs=1,
                        help='path to json file with all the args')
    parser.add_argument('--parser_name', default='argparser.py',
                        help='path to the output arg parser file')
    parser.add_argument('--run_name', default='run.sh',
                        help='path to the output run file')
    args = parser.parse_args()
    main(args)