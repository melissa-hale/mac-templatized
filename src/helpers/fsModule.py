import glob

def construct_template_path(source, sev, type):
    return f'./src/monitors/{source}/templates/{sev}/{type}.yml'

def get_paths(dir):
    """ Returns an array of paths in a directory """
    return glob.glob(dir)

def get_files_from_path(path):
    """ Returns the files within a directory """
    return glob.glob(f'{path}/*')