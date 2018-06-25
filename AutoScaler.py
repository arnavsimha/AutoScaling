import sys
import ruamel.yaml

instances_desired = 0 #from scaleUp/scaleDown function
yaml = ruamel.yaml.YAML()
# yaml.preserve_quotes = True
with open('dev-creds-newcert.yml') as fp:
    data = yaml.load(fp)
for elem in data:
    if elem['name'] == 'info':
         elem['externalWorkerInstances'] = instances_desired
         break  # no need to iterate further
yaml.dump(data, sys.stdout)


#alternative implementation
"""
with open("dev-creds-newcert.yml") as f:
     list_doc = yaml.load(f)

for sense in list_doc:
    if sense["name"] == "info":
         sense["externalWorkerInstances"] = instances_desired

with open("dev-creds-newcert.yml", "w") as f:
    yaml.dump(list_doc, f)
"""
