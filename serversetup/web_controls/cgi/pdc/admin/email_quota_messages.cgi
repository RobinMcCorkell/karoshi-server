#!/bin/bash
#Copyright (C) 2007 Paul Sharrad
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
############################
#Language
############################
LANGCHOICE=englishuk
STYLESHEET=defaultstyle.css
TIMEOUT=300
NOTIMEOUT=127.0.0.1
[ -f /opt/karoshi/web_controls/user_prefs/$REMOTE_USER ] && source /opt/karoshi/web_controls/user_prefs/$REMOTE_USER
[ -f /opt/karoshi/web_controls/language/$LANGCHOICE/email/email_quota_messages ] || LANGCHOICE=englishuk
source /opt/karoshi/web_controls/language/$LANGCHOICE/email/email_quota_messages
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

function show_status {
echo '<SCRIPT language="Javascript">'
echo 'alert("'$MESSAGE'")';
echo '                window.location = "/karoshi/admin/update_servers.html";'
echo '</script>'
echo "</body></html>"
exit
}

#########################
#Get data input
#########################
TCPIP_ADDR=$REMOTE_ADDR
DATA=`cat | tr -cd 'A-Za-z0-9\._:\-'`

echo "Content-type: text/html"
echo ""
echo '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"><html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"><title>'$TITLE'</title><meta http-equiv="REFRESH" content="'$TIMEOUT'; URL=/cgi-bin/admin/logout.cgi"><link rel="stylesheet" href="/css/'$STYLESHEET'"><script src="/all/stuHover.js" type="text/javascript"></script></head><body>'
#########################
#Check https access
#########################
if [ https_$HTTPS != https_on ]
then
export MESSAGE=$HTTPS_ERROR
show_status
fi

#Generate navigation bar
/opt/karoshi/web_controls/generate_navbar_admin

echo '<form action="/cgi-bin/admin/email_quota_messages2.cgi" method="post">'
echo '<div id="actionbox"><b>'$TITLE'</b> <a class="info" href="javascript:void(0)"><img class="images" alt="" src="/images/help/info.png"><span>'$HELPMSG'</span></a><br><br><input value="Submit" type="submit"><input value="Reset" type="reset"><br><br>'
###########################
#Get current email messages
###########################
if [ ! -f /opt/karoshi/postfixdata/warning_messages/level1 ] || [ ! -f /opt/karoshi/postfixdata/warning_messages/level2 ] || [ ! -f /opt/karoshi/postfixdata/warning_messages/level3 ] || [ ! -f /opt/karoshi/postfixdata/warning_messages/level4 ]
then
MD5SUM=`md5sum /var/www/cgi-bin_karoshi/admin/email_quota_messages.cgi | cut -d' ' -f1`
#Get messages from colossus
sudo -H /opt/karoshi/web_controls/exec/email_get_quota_messages $REMOTE_USER:$REMOTE_ADDR:$MD5SUM
fi

#Level1
echo "<b>"$LEVEL1"</b><br>"
if [ -f /opt/karoshi/postfixdata/warning_messages/level1 ]
then
echo -e \<textarea cols=\"80\" rows=\"10\" name=\"_LEVEL1_\"\>
cat /opt/karoshi/postfixdata/warning_messages/level1
echo \</textarea\>
else
echo \<textarea cols=\"80\" rows=\"10\" name=\"_LEVEL1_\"\>\</textarea\>
fi
#Level2
echo "<br><br><b>"$LEVEL2"</b><br>"
if [ -f /opt/karoshi/postfixdata/warning_messages/level2 ]
then
echo -e \<textarea cols=\"80\" rows=\"10\" name=\"_LEVEL2_\"\>
cat /opt/karoshi/postfixdata/warning_messages/level2
echo \</textarea\>
else
echo \<textarea cols=\"80\" rows=\"10\" name=\"_LEVEL2_\"\>\</textarea\>
fi
#Level3
echo "<br><br><b>"$LEVEL3"</b><br>"
if [ -f /opt/karoshi/postfixdata/warning_messages/level3 ]
then
echo -e \<textarea cols=\"80\" rows=\"10\" name=\"_LEVEL3_\"\>
cat /opt/karoshi/postfixdata/warning_messages/level3
echo \</textarea\>
else
echo \<textarea cols=\"80\" rows=\"10\" name=\"_LEVEL3_\"\>\</textarea\>
fi
#Level4
echo "<br><br><b>"$LEVEL4"</b><br>"
if [ -f /opt/karoshi/postfixdata/warning_messages/level4 ]
then
echo -e \<textarea cols=\"80\" rows=\"8\" name=\"_LEVEL4_\"\>
cat /opt/karoshi/postfixdata/warning_messages/level4
echo \</textarea\>
else
echo \<textarea cols=\"80\" rows=\"8\" name=\"_LEVEL4_\"\>\</textarea\>
fi
echo '<br><br><input value="Submit" type="submit"><input value="Reset" type="reset">
</div></form></body></html>'
exit