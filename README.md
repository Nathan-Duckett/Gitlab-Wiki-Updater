# Gitlab Wiki Updater

This app is designed to simplify updating the timetable in Gitlab Wiki to track when we have attended lab sessions.

This will append lab information for every member who is listed in your config file.

## Configuration
Move `template.config.yaml` to `config.yaml` and add the corresponding values required.
```yaml
rootURI: 'gitlab api endpoint e.g. "https://gitlab.ecs.vuw.ac.nz/api/v4/"'
PAT: 'Personal Access Token generated from gitlab'
projectID: 'Project ID of the repo you want to manage'
wikiSlug: 'Slug of the wiki page you're updating (final part of the web link) e.g. "Lab-time-log"'
names:
    - Nathan Duckett
    - "List of names to be added on each line of the table"
```
You must [Generate PAT](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html) for your profile with **API** privileges.

## Usage

Basic usage requires you to pass three parameters date, time in, and time out. Without these the program will not be able to work correctly.

Before Usage make sure to copy `template.config.yaml` to `config.yaml` and fill out the corresponding fields.

**Note if options are not provided it will default to TODAY's DATE, and from 1PM to 2PM**
Options can be omitted if these defaults suit depending on what is necessary.

The lab time will be based off when the time-in begins. For example starting at 11am will result in a morning lab whereas starting at 12pm will be considered an afternoon lab, no matter what time the lab finishes as it is based on when it starts.

```bash
# Install dependencies on first use
python3 -m pip install -r requirements.txt

python3 lab_time.py -d "28/04/2020" -ti "1pm" -to "4pm"
```

### Options
```tree
usage: update_wiki.py [-h] [--date DATE] [--time-in TIME_IN]
                      [--time-out TIME_OUT]

optional arguments:
  -h, --help            show this help message and exit
  --date DATE, -d DATE  Date of this lab session
  --time-in TIME_IN, -ti TIME_IN
                        Time string representing the time lab began
  --time-out TIME_OUT, -to TIME_OUT
                        Time string representing the time lab ended
```
