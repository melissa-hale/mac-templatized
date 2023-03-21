### receive a config, identify which template to use, update variables with config
import yaml
import datetime
from dateutil.relativedelta import relativedelta

def construct_template_path(source, sev, type):
    return f'./src/monitors/{source}/templates/{sev}/{type}.yml'

def get_current_time():
    return str(datetime.datetime.now() + relativedelta(years=1))



def resolve_vars_in_template(source, db, schema, table, sev, type, timestamp):
    """ resolves vars in appropriate template and returns the json """
    template_path = construct_template_path(source, sev, type)
    
    with open(template_path, 'r') as template_file:
        template = yaml.safe_load(template_file)

    #### i need to make all of this better ####
    ## update table name
    template[type][0].update(table=f'{db}:{schema}.{table}')
    
    ## update monitor name
    template[type][0]["name"] = f'{sev} monitoring for {type} on {table}'

    ## update startime if a schedule block exists
    if template[type][0].get("schedule"):
        template[type][0]["schedule"].update({"start_time":get_current_time()})

    ## update timestamp if timstamp field exists
    if template[type][0].get("timestamp_field"):
        template[type][0].update({"timestamp_field":timestamp})

    return template