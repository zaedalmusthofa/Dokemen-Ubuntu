from threading import Thread
import time
import os


def startprgm(i):
    os.system(i)
    time.sleep(1)


if __name__ == '__main__':
    commit = ['sudo python3 /home/pi/raspberry_pi4_streaming_server.py']
    for i in commit:
        thread = Thread(target=startprgm, args=(i,))
        thread.start()
