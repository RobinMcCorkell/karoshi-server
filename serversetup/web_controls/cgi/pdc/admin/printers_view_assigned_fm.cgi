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
############################
#Language
############################
LANGCHOICE=englishuk
STYLESHEET=defaultstyle.css
TIMEOUT=300
NOTIMEOUT=127.0.0.1
[ -f /opt/karoshi/web_controls/user_prefs/$REMOTE_USER ] && source /opt/karoshi/web_controls/user_prefs/$REMOTE_USER
[ -f /opt/karoshi/web_controls/language/$LANGCHOICE/printer/printers_view_assigned ] || LANGCHOICE=englishuk
source /opt/karoshi/web_controls/language/$LANGCHOICE/printer/printers_view_assigned
[ -f /opt/karoshi/web_controls/language/$LANGCHOICE/all ] || LANGCHOICE=englishuk
source /opt/karoshi/web_controls/language/$LANGCHOICE/all
#Check if timout should be disabled
if [ `echo $REMOTE_ADDR | grep -c $NOTIMEOUT` = 1 ]
then
TIMEOUT=86400
fi
############################
#Show page
############################
echo "Content-type: text/html"
echo ""
echo '
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"><html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8">
  <title>'$TITLE'</title><meta http-equiv="REFRESH" content="'$TIMEOUT'; URL=/cgi-bin/admin/logout.cgi">
<link rel="stylesheet" href="/css/'$STYLESHEET'">
<script src="/all/stuHover.js" type="text/javascript"></script>
</head>
<body onLoad="start()">'
#Generate navigation bar
/opt/karoshi/web_controls/generate_navbar_admin

#Check that a print server has been declared
function show_status {
echo '<SCRIPT language="Javascript">'
echo 'alert("'$PRINTSERVERERRORMSG'")';
echo 'window.location = "karoshi_servers_view.cgi";'
echo '</script>'
echo "</body></html>"
exit
}

[ ! -f /opt/karoshi/server_network/printserver ] && show_status

echo '<form action="/cgi-bin/admin/printers_view_assigned.cgi" method="post"><div id="actionbox"><b>'$TITLE'</b> <a class="info" target="_blank" href="http://www.linuxschools.com/karoshi/documentation/wiki/index.php?title=View_Assigned_Printers"><img class="images" alt="" src="/images/help/info.png"><span>'"$HELPMSG1"'</span></a><br><br>'

#Check to see that locations.txt exists
if [ ! -f /var/lib/samba/netlogon/locations.txt ]
then
echo $ERRORMSG1'<br>'
echo '</body></html>'
fi
COUNTER=`grep -n ^--start-- /var/lib/samba/netlogon/printers.txt | cut -d: -f1`
let COUNTER=$COUNTER+1
NOOFLINES=`cat /var/lib/samba/netlogon/printers.txt | wc -l`
#Show locations and printers
while [ $COUNTER -le $NOOFLINES ]
do
DATAENTRY=`sed -n $COUNTER,$COUNTER'p' /var/lib/samba/netlogon/printers.txt`
#Assign data entry to an array
if [ $DATAENTRY'null' != null ]
then
DATARRAY=( `echo $DATAENTRY | sed 's/,/ /g'` )
ARRAYCOUNT=${#DATARRAY[@]}
let ARRAYCOUNT=$ARRAYCOUNT-1
DEFAULTPRINTER=${DATARRAY[$ARRAYCOUNT]}
#Show location an default printer
echo '<table class="standard" style="text-align: left;"><tbody><tr><td style="width: 200px;"><b>'$LOCATIONMSG':</b> '${DATARRAY[0]}'</td><td style="width: 180px;"><b>'$DEFAULTPRINTERMSG':</b> '$DEFAULTPRINTER'</td><td><b>'$PRINTERMSG'</b></td><td style="text-align: center;"></td><td style="text-align: center;"></td></tr>'
#Show printers
ARRAYCOUNTER=2
while [ $ARRAYCOUNTER -lt $ARRAYCOUNT ]
do
#Show printer name
echo '<tr><td></td><td></td><td>'${DATARRAY[$ARRAYCOUNTER]}'</td>'
#Show printer actions
#Set default option
if [ ${DATARRAY[$ARRAYCOUNTER]} != $DEFAULTPRINTER ]
then
echo '<td style="text-align: center;"><a class="info" href="javascript:void(0)"><input name="_PRINTACTION_default:'${DATARRAY[0]}':'${DATARRAY[$ARRAYCOUNTER]}'_" type="image" class="images" src="/images/help/printer_make_default.png" value=""><span>'$DEFAULTMSG'</span></a></td>'
else
echo '<td style="text-align: center;"></td>'
fi
#Delete option

echo '<td><a class="info" href="javascript:void(0)"><input name="_PRINTACTION_delete:'${DATARRAY[0]}':'${DATARRAY[$ARRAYCOUNTER]}'_" type="image" class="images" src="/images/help/printer_remove.png" value=""><span>'$REMOVEMSG'</span></a></td></tr>'
let ARRAYCOUNTER=$ARRAYCOUNTER+1
done
#End table
echo '</tbody></table>'
echo '<br>'
#Clear array
unset DATARRAY
let COUNTER=$COUNTER+1
fi
done
echo '</div></form></body></html>'
exit
