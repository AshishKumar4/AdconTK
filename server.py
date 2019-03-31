# Author : WhiteOracle


from cmdFile import *
import time


cc = cmdFile('demo3')
while True:
    s = input(">>")
    cc.putCommand(s)
    time.sleep(2)
    p = cc.getLastOutput()
    while len(p) == 0:
        p = cc.getLastOutput()
    print("\n")
    print(str(p.decode("utf-8")))
