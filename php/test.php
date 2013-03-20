<?php
$getvars = array('traffic','site','direction');


foreach($getvars as $var)
{
  if (isset($_GET[$var])) {
    $$var = $_GET[$var];
  }
}

// sanity
if(!isset($site) || !isset($traffic) || !isset($direction)) return;


$V1 ="";
$TS2 = time();
$TS1 = $TS2 - 3600 * 10;

/* If "site" is all, then do nothing.. Otherwise V1="site=XXX"
*/
if ( $site != "ALL")
{
  $V1="site=".$site;
}
/* If "traffic type" is both, then do nothing.. Otherwise V1 += ",type=YYY" (or if V1="", ignore the ","..) 
*/
if ( $traffic != "BOTH")
{
  if ( $site != "ALL")
  { 
    $V1 = $V1 . ",type=" .$site;
  }
}
/* If direction is "inbound", V2="redlining.bytes_received", else V2="redlining.bytes_sent"
*/
if ( $direction == "IN" )
{
  $V2 = "redlining.bytes_received";
}
else
{
  $V2 ="redlining.bytes_sent";
}

if ( $V1 != "" )
{
  $V1 = "{".$V1."}";
}


$ch = curl_init("http://10.1.0.67:4242/");
$fp = fopen("q?start=".$TS1."&end=".$TS2."&m=sum:".$V2.$V1."&ascii", "w");

curl_setopt($ch, CURLOPT_FILE, $fp);
curl_setopt($ch, CURLOPT_HEADER, 0);

curl_exec($ch);
curl_close($ch);
fclose($fp);
