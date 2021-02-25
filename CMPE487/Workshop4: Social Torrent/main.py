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
import sys
import hashlib
import base64
#
# REFERENCE: https://stackoverflow.com/questions/1265665/how-can-i-check-if-a-string-represents-an-int-without-using-try-except
#
def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def chunksowned_str_to_list(payload_str):
    if payload_str == "":
        return []
    my_list = str(payload_str).split('|')
    chunks_owned = list()
    for token in my_list:
        id_list = token.split(':')
        if len(id_list) == 1:
            chunks_owned.append(int(id_list[0]))
        else:
            start = int(id_list[0])
            stop = int(id_list[1])
            for i in range(start,stop+1):
                chunks_owned.append(i)
    return chunks_owned

def list_to_chunksowned_str(chunks_owned):
    if len(chunks_owned) ==0 :
        return str()
    start = chunks_owned[0]
    stop = chunks_owned[0]
    payload_str = str()
    for i,elem in enumerate(chunks_owned):
        if i == len(chunks_owned) - 1:
            if start == stop:
                payload_str += str(elem)
            else:
                payload_str += "{}:{}".format(start,elem)
            continue
        next = chunks_owned[i+1]
        if elem + 1 == next:
            stop = next
        else:
            if start == stop:
                payload_str += "{}|".format(stop)
            else:
                payload_str += "{}:{}|".format(start,stop)
            start = next
            stop = next
    return payload_str

#
# REFERENCE: https://www.pythoncentral.io/hashing-strings-with-python/
#
def get_hash(chuck_properties):
    hash_object = hashlib.sha1(chuck_properties.encode())
    return hash_object.hexdigest()[0:32]
