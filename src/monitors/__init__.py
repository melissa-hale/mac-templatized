import src.config as config
import src.helpers as helpers

config = config.get_config('snowflake')

monitors = {}
for db, tables in config["dbs"].items():
    # print(db)
    #monitor_config={} <-- start adding all the stuff you pass into reolve_vars
    for table, monitor_options in tables.items():
        # print(table)
        # print(monitor_options)
        for sev, monitor_types in monitor_options['monitors'].items():
            # print(sev)
            # print(monitor_types)
            for monitor_type in monitor_types:
                monitor = helpers.resolve_vars_in_template(config["source"], 
                                                            db, 
                                                            monitor_options['schema'], 
                                                            table, 
                                                            sev, 
                                                            monitor_type, 
                                                            monitor_options['timestampField'])
                if monitors.get(monitor_type):
                    monitors[monitor_type].append(monitor[monitor_type][0])
                else:
                    monitors[monitor_type] = monitor[monitor_type]
