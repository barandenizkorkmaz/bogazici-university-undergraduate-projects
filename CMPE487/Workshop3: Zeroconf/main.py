import socket
import os
import time
import threading
import subprocess
import json
from datetime import datetime
import netifaces
import re
from _thread import *
import select

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
    os.system('arp -a > BDKChat_Arp_Out.txt')
    file = open('BDKChat_Arp_Out.txt', 'r')
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
    time.sleep(1)
    os.system('clear')

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

def send_tcp_packet(packet,target_ip,port):
    try:
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
            s.settimeout(1)
            s.connect((target_ip,port))
            s.sendall(packet.encode())
            #print(packet)
            s.close()
    except:
        print("ERROR: {name} with IP: {ip} is not online anymore...\n Removing the user from contacts...".format(
            name=ONLINE_USER_LIST[target_ip], ip=target_ip))
        time.sleep(5.0)
        del ONLINE_USER_LIST[target_ip]

def listen_tcp():
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((USER_IP,PORT))
        s.listen()
        while True:
            conn, addr = s.accept()
            data = conn.recv(2048)
            if not data:
                break
            #print(data)
            packet = data.decode()
            #print(packet)
            service_manager(packet)
            conn.close()
        s.close()

def listen_udp():
    with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as s:
        s.bind(('',PORT))
        s.setblocking(0)
        while True:
            result = select.select([s],[],[])
            data = result[0][0].recv(1024)
            if not data:
                break
            #print(data)
            packet = data.decode()
            #print(packet)
            service_manager(packet)
        s.close()

def send_message():
    list_users()
    user_number = input("Please enter the number of user or press 0 to back to main menu: ")
    user_number = is_valid_user_number(user_number)
    receiver_ip = get_receiver_ip(ONLINE_USER_LIST,user_number)
    receiver_name = ONLINE_USER_LIST[receiver_ip]
    payload = input("Please type your message: ")
    packet = create_packet(USER_NAME,USER_IP,"MESSAGE",payload)
    try:
        start_new_thread(send_tcp_packet,(packet,receiver_ip,PORT))
        file_name = "BDKChat_{}_{}.txt".format(receiver_name,receiver_ip)
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        message_text = USER_NAME + ": " + payload + " at " + dt_string + "\n"
        file = open(file_name, 'a')
        file.write(message_text)
        file.close()
        time.sleep(0.5)
    except:
        pass

def service_manager(packet):
    try:
        decoded_packet = decode_packet(packet)
        sender_name = decoded_packet["NAME"]
        sender_ip = decoded_packet["MY_IP"]
        packet_type = decoded_packet["TYPE"]
        payload = decoded_packet["PAYLOAD"]
        if sender_ip == USER_IP:
            return
        if packet_type == "DISCOVER":
            if sender_ip not in ONLINE_USER_LIST:
                print("\n\n##### BDKChat Notification #####")
                print("New User Joined: " + sender_name+"\n")
                ONLINE_USER_LIST[sender_ip] = sender_name
            packet = create_packet(USER_NAME,USER_IP,"RESPOND","")
            start_new_thread(send_tcp_packet,(packet,sender_ip,PORT))
        elif packet_type == "RESPOND":
            if sender_ip not in ONLINE_USER_LIST:
                print("\n\n##### BDKChat Notification #####")
                print("New User Detected: " + sender_name + "\n")
                ONLINE_USER_LIST[sender_ip] = sender_name
        elif packet_type == "MESSAGE":
            print("\n\n##### BDKChat Notification #####")
            print("You have one new message from: "+sender_name)
            print("Please check your inbox!\n")
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            file_name = "BDKChat_{}_{}.txt".format(sender_name,sender_ip)
            message_text = sender_name + ": " + payload + " at " + dt_string + "\n"
            file = open(file_name,'a')
            file.write(message_text)
            file.close()
        elif packet_type == "GOODBYE":
            if sender_ip in ONLINE_USER_LIST:
                print("\n\n##### BDKChat Notification #####")
                print("{name} with IP: {ip} went offline... Removing the user from contacts...".format(name=sender_name,ip=sender_ip))
                del ONLINE_USER_LIST[sender_ip]
        else:
            print("Invalid packet received!")
    except ValueError:
        print("Invalid packet received!")

