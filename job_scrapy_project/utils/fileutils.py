
def get_file_content(filename):
    _ = []
    with open(filename, 'a+') as f:
        f.seek(0)
        ls = f.readlines()
        for l in ls:
            _.append(l.strip())
    return _

def save_data_to_file(filename, data, m='a+'):
    with open(filename, m) as f:
        f.write(data.strip() + '\n')