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

#Detect mobile browser
MOBILE=no
source /opt/karoshi/web_controls/detect_mobile_browser

############################
#Language
############################
LANGCHOICE=englishuk
STYLESHEET=defaultstyle.css
TIMEOUT=300
NOTIMEOUT=127.0.0.1
[ -f /opt/karoshi/web_controls/user_prefs/$REMOTE_USER ] && source /opt/karoshi/web_controls/user_prefs/$REMOTE_USER
[ -f /opt/karoshi/web_controls/language/$LANGCHOICE/system/view_disk_usage_logs ] || LANGCHOICE=englishuk
source /opt/karoshi/web_controls/language/$LANGCHOICE/system/view_disk_usage_logs
[ -f /opt/karoshi/web_controls/language/$LANGCHOICE/all ] || LANGCHOICE=englishuk
source /opt/karoshi/web_controls/language/$LANGCHOICE/all
#Check if timout should be disabled
if [ `echo $REMOTE_ADDR | grep -c $NOTIMEOUT` = 1 ]
then
TIMEOUT=86400
fi

echo "Content-type: text/html"
echo ""
echo '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"><html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"><title>'$TITLE'</title><meta http-equiv="REFRESH" content="'$TIMEOUT'; URL=/cgi-bin/admin/logout.cgi"><link rel="stylesheet" href="/css/'$STYLESHEET'"><script language="JavaScript" src="/all/calendar2/calendar_eu.js" type="text/javascript"></script><meta name="viewport" content="width=device-width, initial-scale=1"> <!--480-->'

if [ $MOBILE = yes ]
then
echo '<link rel="stylesheet" type="text/css" href="/all/mobile_menu/sdmenu.css">
	<script type="text/javascript" src="/all/mobile_menu/sdmenu.js">
		/***********************************************
		* Slashdot Menu script- By DimX
		* Submitted to Dynamic Drive DHTML code library: http://www.dynamicdrive.com
		* Visit Dynamic Drive at http://www.dynamicdrive.com/ for full source code
		***********************************************/
	</script>
	<script type="text/javascript">
	// <![CDATA[
	var myMenu;
	window.onload = function() {
		myMenu = new SDMenu("my_menu");
		myMenu.init();
	};
	// ]]>
	</script>'
fi

echo '<!-- Timestamp input popup (European Format) --><link rel="stylesheet" href="/all/calendar2/calendar.css"><script src="/all/stuHover.js" type="text/javascript"></script></head><body onLoad="start()">'
#########################
#Get data input
#########################
TCPIP_ADDR=$REMOTE_ADDR
DATA=`cat | tr -cd 'A-Za-z0-9\._:\-'`

DATE_INFO=`date +%F`
DAY=`echo $DATE_INFO | cut -d- -f3`
MONTH=`echo $DATE_INFO | cut -d- -f2`
YEAR=`echo $DATE_INFO | cut -d- -f1`

function show_status {
echo '<SCRIPT language="Javascript">'
echo 'alert("'$MESSAGE'")';
#echo '                window.location = "/cgi-bin/admin/incident_log_add.cgi";'
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

#Generate navigation bar
if [ $MOBILE = no ]
then
DIV_ID=actionbox
TABLECLASS=standard
#Generate navigation bar
/opt/karoshi/web_controls/generate_navbar_admin
else
DIV_ID=actionbox2
TABLECLASS=mobilestandard
fi

echo '<form action="/cgi-bin/admin/view_disk_usage_logs.cgi" name="testform" method="post">'

[ $MOBILE = no ] && echo '<div id="'$DIV_ID'">'

#Show back button for mobiles
if [ $MOBILE = yes ]
then
echo '<div style="float: center" id="my_menu" class="sdmenu">
	<div class="expanded">
	<span>'$TITLE'</span>
<a href="/cgi-bin/admin/mobile_menu.cgi">'$FILEMENUMSG'</a>
</div></div>
<div id="mobileactionbox">
'
else
echo '<b>'$TITLE'</b> <a class="info" target="_blank" href="http://www.linuxschools.com/karoshi/documentation/wiki/index.php?title=Disk_Usage_Logs"><img class="images" alt="" src="/images/help/info.png"><span>'"$HELPMSG1"'</span></a><br><br>'
fi


if [ $MOBILE = yes ]
then
echo ''$DATEMSG'<br>'
echo "<!-- calendar attaches to existing form element -->
	<input type=\"text\" value=\"$DAY-$MONTH-$YEAR\" size=14 maxlength=10 name=\"_DATE_\"></td><td style=\"vertical-align: top; text-align: center;\">
	<script language=\"JavaScript\">
	new tcal ({
		// form name
		'formname': 'testform',
		// input name
		'controlname': '_DATE_'
	});

	</script><br>
"

echo ''$VIEWLOGSMSG1'<br>
<input checked="checked" name="_LOGVIEW_" value="today" type="radio"><br>
'$VIEWLOGSMSG2'<br>
<input name="_LOGVIEW_" value="month" type="radio"><br><br>
'

else
echo '<table class="standard" style="text-align: left;" border="0" cellpadding="2" cellspacing="2"><tbody>
<tr><td style="width: 180px;">'$DATEMSG'</td><td>'
echo "	<!-- calendar attaches to existing form element -->
	<input type=\"text\" value=\"$DAY-$MONTH-$YEAR\" size=14 maxlength=10 name=\"_DATE_\"></td><td style=\"vertical-align: top; text-align: center;\">
	<script language=\"JavaScript\">
	new tcal ({
		// form name
		'formname': 'testform',
		// input name
		'controlname': '_DATE_'
	});

	</script></td></tr>"

echo "<tr><td>$VIEWLOGSMSG1</td><td></td><td><div style=\"text-align: center;\"><input checked=\"checked\" name=\"_LOGVIEW_\" value=\"today\" type=\"radio\"></div></td></tr><tr><td>$VIEWLOGSMSG2</td><td></td><td style=\"vertical-align: top;\"><div style=\"text-align: center;\"><input name=\"_LOGVIEW_\" value=\"month\" type=\"radio\"></div></td></tr></tbody></table><br>"
fi

#Show list of ssh enabled servers
SERVERCOUNTER=1
ROWCOUNT=6
[ $MOBILE = yes ] && ROWCOUNT=3
WIDTH=90
[ $MOBILE = yes ] && WIDTH=70

SERVERICON="/images/submenus/system/computer.png"
SERVERICON2="/images/submenus/system/all_computers.png"

echo '<table class="'$TABLECLASS'" style="text-align: left;" border="0" cellpadding="2" cellspacing="2"><tbody><tr>'

for KAROSHI_SERVER in /opt/karoshi/server_network/servers/*
do
KAROSHISERVER=`basename $KAROSHI_SERVER`
echo '<td style="width: '$WIDTH'px; vertical-align: top; text-align: left;"><a class="info" href="javascript:void(0)"><input name="_SERVER_'$KAROSHISERVER'_" type="image" class="images" src="'$SERVERICON'" value="_SERVER_'$KAROSHISERVER'"><span>'$KAROSHISERVER'<br><br>'
cat /opt/karoshi/server_network/servers/$KAROSHISERVER/* | sed '/<a href/c'"&nbsp"
echo '</span></a><br>'$KAROSHISERVER'</td>'
[ $SERVERCOUNTER = $ROWCOUNT ] && echo '</tr><tr>'
let SERVERCOUNTER=$SERVERCOUNTER+1
[ $SERVERCOUNTER -gt $ROWCOUNT ] && SERVERCOUNTER=1
done

echo '</tbody></table></div></form></body></html>'
exit
