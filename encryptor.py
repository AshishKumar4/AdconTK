from Crypto.Cipher import AES
import sys
import base64

print("\nEnter password to encrypt with\n")
encrypt = AES.new(sys.stdin.readline().replace("\n", ''), AES.MODE_CBC, "This is an IV456")
f = open("client.py", "rb")
s  = f.read()
b = base64.b64encode(s)
b += b'='*(16 - (len(b)%16))
h = encrypt.encrypt(b)
g = base64.b64encode(h)
ff = open('ff.py', 'wb')
ff.write(g)
ff.close()
print("\nEncrypted! saved as ff.py")