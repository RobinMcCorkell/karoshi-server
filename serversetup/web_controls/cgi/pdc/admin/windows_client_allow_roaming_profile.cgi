#!/bin/bash
#Copyright (C) 2007  Paul Sharrad

#This file is part of Karoshi Server.
#
#Karoshi Server is free software: you can redistribute it and/or modify
#it under the terms of the GNU Affero General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#Karoshi Server is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU Affero General Public License for more details.
#
#You should have received a copy of the GNU Affero General Public License
#along with Karoshi Server.  If not, see <http://www.gnu.org/licenses/>.

#
#The Karoshi Team can be contacted at: 
#mpsharrad@karoshi.org.uk
#jharris@karoshi.org.uk
#aball@karoshi.org.uk
#
#Website: http://www.karoshi.org.uk
########################
#Required input variables
########################
#  _USERACCOUNT_ (karoshi, root, sambaroot, or ghost)
#  _PASSWORD1_  New Password
#  _PASSWORD2_  Checked against PASSWORD1 for typos.

############################
#Language
############################
LANGCHOICE=englishuk
STYLESHEET=defaultstyle.css
[ -f /opt/karoshi/web_controls/user_prefs/$REMOTE_USER ] && source /opt/karoshi/web_controls/user_prefs/$REMOTE_USER
[ -f /opt/karoshi/web_controls/language/$LANGCHOICE/user/allow_roaming_profile ] || LANGCHOICE=englishuk
source /opt/karoshi/web_controls/language/$LANGCHOICE/user/allow_roaming_profile
[ -f /opt/karoshi/web_controls/language/$LANGCHOICE/all ] || LANGCHOICE=englishuk
source /opt/karoshi/web_controls/language/$LANGCHOICE/all
############################
#Show page
############################
echo "Content-type: text/html"
echo ""
echo '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"><html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"><title>'$TITLE'</title><link rel="stylesheet" href="/css/'$STYLESHEET'"></head><body>'
#########################
#Required data
#########################
#_USERNAME_
#########################
#Get data input
#########################
TCPIP_ADDR=$REMOTE_ADDR
DATA=`cat | tr -cd 'A-Za-z0-9\._:\-'`
#########################
#Assign data to variables
#########################
END_POINT=7
#Assign USERNAME
COUNTER=2
while [ $COUNTER -le $END_POINT ]
do
DATAHEADER=`echo $DATA | cut -s -d'_' -f$COUNTER`
if [ `echo $DATAHEADER'check'` = USERNAMEcheck ]
then
let COUNTER=$COUNTER+1
USERNAME=`echo $DATA | cut -s -d'_' -f$COUNTER`
break
fi
let COUNTER=$COUNTER+1
done

#Assign PERMISSIONS
COUNTER=2
while [ $COUNTER -le $END_POINT ]
do
DATAHEADER=`echo $DATA | cut -s -d'_' -f$COUNTER`
if [ `echo $DATAHEADER'check'` = PERMISSIONScheck ]
then
let COUNTER=$COUNTER+1
PERMISSIONS=`echo $DATA | cut -s -d'_' -f$COUNTER-`
break
fi
let COUNTER=$COUNTER+1
done

function show_status {
echo '<SCRIPT language="Javascript">'
echo 'alert("'$MESSAGE'");'
echo 'window.location = "/cgi-bin/admin/windows_client_allow_roaming_profile_fm.cgi";'
echo '</script>'
echo "</body></html>"
exit
}
#########################
#Check https access
#########################
if [ https_$HTTPS != https_on ]
then
export MESSAGE=$HTTPS_ERROR
show_status
fi
#########################
#Check user accessing this script
#########################
if [ ! -f /opt/karoshi/web_controls/web_access_admin ] || [ $REMOTE_USER'null' = null ]
then
MESSAGE=$ACCESS_ERROR1
show_status
fi

if [ `grep -c ^$REMOTE_USER: /opt/karoshi/web_controls/web_access_admin` != 1 ]
then
MESSAGE=$ACCESS_ERROR1
show_status
fi
#########################
#Check data
#########################
#Check to see that username is not blank
if [ $USERNAME'null' = null ]
then
MESSAGE=$ERRORMSG2
show_status
fi

#Check to see that permissions is not blank
if [ $PERMISSIONS'null' = null ]
then
MESSAGE=$ERRORMSG8
show_status
fi

#Check to see if the user exists
getent passwd $USERNAME 1>/dev/null 
if [ `echo $?` != 0 ]
then
MESSAGE=$ERRORMSG1
show_status
fi

#Check that the username is not for a system account
if [ `id -u $USERNAME` -lt 500 ]
then
MESSAGE=$ERRORMSG3
show_status
fi


#Check that the username is not the karoshi user
if [ $USERNAME = karoshi ]
then
MESSAGE=$ERRORMSG4
show_status
fi

#Check to see that this user does not already have a roaming profile
if [ -d /home/applications/profiles/$USERNAME ]
then
MESSAGE=$ERRORMSG6
show_status
fi 

MD5SUM=`md5sum /var/www/cgi-bin_karoshi/admin/windows_client_allow_roaming_profile.cgi | cut -d' ' -f1`
#Enable roaming profile
echo "$REMOTE_USER:$REMOTE_ADDR:$MD5SUM:$USERNAME:$PERMISSIONS:" | sudo -H /opt/karoshi/web_controls/exec/windows_client_allow_roaming_profile
EXEC_STATUS=`echo $?`
if [ $EXEC_STATUS = 0 ]
then
MESSAGE=`echo $COMPLETEDMSG $USERNAME.`
else
MESSAGE=`echo $ERRORMSG5 $USERNAME.`
fi
show_status
