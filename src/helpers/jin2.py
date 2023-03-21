import datetime
from dateutil.relativedelta import relativedelta
from jinja2 import Environment, FileSystemLoader

def construct_template_path(source, sev):
    return f'./src/monitors/{source}/templates/{sev}/'

def get_current_time():
    return str(datetime.datetime.now() + relativedelta(years=1))

def get_jinja_environment(template_path):
    return Environment(loader=FileSystemLoader(template_path))

def get_jinja_template(environment, type):
    return environment.get_template(f'{type}.yml')

def resolve_vars_in_template(monitor_config):
    """ resolves vars in appropriate template and returns the json """
    template_path = construct_template_path(monitor_config["source"], monitor_config["sev"])
    jinja_env = get_jinja_environment(template_path)
    jinja_template = get_jinja_template(jinja_env, monitor_config["monitor_type"])
    jinja_template.globals['now'] = datetime.datetime.utcnow

    monitor = jinja_template.render(monitor_config=monitor_config)

    return monitor

## monitor config: {'db': 'rentaldata2', 'source': 'snowflake', 'table': 'dim_listings_cleansed2', 'sev': 'sev0', 'monitor_type': 'freshness'}