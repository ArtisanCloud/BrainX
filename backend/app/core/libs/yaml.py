import yaml


def load_yaml_file(filepath):
    """Load a YAML file."""
    with open(filepath, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)
