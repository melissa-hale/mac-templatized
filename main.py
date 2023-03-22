import subprocess
import sys
import os
import shutil

import src.monitor_templates as monitor_templates
import src.config

cmd_str = f"""
    MCD_DEFAULT_API_TOKEN=
    MCD_DEFAULT_API_ID=
    montecarlo validate
    montecarlo monitors apply --namespace dev --dry-run
"""

if __name__ == '__main__':

    templates = monitor_templates.get_templates()
    
    template_target = sys.argv[1]
    use_case_template_vars = src.config.get_use_case_template_vars(template_target)

    data_source = sys.argv[2]
    source_vars = src.config.get_source_vars(data_source)

    monitors = monitor_templates.build_monitors(use_case_template_vars, source_vars)

    with open('monitors.yml', "a") as output:
        output.write('montecarlo:' + '\n')
        for monitor_type, monitor_config_list in monitors.items():
            output.write(f'  {monitor_type}:' + '\n')
            for monitor_config in monitor_config_list:
                monitor = monitor_templates.render_template(monitor_config, templates[monitor_type])
                output.write(monitor + '\n')

    # result = subprocess.run(cmd_str, shell=True)
    os.remove('monitors.yml')
    # shutil.rmtree('target')
    print('done')