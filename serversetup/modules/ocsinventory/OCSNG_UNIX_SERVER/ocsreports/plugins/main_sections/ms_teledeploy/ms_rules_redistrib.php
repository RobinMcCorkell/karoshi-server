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

/*
 * Rules for redistribution servers
 */
if ($_SESSION['OCS']["use_redistribution"] == 1){
	require_once('require/function_rules.php');
	printEnTete($l->g(673));
	echo "<br>";
	//only for Super Admin
	//DEL RULE
	if ($protectedPost['SUP_PROF'] != ""){	
		delete_rule($protectedPost['SUP_PROF']);
		$tab_options['CACHE']='RESET';
	}
	//ADD new rule
	if ($protectedPost['ADD_RULE']){
		add_rule($protectedPost['RULE_NAME'],$protectedPost);
		$tab_options['CACHE']='RESET';
	}
	//modif rule
	if ($protectedPost['MODIF_RULE']){	
		$name_exist=verify_name($protectedPost['RULE_NAME'],"and rule != ".$protectedPost['OLD_MODIF']);
		if ($name_exist == 'NAME_NOT_EXIST'){
			delete_rule($protectedPost['OLD_MODIF']);
			add_rule($protectedPost['RULE_NAME'],$protectedPost,$protectedPost['OLD_MODIF']);
			echo msg_success($l->g(711));
			$tab_options['CACHE']='RESET';
		}
		else{
			msg_error($l->g(670));
		}
	}
	//form name
	$form_name = "rules";
	//show all rules
	echo "<form name='".$form_name."' id='".$form_name."' method='POST' action=''>";
				$list_fields= array('ID_RULE'=>'RULE',
									'RULE_NAME'=>'RULE_NAME',
									'SUP'=>'RULE',
									'MODIF'=>'RULE',
									);
				$table_name="DOWNLOAD_AFFECT_RULES";
				$default_fields= array('ID_RULE'=>'ID_RULE','RULE_NAME'=>'RULE_NAME','SUP'=>'SUP','MODIF'=>'MODIF');
				$list_col_cant_del=array('ID_RULE'=>'ID_RULE','SUP'=>'SUP','MODIF'=>'MODIF');
				$sql=prepare_sql_tab($list_fields,array('SUP'));
				
				$sql['SQL'] .= " from download_affect_rules ";
				$tab_options['ARG_SQL']=$sql['ARG'];
				$result_exist=tab_req($table_name,$list_fields,$default_fields,$list_col_cant_del,$sql['SQL'],$form_name,80,$tab_options); 
				echo "<br>";
		
	//Modif a rule => get this values 
	if ($protectedPost['MODIF'] != "" and $protectedPost['OLD_MODIF'] != $protectedPost['MODIF']){
		$sql="select priority,cfield,op,compto,rule_name 
				from download_affect_rules 
			 where rule='%s' 
				order by priority";
		$arg=$protectedPost['MODIF'];
		$res = mysql2_query_secure( $sql, $_SESSION['OCS']["readServer"],$arg);
		$i=1;
		while ($val = mysql_fetch_array( $res )){
			$protectedPost['PRIORITE_'.$i]=$val['priority'];
			$protectedPost['CFIELD_'.$i]=$val['cfield'];
			$protectedPost['OP_'.$i]=$val['op'];
			$protectedPost['COMPTO_'.$i]=$val['compto'];
			$protectedPost['RULE_NAME']=$val['rule_name'];
			$i++;
		}
		$protectedPost['NUM_RULES']=$i-2;
	}
	
	//new rule
	if ($protectedPost['NEW_RULE'] or $protectedPost['NUM_RULES'] or $protectedPost['MODIF'] != ""){
		if ($protectedPost['MODIF'] != "")
		$modif=$protectedPost['MODIF'];
		else
		$modif=$protectedPost['OLD_MODIF'];
		$numero=$protectedPost['NUM_RULES']+1;
		$tab_nom=$l->g(674)." ".show_modif($protectedPost['RULE_NAME'],"RULE_NAME","0");
		$tab="<table align='center'>";
		$i=1;
		while($i<$numero+1){
			if ($i==1)
			$entete='YES';
			else
			$entete='NO';
		$tab.=fields_conditions_rules($i,$entete);
		$i++;
		}
		echo $tab_nom;
		echo $tab;
		echo "</tr></table>";
		echo "<a onclick='return pag(".$numero.",\"NUM_RULES\",\"rules\")'><font color=green>".$l->g(682)."</font></a>&nbsp<a onclick='return pag(\"RAZ\",\"RAZ\",\"rules\");'><font color=\"red\">".$l->g(113)."</font></a><br><br>";
		if ($protectedPost['MODIF'] != "" or $protectedPost['OLD_MODIF'] != "")
		echo "<input type='submit'  value='".$l->g(625)."' name='MODIF_RULE' onclick='return check();'>";	
		else
		echo "<input type='submit'  value='".$l->g(683)."' name='ADD_RULE' onclick='return check();'>";	
		echo "<input type='hidden' id='NUM_RULES' name='NUM_RULES' value=''>";
		echo "<input type='hidden' id='RAZ' name='RAZ' value=''>";
		echo "<input type='hidden' id='OLD_MODIF' name='OLD_MODIF' value='".$modif."'>";
	}else{	
	echo "<input type='submit'  value='".$l->g(685)."' name='NEW_RULE'>";	
	}
	echo "</form>";
}else{
	msg_info($l->g(1182));
}
?>
