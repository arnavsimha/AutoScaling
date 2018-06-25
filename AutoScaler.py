import sys
import ruamel.yaml

instances_desired = 0 #from scaleUp/scaleDown function
yaml = ruamel.yaml.YAML()
# yaml.preserve_quotes = True
with open('dev-creds-newcert.yaml') as fp:
    data = yaml.load(fp)
for elem in data:
    if elem['name'] == 'info':
         elem['externalWorkerInstances'] = instances_desired
         break  # no need to iterate further
yaml.dump(data, sys.stdout)
