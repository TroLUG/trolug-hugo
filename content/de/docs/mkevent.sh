#!/bin/bash

echo "usage: mkevent.sh <DATE> <SLUG> <TOPIC>" 
echo  
echo "DATE=2020-04-30"
echo "SLUG=VM"
echo 'TOPIC="Virtualisierung von Servern"'

FILENAME="events/${1}_${2}.md"

PADDATE=`echo ${1} | cut -d "-" -f1-2`

cat > ${FILENAME} << EOF 
{
   "meetingdate": "${1}T19:00+01:00",
   "presenter": "Alle",
   "title": "${3}",
   "slug": "${1}_${2}",
   "pad": "https://trolug.pads.ccc.de/${PADDATE}",
   "eventtype": "Workshop",
   "location": "Online",
   "menu": "main",
   "taxonomies": {
        "category": "Workshop",
        "tag": "TroLUG"
    }
}

## Konferenzserver
* https://bbb.trolug.de

## ${3}

## Notizen
Werden hierher aus dem Etherpad übernommen

EOF
