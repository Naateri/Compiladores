import re

ip_num = '([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])'
#Primer caso: 0-9
#Segundo caso: 10-99
#Tercer caso: 100-199
#Cuarto caso: 200-249
#Quinto caso: 250-255
ip_regex = '(' + ip_num + '\.){3}' + ip_num + "$"

print(ip_regex)

p = re.compile(ip_regex)
ip = "192.16.255.5"

if p.match(ip):
    print("Es una IP")
else:
    print("No es una IP")
