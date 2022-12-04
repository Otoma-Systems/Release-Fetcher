import os
import platform

def WaitKeyToClose(message):
    print("-----------------------------------------------------------------------------------------------------------------------")
    print(message)
    if platform.system() == "Windows":
        os.system("pause")
        exit()
    else:
        os.system("/bin/bash -c 'read -s -n 1 -p \"Press any key to continue...\"'")
        exit()