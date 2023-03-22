import subprocess
import os
import yaml
import sys

## this will get the templates ready
import src.monitor_templates as monitor_templates
import src.config

cmd_str = f""" pwd
    ls
    MCD_DEFAULT_API_TOKEN=
    MCD_DEFAULT_API_ID=
    montecarlo validate
    montecarlo monitors apply --namespace dev --dry-run
"""

# def construct_monitor_config():
#     return {

#     }

if __name__ == '__main__':
    print('done')
    
    template_target = sys.argv[1]
    ## for each of the sources passed into main,
    use_case_template_vars = src.config.get_use_case_template_vars(template_target)
    # print(use_case_template_vars)

    data_source = sys.argv[2]
    source_vars = src.config.get_source_vars(data_source)
    # print(source_vars)

    print(monitor_templates.templates)

    for db, db_config in source_vars.items():
        # print(db)
        # print(db_config)
        for schema, table_list in db_config.items():
            # print(schema)
            # print(table_list)
            for table_object in table_list:
                # print(table_object)
                table = table_object['table']
                for option in table_object['options']:
                    # print(option)
                    if use_case_template_vars.get(option):
                        # print(option)
                        use_case_vars = use_case_template_vars[option] ## use case config / needs to merge with defaults
                        # print(use_case_vars)
                        use_case_base_type = use_case_vars["base_type"]
                        if use_case_template_vars["defaults"].get(use_case_base_type):
                            default_vars_for_base_type = use_case_template_vars["defaults"][use_case_base_type]
                            monitor_config = use_case_vars | default_vars_for_base_type
                            monitor_config["project"] = db
                            monitor_config["schema"] = schema
                            monitor_config["table"] = table
                            monitor = monitor_templates.render_template(monitor_config, monitor_templates.templates[use_case_base_type])
                            print(monitor)


    ## first "configure" (get vars)
    ##### the output should be an array of monitor_config objects
    ## loop over the array, render the template and write to a file
    #### monitor_templates.render_template()

    # with open('monitors.yml', 'w') as yml:
    #     yaml.dump({"montecarlo": monitors.monitors}, yml)
    # result = subprocess.run(cmd_str, shell=True)
    # ## cleanup the monitors.yml
    # os.remove('monitors.yml')
    # print('done')