def discover_network():
    if CHANNEL == 1:
        remaining = 3
        while remaining > 0:
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as s:
                s.bind(('',0)) #???
                s.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
                packet = create_packet(USER_NAME,USER_IP,"DISCOVER","")
                try:
                    s.sendto(packet.encode(),('<broadcast>',PORT))
                    remaining -= 1
                except:
                    continue
                s.close()
    else:
        hamachi_broadcast_ip = '25.255.255.255'
        remaining = 3
        while remaining > 0:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.bind(('', 0))  # ???
                s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                packet = create_packet(USER_NAME, USER_IP, "DISCOVER", "")
                try:
                    s.sendto(packet.encode(), (hamachi_broadcast_ip, PORT))
                    remaining -= 1
                except:
                    continue
                s.close()

def goodbye_network():
    if CHANNEL == 1:
        remaining = 3
        while remaining > 0:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.bind(('', 0))  # ???
                s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                packet = create_packet(USER_NAME, USER_IP, "GOODBYE", "")
                try:
                    s.sendto(packet.encode(), ('<broadcast>', PORT))
                    remaining -= 1
                except:
                    continue
                s.close()
    else:
        hamachi_broadcast_ip = '25.255.255.255'
        remaining = 3
        while remaining > 0:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.bind(('', 0))  # ???
                s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                packet = create_packet(USER_NAME, USER_IP, "GOODBYE", "")
                try:
                    s.sendto(packet.encode(), (hamachi_broadcast_ip, PORT))
                    remaining -= 1
                except:
                    continue
                s.close()


def create_packet(sender_name,sender_ip,message_type,payload):
    packet = {"NAME":sender_name,
              "MY_IP":sender_ip,
              "TYPE":message_type,
              "PAYLOAD":payload
              }
    return str(json.dumps(packet) + '\n')

def decode_packet(packet):
    packet = str(packet.rstrip())
    return json.loads(packet)

def show_profile():
    print("##### BDKChat - Profile #####")
    print("User Name: " + USER_NAME)
    print("User IP: " + USER_IP)

def list_users():
    print("##### BDKChat - Users #####")
    print_dict(ONLINE_USER_LIST)

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

def check_inbox():
    print("##### BDKChat Inbox #####")
    print_dict(ONLINE_USER_LIST)
    print("########################")
    user_number = input("Please enter the number of user or press 0 to back to main menu: ")
    user_number = is_valid_user_number(user_number)
    os.system('clear')
    user_ip = get_receiver_ip(ONLINE_USER_LIST, user_number)
    user_name = ONLINE_USER_LIST[user_ip]
    file_name = "BDKChat_{}_{}.txt".format(user_name,user_ip)
    #os.system('clear')
    print("##### BDKChat #####")
    print("Conversation History: "+user_name)
    try:
        file = open(file_name,'r')
        for line in file:
            print(line,end="")
        file.close()
    except FileNotFoundError:
        print("No messages found.")
    print("########## BDKChat ##########\n")
    tmp = input("\nPress any key for main page...")


menu = {
    1: "Show My Profile",
    2: "List Online Users",
    3: "Send a Message",
    4: "Check Inbox",
    5: "Quit"
}

def main_menu():
    os.system('clear')
    print("##### BDKChat Menu #####")
    for key in menu.keys():
        print(str(key) + "." + menu[key])
    command = int(input("Please Enter The Number of The Command: "))
    if command == 1:
        os.system('clear')
        show_profile()
        tmp = input("\nPress any key for main page...")
    elif command == 2:
        os.system('clear')
        list_users()
        tmp = input("\nPress any key for main page...")
    elif command == 3:
        os.system('clear')
        send_message()
    elif command == 4:
        os.system('clear')
        check_inbox()
    elif command == 5:
        goodbye_thread = threading.Thread(target=goodbye_network)
        goodbye_thread.start()
        goodbye_thread.join()
        print("The other users have been notified that you are leaving...")
        time.sleep(1)
        exit_program()
    else:
        print("Please Enter A Valid Command!")

print("Welcome to BDKChat!\n")
USER_NAME = input("Please Enter Your User Name: ")
os.system('clear')

CHANNEL = int(input("Welcome {}, Please Enter the Number of Your Channel: 1 or 2?\n1)Static IP\n2)Hamachi (VPN)\n".format(USER_NAME)))
os.system('clear')
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

print("\nFetching Previous Data...")
fetch_data()
time.sleep(0.5)

listen_tcp_thread = threading.Thread(target=listen_tcp)
listen_udp_thread = threading.Thread(target=listen_udp)
discover_thread = threading.Thread(target=discover_network)

listen_tcp_thread.start()
listen_udp_thread.start()
discover_thread.start()

while True:
    main_menu()