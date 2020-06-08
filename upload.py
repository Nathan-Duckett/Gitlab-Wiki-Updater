import requests
import sys
import yaml
from os import path

file_dir = path.dirname(path.abspath(__file__))

def load_config():
    """Load yaml config"""
    with open(f"{file_dir}/config.yaml") as f:
        config = yaml.load(f, Loader=yaml.SafeLoader)
        return config

def uploadContent(content):
    requests.put(f"{config['rootURI']}/api/v4/projects/{config['projectID']}/wikis/{config['wikiSlug']}",
    headers={"PRIVATE-TOKEN": config['PAT']},
    params={"content": content})

# Global config data
config = load_config()

# Load data from STDIN piped into application
content = ""
for line in sys.stdin:
    content += line

# Upload to Gitlab
uploadContent(content)