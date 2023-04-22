import serial
import re
s = serial.Serial('com11', 115200)

st = ''
while True:

    while True:
        char = str(s.read(), 'utf-8')
        #print(char)
        try:
            #print(char)
            st = st+char

        except:
            continue
        if(char == '\n'):
            break
    try:
        ipList = re.findall(r'[0-9]+(?:\.[0-9]+){3}', st)
        print(ipList[0])
        break
    except:
        continue
