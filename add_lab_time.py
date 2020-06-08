import argparse
import json
import requests
import yaml

from datetime import datetime

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

    # Check exists else default to afternoon | Based off time_in time
    if args.time_in:
        session_time = "afternoon" if "pm" in args.time_in else "morning"
    else:
        session_time = "afternoon"

    for name in config['names']:
        content += f"| {args.date} | {session_time} | {name} | {args.time_in} | {args.time_out} |\n"

    return newLine + content + newLine


def upload_content(newContent):
    """Get the current Wiki document content, append the new timetable to the content and upload it back to Gitlab"""
    # Get current content from Wiki
    currentWiki = requests.get(f"{config['rootURI']}/api/v4/projects/{config['projectID']}/wikis/{config['wikiSlug']}",
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
    requests.put(f"{config['rootURI']}/api/v4/projects/{config['projectID']}/wikis/{config['wikiSlug']}",
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


def checkAndDefaultArgs(args):
    """Go through and check the args are valid otherwise default them to specific values"""
    if not args.date:
        args.date = datetime.now().strftime("%d/%m/%Y")

    if args.time_in:
        if "am" not in args.time_in and "pm" not in args.time_in:
            print("Invalid time_in string provided: Using default 1pm")
            args.time_in = "1pm"
    else:
        args.time_in = "1pm"

    if args.time_out:
        if "am" not in args.time_out and "pm" not in args.time_out:
            print("Invalid time_out string provided: Using default 2pm")
            args.time_out = "2pm"
    else:
        args.time_out = "2pm"


def parse_args():
    """Parse the incoming CLI arguments for the date and lab times to input into the wiki doc"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", "-d", help="Date of this lab session")
    parser.add_argument("--time-in", "-ti", help="Time string representing the time lab began")
    parser.add_argument("--time-out", "-to", help="Time string representing the time lab ended")
    
    return parser.parse_args()


def main():
    args = parse_args()
    checkAndDefaultArgs(args)

    # Load new content
    content = load_content(args)

    # Upload the content to Gitlab
    upload_content(content)

    return

if __name__ == '__main__':
    main()
