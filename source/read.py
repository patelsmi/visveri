

def get_file_lines(input_file, line_delimiter):
    list_of_lines = []
    with open(input_file) as f:
        input_text = f.read()
    if lines_delimiter in input_text:
        list_of_lines = input_text.split(lines_delimiter)
    else:
        list_of_lines = [input_text]
    return list_of_lines

