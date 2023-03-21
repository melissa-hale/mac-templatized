import subprocess
import os
import yaml
import sys

import src.monitors as monitors

cmd_str = f""" pwd
    ls
    MCD_DEFAULT_API_TOKEN=hq8MHzu_6mOEsWdf8-LzrJ8sXojesJ0rAlshrl2jauni21mycxyfSWaK
    MCD_DEFAULT_API_ID=df17f270b0c0497ca86f034a6758c199
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