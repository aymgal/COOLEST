import os
import yaml
import json
import jsonpickle


DEFAULT_EXCLUDE_KEYS = [
    'description',
    'id',
    'latex_str',
    'units',
    'fixed',
    'definition_range',
]


class APISerializer(object):

    def __init__(self,
                 file_path_no_ext: str, 
                 obj: object = None, 
                 indent: int = 2) -> None:
        self.obj = obj
        self.path = file_path_no_ext
        self.indent = indent
        # to distinguish files that can be converted back to the python API
        self._api_suffix = '_pyAPI'

    def json_dump_simple(self, exclude_keys=None):
        if exclude_keys is None:
            exclude_keys = DEFAULT_EXCLUDE_KEYS
        json_path = self.path + '.json'
        result = jsonpickle.encode(self.obj, indent=self.indent)
        with open(json_path, 'w') as f:
            f.write(self.obj.to_JSON(indent=self.indent, exclude_keys=exclude_keys))
        return result

    def json_dump(self):
        json_path = self.path + self._api_suffix + '.json'
        result = jsonpickle.encode(self.obj, indent=self.indent)
        with open(json_path, 'w') as f:
            f.write(result)
        return result

    def yaml_dump(self):
        yaml_path = self.path + self._api_suffix + '.yaml'
        with open(yaml_path, 'w') as f:
            result = yaml.dump(self.obj, f, indent=self.indent,
                               sort_keys=False, default_flow_style=False)
        return result

    def json_load(self):
        json_path = self.path + self._api_suffix + '.json'
        with open(json_path, 'r') as f:
            content = jsonpickle.decode(f.read())
        return content

    def yaml_load(self):
        yaml_path = self.path + self._api_suffix + '.yaml'
        with open(yaml_path, 'r') as f:
            content = yaml.load(f, Loader=yaml.Loader)
        return content

    def dump_yaml_to_json(self):
        yaml_path = self.path + self._api_suffix + '.yaml'
        json_path = self.path + self._api_suffix + '.json'
        def _any_constructor(loader, tag_suffix, node):
            """https://stackoverflow.com/questions/52240554/how-to-parse-yaml-using-pyyaml-if-there-are-within-the-yaml"""
            if isinstance(node, yaml.MappingNode):
                return loader.construct_mapping(node)
            if isinstance(node, yaml.SequenceNode):
                return loader.construct_sequence(node)
            return loader.construct_scalar(node)
        yaml.add_multi_constructor('', _any_constructor, Loader=yaml.SafeLoader)
        if not os.path.exists(yaml_path):
            raise ValueError(f"YAML file {yaml_path} does not exist (did you call yaml_dump()?)")
        with open(yaml_path, 'r') as f:
            content = yaml.safe_load(f)
        with open(json_path, 'w') as f:
            result = json.dump(content, f, indent=self.indent)
        return result
        