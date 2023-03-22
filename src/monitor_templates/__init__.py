import datetime
import glob
import os
from dateutil.relativedelta import relativedelta
from jinja2 import Environment, FileSystemLoader

def get_current_time_plus_one_year():
    return str(datetime.datetime.now() + relativedelta(years=1))

def get_jinja_environment(template_path):
    return Environment(loader=FileSystemLoader(template_path))

def get_jinja_template(environment, type):
    return environment.get_template(f'{type}.yml')

def get_template_paths():
    return glob.glob(f'{os.path.dirname(__file__)}/*.yml')

def get_template(template_name):
    """ Builds a jinja env and returns a template """
    template_dir = f'{os.path.dirname(__file__)}/'
    jinja_env = get_jinja_environment(template_dir)
    jinja_template = get_jinja_template(jinja_env, template_name)
    jinja_template.globals['now'] = get_current_time_plus_one_year()
    return jinja_template

def render_template(monitor_config, monitor_template):
    """ Renders the yaml using the template """
    monitor = monitor_template.render(monitor_config=monitor_config)
    return monitor

def get_templates():
    template_paths = get_template_paths()
    templates = {}
    for path in template_paths:
        template_name = path.split('/')[-1].split('.')[0]
        templates[template_name] = get_template(template_name)

    return templates

def build_monitors(use_case_template_vars, source_vars):
    monitors = {}

    for db, db_config in source_vars.items():
        for schema, table_list in db_config.items():
            for table_object in table_list:
                table = table_object['table']
                for option, option_vars in table_object['options'].items():
                    # print(option)
                    if use_case_template_vars.get(option):
                        # print(option)
                        default_vars_for_use_case = use_case_template_vars[option] ## use case config / needs to merge with defaults
                        # print(default_vars_for_use_case) # this is the block from the use_cases/use_case.yml
                        use_case_base_type = default_vars_for_use_case["base_type"]
                        if use_case_template_vars.get("defaults"):
                            default_vars_for_base_use_case_template = use_case_template_vars.get("defaults")
                            ## default_vars_for_base_use_case_template is the block from base/default.yml
                            if default_vars_for_base_use_case_template.get(use_case_base_type):
                                default_vars_for_base_type = default_vars_for_base_use_case_template[use_case_base_type]

                        # else: what if no use_case_template_vars.get(defaults)
                        monitor_config = {}
                        monitor_config["project"] = db
                        monitor_config["schema"] = schema
                        monitor_config["table"] = table

                        ## first add the most important (what is defined in the datasource.yml (user configured))
                        for table_option in option_vars:
                            monitor_config = monitor_config | table_option

                        ## then add the second imporant (what is defined in the use case yml (use case admin configured))
                        for key, val in default_vars_for_use_case.items():
                            if monitor_config.get(key):
                                continue
                            else:
                                monitor_config[key] = val

                        ## then add the second imporant (what is defined in the default.yml of the use_case pkg (pkg admin configured))
                        for key, val in default_vars_for_base_type.items():
                            if monitor_config.get(key):
                                continue
                            else:
                                monitor_config[key] = val

                        # print(monitor_config)

                        if monitors.get(use_case_base_type):
                            monitors[use_case_base_type].append(monitor_config)
                        else:
                            monitors[use_case_base_type] = [monitor_config]

    return monitors