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
[ -f /opt/karoshi/web_controls/language/$LANGCHOICE/system/remote_management_change_theme ] || LANGCHOICE=englishuk
source /opt/karoshi/web_controls/language/$LANGCHOICE/system/remote_management_change_theme
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
<script src="/all/stuHover.js" type="text/javascript"></script><meta name="viewport" content="width=device-width, initial-scale=1"> <!--480-->'

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

echo '</head><body>'

#Generate navigation bar
if [ $MOBILE = no ]
then
DIV_ID=actionbox
TABLECLASS=standard
MAXSTYLES=5
#Generate navigation bar
/opt/karoshi/web_controls/generate_navbar_admin
else
DIV_ID=actionbox2
TABLECLASS=mobilestandard
MAXSTYLES=4
fi

echo '<form action="/cgi-bin/admin/remote_management_change_theme2.cgi" method="post">'

[ $MOBILE = no ] && echo '<div id="'$DIV_ID'">'

#Show back button for mobiles
if [ $MOBILE = yes ]
then
echo '<div style="float: center" id="my_menu" class="sdmenu">
	<div class="expanded">
	<span>'$TITLE'</span>
<a href="/cgi-bin/admin/mobile_menu.cgi">'$SYSMENUMSG'</a>
</div></div><div id="mobileactionbox4">'
else
echo '<b>'$TITLE'</b> <a class="info" href="javascript:void(0)"><img class="images" alt="" src="/images/help/info.png"><span>'$HELPMSG1'<br><br>'$HELPMSG2'</span></a><br><br>'
fi

echo '<table class="'$TABLECLASS'" style="text-align: left;" border="0" cellpadding="2" cellspacing="2"><tbody><tr>'

STYLESHEET=`echo $STYLESHEET | cut -d. -f1`
STYLECOUNT=1
for THEMES in /var/www/html_karoshi/images/theme_preview/*
do

STYLESHEETCHOICE=`basename $THEMES | sed 's/.png//g'`
if [ $STYLESHEETCHOICE != $STYLESHEET ]
then
echo '<td style="width: 90px; vertical-align: top; height: 160px; text-align: left;"><a class="info" href="javascript:void(0)"><input name="_THEMECHOICE_'$STYLESHEETCHOICE'_" type="image" class="images" src="/images/theme_preview/'$STYLESHEETCHOICE'.png" value="_THEMECHOICE_'$STYLESHEETCHOICE'_"><span>'$STYLESHEETCHOICE'</span></a></td>'
let STYLECOUNT=$STYLECOUNT+1
fi
if [ $STYLECOUNT = $MAXSTYLES ]
then
echo '</tr><tr>'
STYLECOUNT=1
fi
done
[ $STYLECOUNT = 1 ] && echo "<td></td>"
echo '</tr></tbody></table><br></div></form></body></html>'
exit