#
# REFERENCES:
# https://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib/1267524
# https://stackoverflow.com/questions/270745/how-do-i-determine-all-of-my-ip-addresses-when-i-have-multiple-nics
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
    global LAN_ADDRESSES
    os.system('arp -a > BetaZero++_Arp_Out.txt')
    file = open('BetaZero++_Arp_Out.txt', 'r')
    for line in file:
        if 'on ham' in line:
            res = re.search(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', line)
            lan_ip = res.group()
            LAN_ADDRESSES.append(lan_ip)

def previous_data_exists():
    return os.path.exists(os.getcwd()+"/BetaZero++_user_data.txt")

def fetch_data():
    if previous_data_exists() == True:
        print("Previous Data Found!")
        file = open("BetaZero++_user_data.txt", "r")
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
    file = open("BetaZero++_user_data.txt", "w")
    for key in ONLINE_USER_LIST.keys():
        value = ONLINE_USER_LIST[key]
        data = key + "," + value + "\n"
        file.write(data)
    file.close()

def get_manifest(directory="My_Files"):
    global hash_serials
    manifest = dict()
    files = []
    if not os.path.exists(os.path.join(os.getcwd(),directory)):
        os.makedirs(directory)
        return dict()
    folder = os.path.join(os.getcwd(),directory)
    for (dirpath, dirnames, filenames) in os.walk(folder):
        files.extend(filenames)
        break
    for file in files:
        manifest[file] = list()
    for file in files:
        with open(os.path.join(folder,file), 'rb') as f:
            count = 0
            while True:
                byte_s = base64.b64encode(f.read(900)).decode("utf-8")
                if not byte_s:
                    break ## QUESTION ismet: Do not we increase count by 1 before break
                line = byte_s.split('\x00')
                line = list(filter(None, line))
                if len(line) != 0:
                    manifest[file].append(count+1)
                count += 1
    # Update Hash Serials
    for file in manifest:
        for chunk_id in manifest[file]:
            hash_file = get_hash(file + str(chunk_id))
            hash_serials[hash_file] = {"FILE_NAME": file, "CHUNK_ID": chunk_id}
    return manifest

def exit_program():
    save_data()
    print("\nGood Bye {}".format(USER_NAME))
    time.sleep(2)
    subprocess.call(['pkill','-f','main.py'])

def send_udp_packet(packet, receiver_ip):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(('', 0))  # ???
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        try:
            s.sendto(packet.encode(), (receiver_ip, PORT))
        except Exception as e:
            print("Exception in send_udp_packet: {}".format(e))
        s.close()

def send_tcp_packet(packet,target_ip,port):
    try:
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
            s.settimeout(1)
            s.connect((target_ip,port))
            s.sendall(packet.encode())
            s.close()
    except:
        print("\nERROR: IP {} is not online anymore...\nRemoving the user from contacts...".format(target_ip))
        try:
            del ONLINE_USER_LIST[target_ip]
        except:
            pass

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
            packet = data.decode()
            service_manager_tcp(packet)
            conn.close()
        s.close()

def listen_udp():
    with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as s:
        s.bind(('',PORT))
        s.setblocking(0)
        while True:
            result = select.select([s],[],[])
            data = result[0][0].recv(1500)
            if not data:
                break
            packet = data.decode()
            buffer_manager(packet)
        s.close()

def buffer_manager(packet):
    global BUFFER_LIST
    if get_rwnd() > 1048576:
        BUFFER_LIST.append(packet)
    else:
        print("Buffer does not have enough space!")

def get_rwnd():
    global BUFFER_LIST
    rwnd = MAX_BUFFER_SIZE - sys.getsizeof(BUFFER_LIST)
    return rwnd

def send_message():
    list_users()
    user_number = input("Please enter the number of user or press 0 to back to main menu: ")
    user_number = is_valid_user_number(user_number)
    if user_number == 0:
        return
    receiver_ip = get_receiver_ip(ONLINE_USER_LIST, user_number)
    receiver_name = ONLINE_USER_LIST[receiver_ip]
    payload = input("Please type your message: ")
    packet = create_packet(USER_NAME, USER_IP, "MESSAGE", payload)
    try:
        start_new_thread(send_tcp_packet, (packet, receiver_ip, PORT))
        file_name = "BetaZero++_{}_{}.txt".format(receiver_name, receiver_ip)
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        message_text = USER_NAME + ": " + payload + " at " + dt_string + "\n"
        file = open(file_name, 'a')
        file.write(message_text)
        file.close()
        time.sleep(0.5)
    except:
        pass

def service_manager_udp():
    global manifest
    global hash_serials
    global BUFFER_LIST
    while True:
        if len(BUFFER_LIST) == 0:
            continue
        packet = BUFFER_LIST.pop(0)
        try:
            decoded_packet = decode_packet(packet)
            packet_type = decoded_packet["TYPE"]
            if packet_type == "FILE":
                # TODO: Save the chunk in a file
                # TODO: Update seed_list (remove the corresponding chunk_id from the chunks_pending!)
                seed_ip = decoded_packet["MY_IP"]
                # file_name and chunk_id will be derived from decoded_packet[SERIAL] by de-hashing.
                serial = decoded_packet["SERIAL"]
                chunk_id =  hash_serials[serial]["CHUNK_ID"]
                file_name =  hash_serials[serial]["FILE_NAME"]
                chunk_content = decoded_packet["PAYLOAD"].encode("utf-8")
                # Write chunk_content into corresponding chunk of file!
                file_path="My_Files/"+str(file_name)
                if not os.path.exists(file_path):
                    file= open(file_path,"w+")
                    file.close()
                fileData = base64.b64decode(chunk_content)
                with open(file_path, 'r+b') as f2:
                    f2.seek((chunk_id-1)*900, 0)
                    f2.write(fileData)
                print("\nFILE: {}\nSEED: {}\nSERIAL: {}\n".format(file_name,seed_ip,serial))
                send_ack_thread = threading.Thread(target=send_ack_packet, args=(serial,))
                send_ack_thread.start()
                send_ack_thread.join()
                # Update seed_list
                try:
                    seed_list[file_name][seed_ip].remove(chunk_id)
                except:
                    pass
                if len(seed_list[file_name][seed_ip])==0:
                    send_terminate_thread = threading.Thread(target=send_terminate_packet, args=(USER_NAME,USER_IP,'TERMINATE',file_name,seed_ip))
                    send_terminate_thread.start()
                    send_terminate_thread.join()
                    print("DOWNLOAD COMPLETED!\nFILE: {}\n".format(file_name))
            elif packet_type == "ACK":
                leech_ip = decoded_packet["MY_IP"]
                serial = decoded_packet["SERIAL"]
                rwnd = decoded_packet["RWND"]
                print("\nACK:\nIP: {}\nSERIAL: {}\nRWND: {}\n".format(leech_ip,serial,rwnd))
                file_name = hash_serials[serial]["FILE_NAME"] if serial != -1 else ""
                chunk_id = hash_serials[serial]["CHUNK_ID"] if serial != -1 else -1
                if chunk_id != -1 and chunk_id not in receiver_acknowledged_chunks[leech_ip][file_name]:
                    receiver_acknowledged_chunks[leech_ip][file_name].append(chunk_id)
                receiver_remaining_window_sizes[leech_ip] = rwnd
            else:
                print("Invalid Packet Type: {}\n".format(packet_type))
        except Exception as exc:
                print("Exception in service_manager: ",exc)

def service_manager_tcp(packet):
    global manifest
    global hash_serials
    try:
        decoded_packet = decode_packet(packet)
        packet_type = decoded_packet["TYPE"]
        if packet_type == "DISCOVER":
            sender_ip = decoded_packet["MY_IP"]
            if sender_ip == USER_IP:
                return
            sender_name = decoded_packet["NAME"]
            sender_ip = decoded_packet["MY_IP"]
            if sender_ip not in ONLINE_USER_LIST:
                print("\n\n##### BetaZero++ Notification #####")
                print("New User Discovered: " + sender_name+"\n")
                ONLINE_USER_LIST[sender_ip] = sender_name
            packet = create_packet(USER_NAME,USER_IP,"RESPOND","")
            start_new_thread(send_tcp_packet,(packet,sender_ip,PORT))
        elif packet_type == "RESPOND":
            sender_name = decoded_packet["NAME"]
            sender_ip = decoded_packet["MY_IP"]
            if sender_ip not in ONLINE_USER_LIST:
                print("\n\n##### BetaZero++ Notification #####")
                print("New User Responded: " + sender_name + "\n")
                ONLINE_USER_LIST[sender_ip] = sender_name
        elif packet_type == "MESSAGE":
            sender_name = decoded_packet["NAME"]
            sender_ip = decoded_packet["MY_IP"]
            payload = decoded_packet["PAYLOAD"]
            print("\n\n##### BetaZero++ Notification #####")
            print("You have one new message from: "+sender_name)
            print("Please check your inbox!\n")
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            file_name = "BetaZero++_{}_{}.txt".format(sender_name,sender_ip)
            message_text = sender_name + ": " + payload + " at " + dt_string + "\n"
            file = open(file_name,'a')
            file.write(message_text)
            file.close()
        elif packet_type == "MANIFEST":
            global shared_manifests
            sender_ip = decoded_packet["MY_IP"]
            sender_name = decoded_packet["NAME"]
            manifest_payload = decoded_packet["PAYLOAD"]
            manifest_dict = manifest_payload
            for key in manifest_dict:
                manifest_dict[key] = chunksowned_str_to_list(manifest_payload[key])
            ## we need to load string and convert it to directory format then add it into shared_manifests
            shared_manifests[sender_ip] = manifest_dict
            for file_name in manifest_dict:
                for chunk_id in manifest_dict[file_name]:
                    serial = get_hash(file_name + str(chunk_id))
                    hash_serials[serial] = {"FILE_NAME":file_name,"CHUNK_ID":chunk_id}
            print("Manifest is received from {}.".format(sender_name))
        elif packet_type == "REQ_MANIFEST":
            receiver_ip = decoded_packet["MY_IP"]
            receiver_name = decoded_packet["NAME"]
            print("Manifest is requested by {}.".format(receiver_name))
            send_manifest(receiver_ip)
        elif packet_type == "REQ_DOWNLOAD":
            global manifest
            manifest = get_manifest()
            leech_ip = decoded_packet["MY_IP"]
            file_name = decoded_packet["FILE_NAME"]
            chunks_receiver_owned = decoded_packet["CHUNKS_OWNED"]
            chunks_receiver_owned = chunksowned_str_to_list(chunks_receiver_owned)
            leech_available_rwnd = decoded_packet["RWND"]
            receiver_remaining_window_sizes[leech_ip] = leech_available_rwnd
            if leech_ip not in receiver_acknowledged_chunks:
                receiver_acknowledged_chunks[leech_ip] = dict()
            receiver_acknowledged_chunks[leech_ip][file_name] = chunks_receiver_owned
            # TODO: Update hash_serials so that seed knows the hash serials!
            for file in manifest:
                for chunk_id in manifest[file]:
                    hash_file = get_hash(file + str(chunk_id))
                    hash_serials[hash_file] = {"FILE_NAME":file,"CHUNK_ID":chunk_id}
            print("{} downloading the file: {}".format(leech_ip,file_name))
            send_file_thread = threading.Thread(target=send_file, args=(leech_ip, file_name, chunks_receiver_owned))
            send_file_thread.start()
        elif packet_type == "TERMINATE":
            leech_ip = decoded_packet["MY_IP"]
            file_name = decoded_packet["PAYLOAD"]
            if leech_ip not in terminate_received:
                terminate_received[leech_ip] = dict()
            terminate_received[leech_ip][file_name] = True
            print("TERMINATE received from {} for the file: {}".format(leech_ip,file_name))
        elif packet_type == "GOODBYE":
            sender_name = decoded_packet["NAME"]
            sender_ip = decoded_packet["MY_IP"]
            if sender_ip in ONLINE_USER_LIST:
                print("\n\n##### BetaZero++ Notification #####")
                print("{name} with IP: {ip} went offline... Removing the user from contacts...".format(name=sender_name,ip=sender_ip))
                del ONLINE_USER_LIST[sender_ip]
        else:
            print("Invalid Packet Type: {}\n".format(packet_type))
    except Exception as exc:
            print("Exception in service_manager: ",exc)

def discover_network():
    if CHANNEL == 1:
        for i in range(255):
            target_ip = USER_NETWORK + "." + str(i)
            if not (USER_IP == target_ip):
                packet = create_packet(USER_NAME, USER_IP, "DISCOVER", "")
                start_new_thread(send_tcp_packet, (packet, target_ip, PORT))
    else:
        for target_ip in LAN_ADDRESSES:
            packet = create_packet(USER_NAME, USER_IP, "DISCOVER", "")
            start_new_thread(send_tcp_packet, (packet, target_ip, PORT))

def goodbye_network():
    if CHANNEL == 1:
        for i in range(255):
            target_ip = USER_NETWORK + "." + str(i)
            if not (USER_IP == target_ip):
                packet = create_packet(USER_NAME, USER_IP, "GOODBYE", "")
                start_new_thread(send_tcp_packet, (packet, target_ip, PORT))
    else:
        for target_ip in LAN_ADDRESSES:
            packet = create_packet(USER_NAME, USER_IP, "GOODBYE", "")
            start_new_thread(send_tcp_packet, (packet, target_ip, PORT))

def get_chunk_from_file(file_name, chunk_id):
    # TODO: Check the byte reading! (decode might be a problem)
    # payload['content'] = base64.b64encode(fh.read())
    file_path = "My_Files/" + file_name
    with open(file_path, 'rb') as file:
        file.seek((chunk_id-1)*900, 0)
        chunk = base64.b64encode(file.read(900)).decode("utf-8")
        return chunk

#-chunk_id = serial_id
def create_file_packet(file_name, chunk_id, type="FILE"):
    chunk = get_chunk_from_file(file_name, chunk_id)
    if chunk is None:
        return
    file_packet = {"SERIAL": get_hash(file_name + str(chunk_id)), "TYPE": type ,"MY_IP": USER_IP, "PAYLOAD": chunk}
    return json.dumps(file_packet)

def send_file_packet(receiver_ip, file_name, chunk_id, type="FILE"):
    packet = create_file_packet(file_name, chunk_id)
    send_udp_packet(packet, receiver_ip)

# Send File:
#-receiver_ip: The IP to which the chunk is sent.-from REQ_DOWNLOAD
#-file_name: payload from REQ_DOWNLOAD.
#-chunks_receiver_owned: paylaod2 from REQ_DOWNLOAD. Represent chunks owned by the sender.
def send_file(receiver_ip, file_name, chunks_receiver_owned, type="FILE"):
    chunks_sender = manifest[file_name]
    chunks_receiver_not_owned = [item for item in chunks_sender if item not in chunks_receiver_owned]
    # There are no available chunks that the receiver does not own. What to do here?
    # TO-DO: Send message to receiver that says 'The seed does not own the requested chunks!'.
    if not chunks_receiver_not_owned:
        return
    # Should we wait for the receiver to collect all the chunks that he does not have but the sender has?
    # A while loop could be better.
    limit = 0
    # Initialize terminate_received
    if receiver_ip not in terminate_received:
        terminate_received[receiver_ip] = dict()
    terminate_received[receiver_ip][file_name] = True
    while len(chunks_receiver_not_owned) != 0 or terminate_received[receiver_ip][file_name] == False:
        if limit == 3:
            break
        while receiver_remaining_window_sizes[receiver_ip] <= 1048576: ## MB
            time.sleep(60)
            packet = {"SERIAL": -1, "TYPE": "FILE", "MY_IP": USER_IP, "PAYLOAD": ""}
            packet = json.dumps(packet)
            send_udp_packet(packet, receiver_ip)
            time.sleep(1)
        chunk_id = chunks_receiver_not_owned[0]
        if chunk_id in receiver_acknowledged_chunks[receiver_ip][file_name]:
            chunks_receiver_not_owned.remove(chunk_id)
            limit = 0
            continue
        send_file_packet(receiver_ip, file_name, chunk_id)
        time.sleep(1)
        if chunk_id in receiver_acknowledged_chunks[receiver_ip][file_name]:
            chunks_receiver_not_owned.remove(chunk_id)
            limit = 0
        else:
            for i in range(3):
                send_file_packet(receiver_ip, file_name, chunk_id)
            time.sleep(1)
            if chunk_id in receiver_acknowledged_chunks[receiver_ip][file_name]:
                chunks_receiver_not_owned.remove(chunk_id)
                limit = 0
            else:
                print("Error: Lost packet with serial {} of the file {}".format(get_hash(file_name + str(chunk_id)), file_name))
                chunks_receiver_not_owned.remove(chunk_id)
                chunks_receiver_not_owned.append(chunk_id)
                limit += 1
        # First check if the packet sent is acknowledged or not.
        # - If so, check if the remaining window size is large enough(>1MB(KB?))
        #   -- If so, send the next packet if possible.
        #   -- If not, wait for 1 minute.
        # - If not, send it 3 times, and wait for 1 sec to check if it is acknowledged or not.
        #   -- If it is acknowledged, send the next packet.
        #   -- If not, give an error message related to that packet(Should we send the next packet at this point?)

def send_ack_packet(serial, type="ACK"):
    global BUFFER_LIST
    packet = {"SERIAL": serial, "TYPE": type, "MY_IP": USER_IP, "RWND": get_rwnd()}
    packet = json.dumps(packet)
    file_name = hash_serials[serial]["FILE_NAME"]
    for seed_ip in seed_list[file_name]: #Send all seeds, which you download this file, an ACK packet.
        send_udp_packet(packet, seed_ip)

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
    print("##### BetaZero++ - Profile #####")
    print("User Name: " + USER_NAME)
    print("User IP: " + USER_IP)

def list_users():
    print("##### BetaZero++ - Users #####")
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
    while RepresentsInt(user_number) == False or get_receiver_ip(ONLINE_USER_LIST, user_number) is None:
        if (RepresentsInt(user_number) == True):
            if not(get_receiver_ip(ONLINE_USER_LIST, user_number) is None) or int(user_number) == 0:
                return int(user_number)
            else:
                user_number = input("Please enter a valid user number or press 0 to back to main menu: ")
        else:
            user_number = input("Please enter a valid user number or press 0 to back to main menu: ")
    return int(user_number)

def check_inbox():
    print("##### BetaZero++ Inbox #####")
    print_dict(ONLINE_USER_LIST)
    print("########################")
    user_number = input("Please enter the number of user or press 0 to back to main menu: ")
    user_number = is_valid_user_number(user_number)
    if user_number == 0:
        return
    os.system('clear')
    user_ip = get_receiver_ip(ONLINE_USER_LIST, user_number)
    user_name = ONLINE_USER_LIST[user_ip]
    file_name = "BetaZero++_{}_{}.txt".format(user_name, user_ip)
    # os.system('clear')
    print("##### BetaZero++ #####")
    print("Conversation History: " + user_name)
    try:
        file = open(file_name, 'r')
        for line in file:
            print(line, end="")
        file.close()
    except FileNotFoundError:
        print("No messages found.")
    print("########## BetaZero++ ##########\n")
    tmp = input("\nPress any key for main page...")

def request_manifest():
    print("##### BetaZero++ - Users #####")
    print_dict(ONLINE_USER_LIST)
    print("########################")
    user_number = input("Please enter the number of user or press 0 to back to main menu: ")
    user_number = is_valid_user_number(user_number)
    if user_number == 0:
        return
    receiver_ip = get_receiver_ip(ONLINE_USER_LIST, user_number)
    receiver_name = ONLINE_USER_LIST[receiver_ip]
    packet = create_packet(USER_NAME,USER_IP,"REQ_MANIFEST","")
    start_new_thread(send_tcp_packet, (packet, receiver_ip, PORT))

def send_manifest(receiver_ip):
    global manifest
    manifest = get_manifest()
    manifest_payload = manifest
    for key in manifest:
        manifest_payload[key] = list_to_chunksowned_str(manifest[key])
    packet = create_packet(USER_NAME,USER_IP,'MANIFEST',manifest_payload)
    start_new_thread(send_tcp_packet, (packet, receiver_ip, PORT))

def print_manifest(manifest):
    for i,key in enumerate(manifest):
        print("{}) {} - Available Chunks: {}".format(i+1,key,str(manifest[key])))

def download_file():
    global manifest
    print("##### BetaZero++ - Manifests Available #####")
    print_dict(ONLINE_USER_LIST)
    print("########################")
    seed_number = input("Please enter the number of user or press 0 to back to main menu: ")
    seed_number = is_valid_user_number(seed_number)
    if seed_number == 0:
        return
    os.system('clear')
    seed_ip = get_receiver_ip(ONLINE_USER_LIST, seed_number)
    seed_name = ONLINE_USER_LIST[seed_ip]
    seed_manifest = dict()
    if seed_ip in shared_manifests:
        seed_manifest = shared_manifests[seed_ip]
    print("##### BetaZero++ - {}'s Manifest #####".format(seed_name))
    print_manifest(seed_manifest)
    print("########################")
    file_number = int(input("Please enter the number of file or press 0 to back to main menu: "))
    if file_number == 0:
        return
    file_name = str()
    leech_manifest = get_manifest()
    for i,key in enumerate(seed_manifest):
        if i+1 == file_number:
            file_name = key
            break
    chunks_leech_owns = list() if file_name not in leech_manifest else leech_manifest[file_name]
    chunks_leech_owns_str = list_to_chunksowned_str(chunks_leech_owns)
    chunks_seed_owns = seed_manifest[file_name]
    chunks_pending = [chunk_id for chunk_id in chunks_seed_owns if chunk_id not in chunks_leech_owns]
    # Update seed_list
    if file_name not in seed_list:
        seed_list[file_name] = dict()
    seed_list[file_name][seed_ip] = chunks_pending
    packet = {"NAME": USER_NAME,
              "MY_IP": USER_IP,
              "TYPE": 'REQ_DOWNLOAD',
              "FILE_NAME": file_name,
              "CHUNKS_OWNED": chunks_leech_owns_str,
              "RWND": get_rwnd()
             }
    packet = json.dumps(packet)
    start_new_thread(send_tcp_packet, (packet, seed_ip, PORT))

def send_terminate_packet(user_name,user_ip,type,file_name,receiver_ip):
    packet = create_packet(user_name,user_ip,type,file_name)
    send_tcp_packet(packet, receiver_ip, PORT)

menu = {
    1: "Show My Profile",
    2: "List Online Users",
    3: "Send a Message",
    4: "Check Inbox",
    5: "Request Manifest",
    6: "Download a File",
    7: "Quit"
}

def main_menu():
    os.system('clear')
    print("##### BetaZero++ Menu #####")
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
        os.system('clear')
        request_manifest()
    elif command == 6:
        os.system('clear')
        download_file()
    elif command == 7:
        goodbye_thread = threading.Thread(target=goodbye_network)
        goodbye_thread.start()
        goodbye_thread.join()
        print("The other users have been notified that you are leaving...")
        time.sleep(1)
        exit_program()
    else:
        print("Please Enter A Valid Command!")

print("Welcome to BetaZero++!\n")
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
hash_serials = dict()
manifest = get_manifest()
shared_manifests = dict()
receiver_acknowledged_chunks = dict()
receiver_remaining_window_sizes = dict()
seed_list = dict()
terminate_received = dict()
BUFFER_LIST = list()
MAX_BUFFER_SIZE = 4194304 #4 MB

print("\nFetching Previous Data...")
fetch_data()
time.sleep(0.5)

collect_lan_ips()

listen_tcp_thread = threading.Thread(target=listen_tcp)
listen_udp_thread = threading.Thread(target=listen_udp)
discover_thread = threading.Thread(target=discover_network)
service_manager_udp_thread = threading.Thread(target=service_manager_udp)

listen_tcp_thread.start()
listen_udp_thread.start()
service_manager_udp_thread.start()
discover_thread.start()

while True:
    main_menu()
