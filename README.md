# FMC
Bulk Object Push API for FMC
<br>
This python code works in Python3 and I just followed step by step instruction based on the site below.
https://www.cisco.com/c/en/us/support/docs/security/firepower-management-center/215972-push-objects-in-bulk-to-fmc-using-rest-a.html

<br>
Because this web app is based on Flask framework, folders and hierarchy is important.
<br><br>
Hierarchy should be like below.
<br><br>
fmc_bulk_object.py<br>
 L templates <br>
&emsp;    L index.html <br>
&emsp;    L base.html <br>
 L static <br>
&emsp;    L securefw.jpg <br>
 L uploads <br>
&emsp;    L {files will be uploaded here}<br>
    <br>
for libraries, please install using requirements.txt
<br>
pip install -r requirements.txt
