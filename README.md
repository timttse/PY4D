# PY4D
Execute python function or script from 4D software.<br/>

4D Method: PY_EXECUTE<br/>
Parameters:<br/>
$1 - Full path to python script, or "" for  built in python functions<br/>
$2 - input function name<br/>
$3 - Pointer to  variable to contain result, or "*" if no results<br/>
${4} - Pointer to parameter(s) (optional)<br/>
$0 - error, or "" if no error<br/>
<br/><br/>
Tested for Python versions:<br/>
2.7.12<br/>
3.5.2<br/>
<br/>
Works in:<br/>
2.7.x, 3.3.x, 3.4.x, 3.5.x<br/>
<br/>
Compatible (not all features work)<br/>
3.1.x, 3.2.x<br/>
<br/>
Does not work:<br/>
2.6.x, 3.0.x<br/>
