# Parser for sucking in Command Line Options
# CLI: parser -o <output_filename> -top <top_module_name> -i <space separated input files>

import argparse
import helper as hlp
import os.path
import read as rd
import yaml


# Parser
parser = argparse.ArgumentParser(description='Generate visio based block diagram from the Verilog / SystemVerilog code')
parser.add_argument('-o',   action='store', dest='output_filename',  help='Output visio filename')
parser.add_argument('-top', action='store', dest='design_top',       help='Design top')
parser.add_argument('-i',   action='store', dest='input_filelist',     nargs='*', help='Input files separated by whitespace')
args = parser.parse_args()


# Check arguments
if args.output_filename is None:
    hlp.error(ertype='usage')
if args.design_top is None:
    hlp.error(ertype='usage')
if args.input_filelist is None:
    hlp.error(ertype='usage')

# Check if output already exists
if os.path.isfile(args.output_filename):
    overwrite = hlp.get_bool_input(msg='File %s already exists! Want to overwrite?' % (args.output_filename))
    if overwrite is False:
        hlp.error()

# Check if all inputs exist
for input_file in args.input_filelist:
    if not os.path.isfile(input_file):
        hlp.error(custom_msg='Input file %s not found!' % (input_file))

# Read all files and populate the database
db = rd.database()

for input_file in args.input_filelist:
    parseFile = rd.vfile(input_file)
    parseFile.process_file()
    module = parseFile.modulename
    db.add_module(module)
    for each_input in parseFile.inputs:
        db.add_input(each_input)
    for each_output in parseFile.outputs:
        db.add_output(each_output)
    for instance in parseFile.submodules:
        submodule = parseFile.submodules[instance]
        db.add_submodule(submodule,instance)

with open("design_db.yaml", 'w') as f:
    yaml.dump(db.design, f, default_flow_style=False)

