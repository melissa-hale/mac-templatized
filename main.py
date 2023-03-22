import subprocess
import os
import yaml
import sys

## this will get the templates ready
import src.monitor_templates as monitor_templates
import src.config

cmd_str = f""" pwd
    ls
    MCD_DEFAULT_API_TOKEN=hq8MHzu_6mOEsWdf8-LzrJ8sXojesJ0rAlshrl2jauni21mycxyfSWaK
    MCD_DEFAULT_API_ID=df17f270b0c0497ca86f034a6758c199
    montecarlo validate
    montecarlo monitors apply --namespace dev --dry-run
"""

# def construct_monitor_config():
#     return {

#     }

if __name__ == '__main__':
    
    template_target = sys.argv[1]
    ## for each of the sources passed into main,
    use_case_template_vars = src.config.get_use_case_template_vars(template_target)
    # print(use_case_template_vars)

    data_source = sys.argv[2]
    source_vars = src.config.get_source_vars(data_source)
    # print(source_vars)

    # print(monitor_templates.templates)

    for db, db_config in source_vars.items():
        # print(db)
        # print(db_config)
        for schema, table_list in db_config.items():
            # print(schema)
            # print(table_list)
            for table_object in table_list:
                # print(table_object)
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
                                ## default vars for base type is the block within defaults but specific to the base_type
                        

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
                        monitor = monitor_templates.render_template(monitor_config, monitor_templates.templates[use_case_base_type])
                        
                        # with open('monitors.yml', "a") as output:
                        #     output.write(monitor + '\n')


                    # else:
                        #no template

                            # monitor_config = default_vars_for_use_case | default_vars_for_base_type
                            # monitor_config["project"] = db
                            # monitor_config["schema"] = schema
                            # monitor_config["table"] = table
                            # print(monitor_config)
                            # print(monitor_config)
                            # monitor = monitor_templates.render_template(monitor_config, monitor_templates.templates[use_case_base_type])
                            # print(monitor)

    result = subprocess.run(cmd_str, shell=True)
    ## cleanup the monitors.yml
    # os.remove('monitors.yml')
    print('done')


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