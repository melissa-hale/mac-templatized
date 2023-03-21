import subprocess
import os
import yaml
import sys

import src.monitors as monitors

cmd_str = f""" pwd
    ls
    MCD_DEFAULT_API_TOKEN=
    MCD_DEFAULT_API_ID=
    montecarlo validate
    montecarlo monitors apply --namespace dev --dry-run
"""

if __name__ == '__main__':
    print('done')
    # with open('monitors.yml', 'w') as yml:
    #     yaml.dump({"montecarlo": monitors.monitors}, yml)
    # result = subprocess.run(cmd_str, shell=True)
    # ## cleanup the monitors.yml
    # os.remove('monitors.yml')
    # print('done')