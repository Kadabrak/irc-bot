def read_file(file):
    with open(file, 'r') as text_read:
        help_file_content = text_read.readlines()
    return help_file_content
