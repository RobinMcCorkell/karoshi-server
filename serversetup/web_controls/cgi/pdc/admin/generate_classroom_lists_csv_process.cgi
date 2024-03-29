#!/bin/bash
#Copyright (C) 2008 Paul Sharrad

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
#  _USERNAME_
#  _PASSWORD1_  Password used for new user
#  _PASSWORD2_  Checked against PASSWORD1 for typos.
#  _GROUP_      This is the primary group for the new user eg yr2000, staff, officestaff.
############################
#Language
############################
LANGCHOICE=englishuk
STYLESHEET=defaultstyle.css
[ -f /opt/karoshi/web_controls/user_prefs/$REMOTE_USER ] && source /opt/karoshi/web_controls/user_prefs/$REMOTE_USER
[ -f /opt/karoshi/web_controls/language/$LANGCHOICE/client/generate_classroom_lists_csv ] || LANGCHOICE=englishuk
source /opt/karoshi/web_controls/language/$LANGCHOICE/client/generate_classroom_lists_csv
[ -f /opt/karoshi/web_controls/language/$LANGCHOICE/all ] || LANGCHOICE=englishuk
source /opt/karoshi/web_controls/language/$LANGCHOICE/all
############################
#Show page
############################
echo "Content-type: text/html"
echo ""
echo '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"><html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"><title>'$TITLE'</title><meta http-equiv="REFRESH" content="0; URL=/cgi-bin/admin/generate_classroom_lists_csv_upload_fm.cgi"><link rel="stylesheet" href="/css/'$STYLESHEET'"></head><body>'
#########################
#Get data input
#########################
TCPIP_ADDR=$REMOTE_ADDR
#DATA=`cat | tr -cd 'A-Za-z0-9\._:\-'`
#GROUP=`echo $DATA | cut -d'_' -f3`

function show_status {

echo '<SCRIPT language="Javascript">'
echo 'alert("'$MESSAGE'")';
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
#Check input file
[ -d /var/www/karoshi/classroom_lists ] || mkdir -p /var/www/karoshi/classroom_lists
chmod 0700 /var/www/karoshi/
chmod 0700 /var/www/karoshi/classroom_lists
if [ `dir /var/www/karoshi/classroom_lists --format=single-column | wc -l` != 1 ]
then
MESSAGE=$ERRORMSG1
show_status
fi
CSVFILE=`ls /var/www/karoshi/classroom_lists`
echo >> /var/www/karoshi/classroom_lists/"$CSVFILE"
sed -i '/^$/d' /var/www/karoshi/classroom_lists/"$CSVFILE"
CSVFILE_LINES=`cat /var/www/karoshi/classroom_lists/"$CSVFILE" | wc -l`
#Sort file
cat /var/www/karoshi/classroom_lists/"$CSVFILE" | tr -cd 'A-Za-z0-9\,._:\-\n' | sort  > /var/www/karoshi/classroom_lists/"$CSVFILE".$$
#Check the data for errors
COUNTER=1
while [ $COUNTER -le $CSVFILE_LINES ]
do
DATA=`sed -n $COUNTER,$COUNTER'p' /var/www/karoshi/classroom_lists/"$CSVFILE.$$"`
LOCATION=`echo $DATA | cut -d, -f1`
TYPE=`echo $DATA | cut -d, -f2`
CLIENTHOSTNAME=`echo $DATA | cut -d, -f3`
CLIENTTCPIP=`echo $DATA | cut -d, -f4`
CLIENTMAC=`echo $DATA | cut -d, -f5`

#Check that client location is not blank
if [ $LOCATION'null' = null ]
then
MESSAGE=`echo $LINEMSG $COUNTER - $LOCATIONERROR.`
show_status
fi
#Check that client hostname is not blank
if [ $CLIENTHOSTNAME'null' = null ]
then
MESSAGE=`echo $LINEMSG $COUNTER - $CLIENTHOSTNAMEERROR.`
show_status
fi
#Check that type is correct
if [ $TYPE'check' != `echo $STUDENTTYPE'check' | sed 's/ //g'` ] && [ $TYPE'check' != `echo $STAFFTYPE'check' | sed 's/ //g'` ]
then
MESSAGE=`echo $LINEMSG $COUNTER - $TYPEERROR1. $TYPEERROR2 - $STUDENTTYPE,$STAFFTYPE.`
show_status
fi
#Check to see that TCPIP number has correct dots
if [ `echo $CLIENTTCPIP | sed 's/\./\n/g'  | sed /^$/d | wc -l` != 4 ]
then
MESSAGE=`echo $LINEMSG $COUNTER - $TCPIPERROR.`
show_status
fi
#Check to see that MAC address has correct colons
if [ `echo $CLIENTMAC | sed 's/:/\n/g'  | sed /^$/d | wc -l` != 6 ]
then
MESSAGE=`echo $LINEMSG $COUNTER - $MACERROR.`
show_status
fi

let COUNTER=$COUNTER+1
done

#Sort data
sort /var/www/karoshi/classroom_lists/"$CSVFILE".$$ > /var/www/karoshi/classroom_lists/processed_data.$$

MD5SUMCSV=`md5sum /var/www/karoshi/classroom_lists/processed_data.$$ | cut -d' ' -f1`
#rm -f /var/www/karoshi/classroom_lists/"$CSVFILE"
MD5SUM=`md5sum /var/www/cgi-bin_karoshi/admin/generate_classroom_lists_csv_process.cgi | cut -d' ' -f1`
echo "$REMOTE_USER:$REMOTE_ADDR:$MD5SUM:$MD5SUMCSV:$$:" | sudo -H /opt/karoshi/web_controls/exec/generate_classroom_lists_csv
MESSAGE=`echo $COMPLETEDMSG`
show_status
echo "</body></html>"
