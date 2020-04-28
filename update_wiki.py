import argparse
import json
import requests
import yaml

# Must be before data declaration
def load_config():
    """Load yaml config"""
    with open("config.yaml") as f:
        config = yaml.load(f, Loader=yaml.SafeLoader)
        return config

# Global config data
config = load_config()

# Global standard for Markdown newline character
newLine = "\n\n"

def load_content(args):
    """Load and generate the new content from the provided args and listings in config.yaml"""
    # Load the content from the filename, extract any %var% characters and request them from argparse
    content = f"#### Group Lab Session $ID \n"
    content += "| Lab date   | Lab time (morning/afternoon) | Person         | Arrive time | Departure time |\n"
    content += "| ---------- | :--------------------------: | -------------: | ----------- | -------------- |\n"

    session_time = "afternoon" if "pm" in args.time_out else "morning"

    for name in config['names']:
        content += f"| {args.date} | {session_time} | {name} | {args.time_in} | {args.time_out} |\n"

    return newLine + content + newLine


def upload_content(newContent):
    """Get the current Wiki document content, append the new timetable to the content and upload it back to Gitlab"""
    # Get current content from Wiki
    currentWiki = requests.get(f"{config['rootURI']}/projects/{config['projectID']}/wikis/{config['wikiSlug']}",
    headers={"PRIVATE-TOKEN": config['PAT']})

    # Append load_content to current content
    oldContent = getContent(currentWiki)
    # Get old ID - Increment
    id = getLastId(oldContent)
    id += 1
    # Set the ID value on the new content
    newContent = setID(id, newContent)
    content = oldContent + newContent

    # Push changes to Gitlab
    requests.put(f"{config['rootURI']}/projects/{config['projectID']}/wikis/{config['wikiSlug']}",
    headers={"PRIVATE-TOKEN": config['PAT']},
    params={"content": content})
    return


def getContent(currentWiki):
    """Get the content from the wiki response - Decode and convert to python dict"""
    json_string = currentWiki.content.decode("ascii")
    dictWiki = json.loads(json_string)
    return dictWiki["content"]


def getLastId(content):
    """Get the last ID from the previous content within the Wiki document"""
    substr = "Group Lab Session "
    pos = content.rfind(substr)
    length = len(substr)

    return int(content[pos + length])



def setID(id, content):
    """Set the ID in the new document with the updated ID"""
    return content.replace("$ID", str(id))


def parse_args():
    """Parse the incoming CLI arguments for the date and lab times to input into the wiki doc"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", "-d", help="Date of this lab session")
    parser.add_argument("--time-in", "-ti", help="Time string representing the time lab began")
    parser.add_argument("--time-out", "-to", help="Time string representing the time lab ended")
    
    return parser.parse_args()


def main():
    args = parse_args()

    # Load new content
    content = load_content(args)

    # Upload the content to Gitlab
    upload_content(content)

    return

if __name__ == '__main__':
    main()
