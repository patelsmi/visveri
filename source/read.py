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

    def print_inputs(self, module=None):
        if module is None:
            if self.last_module is None:
                hlp.error(custom_msg='No module added in database yet!', fatal=False)
                return 1
            else:
                module = self.last_module
        print "Inputs of module: %s" %module
        for port in self.design[module]['inputs']:
            print port
        hlp.print_new_line()

    def print_outputs(self, module=None):
        if module is None:
            if self.last_module is None:
                hlp.error(custom_msg='No module added in database yet!', fatal=False)
                return 1
            else:
                module = self.last_module
        print "Outputs of module: %s" %module
        for port in self.design[module]['outputs']:
            print port
        hlp.print_new_line()

    def print_submodules(self, module=None):
        if module is None:
            if self.last_module is None:
                hlp.error(custom_msg='No module added in database yet!', fatal=False)
                return 1
            else:
                module = self.last_module
        print "For module: %s" %module
        print " Instance   --->   Submodule"
        for instance in self.design[module]['submodules'].keys():
            print " %s   --->   %s " %(instance, self.design[module]['submodules'][instance])
        hlp.print_new_line()


