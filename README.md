# Gitlab Wiki Updater

This app is designed to simplify updating the timetable in Gitlab Wiki to track when we have attended lab sessions.

This will append lab information for every member who is listed in your config file.

## Usage

Basic usage requires you to pass three parameters date, time in, and time out. Without these the program will not be able to work correctly.

Before Usage make sure to copy `template.config.yaml` to `config.yaml` and fill out the corresponding fields.

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