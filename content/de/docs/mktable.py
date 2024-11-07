#!/usr/bin/env python 

__author__ = "Jonas Stein"

import pathlib

import json
import frontmatter
import os
from frontmatter.default_handlers import JSONHandler

from py_markdown_table.markdown_table import markdown_table
import fileinput
import pandas as pd


from icalendar import Calendar, Event
from datetime import datetime, timedelta
import pytz
    
# def getyear(time_str)


def create_ical_event(icaldir, rfc_time_str, summary, presenter):
    """
    usage: 
    create_ical_event(ics_dir, '2024-07-19T19:00+02:00', 'Workshop')
    """
    event_datetime = datetime.fromisoformat(rfc_time_str)
    event_datetime_UTC = event_datetime.astimezone(pytz.utc)

    filename=os.path.join(icaldir, event_datetime_UTC.strftime("%Y-%m-%dT%H%MZ") + '.ics')

    cal = Calendar()
    event = Event()
    event.add('summary', '[TroLUG] ' + summary + ' (' + presenter + ')' )
    event.add('dtstart', event_datetime)
    event.add('dtend', event_datetime + timedelta(hours=2))
    event.add('dtstamp', datetime.now(pytz.utc))
    event.add('url', 'https://trolug.de/')

    cal.add_component(event)
    with open(filename, 'wb') as f:
        f.write(cal.to_ical())
    print("I: " + filename + " written")



"""
def create_ical_link(rfc_time_str):
    event_datetime = datetime.fromisoformat(rfc_time_str)
    filename=os.path.join(icaldir, event_datetime_UTC.strftime("%Y-%m-%dT%H%MZ") + '.ics')
    event_datetime = pytz.timezone('Europe/Berlin').localize(event_datetime)

    returnstring = '[' + event_datetime_UTC.strftime("%Y-%m-%d %H:%M") + ']({{< ref "' + filename + '" >}})'
    return returnstring
"""

def md_link(caption, url):
    markdown_str = '[' + caption + '](' + url + ')'
    return markdown_str

def md_reflink(caption, reflink):
    markdown_str = '[' + caption + ']({{< ref "' + reflink + '" >}})'
    return markdown_str


def add_ical_link_column(folder_name, df):
    """
    Converts the 'meetingdate' column in the DataFrame to filenames based on the date in UTC.
    
    Args:
        df (pd.DataFrame): DataFrame containing the 'meetingdate' column with RFC 3339 formatted strings.
        folder_name (str): The folder name to prepend to the filenames.
    
    Returns:
        pd.DataFrame: DataFrame with the 'icallink' column converted to filenames.
    """
    folder_name = "/ics"

    # Define a function to convert RFC 3339 format to filename
    def rfc3339_to_link(date_str):
        # Parse the date string into a datetime object
        dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        # Convert to UTC
        dt_utc = dt.astimezone(pytz.utc)
        # Format as RFC 3339 date (without time)
        date_utc_str = dt_utc.strftime('%Y-%m-%dT%H%MZ')
        # Create the filename
        calendarlink = os.path.join(folder_name, date_utc_str + '.ics')

        return calendarlink
    
    # Apply the function to the 'meetingdate' column
    df['icallink'] = df['meetingdate'].apply(rfc3339_to_link)
    return df

def meetingdate_printable(date_str):
    dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))

    return df

base_dir = '/home/stein/my/prj/web/trolug.de/trolug/'
content_dir = os.path.join(base_dir, 'content/de/docs/')
events_dir = os.path.join(content_dir, 'events')
template_file = os.path.join(content_dir, 'mktable_template.txt')
output_file = os.path.join(content_dir, 'termine.md')
ics_dir=os.path.join(base_dir, 'static/ics/')

myfilelist = list(pathlib.Path(events_dir).glob('20*.md'))

    

data = []

for myfile in myfilelist:
    print("Reading file: ", myfile )
    mydict = frontmatter.load(myfile, handler=JSONHandler())
    row = (mydict["meetingdate"], mydict["eventtype"], mydict["location"], mydict["title"], mydict["slug"], mydict["presenter"], mydict["pad"])
    data.append(row)
    
df = pd.DataFrame(data, columns=['meetingdate', 'eventtype','location', 'title', 'slug', 'presenter', 'pad'])
df.sort_values(by='meetingdate', inplace=True, ascending=False)

df = add_ical_link_column(ics_dir, df)


df["mdcalendar"] = md_link(df["meetingdate"], df["icallink"])


df["titlelink"] = md_reflink(df["title"], df["slug"])
df["padlink"] = '[pad](' + df["pad"] + ')'

mydf = df[["mdcalendar", "presenter", "titlelink", "padlink"]]
mydf.rename(columns={'mdcalendar': 'Termin', 'presenter': 'Presenter', 'titlelink': 'Thema', 'padlink': 'Pad'}, inplace=True)
df.apply(lambda x: create_ical_event(ics_dir, x['meetingdate'], x['title'], x['presenter']), axis=1)


markdown_table = mydf.to_markdown(index=False)

"""
Thanks to Jack Aidley in https://stackoverflow.com/a/17141572/1749675
for the snippet to insert a text block into a file
"""
with open(template_file, 'r') as file:
  filedata = file.read()

filedata = filedata.replace('INSERT_EVENTS_HERE', markdown_table)

with open(output_file, 'w') as file:
  file.write(filedata)



