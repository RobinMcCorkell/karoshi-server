#!/bin/bash
#Copyright (C) 2010  Paul Sharrad
#This program is free software; you can redistribute it and/or
#modify it under the terms of the GNU General Public License
#as published by the Free Software Foundation; either version 2
#of the License, or (at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
#The Karoshi Team can be contacted at: 
#mpsharrad@karoshi.org.uk
#jharris@karoshi.org.uk
#aball@karoshi.org.uk
#
#Website: http://www.karoshi.org.uk

##########################
#Language
##########################
LANGCHOICE=englishuk
STYLESHEET=defaultstyle.css
[ -f /opt/karoshi/web_controls/global_prefs ] && source /opt/karoshi/web_controls/global_prefs
[ -f /opt/karoshi/web_controls/language/$LANGCHOICE/user/helpdesk ] || LANGCHOICE=englishuk
source /opt/karoshi/web_controls/language/$LANGCHOICE/user/helpdesk
[ -f /opt/karoshi/web_controls/language/$LANGCHOICE/all ] || LANGCHOICE=englishuk
source /opt/karoshi/web_controls/language/$LANGCHOICE/all
##########################
#Show page
##########################
echo "Content-type: text/html"
echo ""
echo '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"
<link rel="stylesheet" href="/css/'$STYLESHEET'"><meta http-equiv="REFRESH" content="0;url=helpdesk_view_fm.cgi"><title>'$TITLE'</title></head><body>'
#########################
#Get data input
#########################
TCPIP_ADDR=$REMOTE_ADDR
DATA=`cat | tr -cd 'A-Za-z0-9\.%+_:\-'`
#########################
#Assign data to variables
#########################
END_POINT=15
#Assign DEPARTMENT
COUNTER=2
while [ $COUNTER -le $END_POINT ]
do
DATAHEADER=`echo $DATA | cut -s -d'_' -f$COUNTER`
if [ `echo $DATAHEADER'check'` = DEPARTMENTcheck ]
then
let COUNTER=$COUNTER+1
DEPARTMENT=`echo $DATA | cut -s -d'_' -f$COUNTER`
break
fi
let COUNTER=$COUNTER+1
done
#Assign CATEGORY
COUNTER=2
while [ $COUNTER -le $END_POINT ]
do
DATAHEADER=`echo $DATA | cut -s -d'_' -f$COUNTER`
if [ `echo $DATAHEADER'check'` = CATEGORYcheck ]
then
let COUNTER=$COUNTER+1
CATEGORY=`echo $DATA | cut -s -d'_' -f$COUNTER`
break
fi
let COUNTER=$COUNTER+1
done
#Assign REQUEST
COUNTER=2
while [ $COUNTER -le $END_POINT ]
do
DATAHEADER=`echo $DATA | cut -s -d'_' -f$COUNTER`
if [ `echo $DATAHEADER'check'` = REQUESTcheck ]
then
let COUNTER=$COUNTER+1
REQUEST=`echo $DATA | cut -s -d'_' -f$COUNTER`
break
fi
let COUNTER=$COUNTER+1
done
#Assign JOBTITLE
COUNTER=2
while [ $COUNTER -le $END_POINT ]
do
DATAHEADER=`echo $DATA | cut -s -d'_' -f$COUNTER`
if [ `echo $DATAHEADER'check'` = JOBTITLEcheck ]
then
let COUNTER=$COUNTER+1
JOBTITLE=`echo $DATA | cut -s -d'_' -f$COUNTER`
break
fi
let COUNTER=$COUNTER+1
done
#Assign LOCATION
COUNTER=2
while [ $COUNTER -le $END_POINT ]
do
DATAHEADER=`echo $DATA | cut -s -d'_' -f$COUNTER`
if [ `echo $DATAHEADER'check'` = LOCATIONcheck ]
then
let COUNTER=$COUNTER+1
LOCATION=`echo $DATA | cut -s -d'_' -f$COUNTER`
break
fi
let COUNTER=$COUNTER+1
done
#Assign ASSETNUMBER
COUNTER=2
while [ $COUNTER -le $END_POINT ]
do
DATAHEADER=`echo $DATA | cut -s -d'_' -f$COUNTER`
if [ `echo $DATAHEADER'check'` = ASSETNUMBERcheck ]
then
let COUNTER=$COUNTER+1
ASSETNUMBER=`echo $DATA | cut -s -d'_' -f$COUNTER`
break
fi
let COUNTER=$COUNTER+1
done
ASSETNUMBER=`echo $ASSETNUMBER | tr -cd '0-9'`

function show_status {
echo '<SCRIPT language="Javascript">'
echo 'alert("'$MESSAGE'")';
echo 'window.location = "/cgi-bin/staff/helpdesk_add_fm.cgi";'
echo '</script>'
echo "</body></html>"
exit
}

