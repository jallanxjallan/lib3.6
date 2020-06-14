from ruamel.yaml import YAML
from ruamel.yaml.compat import StringIO


yaml = YAML()
yaml.explicit_start = True
yaml.explicit_end = True
yaml.default_flow_style = False


def dump_yaml(data):
    stream = StringIO()
    yaml.dump(data, stream)
    stream.seek(0)
    return stream.read()
