import helper as hlp
import re


class vline:
    def __init__(self, line):
        self.line = line

    def strip_whitespaces(self):
        return re.sub('\s+', ' ', self.line).strip()

    def remove_whitespaces(self, string):
        whitespaces = ['\n','\t',' ']
        for whitespace in whitespaces:
            string = string.replace(whitespace, '')
        return string

    def print_line(self):
        print self.line

    def is_input(self):
        if 'input ' in self.line:
            return True
        elif 'input[' in self.line:
            return True
        else:
            return False

    def is_output(self):
        if 'output ' in self.line:
            return True
        elif 'output[' in self.line:
            return True
        else:
            return False

    def is_submodule(self):
        if '(' in self.line:
            module_instance = self.line.split('(')[0]
            if ' ' in module_instance:
                module_instance = module_instance.split(' ')
                if len(module_instance) is 2:
                    return True

    def is_module(self):
        if 'module ' in self.line:
            if 'endmodule' not in self.line:
                return True

    def get_inputname(self):
        input_name = self.line.split('input')[1]
        if ']' in input_name:
            input_name = input_name.split(']')[1]
        if ')' in input_name:
            input_name= input_name.split(')')[0]
        return self.remove_whitespaces(input_name)

    def get_outputname(self):
        output_name = self.line.split('output')[1]
        if ']' in output_name:
            output_name = output_name.split(']')[1]
        if ')' in output_name:
            output_name = output_name.split(')')[0]
        return self.remove_whitespaces(output_name)

    def get_submodule(self):
        instance = self.line.split('(')[0].split(' ')[1]
        module = self.line.split('(')[0].split(' ')[0]
        return {'instance':self.remove_whitespaces(instance), 'module':self.remove_whitespaces(module)}

    def get_modulename(self):
        return self.remove_whitespaces(self.line.split('module ')[1].split('(')[0])


class vfile:
    def __init__(self, filepath):
        self.filetext = hlp.get_text(filepath)
        self.input = []
        self.output = []
        self.submodules = {}
        self.modulename = None

    def remove_comments(self):
        self.filetext = hlp.remove_delimited_ss(self.filetext, start='//', end='\n')
        self.filetext = hlp.remove_delimited_ss(self.filetext, start='/*', end='*/')

    def get_lines(self):
        lines = []
        if ';' in self.filetext:
            semicolon_sep = self.filetext.split(';')
        else:
            semicolon_sep = [self.filetext]
        for each in semicolon_sep:
            if ',' in each:
                lines.extend(each.split(','))
            else:
                lines.append(each)
        return lines

        return self.remove_whitespaces(self.filetext.split('module ')[1].split('(')[0])

    def process_file(self):
        self.remove_comments()
        lines = self.get_lines()
        for each in lines:
            line = vline(each)
            line.strip_whitespaces()
            if line.is_input():
                self.input.append(line.get_inputname())
            elif line.is_output():
                self.output.append(line.get_outputname())
            elif line.is_submodule():
                self.submodules[line.get_submodule()['instance']] = line.get_submodule()['module']
            elif line.is_module():
                self.modulename = line.get_modulename()

    def print_inputs(self):
        for input_ in self.input:
            print input_

    def print_outputs(self):
        for output_ in self.output:
            print output_

    def print_submodules(self):
        for entry in self.submodules.keys():
            print "%s  ---> %s" (entry,self.submodules[entry])


class database:
    def __init__(self):
        self.design = {}
        self.last_module = None

    def add_module(self, module):
        if module in self.design.keys():
            hlp.error(custom_msg='Trying to add duplicate module in database - "%s"' % (module))
        else:
            self.design[module] = {'inputs':[], 'outputs':[], 'submodules':{}}
            self.last_module = module

    def add_input(self, port, module=None):
        if module is None:
            module = self.last_module
        # Not checking for duplicate ports - for performance
        self.design[module]['inputs'].append(port)

    def add_output(self, port, module=None):
        if module is None:
            module = self.last_module
        # Not checking for duplicate ports - for performance
        self.design[module]['outputs'].append(port)

    def add_submodule(self, submodule, instance, module=None):
        if module is None:
            module = self.last_module
        # Not checking for duplicate instance - for performance
        self.design[module]['submodules'][instance] = submodule
        self.last_module = submodule
        self.add_module(submodule)

    def get_inputs(self, module=None):
        if module is None:
            if self.last_module is None:
                hlp.error(custom_msg='No module added in database yet!', fatal=False)
                return None
            else:
                module = self.last_module
        return self.design[module]['inputs']

    def print_inputs(self, module=None):
        all_inputs = self.get_inputs(module)
        print "Inputs of module: %s" %module
        for port in all_inputs:
            print port
        hlp.print_new_line()

    def get_outputs(self, module=None):
        if module is None:
            if self.last_module is None:
                hlp.error(custom_msg='No module added in database yet!', fatal=False)
                return None
            else:
                module = self.last_module
        return self.design[module]['outputs']

    def print_outputs(self, module=None):
        all_outputs = self.get_outputs(module)
        print "Outputs of module: %s" %module
        for port in all_outputs:
            print port
        hlp.print_new_line()

    def get_submodules(self, module=None):
        if module is None:
            if self.last_module is None:
                hlp.error(custom_msg='No module added in database yet!', fatal=False)
                return None
            else:
                module = self.last_module
        return self.design[module]['submodules']

    def print_submodules(self, module=None):
        submodules = self.get_submodules(module)
        print "For module: %s" %module
        print " Instance   --->   Submodule"
        for instance in submodules.keys():
            print " %s   --->   %s " %(instance, submodules[instance])
        hlp.print_new_line()

