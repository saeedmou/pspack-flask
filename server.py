import os
import time
def servercommander(cmd):
    if cmd=="shutdown":
        print("Shutting Down in 1s")
        time.sleep(1)
        os.system("sudo shutdown -h now")
    elif cmd=="reboot":
        print("Rebooting in 1s")
        time.sleep(1)
        os.system("sudo reboot")
    print(cmd)
    return "OK"