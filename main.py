import subprocess  # to use the ping command
import threading  # to make ip
import time  # to sleep
import socket  # to test ips


def test_ip(s):  # to test if a string is an ip or no
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


def pinger(i):  # function to ping an ip, if the ip responds then it will be added to the list
	global ip_list
	address = his_ip + str(i)
	ping = "ping -n 4 -w 2000 " + address

	res = subprocess.Popen(ping, shell=True, stdout=subprocess.PIPE)
	h = str(res.communicate())

	count = h.count("timed out") + h.count("unreach")
	if count != 4:  # the ip will get pinged xx times, so if we have less than xx "time outs" and "unreachables" then the ip is up

		ip_list.add(address)


def get_ip():
	global his_ip
	his_ip = socket.gethostbyname(socket.gethostname())  # getting the local ip
	his_input = ""
	while not (his_input in ["yes",
	                         "no"]):  # testing if the ip is correct because sometimes the laptop may have multiple local ips
		his_input = input(str("is this your local ip " + his_ip + ": "))
	if his_input == "no":  # getting the correct ip
		his_ip = ""
		while not (test_ip(his_ip)):
			his_ip = input(str("please write down your ip"))

	his_ip = his_ip.split(".")
	his_ip = his_ip[0] + "." + his_ip[1] + "." + his_ip[
		2] + "."  # converting ip from like this 192.168.1.5 to like this 192.168.1. (remove the 5 in the end)


first_execution = True
his_ip = ""
ip_list = set()  # this will contain the connected ips
get_ip()

while 1:
	old_list = ip_list.copy()
	ip_list = set()  # rempty the set
	print("starting, please wait..")
	try:
		for ping in range(2, 254):  # starting a thread for every ip
			time.sleep(0.01)
			while threading.activeCount() > 100:
				time.sleep(1)

			threading.Thread(target=pinger, args=(ping,)).start()



	except:
		print("Error: unable to start thread")
		exit(-1)

	time.sleep(3)
	while threading.activeCount() > 1:  # waiting for the ping threads to finish
		time.sleep(2)

	connected = ip_list - old_list  # list of new connected devices
	disconnected = old_list - ip_list  # list of disconnected devices

	if first_execution:
		first_execution = False
		print(str(str(connected) + "are connected initially"))


	else:

		if old_list == ip_list:
			print("no one connected nor disconnected")

		else:
			if len(connected) != 0:
				print(connected)
				print("connected")
			if len(disconnected) != 0:
				print(disconnected)
				print("disconnected")
	print("sleeping for 10 seconds")
	time.sleep(10)
