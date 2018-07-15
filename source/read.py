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
                    if 'module' not in module_instance[0]:
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
        self.inputs = []
        self.outputs = []
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

    def process_file(self):
        self.remove_comments()
        lines = self.get_lines()
        for each in lines:
            line = vline(each)
            line.strip_whitespaces()
            if line.is_module():
                self.modulename = line.get_modulename()
            if line.is_input():
                self.inputs.append(line.get_inputname())
            elif line.is_output():
                self.outputs.append(line.get_outputname())
            elif line.is_submodule():
                self.submodules[line.get_submodule()['instance']] = line.get_submodule()['module']

    def print_inputs(self):
        for input_ in self.inputs:
            print input_

    def print_outputs(self):
        for output_ in self.outputs:
            print output_

    def print_submodules(self):
        for entry in self.submodules.keys():
            print "%s  ---> %s" (entry,self.submodules[entry])

