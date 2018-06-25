import yaml

#set function to get bosh worker info
def get_account_info():

    api_url = '{0}account'.format(api_url_base)

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None

#print yaml file
def read_file():
    with open("example.yaml", 'r') as stream:
            try:
                YML = yaml.load(stream)
            except yaml.YAMLError as exc:
                print(exc)
#iterate through Yaml file
from ruamel.yaml import YAML

yaml = YAML()
input_file = 'dev-creds-newcert.yml'

for key, value in YML.items():
    print(str(key))



#search 
