import datetime
import glob
import os
from dateutil.relativedelta import relativedelta
from jinja2 import Environment, FileSystemLoader

def get_current_time():
    return str(datetime.datetime.now() + relativedelta(years=1))

def get_jinja_environment(template_path):
    return Environment(loader=FileSystemLoader(template_path))

def get_jinja_template(environment, type):
    return environment.get_template(f'{type}.yml')

def get_template_paths():
    return glob.glob(f'{os.path.dirname(__file__)}/*.yml')

def get_template(key):
    """go do the things"""
    jinja_env = get_jinja_environment(template_dir)
    jinja_template = get_jinja_template(jinja_env, key)
    jinja_template.globals['now'] = datetime.datetime.utcnow
    return jinja_template

def render_template(monitor_config, monitor_template):
    monitor = monitor_template.render(monitor_config=monitor_config)
    return monitor

template_dir = f'{os.path.dirname(__file__)}/'
template_paths = get_template_paths()

templates = {}
for path in template_paths:
    key = path.split('/')[-1].split('.')[0]
    templates[key] = get_template(key)
