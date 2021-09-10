import os
import yaml
import json


class HierarchyEncoder(object):

    def __init__(self,
                 obj: object, 
                 file_path_no_ext: str, 
                 indent: int = 2) -> None:
        setattr(self, obj.__class__.__name__, obj)
        self.path = file_path_no_ext
        self.indent = indent

    def yaml_dump(self):
        yaml_path = self.path + '.yaml'
        with open(yaml_path, 'w') as f:
            result = yaml.dump(self, f, indent=self.indent,
                               sort_keys=True, default_flow_style=False)
        return result

    def yaml_to_json(self):
        yaml_path = self.path + '.yaml'
        json_path = self.path + '.json'
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
