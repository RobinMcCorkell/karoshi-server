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
[ -f /opt/karoshi/web_controls/language/$LANGCHOICE/menus/logs ] || LANGCHOICE=englishuk
source /opt/karoshi/web_controls/language/$LANGCHOICE/menus/logs
############################
#Show page
############################
echo "Content-type: text/html"
echo ""
echo '
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html><head><title>Karoshi Web Application</title><meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1"><link href="/css/'$STYLESHEET'"rel="stylesheet" type="text/css"></head>
<body><table class="leftmenu" style="text-align: left; width: 222px; height: 426px;" border="0" cellpadding="6" cellspacing="0"><tbody><tr><td style="vertical-align: top;">
<a href="/cgi-bin/admin/view_karoshi_web_management_logs.cgi" target="_top"><img style="border: 0px solid ; width: 16px; height: 16px;" alt="" src="/images/submenus/system/web.png">'$WEBLOGSMSG'</a><br>
<a href="/cgi-bin/admin/view_disk_usage_logs_fm.cgi" target="_top"><img style="border: 0px solid ; width: 16px; height: 16px;" alt="" src="/images/submenus/system/web.png">'$DISKLOGSMSG'</a><br>
<a href="/cgi-bin/admin/view_karoshi_auth_errors.cgi" target="_top"><img style="border: 0px solid ; width: 16px; height: 16px;" alt="" src="/images/submenus/system/web.png">'$AUTHERRMSG'</a><br>
<a href="/cgi-bin/admin/clear_warnings_fm.cgi" target="_top"><img style="border: 0px solid ; width: 16px; height: 16px;" alt="" src="/images/submenus/system/clear_warnings.png">'$CLEARWARNINGSMSG'</a><br>
<a href="/cgi-bin/admin/change_management_passwords_fm.cgi" target="_top"><img style="border: 0px solid ; width: 16px; height: 16px;" alt="" src="/images/submenus/all/back.png"></a><br>
</td></tr></tbody></table></body></html>
'
#Not in use - not happy with gui being enabled and not unlinking properly from parent apache cgi
#<a href="/cgi-bin/admin/enable_disable_gui_fm.cgi" target="_top"><img style="border: 0px solid ; width: 16px; height: 16px;" alt="" src="/images/submenus/system/enable_disable_gui.png">'$GUIMSG'</a><br>
exit
