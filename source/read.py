import helper as hlp


def get_file_lines(input_file, line_delimiter):
    list_of_lines = []
    with open(input_file) as f:
        input_text = f.read()
    if lines_delimiter in input_text:
        list_of_lines = input_text.split(lines_delimiter)
    else:
        list_of_lines = [input_text]
    return list_of_lines



class vfile:
    def __init__(self,db,filepath):
        self.db = db
        self.filepath = filepath
        self.comment = False
        self.line = ''

    def remove_whitespaces():
        whitepaces = [' ', '/n', '/t']
        for whitespace in whitespaces:
            self.line = self.line.replace(whitespace,'')

    def end_comment_block():
        if '*/' in self.line:
            self.comment = False
            return True
        else:
            return False

    def is_comment():
        if '//' in self.line:
            return True
        elsif '/*' in self.line:
            self.comment = True
            return True
        else:
            return False

    def is_input():
        if 'input' in self.line:
            return True
        else:
            return False

    def is_output():
        if 'output' in self.line:
            return True
        else:
            return False

    def is_instance():
        return False

    def get_intput_name():
        

    def process_line():
        self.remove_whitespaces()
        if self.is_input():
            return get_input_name()
        elsif self.is_output():
            return get_output_name()
        else self.is_instance():
            return get_instance_name()

    def add_line_to_db(line):
        if self.comment:
            if end_comment_block(line):
                return False
        else:
            if is_comment(line):
                return False
            else:
                process_line(line)
                return True

    def populate_db():
        lines = get_file_lines(self.filepath)
        for line in lines:
            self.line = line
            add_line_to_db(line)


def rm_white_spaces(line):
    white_spaces = [' ', '\n', '\t']
    for each in white_spaces:
        line = line.replace(each,'')
    return line


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


