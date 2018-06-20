# Parser for sucking in Command Line Options
# CLI: parser -o <output_filename> -top <top_module_name> -i <space separated input files>

import argparse
import helper as hlp
import os.path


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

# Arguments accepted.
