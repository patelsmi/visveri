import helper as hlp
import re


def get_file_lines(input_file, line_delimiter):
    list_of_lines = []
    with open(input_file) as f:
        input_text = f.read()
    if lines_delimiter in input_text:
        list_of_lines = input_text.split(lines_delimiter)
    else:
        list_of_lines = [input_text]
    return list_of_lines


class vline:
    def __init__(self, line, comment):
        self.line = line
        self.comment = comment

    def remove_whitspaces(self,custom=None):
        if curtom is None:
            return re.sub('\s+', ' ', self.line).strip()
        else:
            return re.sub('\s+', ' ', custom).strip()

    def remove_comment(self):
        if self.comment:
            if '*/' in self.line:
                self.line = self.line.split('*/')[1]
                self.comment = False
            else:
                self.line = ''
                self.comment = True
        else:
            if '//' in string:
                self.line = self.line.split('//')[0]
                self.comment = False
            elif '/*' in string:
                non_comment = self.line.split('/*')[0]
                self.comment = True
                if '*/' in self.line.split('/*')[1]:
                    non_comment += self.line.split('/*')[1].split('*/')[1]
                    self.comment = False
                self.line = non_comment

    def print_line(self):
        print self.line

    def print_comment_status(self):
        print self.comment

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
        return {instance:module}


class vfile:
    def __init__(self,db,filepath):
        self.db = db
        self.filepath = filepath
        self.comment = False

    def process_file(self):
        lines = get_file_lines(self.filepath)
        for each in lines:
            line = vline(each,self.comment)
            line.remove_whitespaces()
            line.remove_comment()
            if line.is_input()
                name = line.get_inputname()
            elif line.is_output():
                name = line.get_outputname()
            elif line.is_submodule():
                entry = line.get_submodule()


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


