import sys, socket, time, bitstring
from datetime import datetime

def agw_connect(s):
    s.send(b'\x00\x00\x00\x00k\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
    return

def start_socket(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print('Failed to create socket')
        time.sleep(5)
        sys.exit()
    host = str(ip)
    try:
        remote_ip = socket.gethostbyname(host)
    except socket.gaierror:
        print('Hostname could not be resolved. Exiting')
        time.sleep(5)
        sys.exit()
    try:
        s.connect((remote_ip , port))
    except ConnectionRefusedError:
        print('ConnectionRefusedError: No connection could be made because the target machine actively refused it')
        time.sleep(5)
        sys.exit()
    print('Connected to ' + str(remote_ip) + ":" + str(port))
    print("")
    return s

def telemetry_decoder(frame):
    frame=frame[48:]
    out_tmp_txt=open('tm.tmp', 'w')
    out_tmp_txt.write(str(round(float(int(bitstring.BitStream(hex=frame[:4]).read('uintle'))/1000), 3))+' V\n') # U sb1
    out_tmp_txt.write(str(round(float(int(bitstring.BitStream(hex=frame[4:8]).read('uintle'))/1000), 3))+' V\n') # U sb2
    out_tmp_txt.write(str(round(float(int(bitstring.BitStream(hex=frame[8:12]).read('uintle'))/1000), 3))+' V\n') # U sb3
    out_tmp_txt.write(str(bitstring.BitStream(hex=frame[12:16]).read('uintle'))+' mA\n') # I sb1
    out_tmp_txt.write(str(bitstring.BitStream(hex=frame[16:20]).read('uintle'))+' mA\n') # I sb2
    out_tmp_txt.write(str(bitstring.BitStream(hex=frame[20:24]).read('uintle'))+' mA\n') # I sb3
    out_tmp_txt.write(str(bitstring.BitStream(hex=frame[24:28]).read('intle'))+' mA\n') # I battery
    out_tmp_txt.write(str(bitstring.BitStream(hex=frame[28:32]).read('uintle'))+' mA\n') # I ch1
    out_tmp_txt.write(str(bitstring.BitStream(hex=frame[32:36]).read('uintle'))+' mA\n') # I ch2
    out_tmp_txt.write(str(bitstring.BitStream(hex=frame[36:40]).read('uintle'))+' mA\n') # I ch3
    out_tmp_txt.write(str(bitstring.BitStream(hex=frame[40:44]).read('uintle'))+' mA\n') # I ch4
    out_tmp_txt.write(str(bitstring.BitStream(hex=frame[44:48]).read('intle'))+' Deg. C\n') # deg. C bat 1
    out_tmp_txt.write(str(bitstring.BitStream(hex=frame[48:52]).read('intle'))+' Deg. C\n') # deg. C bat 2
    out_tmp_txt.write(str(bitstring.BitStream(hex=frame[52:56]).read('intle'))+' Deg. C\n') # deg. C bat 3
    out_tmp_txt.write(str(bitstring.BitStream(hex=frame[56:60]).read('intle'))+' Deg. C\n') # deg. C bat 4
    out_tmp_txt.write(str(round(float(int(bitstring.BitStream(hex=frame[68:72]).read('intle'))/1000), 3))+' V\n') # U battery
    out_tmp_txt.write(str(bitstring.BitStream(hex=frame[72:80]).read('uintle'))+'\n') # tlm counter
    out_tmp_txt.write(str(datetime.utcfromtimestamp(int(bitstring.BitStream(hex=frame[80:88]).read('uintle'))).strftime('%Y-%m-%d %H:%M:%S'))+' UTC\n') # ttime PS
    out_tmp_txt.write(str(bitstring.BitStream(hex=frame[88:90]).read('uintle'))+'\n') # ps resets
    out_tmp_txt.write(str(bitstring.BitStream(hex=frame[92:94]).read('intle'))+' Deg. C\n') # temp amp UHF 
    out_tmp_txt.write(str(bitstring.BitStream(hex=frame[94:96]).read('intle'))+' Deg. C\n') # temp UHF
    out_tmp_txt.write(str(bitstring.BitStream(hex=frame[104:106]).read('uintle'))+'\n') # resrts uhf
    out_tmp_txt.write(str(datetime.utcfromtimestamp(int(bitstring.BitStream(hex=frame[108:116]).read('uintle'))).strftime('%Y-%m-%d %H:%M:%S'))+' UTC\n') # time UHF
    out_tmp_txt.write(str(bitstring.BitStream(hex=frame[116:124]).read('uintle'))+' Sec.\n') # uptime 
    out_tmp_txt.write(str(bitstring.BitStream(hex=frame[124:128]).read('uintle'))+' mA\n') # I UHF
    out_tmp_txt.write(str(round(float(int(bitstring.BitStream(hex=frame[128:132]).read('uintle'))/1000), 3))+' V\n') # U UHF

    ### flags ###
    # 60-68
    #############

    data=str(bitstring.BitStream(hex=frame[60:68]).read('bin'))
    bit_arr=[data[i:i+1] for i in range(0, len(data), 1)]
    out_tmp_txt.write(str(bit_arr[0]).replace('0', 'NO').replace('1', 'YES')+'\n') #battery in critical value
    out_tmp_txt.write(str(bit_arr[1]).replace('0', 'NO').replace('1', 'YES')+'\n') #battery in minimum value
    out_tmp_txt.write(str(bit_arr[2]).replace('0', 'NO').replace('1', 'YES')+'\n') #manual control heater 2
    out_tmp_txt.write(str(bit_arr[3]).replace('0', 'NO').replace('1', 'YES')+'\n') #manual control heater 1
    out_tmp_txt.write(str(bit_arr[4]).replace('0', 'OFF').replace('1', 'ON')+'\n') #on/off heater 2
    out_tmp_txt.write(str(bit_arr[5]).replace('0', 'OFF').replace('1', 'ON')+'\n') #on/off heater 1
    out_tmp_txt.write(str(bit_arr[6]).replace('0', 'NO').replace('1', 'YES')+'\n') #temp over max
    out_tmp_txt.write(str(bit_arr[7]).replace('0', 'NO').replace('1', 'YES')+'\n') #tiny temp
    out_tmp_txt.write(str(bit_arr[8])+'\n') #status ch 4
    out_tmp_txt.write(str(bit_arr[9])+'\n') #status ch 3
    out_tmp_txt.write(str(bit_arr[10])+'\n') #status ch 2
    out_tmp_txt.write(str(bit_arr[11])+'\n') #status ch 1
    out_tmp_txt.write(str(bit_arr[12]).replace('0', 'NO').replace('1', 'YES')+'\n') #I over on ch 4
    out_tmp_txt.write(str(bit_arr[13]).replace('0', 'NO').replace('1', 'YES')+'\n') #I over on ch 3
    out_tmp_txt.write(str(bit_arr[14]).replace('0', 'NO').replace('1', 'YES')+'\n') #I over on ch 2
    out_tmp_txt.write(str(bit_arr[15]).replace('0', 'NO').replace('1', 'YES')+'\n') #I over on ch 1
    out_tmp_txt.write(str(bit_arr[24]).replace('0', 'NO').replace('1', 'YES')+'\n') #U on charger socket
    out_tmp_txt.close()
    return


def main(s):
    while True:
        frame = s.recv(1024).hex()
        frame = frame[74:]
        if(frame[:8]=='a464829c'):
            telemetry_decoder(frame)

if(__name__=='__main__'):
    ip=sys.argv[1]
    port=sys.argv[2]
    s=start_socket(ip=ip, port=int(port))
    agw_connect(s=s)
    main(s=s)