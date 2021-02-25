import socket
import os
import time
import threading
import subprocess
import json
from datetime import datetime
import netifaces
import re

#
# REFERENCE: https://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib/1267524
#
#
# REFERENCE2: https://stackoverflow.com/questions/270745/how-do-i-determine-all-of-my-ip-addresses-when-i-have-multiple-nics
#
def get_ip(CHANNEL):
    if CHANNEL == 1:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except Exception:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP
    else:
        ip_list = list()
        res_list = list()
        for i in netifaces.interfaces():
            for l in netifaces.ifaddresses(i).get(netifaces.AF_INET, ()):
                ip_list.append(l['addr'])
        for ip in ip_list:
            res = re.search(r'\b25(\.[0-9]{1,3}){3}\b', ip)
            if not(res is None):
                res_list.append(res.group())
        if len(res_list) == 1:
            return res_list[0]
        else:
            for i,ip in enumerate(res_list):
                print("{:d}) {}".format(i+1,ip))
            ip_num = int(input("Please enter the number of your IP: "))
            return res_list[ip_num-1]

def collect_lan_ips():
    os.system('arp -a > BDKChat_arp.txt')
    file = open('BDKChat_arp.txt', 'r')
    for line in file:
        if 'on ham' in line:
            res = re.search(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', line)
            lan_ip = res.group()
            LAN_ADDRESSES.append(lan_ip)

def previous_data_exists():
    return os.path.exists(os.getcwd()+"/BDKChat_user_data.txt")

def fetch_data():
    if previous_data_exists() == True:
        print("Previous Data Found!")
        file = open("BDKChat_user_data.txt", "r")
        for line in file:
            parsed_line = line.strip().split(sep=",")
            if len(parsed_line)<2:
                continue
            ONLINE_USER_LIST[parsed_line[0]] = parsed_line[1]
        file.close()
        print("Online user list has been updated!")
    else:
        print("Previous Data Not Found!")

def save_data():
    file = open("BDKChat_user_data.txt", "w")
    for key in ONLINE_USER_LIST.keys():
        value = ONLINE_USER_LIST[key]
        data = key + "," + value + "\n"
        file.write(data)
    file.close()

#
# REFERENCE: https://stackoverflow.com/questions/1265665/how-can-i-check-if-a-string-represents-an-int-without-using-try-except
#
def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def exit_program():
    save_data()
    print("\nGood Bye {}".format(USER_NAME))
    time.sleep(2)
    subprocess.call(['pkill','-f','main.py'])

def listen_port():
    global PROC_PID
    stdout = b""
    while LISTEN_BOOL:
        ### Other option: nc -l -k PORT
        ps = subprocess.Popen(['netcat', '-l', str(PORT)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        PROC_PID = ps.pid
        stdout, stderr = ps.communicate()
        packet = stdout.decode('utf8')[:-1]
        service_manager(packet)

def discover_network():
    if CHANNEL == 1:
        for i in range(255):
            target_ip = USER_NETWORK + "." + str(i)
            if not(USER_IP == target_ip):
                packet = create_packet(USER_NAME,USER_IP,"DISCOVER","")
                try:
                    ps = subprocess.Popen(['echo',packet], stdout=subprocess.PIPE)
                    out = subprocess.check_output(['netcat','-w','1',target_ip,str(PORT)],stdin=ps.stdout)
                    ps.wait()
                except subprocess.CalledProcessError as exc:
                    continue
    else:
        for ip in LAN_ADDRESSES:
            packet = create_packet(USER_NAME, USER_IP, "DISCOVER", "")
            try:
                ps = subprocess.Popen(['echo', packet], stdout=subprocess.PIPE)
                out = subprocess.check_output(['netcat', '-w', '1', ip, str(PORT)], stdin=ps.stdout)
                ps.wait()
            except subprocess.CalledProcessError as exc:
                continue
    #time.sleep(60)

def create_packet(sender_name,sender_ip,message_type,payload):
    packet = {"NAME":sender_name,
              "MY_IP":sender_ip,
              "TYPE":message_type,
              "PAYLOAD":payload
              }
    return json.dumps(packet)

def decode_packet(packet):
    return json.loads(packet)

def show_profile():
    print("\n##### BDKChat - Profile #####")
    print("User Name: " + USER_NAME)
    print("User IP: " + USER_IP)
    print("########## BDKChat ##########\n")

def list_users():
    print("\n##### BDKChat - Users #####")
    print_dict(ONLINE_USER_LIST)
    print("########## BDKChat ##########\n")

def print_dict(dict):
    for i,key in enumerate(dict.keys()):
        print(str(i+1)+") Name: "+dict[key]+" IP: "+key)

def get_receiver_ip(dict,num):
    if RepresentsInt(num) == False:
        return None
    num = int(num)
    if num <= 0:
        return None
    for i,key in enumerate(dict.keys()):
        if num-1 == i:
            return key
    return None

def is_valid_user_number(user_number):
    while RepresentsInt(user_number)== False or get_receiver_ip(ONLINE_USER_LIST,user_number) is None:
        if (RepresentsInt(user_number) == True):
            if int(user_number) == 0:
                main_menu()
                time.sleep(0.5)
            elif not(get_receiver_ip(ONLINE_USER_LIST,user_number) is None):
                pass
            else:
                user_number = input("Please enter a valid user number or press 0 to back to main menu: ")
        else:
            user_number = input("Please enter a valid user number or press 0 to back to main menu: ")
    return user_number

def send_message():
    list_users()
    user_number = input("Please enter the number of user or press 0 to back to main menu: ")
    user_number = is_valid_user_number(user_number)
    receiver_ip = get_receiver_ip(ONLINE_USER_LIST,user_number)
    receiver_name = ONLINE_USER_LIST[receiver_ip]
    payload = input("Please type your message: ")
    packet = create_packet(USER_NAME,USER_IP,"MESSAGE",payload)
    try:
        file_name = "BDKChat_{}_{}.txt".format(receiver_name,receiver_ip)
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        message_text = USER_NAME + ": " + payload + " at " + dt_string + "\n"
        file = open(file_name, 'a')
        file.write(message_text)
        file.close()
        ps = subprocess.Popen(['echo',packet], stdout=subprocess.PIPE)
        out = subprocess.check_output(['netcat','-w','1',receiver_ip,str(PORT)], stdin=ps.stdout)
        ps.wait()
    except subprocess.CalledProcessError as exc:
        print("ERROR: The user is not online or wrong IP. Deleting the user.")
        del ONLINE_USER_LIST[receiver_ip]

def service_manager(packet):
    decoded_packet = decode_packet(packet)
    sender_name = decoded_packet["NAME"]
    sender_ip = decoded_packet["MY_IP"]
    packet_type = decoded_packet["TYPE"]
    payload = decoded_packet["PAYLOAD"]
    if packet_type == "DISCOVER":
        print("\n##### BDKChat Notification #####")
        print("New User Joined: " + sender_name+"\n")
        ONLINE_USER_LIST[sender_ip] = sender_name
        packet = create_packet(USER_NAME,USER_IP,"RESPOND","")
        try:
            ps = subprocess.Popen(['echo', packet], stdout=subprocess.PIPE)
            out = subprocess.check_output(['netcat', '-w', '1', sender_ip, str(PORT)], stdin=ps.stdout)
            ps.wait()
        except subprocess.CalledProcessError as exc:
            print(exc)
    elif packet_type == "RESPOND":
        print("\n##### BDKChat Notification #####")
        print("New User Detected: " + sender_name + "\n")
        ONLINE_USER_LIST[sender_ip] = sender_name
    elif packet_type == "MESSAGE":
        print("\n##### BDKChat Notification #####")
        print("You have one new message from: "+sender_name)
        print("Please check your inbox!")
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        file_name = "BDKChat_{}_{}.txt".format(sender_name,sender_ip)
        message_text = sender_name + ": " + payload + " at " + dt_string + "\n"
        file = open(file_name,'a')
        file.write(message_text)
        file.close()
    else:
        print("Invalid packet received!")
        pass

def check_inbox():
    print("\n##### BDKChat Inbox #####")
    print_dict(ONLINE_USER_LIST)
    print("########################")
    user_number = input("Please enter the number of user or press 0 to back to main menu: ")
    user_number = is_valid_user_number(user_number)
    user_ip = get_receiver_ip(ONLINE_USER_LIST, user_number)
    user_name = ONLINE_USER_LIST[user_ip]
    file_name = "BDKChat_{}_{}.txt".format(user_name,user_ip)
    print("\n##### BDKChat #####")
    print("Conversation History: "+user_name)
    try:
        file = open(file_name,'r')
        for line in file:
            print(line,end="")
        file.close()
    except FileNotFoundError:
        print("No messages found.")
    print("########## BDKChat ##########\n")


menu = {
    1: "Show My Profile",
    2: "List Online Users",
    3: "Send a Message",
    4: "Check Inbox",
    5: "Quit"
}

def main_menu():
    global LISTEN_BOOL
    print("\n##### BDKChat Menu #####")
    for key in menu.keys():
        print(str(key) + "." + menu[key])
    command = int(input("Please Enter The Number of The Command: "))
    if command == 1:
        show_profile()
    elif command == 2:
        list_users()
    elif command == 3:
        send_message()
    elif command == 4:
        check_inbox()
    elif command == 5:
        LISTEN_BOOL = False
        subprocess.run(['kill', '-9', str(PROC_PID)])
        #subprocess.call(['kill', '-9', str(PROC_PID)])
        exit_program()
    else:
        print("Please Enter A Valid Command!")

print("Welcome to BDKChat!\n")
USER_NAME = input("Please Enter Your User Name: ")

CHANNEL = int(input("Welcome {}, Please Enter the Number of Your Channel: 1 or 2?\n1)Static IP\n2)Hamachi (VPN)\n".format(USER_NAME)))

"""
#
# GLOBAL VARIABLES
#
"""
PORT = 12345
USER_IP = get_ip(CHANNEL)
PARSED_USER_IP = USER_IP.split(sep=".")
USER_NETWORK = PARSED_USER_IP[0] + "." + PARSED_USER_IP[1] + "." + PARSED_USER_IP[2]
ONLINE_USER_LIST = {}
LAN_ADDRESSES = list()
PROC_PID = -1
LISTEN_BOOL = True
""""""

if CHANNEL == 2:
    collect_lan_ips()

print("\nFetching Previous Data...")
fetch_data()
time.sleep(0.5)

listen_thread = threading.Thread(target=listen_port,daemon=True)
discover_thread = threading.Thread(target=discover_network)

listen_thread.start()
discover_thread.start()

while True:
    main_menu()