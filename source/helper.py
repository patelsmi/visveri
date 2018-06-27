import sys


def print_new_line():
    print ''


def get_attention():
    print "!!!!!!!!!!!!!!!!!!!!!!!!!!!"


def exit(status=0):
    sys.exit(status)


def error(ertype='custom', custom_msg='', fatal=True):
    error_map = {\
            'usage'  : 'Usage Error. See -h for correct usage.',\
            'custom' : custom_msg\
            }
    if ertype in error_map:
        print_new_line()
        get_attention()
        print  error_map[ertype]
    else:
        print "Helper Error! error called with invalid ertype..."
        exit()

    if fatal:
        print_new_line()
        exit()


def get_bool_input(msg=''):
    yes = ['y','ye','yes']
    no  = ['n','no']
    print_new_line()
    get_attention()
    print msg
    print "[Y/N]?"
    user_input = raw_input().lower()
    if user_input in yes:
        return True
    elif user_input in no:
        return False
    else:
        error(custom_msg='Invalid entry!')


def get_list_from_str(string, delim):
    return string.split(delim)


def remove_delimited_ss(string, start, end):
    split_string = string.split(start)
    delimited_string = split_string[0]
    if len(split_string) > 1:
        for segment in split_string[1:]:
            if '\n' in segment:
                delimited_string += ' ' + re.split(end, segment, maxsplit=1)[1]
    return delimited_string


def get_text(filepath):
    with open(filepath) as f:
        text = f.read()
    return text
