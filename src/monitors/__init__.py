import src.config as config
import src.helpers as helpers
import sys

def get_source_config(source):
    return config.get_config(f'{source}')

def write_monitors_to_file(sources):
    print(sources)
    for source in sources:
        source_config = get_source_config(source)
        for db, tables in source_config["dbs"].items():
            monitor_config={"db":db, "source":source}
            for table, monitor_options in tables.items():
                monitor_config["table"] = table
                for sev, monitor_types in monitor_options['monitors'].items():
                    monitor_config["sev"] = sev
                    for monitor_type in monitor_types:
                        monitor_config["monitor_type"] = monitor_type
                        print(monitor_config)
                        monitor = helpers.resolve_vars_in_template(monitor_config)
                        print(monitor)
                        ## write to a file in a folder called "generated"?

write_monitors_to_file(sys.argv[1:])