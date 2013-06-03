<?php
//====================================================================================
// OCS INVENTORY REPORTS
// Copyleft Erwan GOALOU 2010 (erwan(at)ocsinventory-ng(pt)org)
// Web: http://www.ocsinventory-ng.org
//
// This code is open source and may be copied and modified as long as the source
// code is always made freely available.
// Please refer to the General Public Licence http://www.gnu.org/ or Licence.txt
//====================================================================================
require('require/function_stats.php');

$form_name="stats";
$table_name=$form_name;	
printEnTete($l->g(1251));
echo "<form name='".$form_name."' id='".$form_name."' method='POST' action=''>";
$plugin=false;
$stats='';
foreach ($_SESSION['OCS']['URL'] as $name=>$lbl){
	if (substr($name,0,9) == 'ms_stats_' and $_SESSION['OCS']['DIRECTORY'][$name] == 'ms_stats'){
		$plugin=true;
		require_once($name.".php");
	}	
}

if ($plugin){
	//Create the chart - Column 3D Chart with data from strXML variable using dataXML method
	onglet($data_on,$form_name,"onglet",4);
	echo '<div class="mlt_bordure" >';
	echo $stats;		
	echo "</div>";
}else
	msg_warning($l->g(1262));
echo "</form>";

?>