#########################
#Check data
#########################

#Check to see that CATEGORY is not blank
#if [ $CATEGORY'null' = null ]
#then
#MESSAGE=$ERRORMSG2
#show_status
#fi

#Check that REQUEST is not blank
#if [ $REQUEST'null' = null ]
#then
#MESSAGE=$ERRORMSG3
#show_status
#fi

#Check that JOBTITLE is not blank
if [ $JOBTITLE'null' = null ]
then
MESSAGE=$ERRORMSG7
show_status
fi

#Check that DEPARTMENT is not blank
#if [ $DEPARTMENT'null' = null ]
#then
#MESSAGE=$ERRORMSG4
#show_status
#fi

#Check that LOCATION is not blank
#if [ $LOCATION'null' = null ]
#then
#MESSAGE=$ERRORMSG5
#show_status
#fi

#Convert special characters
NAME=`echo $NAME | sed 's/+/ /g'`
JOBTITLE=`echo $JOBTITLE | sed 's/%0D%0A/ /g' | sed 's/+/ /g' | sed 's/%3E//g' | sed 's/%27//g' | sed 's/%22//g' | sed 's/%3F/?/g' | sed 's/%2C/,/g' | sed 's/%21/!/g' | sed 's/%2F/\//g' | sed 's/%26/\&/g'`
REQUEST=`echo $REQUEST | sed 's/%0D%0A/ /g' | sed 's/+/ /g' | sed 's/%3E//g' | sed 's/%27//g'  | sed 's/%22//g' | sed 's/%3F/?/g' | sed 's/%2C/,/g' | sed 's/%21/!/g' | sed 's/%2F/\//g' | sed 's/%28/(/g' | sed 's/%29/)/g' | sed 's/%26/\&/g'`
DEPARTMENT=`echo $DEPARTMENT | sed 's/%24/$/g' | sed 's/%26/\&/g'`
CATEGORY=`echo $CATEGORY | sed 's/%24/$/g'`

#See if a default person has been declared for assigning jobs to
[ -f /opt/karoshi/helpdesk/defaultassign ] && ASSIGNED=`sed -n 1,1p /opt/karoshi/helpdesk/defaultassign`

#See if a default priority has been declared for assigning jobs to
[ -f /opt/karoshi/helpdesk/defaultpriority ] && PRIORITY=`sed -n 1,1p /opt/karoshi/helpdesk/defaultpriority`

#Add request
REQUESTNAME="`date +%s`.$$"

[ ! -d /opt/karoshi/helpdesk/log ] && mkdir -p /opt/karoshi/helpdesk/log
[ ! -d /opt/karoshi/helpdesk/todo ] && mkdir -p /opt/karoshi/helpdesk/todo
echo NAME='"'"$REMOTE_USER"'"' > /opt/karoshi/helpdesk/todo/$REQUESTNAME
echo DATE='"'"`date +%d-%m-%y`"'"' >> /opt/karoshi/helpdesk/todo/$REQUESTNAME
echo DATE2='"'"`date +%s`"'"' >> /opt/karoshi/helpdesk/todo/$REQUESTNAME
echo LOCATION='"'"$LOCATION" "$ASSETNUMBER"'"' >> /opt/karoshi/helpdesk/todo/$REQUESTNAME
echo DEPARTMENT="$DEPARTMENT" >> /opt/karoshi/helpdesk/todo/$REQUESTNAME
echo CATEGORY="$CATEGORY" >> /opt/karoshi/helpdesk/todo/$REQUESTNAME
echo JOBTITLE='"'"$JOBTITLE"'"' >> /opt/karoshi/helpdesk/todo/$REQUESTNAME
echo REQUEST='"'"$REQUEST"'"' >> /opt/karoshi/helpdesk/todo/$REQUESTNAME
echo ASSIGNED='"'"$ASSIGNED"'"' >> /opt/karoshi/helpdesk/todo/$REQUESTNAME
echo PRIORITY='"'"$PRIORITY"'"' >> /opt/karoshi/helpdesk/todo/$REQUESTNAME
echo FEEDBACK="" >> /opt/karoshi/helpdesk/todo/$REQUESTNAME
echo COMPLETEDDATE="" >> /opt/karoshi/helpdesk/todo/$REQUESTNAME
echo COMPLETEDDATE2="" >> /opt/karoshi/helpdesk/todo/$REQUESTNAME
LOG_DATE=`date +%F`
echo `date`: Helpdesk - $REQUESTNAME added by $REMOTE_USER from $REMOTE_ADDR >> /opt/karoshi/helpdesk/log/$LOG_DATE

echo "$REMOTE_USER:$REMOTE_ADDR:$MD5SUM:yes:" | sudo -H /opt/karoshi/web_controls/exec/helpdesk_warning_message

exit
