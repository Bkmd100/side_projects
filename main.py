import subprocess
import threading
import time
import socket


def test_ip(s):
    a = s.split('.')
    if len(a) != 4:
        return False
    for x in a:
        if not x.isdigit():
            return False
        i = int(x)
        if i < 0 or i > 255:
            return False
    return True


list = set()

his_ip = socket.gethostbyname(socket.gethostname())
his_input = ""
while not (his_input in ["yes", "no"]):
    his_input = input(str("is this your local ip " + his_ip + ": "))
if his_input == "no":
    his_ip = ""
    while not (test_ip(his_ip)):
        his_ip = input(str("please write down your ip"))

his_ip = his_ip.split(".")
his_ip = his_ip[0] + "." + his_ip[1] + "." + his_ip[2] + "."
print(his_ip)
first_execution = True


def pinger(i):
    global list
    address = his_ip + str(i)
    ping = "ping -n 4 -w 2000 " + address
    # print(ping)
    res = subprocess.Popen(ping, shell=True, stdout=subprocess.PIPE)
    h = str(res.communicate())
    # print(h)
    count = h.count("timed out") + h.count("unreach")
    if count != 4:
        # print( "ping to", address, "OK")
        list.add(address)


while 1:
    old_list = list.copy()
    list = set()  # rempty the set
    try:
        for ping in range(2, 254):
            time.sleep(0.01)
            while threading.activeCount() > 100:
                time.sleep(1)

            threading.Thread(target=pinger, args=(ping,)).start()



    except:
        print("Error: unable to start thread")

    time.sleep(3)
    while threading.activeCount() > 1:
        time.sleep(2)

    connected = list - old_list
    disconnected = old_list - list
    print(threading.activeCount())
    if not (first_execution):

        if (old_list == list):
            print("no one connected nor disconnected, sleeping for 10 seconds")
            time.sleep(10)
        else:
            if (len(connected) != 0):
                print(connected)
                print("connected")
            if (len(disconnected) != 0):
                print(disconnected)
                print("disconnected")




    else:
        first_execution = False
        print(connected)
        print("are connected initially")


