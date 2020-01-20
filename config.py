import yaml

def yaml_loader(filepath):
    with open(filepath, "r") as s:
        data = yaml.safe_load(s)
    return data

def yaml_dump(filepath, data):
    with open(filepath, "w") as s:
        yaml.dump(data, s)

def get(element):
    return yaml_loader("account.yml").get(element)