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
[ -f /opt/karoshi/web_controls/user_prefs/$REMOTE_USER ] && source /opt/karoshi/web_controls/user_prefs/$REMOTE_USER
[ -f /opt/karoshi/web_controls/language/$LANGCHOICE/logout ] || LANGCHOICE=englishuk
source /opt/karoshi/web_controls/language/$LANGCHOICE/logout
############################
#Create redirect page
############################
MD5SUM=`md5sum /var/www/cgi-bin_karoshi/admin/logout.cgi | cut -d' ' -f1`
sudo -H /opt/karoshi/web_controls/exec/logout $REMOTE_USER:$REMOTE_ADDR:$MD5SUM:

############################
#Show page
############################
echo "Content-type: text/html"
echo ""
echo '
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"><html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8">
  <title>'$TITLE'</title><meta http-equiv="REFRESH" target="_top" content="5; URL='/cgi-bin/menu.cgi'">
<link rel="stylesheet" href="/css/'$STYLESHEET'">
</head>
<body>
<iframe src="/cgi-bin/logout/'$REMOTE_USER'/logout2.cgi" name="submenu" frameborder="0" width="1024" height="768" scrolling="no" marginwidth="0" marginheight="0">
</iframe>'

sleep 4
sudo -H /opt/karoshi/web_controls/exec/logout2 $REMOTE_USER:$REMOTE_ADDR:$MD5SUM:

echo '</body>
</html>
'

