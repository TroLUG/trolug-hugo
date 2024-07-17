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

base_dir = '/home/stein/my/prj/web/trolug.de/trolug/content/de/docs/'
events_dir = os.path.join(base_dir, 'events')
template_file = os.path.join(base_dir, 'mktable_template.txt')
output_file = os.path.join(base_dir, 'termine.md')

# print(events_dir)

# myfilelist = glob.glob('./*.md')
myfilelist = list(pathlib.Path(events_dir).glob('20*.md'))


data = []

for myfile in myfilelist:
    print("Reading file: ", myfile )
    mydict = frontmatter.load(myfile, handler=JSONHandler())
    row = (mydict["meetingdate"], mydict["eventtype"], mydict["location"], mydict["title"], mydict["slug"], mydict["presenter"], mydict["pad"])
    data.append(row)

df = pd.DataFrame(data, columns=['meetingdate', 'eventtype','location', 'title', 'slug', 'presenter', 'pad'])
df = df.sort_values(by='meetingdate')

df["titlelink"] = '[' + df["title"] + ']({{< ref "/docs/events/' + df["slug"] + '" >}})'
df["padlink"] = '[pad](' + df["pad"] + ')'

mydf = df[["meetingdate", "presenter", "titlelink", "padlink"]]




# print(df)

markdown_table = mydf.to_markdown(index=False)

# Thanks to Jack Aidley in https://stackoverflow.com/a/17141572/1749675
# Read in the file
with open(template_file, 'r') as file:
  filedata = file.read()

# Replace the target string
filedata = filedata.replace('INSERT_EVENTS_HERE', markdown_table)


# Write the file out again
with open(output_file, 'w') as file:
  file.write(filedata)


