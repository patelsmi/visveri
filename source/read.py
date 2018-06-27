import helper as hlp
import re


class vline:
    def __init__(self, line, comment):
        self.line = line

    def remove_whitspaces(self,custom=None):
        if curtom is None:
            return re.sub('\s+', ' ', self.line).strip()
        else:
            return re.sub('\s+', ' ', custom).strip()

    def print_line(self):
        print self.line

    def is_input(self):
        if any('input ', 'input[') in self.line:
            return True
        else:
            return False

    def is_output(self):
        if any('output ', 'output[') in self.line:
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

    def get_inputname(self):
        input_name = self.line.split('input')
        if ']' in input_name:
            input_name = input_name.split(']')[1]
        return self.remove_whitespaces(input_name)

    def get_outputname(self):
        output_name = self.line.split('output')
        if ']' in output_name:
            output_name = output_name.split(']')[1]
        return self.remove_whitespaces(output_name)

    def get_submodule(self):
        instance = self.line.split('(')[0].split(' ')[1]
        module = self.line.split('(')[0].split(' ')[0]
        return {'instance':instance, 'module':module}


class vfile:
    def __init__(self, filepath):
        self.filetext = hlp.get_text(filepath)
        self.input = []
        self.output = []
        self.submodules = {}

    def remove_comments(self):
        self.filetext = hlp.remove_delimited_ss(self.filetext, start='//', end='\n')
        self.filetext = hlp.remove_delimited_ss(self.filetext, start='/*', end='*/')

    def get_lines(self):
        if (';') in self.filetext:
            return self.filetext.split(';')
        else:
            return [self.filetext]

    def process_file(self):
        self.remove_comments()
        lines = self.get_lines()
        for each in lines:
            line = vline(each)
            line.remove_whitespaces()
            if line.is_input()
                self.input.append(line.get_inputname())
            elif line.is_output():
                self.output.append(name = line.get_outputname())
            elif line.is_submodule():
                self.submodules[line.get_submodule()['instance']] = line.get_submodule()['module']


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

