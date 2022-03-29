import socket
from bcolors import bcolors,printColor

def send(ip, port, file):
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
    clientSocket.settimeout(3000)
    print(('try sending "' + file +'" to "' + ip + ':' + str(port) + '"'))
    # print(port)
    # print (file)
    

    try:
        clientSocket.connect((ip, port))
        with open(file, "rb") as fp:
            clientSocket.sendfile(fp)
            clientSocket.close()
    except Exception as inst:
        # print(type(inst))    # the exception instance
        # print(inst.args)     # arguments stored in .args
        # print(inst)
        if(inst.args[1]):
            printColor(bcolors.ERROR,inst.args[1])
            return inst.args[1]
        else:
            print("error")
            return "Unknown error"

    else:
        return "You're all set!"
    finally:
        clientSocket.close()
