
from .ccavutil import encrypt,decrypt
from string import Template

def res(encResp):
	print("called res")
	'''
	Please put in the 32 bit alphanumeric key in quotes provided by CCAvenues.
	'''	 
	workingKey = 'B9924C2160DF36BB91F30C6065758B86'
	decResp = decrypt(encResp,workingKey)
	print('this is resp',decResp)
	data = '<table border=1 cellspacing=2 cellpadding=2><tr><td>'	
	data = data + decResp.replace('=','</td><td>')
	data = data.replace('&','</td></tr><tr><td>')
	data = data + '</td></tr></table>'
	
	html = '''\
	<html>
		<head>
			<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
			<title>Response Handler</title>
		</head>
		<body>
			<center>
				<font size="4" color="blue"><b>Response Page</b></font>
				<br>
				$response
			</center>
			<br>
		</body>
	</html>
	'''
	fin = Template(html).safe_substitute(response=data)
	print(fin)
	return fin
