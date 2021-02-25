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
import random

#
# REFERENCE: https://stackoverflow.com/questions/1265665/how-can-i-check-if-a-string-represents-an-int-without-using-try-except
#
def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def print_dict(dict):
    for i, key in enumerate(dict.keys()):
        print(str(i + 1) + ") Name: " + dict[key]["NAME"] + " IP: " + key + " IN_ROOM: " + str(dict[key]["IN_ROOM"]))

def get_receiver_ip(dict, num):
    if RepresentsInt(num) == False:
        return None
    num = int(num)
    if num <= 0:
        return None
    for i, key in enumerate(dict.keys()):
        if num - 1 == i:
            return key
    return None


def is_valid_user_number(user_number):
    while RepresentsInt(user_number) == False or get_receiver_ip(ONLINE_USER_LIST, user_number) is None:
        if (RepresentsInt(user_number) == True):
            if int(user_number) == 0:
                main_menu()
                time.sleep(0.5)
            elif not (get_receiver_ip(ONLINE_USER_LIST, user_number) is None):
                pass
            else:
                user_number = input("Please enter a valid number or press 0 to back to main menu: ")
        else:
            user_number = input("Please enter a valid number or press 0 to back to main menu: ")
    return user_number


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
            if not (res is None):
                res_list.append(res.group())
        if len(res_list) == 1:
            return res_list[0]
        else:
            for i, ip in enumerate(res_list):
                print("{:d}) {}".format(i + 1, ip))
            ip_num = int(input("Please enter the number of your IP: "))
            return res_list[ip_num - 1]


def create_packet(sender_name, sender_ip, message_type, payload):
    packet = {"NAME": sender_name,
              "MY_IP": sender_ip,
              "TYPE": message_type,
              "PAYLOAD": payload
              }
    return json.dumps(packet)


def decode_packet(packet):
    return json.loads(packet)


def broadcast(packet):
    if CHANNEL == 1:
        remaining = 3
        while remaining > 0:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.bind(('', 0))  # ???
                s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

                try:
                    s.sendto(packet.encode(), ('<broadcast>', GENERAL_PORT))
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
                try:
                    s.sendto(packet.encode(), (hamachi_broadcast_ip, GENERAL_PORT))
                    remaining -= 1
                except:
                    continue
                s.close()


def send_udp_packet(packet, receiver_ip):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(('', 0))  # ???
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        try:
            s.sendto(packet.encode(), (receiver_ip, GENERAL_PORT))
        except Exception as e:
            print("Exception in send_udp_packet: {}".format(e))
        s.close()


def send_tcp_packet(packet, target_ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            s.connect((target_ip, port))
            s.sendall(packet.encode())
            s.close()
    except:
        print("\nERROR: IP {} is not online anymore...\nRemoving the user from contacts...".format(target_ip))
        try:
            del ONLINE_USER_LIST[target_ip]
        except:
            pass


def listen_tcp():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((USER_IP, GENERAL_PORT))
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

def listen_tcp_port(port):
    packet = str()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((USER_IP, port))
        s.listen()
        conn, addr = s.accept()
        data = conn.recv(2048)
        if not data:
            return
        packet = data.decode()
        conn.close()
        s.close()
    return packet

def listen_tcp_room():
    global IN_ROOM, AVAILABLE_ROOMS, MY_ROOM_ADMIN_IP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((USER_IP, AVAILABLE_ROOMS[MY_ROOM_ADMIN_IP]["ROOM_PORT"]))
        s.listen()
        while IN_ROOM:
            conn, addr = s.accept()
            data = conn.recv(2048)
            if not data:
                break
            packet = data.decode()
            room_manager_tcp(packet)
            conn.close()
        s.close()

def listen_udp():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(('', GENERAL_PORT))
        s.setblocking(0)
        while True:
            result = select.select([s], [], [])
            data = result[0][0].recv(1024)
            if not data:
                break
            packet = data.decode()
            service_manager_udp(packet)
        s.close()

def service_manager_udp(packet):
    try:
        global IN_ROOM, ROOM_ADMIN, MY_ROOM_PASSWORD, MY_ROOM_ADMIN_IP,AVAILABLE_ROOMS,ONLINE_USER_LIST
        decoded_packet = decode_packet(packet)
        sender_name = decoded_packet["NAME"]
        sender_ip = decoded_packet["MY_IP"]
        packet_type = decoded_packet["TYPE"]
        payload = decoded_packet["PAYLOAD"]
        if sender_ip == USER_IP:
            return
        if packet_type == "DISCOVER":
            if sender_ip not in ONLINE_USER_LIST:
                print("\n\n##### UnoGame Notification #####")
                print("New User Discovered: " + sender_name + "\n")
                ONLINE_USER_LIST[sender_ip] = {
                    "NAME": sender_name,
                    "IN_ROOM": payload
                }
            packet = create_packet(USER_NAME, USER_IP, "RESPOND", IN_ROOM)
            start_new_thread(send_tcp_packet, (packet, sender_ip, GENERAL_PORT))
        elif packet_type == "REQUEST_ROOMS":
            if ROOM_ADMIN:
                # TODO: Room specifications will be sent as TCP. TYPE: "ROOM_INFO"
                packet = create_packet(USER_NAME, USER_IP, "ROOM_INFO", AVAILABLE_ROOMS[USER_IP])
                start_new_thread(send_tcp_packet, (packet, sender_ip, GENERAL_PORT))
        elif packet_type == "USER_STATUS_UPDATE":
            if payload["IN_ROOM"]:
                if payload["ROOM_ADMIN"] == USER_IP:
                    if sender_ip not in MY_ROOM_USERS_INFO.keys() and payload['IN_ROOM']:
                        MY_ROOM_USERS_INFO[sender_ip] = {"READY": False,
                                                         "CARDS": -1}
                if sender_ip not in AVAILABLE_ROOMS[payload['ROOM_ADMIN']]['ACTIVE_USERS']:
                    ONLINE_USER_LIST[sender_ip]["IN_ROOM"] = payload['IN_ROOM']
                    AVAILABLE_ROOMS[payload['ROOM_ADMIN']]['ACTIVE_USERS'].append(sender_ip)
            elif not payload["IN_ROOM"]:
                if payload["ROOM_ADMIN"] not in AVAILABLE_ROOMS:
                    return
                if sender_ip in AVAILABLE_ROOMS[payload["ROOM_ADMIN"]]["ACTIVE_USERS"]:
                    AVAILABLE_ROOMS[payload["ROOM_ADMIN"]]["ACTIVE_USERS"].remove(sender_ip)
                ONLINE_USER_LIST[sender_ip]["IN_ROOM"] = payload['IN_ROOM']
                if sender_ip == payload["ROOM_ADMIN"]: # admin çıkıyorsa
                    if AVAILABLE_ROOMS[payload["ROOM_ADMIN"]]["ROOM_PORT"] not in AVAILABLE_PORTS:
                        AVAILABLE_PORTS.append(AVAILABLE_ROOMS[payload["ROOM_ADMIN"]]["ROOM_PORT"])
                    if MY_ROOM_ADMIN_IP == sender_ip: # ben içerdeysem
                        IN_ROOM = False
                        ROOM_ADMIN = False
                        MY_ROOM_PASSWORD = ""
                        MY_ROOM_ADMIN_IP = ""
                        for user in AVAILABLE_ROOMS[payload["ROOM_ADMIN"]]["ACTIVE_USERS"]:
                            if user != USER_IP:
                                ONLINE_USER_LIST[user]["IN_ROOM"] = False
                        tmp = input("The admin has left the room, press any key to go back to main menu...")
                    else:
                        for user in AVAILABLE_ROOMS[payload["ROOM_ADMIN"]]["ACTIVE_USERS"]:
                            ONLINE_USER_LIST[user]["IN_ROOM"] = False
                    if payload["ROOM_ADMIN"] in AVAILABLE_ROOMS:
                        del AVAILABLE_ROOMS[payload["ROOM_ADMIN"]]
        elif packet_type == "ROOM_INFO":
            if payload["ROOM_ADMIN"] not in AVAILABLE_ROOMS:
                print("\n\n##### UnoGame Notification #####")
                print("New room has been created: " + payload["ROOM_NAME"] + " by " + ONLINE_USER_LIST[payload["ROOM_ADMIN"]][
                        "NAME"])
            AVAILABLE_ROOMS[payload["ROOM_ADMIN"]] = payload
            ONLINE_USER_LIST[sender_ip]["IN_ROOM"] = True
            if payload['ROOM_PORT'] in AVAILABLE_PORTS:
                AVAILABLE_PORTS.remove(payload["ROOM_PORT"])
        elif packet_type == "GAME_INFO":
            if payload['ROOM_ADMIN'] == MY_ROOM_ADMIN_IP and payload["IN_GAME"] and (not AVAILABLE_ROOMS[payload["ROOM_ADMIN"]]["IN_GAME"]):
                print("Every player is ready. Press any key to start the game.")
            AVAILABLE_ROOMS[payload["ROOM_ADMIN"]] = payload
        elif packet_type == "GAME_OVER":
            AVAILABLE_ROOMS[sender_ip]["IN_GAME"] = False
        elif packet_type == "GOODBYE":
            if sender_ip in ONLINE_USER_LIST.keys():
                if not IN_ROOM:
                    print("\n##### UnoGame Notification #####")
                    print("{name} with IP: {ip} went offline... Removing the user from contacts...".format(name=sender_name,
                                                                                                           ip=sender_ip))
                del ONLINE_USER_LIST[sender_ip]
        else:
            print("Invalid Packet Type UDP: {}\n".format(packet_type))
    except Exception as exc:
        print("Exception in service_manager UDP: ", exc)
        print(packet)


def service_manager_tcp(packet):
    try:
        decoded_packet = decode_packet(packet)
        sender_name = decoded_packet["NAME"]
        sender_ip = decoded_packet["MY_IP"]
        packet_type = decoded_packet["TYPE"]
        payload = decoded_packet["PAYLOAD"]
        if packet_type == "RESPOND":
            if sender_ip not in ONLINE_USER_LIST:
                print("\n\n##### UnoGame Notification #####")
                print("New User Responded: " + sender_name + "\n")
                ONLINE_USER_LIST[sender_ip] = {
                    "NAME": sender_name,
                    "IN_ROOM": payload
                }
        elif packet_type == "MESSAGE":
            print("\n\n##### UnoGame Notification #####")
            print("You have one new message from: " + sender_name)
            print("Please check your inbox!\n")
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            file_name = "UnoGame_{}_{}.txt".format(sender_name, sender_ip)
            message_text = sender_name + ": " + payload + " at " + dt_string + "\n"
            file = open(file_name, 'a')
            file.write(message_text)
            file.close()
        elif packet_type == "ROOM_INFO":
            if payload["ROOM_ADMIN"] not in AVAILABLE_ROOMS:
                print("\n\n##### UnoGame Notification #####")
                print("New room has been detected: " + payload["ROOM_NAME"] + " by " +
                      ONLINE_USER_LIST[payload["ROOM_ADMIN"]]["NAME"])
            AVAILABLE_ROOMS[payload["ROOM_ADMIN"]] = payload
            if payload['ROOM_PORT'] in AVAILABLE_PORTS:
                AVAILABLE_PORTS.remove(payload['ROOM_PORT'])
        elif packet_type == "ROOM_JOIN_REQUEST":
            if MY_ROOM_PASSWORD == payload:
                packet = create_packet(USER_NAME, USER_IP, "ROOM_JOIN_RESPOND", True)
                room_join_request_thread = threading.Thread(target=send_tcp_packet,
                                                            args=(packet, sender_ip, ROOM_REQUEST_PORT))
                room_join_request_thread.start()
            else:
                packet = create_packet(USER_NAME, USER_IP, "ROOM_JOIN_RESPOND", False)
                room_join_request_thread = threading.Thread(target=send_tcp_packet,
                                                            args=(packet, sender_ip, ROOM_REQUEST_PORT))
                room_join_request_thread.start()
        else:
            print("Invalid Packet Type TCP: {}\n".format(packet_type))
    except Exception as exc:
        print("Exception in service_manager TCP: ", exc)


def room_manager_tcp(packet):
    try:
        global TURN, MY_CARDS, IS_MY_TURN, LAST_CARD, GAME_START
        decoded_packet = decode_packet(packet)
        sender_name = decoded_packet["NAME"]
        sender_ip = decoded_packet["MY_IP"]
        packet_type = decoded_packet["TYPE"]
        payload = decoded_packet["PAYLOAD"]
        if packet_type == "ROOM_MESSAGE":
            print("\n\n##### UnoGame Room Notification #####")
            print("You have one new message from: " + sender_name)
            print("Message: {} ".format(payload))
        elif packet_type == "READY_STATUS_UPDATE":
            MY_ROOM_USERS_INFO[sender_ip]['READY'] = payload['READY']
        elif packet_type == "GAME_START":
            TURN = payload['TURN']
            MY_CARDS = payload['CARDS']
            IS_MY_TURN = get_is_my_turn(TURN)
            LAST_CARD = payload['LAST_CARD']
            GAME_START = True
        elif packet_type == "PLAYER_ACTION":
            action_admin_game(sender_name,sender_ip,payload)
        elif packet_type == "ACTION_INFORM":
            action_inform_manager(sender_name,sender_ip,payload)
        else:
            print("Invalid packet type in room_manager_tcp!")
    except Exception as exc:
        print("Exception in room_manager TCP: ", exc)

def action_inform_manager(sender_name,sender_ip,payload):
    global GAME_START,MY_CARDS,TURN,LAST_CARD,IS_MY_TURN,UNO_CARDS,SPECIALS,COLORS,MY_ROOM_USERS_INFO,MY_ROOM_ADMIN_IP,AVAILABLE_ROOMS,MY_ROOM_PASSWORD,ROOM_ADMIN,IN_ROOM,ONLINE_USER_LIST,USER_IP
    print("_________________________________________________________________________________")
    if payload["ACTION_TYPE"] == 1:
        TURN = payload["TURN"]
        LAST_CARD = payload["PLAYED_CARD"]
        if USER_IP != payload["PLAYER"]:
            player = ONLINE_USER_LIST[payload["PLAYER"]]["NAME"]
        else:
            player = USER_NAME
        deck_size = payload["DECK_SIZE"]
        next_player = str()
        if USER_IP != TURN[1][TURN[0]]:
            next_player = ONLINE_USER_LIST[TURN[1][TURN[0]]]["NAME"]
        else:
             next_player = USER_NAME
        if deck_size < 0:
            tmp = input("Insufficient cards on the deck, the game is over. Press any key to go to the room menu...")
            AVAILABLE_ROOMS[MY_ROOM_ADMIN_IP]['IN_GAME'] = False
            reset_game_variables()
            if MY_ROOM_ADMIN_IP==USER_IP:
                packet = create_packet(USER_NAME, USER_IP, "GAME_OVER", "")
                inform_game_over = threading.Thread(target=broadcast, args=(packet,))
                inform_game_over.start()
            return
        if payload["WON_GAME"]:
            if payload["PLAYER"] == USER_IP:
                tmp = input("!!! CONGRATULATIONS !!!\n... YOU WON THE GAME ...\nPress any key to go to the room menu.".format(USER_NAME))
            else:
                tmp = input("Player {} has won the game. Press any key to go to the room menu".format(ONLINE_USER_LIST[sender_ip]["NAME"]))
            AVAILABLE_ROOMS[MY_ROOM_ADMIN_IP]['IN_GAME'] = False
            reset_game_variables()
            if MY_ROOM_ADMIN_IP==USER_IP:
                packet = create_packet(USER_NAME, USER_IP, "GAME_OVER", "")
                inform_game_over = threading.Thread(target=broadcast, args=(packet,))
                inform_game_over.start()
            return
        print("PLAYER: {} , PLAYED CARD: {} , DECK_SIZE: {} , NEXT TURN {}".format(player,LAST_CARD,deck_size,next_player))
        IS_MY_TURN = get_is_my_turn(TURN)
        if LAST_CARD[1] == "BLOCK":
            if USER_IP != TURN[1][(TURN[0]-1)%len(AVAILABLE_ROOMS[MY_ROOM_ADMIN_IP]["ACTIVE_USERS"])]:
                blocked_player = ONLINE_USER_LIST[TURN[1][(TURN[0]-1)%len(AVAILABLE_ROOMS[MY_ROOM_ADMIN_IP]["ACTIVE_USERS"])]]["NAME"]
            else:
                blocked_player = USER_NAME
            print("Player {} has blocked {}".format(player,blocked_player))
        elif LAST_CARD[1] == "REVERSE":
            print("Player {} has reversed direction".format(player))
        elif LAST_CARD[0] =="WILD":
            if LAST_CARD[1] == "":
                last_card_tmp = list(LAST_CARD)
                last_card_tmp[0] = payload["COLOR"]
                last_card_tmp[1] = ""
                LAST_CARD = tuple(last_card_tmp)
                print("Player {} has changed the game color to {}".format(player,payload["COLOR"]))
            elif LAST_CARD[1]=="+4":
                last_card_tmp = list(LAST_CARD)
                last_card_tmp[0] = payload["COLOR"]
                last_card_tmp[1] = ""
                LAST_CARD = tuple(last_card_tmp)
                #LAST_CARD[0] = payload["COLOR"]
                print("Player {} has changed the game color to {}".format(player,payload["COLOR"]))
                print("Player {} forces player {} to pick +4 cards from the deck".format(player,next_player))
                if IS_MY_TURN:
                    MY_CARDS.extend(payload["NEW_CARDS"])
                    print("Player {} forces you to pick +4 cards from the deck.".format(player))
                    print_cards(payload["NEW_CARDS"], new_cards = True)
        elif LAST_CARD[1] == "+2" :
            print("Player {} forces player {} to pick {} cards from the deck".format(player,next_player,LAST_CARD[1]))
            if IS_MY_TURN:
                MY_CARDS.extend(payload["NEW_CARDS"])
                print("Player {} forces you to pick {} cards from the deck.".format(player,LAST_CARD[1]))
                print_cards(payload["NEW_CARDS"], new_cards = True)
    elif payload["ACTION_TYPE"] == 2:
        deck_size = payload["DECK_SIZE"]
        if deck_size < 0:
            tmp = input("Insufficient cards on the deck, the game is over. Press any key to go to the room menu...")
            AVAILABLE_ROOMS[MY_ROOM_ADMIN_IP]['IN_GAME'] = False
            reset_game_variables()
            if MY_ROOM_ADMIN_IP==USER_IP:
                packet = create_packet(USER_NAME, USER_IP, "GAME_OVER", "")
                inform_game_over = threading.Thread(target=broadcast, args=(packet,))
                inform_game_over.start()
            return
        player = payload["PLAYER"]
        if payload["PLAYER"] == USER_IP:
            print("{} draws a card.".format(USER_NAME))
        else:
            print("{} draws a card.".format(ONLINE_USER_LIST[payload["PLAYER"]]["NAME"]))
    elif payload["ACTION_TYPE"] == 3:
        player = payload["PLAYER"]
        if player == USER_IP:
            player = USER_NAME
        else:
            player = ONLINE_USER_LIST[player]["NAME"]
        print("{} has left the game. The game is over!".format(player))
        AVAILABLE_ROOMS[MY_ROOM_ADMIN_IP]["IN_GAME"] = False
        reset_game_variables()
        if USER_IP == MY_ROOM_ADMIN_IP:
            # TODO: Send udp packet saying that IN_GAME -> False
            AVAILABLE_ROOMS[USER_IP]["IN_GAME"] = False
            packet = create_packet(USER_NAME, USER_IP, "GAME_OVER", "")
            inform_game_over = threading.Thread(target=broadcast, args=(packet,))
            inform_game_over.start()
        pass
    elif payload["ACTION_TYPE"] == 4:
        if USER_IP != payload["PLAYER"]:
            player = ONLINE_USER_LIST[payload["PLAYER"]]["NAME"]
        else:
            player = USER_NAME
        TURN = payload["TURN"]
        if USER_IP != TURN[1][TURN[0]]:
            next_player = ONLINE_USER_LIST[TURN[1][TURN[0]]]["NAME"]
        else:
             next_player = USER_NAME
        deck_size = payload["DECK_SIZE"]
        IS_MY_TURN = get_is_my_turn(TURN)
        print("PLAYER: {} , PLAYED CARD: NONE , DECK_SIZE: {} , NEXT TURN {}".format(player,deck_size,next_player))
        print("Player {} passes the round".format(player))
    else:
        tmp = input("UNDEFINED TYPE OF ACTION IN ACTION INFORM MANAGER")
    print("_________________________________________________________________________________")

def reset_game_variables():
    global AVAILABLE_ROOMS, MY_ROOM_USERS_INFO, UNO_CARDS, IS_MY_TURN, LAST_CARD, TURN, MY_CARDS, GAME_START, MY_ROOM_ADMIN_IP
    AVAILABLE_ROOMS[MY_ROOM_ADMIN_IP]["IN_GAME"] = False
    if USER_IP == MY_ROOM_ADMIN_IP:
        for key in MY_ROOM_USERS_INFO:
            MY_ROOM_USERS_INFO[key]['CARDS'] = list()
            MY_ROOM_USERS_INFO[key]['TURN'] = tuple()
            MY_ROOM_USERS_INFO[key]['LAST_CARD'] = tuple()
            MY_ROOM_USERS_INFO[key]['READY'] = False
    UNO_CARDS = list()
    IS_MY_TURN = False
    LAST_CARD = tuple()
    TURN = tuple()
    MY_CARDS = list()
    GAME_START = False

def action_admin_game(sender_name,sender_ip,payload):
    num_players = len(AVAILABLE_ROOMS[MY_ROOM_ADMIN_IP]['ACTIVE_USERS'])
    action = payload["ACTION"]
    global TURN
    if action == "1": # select a card
        card = payload["CARD"]
        is_int = RepresentsInt(card[1])
        new_game_status = dict()
        if is_int and (card[1] != "+2" and card[1]!= "+4"): # card is integer
            #MY_ROOM_USERS_INFO[sender_ip]['CARDS'].remove(card)
            new_turn = (TURN[0] + 1) % num_players
            tmp_turn = list(TURN)
            tmp_turn[0] = new_turn
            TURN = tuple(tmp_turn)
            new_game_status = {
                "TURN" : TURN,
                "PLAYED_CARD": card,
                "PLAYER": sender_ip,
                "NEW_CARDS": list(),
                "DECK_SIZE": len(UNO_CARDS),
                "COLOR": card[0],
                "LEAVE_GAME": False,
                "WON_GAME": payload["WON_GAME"],
                "ACTION_TYPE":1
            }
        else:
            if card[1] == "BLOCK":
                new_turn = (TURN[0] + 2) % num_players
                tmp_turn = list(TURN)
                tmp_turn[0] = new_turn
                TURN = tuple(tmp_turn)
                new_game_status = {
                    "TURN" : TURN,
                    "PLAYED_CARD": card,
                    "PLAYER": sender_ip,
                    "NEW_CARDS": list(),
                    "DECK_SIZE": len(UNO_CARDS),
                    "COLOR": card[0],
                    "LEAVE_GAME": False,
                    "WON_GAME": payload["WON_GAME"],
                    "ACTION_TYPE":1,
                }
            elif card[1] == "REVERSE":
                TURN[1].reverse()
                new_turn = (num_players - TURN[0]) % num_players
                tmp_turn = list(TURN)
                tmp_turn[0] = new_turn
                TURN = tuple(tmp_turn)
                new_game_status = {
                    "TURN" : TURN,
                    "PLAYED_CARD": card,
                    "PLAYER": sender_ip,
                    "NEW_CARDS": list(),
                    "DECK_SIZE": len(UNO_CARDS),
                    "COLOR": card[0],
                    "LEAVE_GAME": False,
                    "WON_GAME": payload["WON_GAME"],
                    "ACTION_TYPE":1,
                }
            elif card[1] == "+2":
                new_turn = (TURN[0] + 1) % num_players
                tmp_turn = list(TURN)
                tmp_turn[0] = new_turn
                TURN = tuple(tmp_turn)
                new_cards = list()
                new_deck_size = len(UNO_CARDS) - 2
                if len(UNO_CARDS) >1:
                    for i in range(2):
                        new_cards.append(UNO_CARDS.pop())
                new_game_status = {
                    "TURN" : TURN,
                    "PLAYED_CARD": card,
                    "PLAYER": sender_ip,
                    "NEW_CARDS": new_cards,
                    "DECK_SIZE": new_deck_size,
                    "COLOR": card[0],
                    "LEAVE_GAME": False,
                    "WON_GAME": payload["WON_GAME"],
                    "ACTION_TYPE":1,
                }
            elif card[0]== "WILD" and card[1] == "":
                new_turn = (TURN[0] + 1) % num_players
                tmp_turn = list(TURN)
                tmp_turn[0] = new_turn
                TURN = tuple(tmp_turn)
                new_game_status = {
                    "TURN" : TURN,
                    "PLAYED_CARD": card,
                    "PLAYER": sender_ip,
                    "NEW_CARDS": list(),
                    "DECK_SIZE": len(UNO_CARDS),
                    "COLOR": payload["COLOR"],
                    "LEAVE_GAME": False,
                    "WON_GAME": payload["WON_GAME"],
                    "ACTION_TYPE":1,
                }
            elif card[0]== "WILD" and card[1] == "+4":
                new_turn = (TURN[0] + 1) % num_players
                tmp_turn = list(TURN)
                tmp_turn[0] = new_turn
                TURN = tuple(tmp_turn)
                new_deck_size = len(UNO_CARDS) - 4
                new_cards = list()
                if len(UNO_CARDS) > 3:
                    for i in range(4):
                        new_cards.append(UNO_CARDS.pop())
                new_game_status = {
                    "TURN" : TURN,
                    "PLAYED_CARD": card,
                    "PLAYER": sender_ip,
                    "NEW_CARDS": new_cards,
                    "DECK_SIZE": new_deck_size,
                    "COLOR": payload["COLOR"],
                    "LEAVE_GAME": False,
                    "WON_GAME": payload["WON_GAME"],
                    "ACTION_TYPE":1,
                }
                #TODO finish the game sent the winner info
        packet = create_packet(USER_NAME,USER_IP,"ACTION_INFORM",new_game_status)
        tcp_room_sender(AVAILABLE_ROOMS[MY_ROOM_ADMIN_IP]["ROOM_PORT"],MY_ROOM_ADMIN_IP,packet)
    elif action == "2": # draw a card
        # Respond must be given via ROOM_REQUEST_PORT port!!! (DONE)
        new_deck_size = len(UNO_CARDS) - 1
        new_cards = list()

        new_game_status = {
            "PLAYER": sender_ip,
            "ACTION_TYPE":2,
            "DECK_SIZE": new_deck_size
        }
        packet = create_packet(USER_NAME,USER_IP,"ACTION_INFORM",new_game_status)
        tcp_room_sender(AVAILABLE_ROOMS[MY_ROOM_ADMIN_IP]["ROOM_PORT"],MY_ROOM_ADMIN_IP,packet)

        if len(UNO_CARDS) > 0:
            for i in range(1):
                new_cards.append(UNO_CARDS.pop())
        new_game_status = {
            "PLAYER": sender_ip,
            "ACTION_TYPE": 2,
            "NEW_CARDS": new_cards,
            "DECK_SIZE": new_deck_size
        }
        packet = create_packet(USER_NAME,USER_IP,"ACTION_INFORM",new_game_status)
        request_card_thread = threading.Thread(target=send_tcp_packet, args=(packet, sender_ip, ROOM_REQUEST_PORT))
        request_card_thread.start()
    elif action == "3": # LEAVE GAME AVAILABLE_ROOMS[MY_ROOM_ADMIN_IP]['IN_GAME'] -> False
        new_game_status = {
            "PLAYER": sender_ip,
            "ACTION_TYPE": 3,
            "LEAVE_GAME":True
        }
        packet = create_packet(USER_NAME,USER_IP,"ACTION_INFORM",new_game_status)
        tcp_room_sender(AVAILABLE_ROOMS[MY_ROOM_ADMIN_IP]["ROOM_PORT"],MY_ROOM_ADMIN_IP,packet)
    elif action == "4":
        new_turn = (TURN[0] + 1) % num_players
        tmp_turn = list(TURN)
        tmp_turn[0] = new_turn
        TURN = tuple(tmp_turn)
        new_game_status = {
            "TURN" : TURN,
            "PLAYED_CARD": "",
            "PLAYER": sender_ip,
            "NEW_CARDS": list(),
            "DECK_SIZE": len(UNO_CARDS),
            "COLOR": "",
            "LEAVE_GAME": False,
            "WON_GAME": "",
            "ACTION_TYPE":4
        }
        packet = create_packet(USER_NAME,USER_IP,"ACTION_INFORM",new_game_status)
        tcp_room_sender(AVAILABLE_ROOMS[MY_ROOM_ADMIN_IP]["ROOM_PORT"],MY_ROOM_ADMIN_IP,packet)
    else:
        print("INVALID ACTION_TYPE IN action_admin_game")

def get_is_my_turn(turn):
    if turn[1][turn[0]] == USER_IP:
         return True
    else:
        return False


menu = {
    1: "Show My Profile",
    2: "List Online Users",
    3: "Send a Message",
    4: "Check Inbox",
    5: "Create a Room",
    6: "Join a Room",
    99: "Quit"

}
room_menu_commands = {
    1: "List Players",
    2: "Send a Message",
    3: "Ready",
    4: "Refresh",
    99: "Exit Room",
}


def show_profile():
    print("##### UnoGame - Profile #####")
    print("User Name: " + USER_NAME)
    print("User IP: " + USER_IP)


def list_online_users():
    print("##### UnoGame - Users #####")
    print_dict(ONLINE_USER_LIST)


def send_message():
    list_online_users()
    user_number = input("Please enter the number of user or press 0 to back to main menu: ")
    user_number = is_valid_user_number(user_number)
    receiver_ip = get_receiver_ip(ONLINE_USER_LIST, user_number)
    receiver_name = ONLINE_USER_LIST[receiver_ip]["NAME"]
    receiver_in_room = ONLINE_USER_LIST[receiver_ip]["IN_ROOM"]
    if not receiver_in_room:
        payload = input("Please type your message: ")
        packet = create_packet(USER_NAME, USER_IP, "MESSAGE", payload)
        try:
            start_new_thread(send_tcp_packet, (packet, receiver_ip, GENERAL_PORT))
            file_name = "UnoGame_{}_{}.txt".format(receiver_name, receiver_ip)
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            message_text = USER_NAME + ": " + payload + " at " + dt_string + "\n"
            file = open(file_name, 'a')
            file.write(message_text)
            file.close()
            time.sleep(0.5)
        except:
            pass
    else:
        tmp = input("This user is currently in a room, press any key to back to main menu...")


def check_inbox():
    print("##### UnoGame Inbox #####")
    print_dict(ONLINE_USER_LIST)
    print("########################")
    user_number = input("Please enter the number of user or press 0 to back to main menu: ")
    user_number = is_valid_user_number(user_number)
    os.system('clear')
    user_ip = get_receiver_ip(ONLINE_USER_LIST, user_number)
    user_name = ONLINE_USER_LIST[user_ip]["NAME"]
    file_name = "UnoGame_{}_{}.txt".format(user_name, user_ip)
    print("##### UnoGame #####")
    print("Conversation History: " + user_name)
    try:
        file = open(file_name, 'r')
        for line in file:
            print(line, end="")
        file.close()
    except FileNotFoundError:
        print("No messages found.")
    print("########## UnoGame ##########\n")
    tmp = input("\nPress any key for main page...")


def create_room():
    global IN_ROOM, MY_ROOM_PASSWORD, ROOM_ADMIN, AVAILABLE_PORTS, MY_ROOM_ADMIN_IP
    # ROOM_INFO -> UDP
    # Room Name, Max Capacity, Password
    os.system('clear')
    print("##### UnoGame Create a Room #####")
    if len(AVAILABLE_PORTS) == 0:
        tmp = input("Maximum room number has been reached... Press any key to back to main menu.")
        return
    room_name = input("Please enter a name or press 0 to back to main menu: ")
    if room_name == '0':
        return
    max_capacity = input(
        "Please enter a max capacity number (maximum 8) for the room or press 0 to back to main menu: ")
    while not RepresentsInt(max_capacity) or (RepresentsInt(max_capacity) and int(max_capacity) > 8):
        max_capacity = input(
            "Please enter a valid max capacity number (maximum 8) for the room or press 0 to back to main menu: ")
    if int(max_capacity) == 0:
        return
    password = input("Please enter a password: ")
    print("Do you confirm creating the room with following credentials:\nName: {}\nMax Capacity: {}\nPassword: {}\n".format(room_name, max_capacity, password))
    tmp = input("[Y]es | [N]o\n")
    while tmp.lower() != "y" and tmp.lower() != "yes" and tmp.lower() != "n" and tmp.lower() != "no":
        tmp = input(
            "Invalid type of input. \n Do you confirm creating the room with following credentials:\nName: {}\nMax Capacity: {}\nPassword: {}\n[Y]es | [N]o\n".format(
                room_name, max_capacity, password))
    if tmp.lower() == 'n' or tmp.lower() == 'no':
        return
    elif tmp.lower() == 'y' or tmp.lower() == 'yes':
        ROOM_ADMIN = True
        IN_ROOM = True
        MY_ROOM_PASSWORD = password
        room_port = AVAILABLE_PORTS[0]
        AVAILABLE_PORTS.remove(room_port)
        current_room_info = {
            "ROOM_ADMIN": USER_IP,
            "ROOM_NAME": room_name,
            "ROOM_PORT": room_port,
            "MAX_CAPACITY": max_capacity,
            "MIN_CAPACITY": 2,
            "ACTIVE_USERS": [USER_IP],
            "IN_GAME": False,
        }
        MY_ROOM_USERS_INFO[USER_IP] = {"READY": False,
                                       "CARDS": -1}
        MY_ROOM_ADMIN_IP = USER_IP
        AVAILABLE_ROOMS[USER_IP] = current_room_info
        packet = create_packet(USER_NAME, USER_IP, "ROOM_INFO", current_room_info)
        inform_new_room = threading.Thread(target=broadcast, args=(packet,))
        inform_new_room.start()
        room_menu_start()


def list_rooms():
    for i, key in enumerate(AVAILABLE_ROOMS.keys()):
        print(
            str(i + 1) + ") Room name: {} , Room Admin: {} , Max Player: {} , Current Player: {} , In Game: {} ".format(
                AVAILABLE_ROOMS[key]["ROOM_NAME"],
                ONLINE_USER_LIST[AVAILABLE_ROOMS[key]["ROOM_ADMIN"]]["NAME"],
                AVAILABLE_ROOMS[key]["MAX_CAPACITY"],
                len(AVAILABLE_ROOMS[key]["ACTIVE_USERS"]),
                AVAILABLE_ROOMS[key]["IN_GAME"]))


def get_room_info(dict, num):
    if RepresentsInt(num) == False:
        return None
    num = int(num)
    if num <= 0:
        return None
    for i, key in enumerate(dict.keys()):
        if num - 1 == i:
            return key
    return None


def is_valid_room_number(room_number):
    while RepresentsInt(room_number) == False or get_room_info(AVAILABLE_ROOMS, room_number) is None:
        if (RepresentsInt(room_number) == True):
            if int(room_number) == 0:
                main_menu()
                time.sleep(0.5)
            elif not (get_room_info(AVAILABLE_ROOMS, room_number) is None):
                pass
            else:
                room_number = input("Please enter a valid number or press 0 to back to main menu: ")
        else:
            room_number = input("Please enter a valid number or press 0 to back to main menu: ")
    return room_number


def join_room():
    global AVAILABLE_ROOMS, IN_ROOM, MY_ROOM_ADMIN_IP
    os.system('clear')
    print("##### UnoGame Join a Room Menu #####")
    list_rooms()
    room_number = input("Please enter the room number that you want to join or press 0 to back to the main menu: ")
    room_number = is_valid_room_number(room_number)
    room_admin_ip = get_room_info(AVAILABLE_ROOMS, room_number)
    tmp = input(
        "Please type the password of the room: {}\nPassword: ".format(AVAILABLE_ROOMS[room_admin_ip]["ROOM_NAME"]))
    packet = create_packet(USER_NAME, USER_IP, "ROOM_JOIN_REQUEST", tmp)
    room_join_request_thread = threading.Thread(target=send_tcp_packet, args=(packet, room_admin_ip, GENERAL_PORT))
    room_join_request_thread.start()
    room_join_request_thread.join()
    room_join_respond_packet = listen_tcp_port(ROOM_REQUEST_PORT)
    room_join_respond_packet = decode_packet(room_join_respond_packet)
    payload = room_join_respond_packet["PAYLOAD"]
    if payload == True:
        AVAILABLE_ROOMS[room_admin_ip]["ACTIVE_USERS"].append(USER_IP)
        MY_ROOM_ADMIN_IP = room_admin_ip
        IN_ROOM = True
        payload = {'IN_ROOM': True,
                   'ROOM_ADMIN': room_admin_ip
                   }
        packet = create_packet(USER_NAME, USER_IP, "USER_STATUS_UPDATE", payload)
        user_status_update_thread = threading.Thread(target=broadcast, args=(packet,))
        user_status_update_thread.start()
        user_status_update_thread.join()
        tmp = input("You have entered the correct password! Press any key to enter the room...")
        room_menu_start()
    else:
        tmp = input("You have entered the wrong password! Press any key to back to main menu...")


def exit_program():
    print("\nGood Bye {}".format(USER_NAME))
    time.sleep(2)
    subprocess.call(['pkill', '-f', 'main.py'])


def main_menu():
    global USER_IP, USER_NAME
    os.system('clear')
    print("##### UnoGame Menu #####")
    for key in menu.keys():
        print(str(key) + "." + menu[key])
    command = int(input("Please Enter The Number of The Command: "))
    if command == 1:
        os.system('clear')
        show_profile()
        tmp = input("\nPress any key for main page...")
    elif command == 2:
        os.system('clear')
        list_online_users()
        tmp = input("\nPress any key for main page...")
    elif command == 3:
        os.system('clear')
        send_message()
    elif command == 4:
        os.system('clear')
        check_inbox()
    elif command == 5:
        create_room()
    elif command == 6:
        join_room()
    elif command == 99:
        packet = create_packet(USER_NAME,USER_IP,"GOODBYE","")
        goodbye_thread = threading.Thread(target=broadcast,args=(packet,))
        goodbye_thread.start()
        goodbye_thread.join()
        print("The other users have been notified that you are leaving...")
        exit_program()
    else:
        print("Please Enter A Valid Command!")


def room_menu_start():
    listen_tcp_room_thread = threading.Thread(target=listen_tcp_room)
    listen_tcp_room_thread.start()
    while IN_ROOM:
        room_menu()


def room_menu():
    global ROOM_ADMIN
    os.system('clear')
    print("##### UnoGame Room {} Menu #####".format(AVAILABLE_ROOMS[MY_ROOM_ADMIN_IP]["ROOM_NAME"]))
    able_to_start = get_able_to_start()
    if ROOM_ADMIN:
        if able_to_start:
            room_menu_commands[3] = "Start the game"
        else:
            if (len(AVAILABLE_ROOMS[MY_ROOM_ADMIN_IP]['ACTIVE_USERS']) < 2):
                room_menu_commands[3] = "Start the game (Insufficient number of players...) Press refresh to update the status."
            else:
                room_menu_commands[3] = "Start the game (Waiting for other users...) Press refresh to update the status."
    else:
        room_menu_commands[3] = "Ready"
    for key in room_menu_commands.keys():
        print(str(key) + "." + room_menu_commands[key])
    command = int(input("Please Enter The Number of The Command: "))
    if command == 1:
        os.system('clear')
        list_players()
        tmp = input("\nPress any key for room menu...")
    elif command == 2:
        os.system('clear')
        send_message_room()
        tmp = input("\nPress any key for room menu...")
    elif command == 3:
        if ROOM_ADMIN:
            able_to_start = get_able_to_start()
            if able_to_start:
                admin_game_start()
                tmp = input("\nPress any key for room menu...")
            else:
                if (len(AVAILABLE_ROOMS[MY_ROOM_ADMIN_IP]['ACTIVE_USERS']) < 2):
                    tmp = input("Insufficient number of players. Press any key to back to the room menu")
                else:
                    tmp = input("There are user(s) who is(are) not ready. Press any key to back to the room menu")
        else:
            ready_user()
            tmp = input("\nPress any key for room menu...")
    elif command == 4:
        os.system('clear')
        tmp = input("Press any key to refresh the room menu. ")
    elif command == 99:
        room_exit()
        tmp = input("You are quiting the room press any key to continue... ")
        pass
    else:
        os.system('clear')
        tmp = input("Please Enter A Valid Command! Press any key to go to the room menu...")

def room_exit():
    global IN_ROOM,MY_ROOM_PASSWORD,ROOM_ADMIN,MY_ROOM_ADMIN_IP,AVAILABLE_ROOMS
    AVAILABLE_ROOMS[MY_ROOM_ADMIN_IP]['ACTIVE_USERS'].remove(USER_IP)
    if USER_IP == MY_ROOM_ADMIN_IP:
        AVAILABLE_PORTS.append(AVAILABLE_ROOMS[MY_ROOM_ADMIN_IP]["ROOM_PORT"])
        for user in AVAILABLE_ROOMS[USER_IP]["ACTIVE_USERS"]:
            if user != USER_IP:
                ONLINE_USER_LIST[user]["IN_ROOM"] = False
        del AVAILABLE_ROOMS[MY_ROOM_ADMIN_IP]
    payload = {'IN_ROOM': False,
               'ROOM_ADMIN': MY_ROOM_ADMIN_IP
               }
    IN_ROOM = False
    MY_ROOM_PASSWORD =""
    ROOM_ADMIN = False
    MY_ROOM_ADMIN_IP = ""
    packet = create_packet(USER_NAME, USER_IP, "USER_STATUS_UPDATE", payload)
    user_status_update_thread = threading.Thread(target=broadcast, args=(packet,))
    user_status_update_thread.start()
    user_status_update_thread.join()




def tcp_room_sender(port, room_admin_ip ,packet):
    # start_new_thread(send_tcp_packet, (packet, MY_ROOM_ADMIN_IP, AVAILABLE_ROOMS[MY_ROOM_ADMIN_IP]['ROOM_PORT']))
    for player in AVAILABLE_ROOMS[room_admin_ip]['ACTIVE_USERS']:
        start_new_thread(send_tcp_packet, (packet, player, AVAILABLE_ROOMS[MY_ROOM_ADMIN_IP]['ROOM_PORT']))

def admin_game_start():
    global UNO_CARDS, MY_ROOM_USERS_INFO, TURN, MY_CARDS, LAST_CARD, IS_MY_TURN
    MY_ROOM_USERS_INFO[USER_IP]['READY'] = True
    AVAILABLE_ROOMS[MY_ROOM_ADMIN_IP]['IN_GAME'] = True
    packet = create_packet(USER_NAME, USER_IP, "GAME_INFO", AVAILABLE_ROOMS[MY_ROOM_ADMIN_IP])
    inform_game_start = threading.Thread(target=broadcast, args=(packet,))
    inform_game_start.start()
    UNO_CARDS = get_cards()
    random.shuffle(UNO_CARDS)
    turn_l = AVAILABLE_ROOMS[USER_IP]['ACTIVE_USERS']
    random.shuffle(turn_l)
    TURN = (0, turn_l)
    LAST_CARD = UNO_CARDS.pop()
    while LAST_CARD[1] in SPECIALS or LAST_CARD[0] == "WILD":
        LAST_CARD = UNO_CARDS.pop()
    for player in AVAILABLE_ROOMS[USER_IP]['ACTIVE_USERS']:
        #MY_ROOM_USERS_INFO[player] = dict()
        player_cards = []
        for i in range(7):
            card = UNO_CARDS.pop()
            player_cards.append(card)
        MY_ROOM_USERS_INFO[player]['CARDS'] = player_cards
        MY_ROOM_USERS_INFO[player]['TURN'] = TURN
        MY_ROOM_USERS_INFO[player]['LAST_CARD'] = LAST_CARD
        if player != USER_IP:
            packet = create_packet(USER_NAME,USER_IP,"GAME_START",MY_ROOM_USERS_INFO[player])
            start_new_thread(send_tcp_packet, (packet, player, AVAILABLE_ROOMS[MY_ROOM_ADMIN_IP]['ROOM_PORT']))
    MY_CARDS = MY_ROOM_USERS_INFO[USER_IP]['CARDS']
    if turn_l[0] == USER_IP:
        IS_MY_TURN = True
    else:
        IS_MY_TURN = False
    GAME_START = True
    game()

def print_cards(cards,new_cards=False,last_card=False,space=10):
    global MUTEX
    while not MUTEX:
        pass
    MUTEX = False
    if last_card:
        print("The Card on the Top:")
    elif new_cards:
        print("Your New Cards:")
    else:
        print("Your Current Hand:")
    for i,card in enumerate(cards):
        end_str = ' ' * (space-len(str(i+1))-1) + '|'
        print(i+1,end=end_str)
    print()
    for card in cards:
        end_str = ' ' * (space-len(card[0])-1) + '|'
        print(card[0],end=end_str)
    print()
    for card in cards:
        end_str = ' ' * (space-len(card[1])-1) + '|'
        print(card[1],end=end_str)
    print()
    MUTEX = True

def card_check(current_choice):
    if current_choice[0] == "WILD":
        return True
    if (LAST_CARD[0] == current_choice[0]):
        return True
    if (LAST_CARD[1] == current_choice[1]):
        return True
    return False

def get_valid_card_number(tmp):
    try:
        int(tmp)
    except:
        return False
    if  len(MY_CARDS)<int(tmp) or int(tmp)<1 :
        return False
    return True

def get_valid_action_number(tmp):
    try:
        int(tmp)
    except:
        return False
    if int(tmp) not in [1,2,3]:
        return False
    return True

def get_valid_color_number(color_answer):
    try:
        int(color_answer)
    except:
        return False
    if int(color_answer) not in [1,2,3,4]:
        return False
    return True

def get_valid_draw_card_action_number(answer):
    try:
        int(answer)
    except:
        return False
    if int(answer) not in [1,2]:
        return False
    return True

def game():
    global GAME_START,MY_CARDS,TURN,LAST_CARD,IS_MY_TURN,UNO_CARDS,SPECIALS,COLORS,MY_ROOM_USERS_INFO,MY_ROOM_ADMIN_IP,AVAILABLE_ROOMS,MY_ROOM_PASSWORD,ROOM_ADMIN,IN_ROOM,ONLINE_USER_LIST,USER_IP
    os.system('clear')
    print("#### Welcome to UNOGame ####")
    print_cards(MY_CARDS)
    while AVAILABLE_ROOMS[MY_ROOM_ADMIN_IP]['IN_GAME']:
        if IS_MY_TURN:
            # Print last card.
            print_cards([LAST_CARD],last_card=True)
            action = input("Select your action:\n1)Select a card\n2)Draw a card from deck\n3)Leave Game\n")
            while not get_valid_action_number(action):
                action = input("Select a valid action:\n1) Select a card\n2) Draw a card from deck\n3) Leave Game\n")
            if action == "1":
                print_cards(MY_CARDS)
                card_number = input("Select the card number that you want to play. Or press 0 to back to the action menu.")
                while (not get_valid_card_number(card_number) and card_number != "0") or (card_number != "0" and (not card_check(MY_CARDS[int(card_number) - 1]))):
                    card_number = input("Select a valid card number that you want to play. Or press 0 to back to the action menu.")
                if card_number == "0":
                    continue
                selected_card = MY_CARDS.pop(int(card_number)-1)
                color_answer = "1"
                if selected_card[0] == "WILD":
                    color_answer = input("Please enter the number of color that you want to choose:\n1)Yellow\n2)Blue\n3)Green\n4)Red\n")
                    while not get_valid_color_number(color_answer):
                        color_answer = input("Please enter the number of color that you want to choose:\n1)Yellow\n2)Blue\n3)Green\n4)Red\n")
                won_game = False
                if len(MY_CARDS) == 0:
                    won_game = True
                packet = create_packet(USER_NAME,USER_IP,"PLAYER_ACTION", {"ACTION":action,"CARD": selected_card,"COLOR": COLORS[int(color_answer)-1],"WON_GAME":won_game})
                start_new_thread(send_tcp_packet, (packet, MY_ROOM_ADMIN_IP, AVAILABLE_ROOMS[MY_ROOM_ADMIN_IP]['ROOM_PORT']))
            elif action =="2": # Draw a card.
                packet = create_packet(USER_NAME,USER_IP,"PLAYER_ACTION", {"ACTION":action})
                start_new_thread(send_tcp_packet, (packet, MY_ROOM_ADMIN_IP, AVAILABLE_ROOMS[MY_ROOM_ADMIN_IP]['ROOM_PORT']))
                action_respond_packet = listen_tcp_port(ROOM_REQUEST_PORT)
                action_respond_packet = decode_packet(action_respond_packet)
                print_cards(action_respond_packet["PAYLOAD"]["NEW_CARDS"],new_cards=True)
                action = input("Please select the action:\n\n1)Play the new card\n2)Pass\n")
                new_card = action_respond_packet["PAYLOAD"]["NEW_CARDS"][0]
                while not get_valid_draw_card_action_number(action) or (not card_check(new_card) and action=="1"):
                    action = input("Please choose a valid action number or check if you can play this card.\nPlease select the action:\n1)Play the new card\n2)Pass\n")
                if action == "1":
                    selected_card = action_respond_packet["PAYLOAD"]["NEW_CARDS"][0]
                    color_answer = "1"
                    if selected_card[0] == "WILD":
                        color_answer = input("Please enter the number of color that you want to choose:\n1)Yellow\n2)Blue\n3)Green\n4)Red\n")
                        while not get_valid_color_number(color_answer):
                            color_answer = input("Please enter the number of color that you want to choose:\n1)Yellow\n2)Blue\n3)Green\n4)Red\n")
                    packet = create_packet(USER_NAME,USER_IP,"PLAYER_ACTION", {"ACTION":action,"CARD": selected_card,"COLOR":COLORS[int(color_answer)-1],"WON_GAME":False})
                    start_new_thread(send_tcp_packet, (packet, MY_ROOM_ADMIN_IP, AVAILABLE_ROOMS[MY_ROOM_ADMIN_IP]['ROOM_PORT']))
                else:
                    MY_CARDS.append(tuple(action_respond_packet["PAYLOAD"]["NEW_CARDS"][0])) # TODO: Admin will send the new card in the field called 'NEW_CARDS'
                    packet = create_packet(USER_NAME,USER_IP,"PLAYER_ACTION", {"ACTION":"4"})
                    start_new_thread(send_tcp_packet, (packet, MY_ROOM_ADMIN_IP, AVAILABLE_ROOMS[MY_ROOM_ADMIN_IP]['ROOM_PORT']))
                    pass
            else: # LEAVE GAME
                tmp = input("Are you sure you want to leave the game?\n[Y]es|[N]o\n")
                while not(tmp.lower() == 'n' or tmp.lower() == 'y'):
                    tmp = input("Invalid input! Are you sure you want to leave the game?\n[Y]es|[N]o\n")
                if tmp.lower() == 'n' or tmp.lower() == 'no':
                    continue
                else:
                    packet = create_packet(USER_NAME,USER_IP,"PLAYER_ACTION", {"ACTION":action})
                    start_new_thread(send_tcp_packet, (packet, MY_ROOM_ADMIN_IP, AVAILABLE_ROOMS[MY_ROOM_ADMIN_IP]['ROOM_PORT']))
                    # ADMIN will notify users that AVAILABLE_ROOMS[MY_ROOM_ADMIN_IP]['IN_GAME'] - > False!!!
            IS_MY_TURN = False
            print_cards(MY_CARDS)

def get_cards():
    uno_cards = []
    for color in COLORS:
        for i in range(10):
            uno_cards.append((color, str(i)))
            if i != 0:
                uno_cards.append((color, str(i)))
        for special in SPECIALS:
            for i in range(2):
                uno_cards.append((color, special))
    for i in range(4):
        uno_cards.append(("WILD", "+4"))
    for i in range(4):
        uno_cards.append(("WILD", ""))
    return uno_cards


def get_able_to_start():
    if len(AVAILABLE_ROOMS[MY_ROOM_ADMIN_IP]['ACTIVE_USERS']) < 2:
        return False
    for user in MY_ROOM_USERS_INFO:
        if user != USER_IP:
            if not MY_ROOM_USERS_INFO[user]['READY']:
                return False
    return True

def ready_user():
    packet = create_packet(USER_NAME, USER_IP, "READY_STATUS_UPDATE", {"READY": True})
    start_new_thread(send_tcp_packet, (packet, MY_ROOM_ADMIN_IP, AVAILABLE_ROOMS[MY_ROOM_ADMIN_IP]['ROOM_PORT']))
    tmp = -1
    while (not AVAILABLE_ROOMS[MY_ROOM_ADMIN_IP]['IN_GAME']) and tmp != '0':
        tmp = input("\nWaiting for other players... Press 0 to cancel...\n")
    if tmp == '0':
        packet = create_packet(USER_NAME, USER_IP, "READY_STATUS_UPDATE", {"READY": False})
        start_new_thread(send_tcp_packet, (packet, MY_ROOM_ADMIN_IP, AVAILABLE_ROOMS[MY_ROOM_ADMIN_IP]['ROOM_PORT']))
        return
    else:
        while not GAME_START :
            pass
        game()

def list_players():
    global AVAILABLE_ROOMS
    COUNT = 2
    active_users = AVAILABLE_ROOMS[MY_ROOM_ADMIN_IP]["ACTIVE_USERS"]
    print("##### UnoGame - {} #####".format(AVAILABLE_ROOMS[MY_ROOM_ADMIN_IP]["ROOM_NAME"]))
    print("{}) Name: {} IP: {}".format(1, USER_NAME, USER_IP))
    for active_user_ip in active_users:
        if active_user_ip != USER_IP:
            print("{}) Name: {} IP: {}".format(COUNT, ONLINE_USER_LIST[active_user_ip]["NAME"], active_user_ip))
            COUNT += 1


def send_message_room():
    tmp = input('Type the message that you want to send to the room chat or press 0 to go back to the room menu..\nMessage: ')
    if tmp == '0':
        return
    packet = create_packet(USER_NAME, USER_IP, "ROOM_MESSAGE", tmp)
    active_room_users = AVAILABLE_ROOMS[MY_ROOM_ADMIN_IP]['ACTIVE_USERS']
    for room_user_ip in active_room_users:
        if room_user_ip != USER_IP:
            start_new_thread(send_tcp_packet, (packet, room_user_ip, AVAILABLE_ROOMS[MY_ROOM_ADMIN_IP]['ROOM_PORT']))


print("Welcome to UnoGame!\n")
USER_NAME = input("Please Enter Your User Name: ")
os.system('clear')

CHANNEL = int(input(
    "Welcome {}, Please Enter the Number of Your Channel: 1 or 2?\n1)Static IP\n2)Hamachi (VPN)\n".format(USER_NAME)))
os.system('clear')

"""
#
# GLOBAL VARIABLES
#
"""
AVAILABLE_PORTS = [12343, 12344, 12347, 12348, 12349]
GENERAL_PORT = 12345
ROOM_REQUEST_PORT = 12346
USER_IP = get_ip(CHANNEL)
PARSED_USER_IP = USER_IP.split(sep=".")
USER_NETWORK = PARSED_USER_IP[0] + "." + PARSED_USER_IP[1] + "." + PARSED_USER_IP[2]
ONLINE_USER_LIST = dict()

IN_ROOM = False
ROOM_ADMIN = False
MY_ROOM_PASSWORD = ""
AVAILABLE_ROOMS = dict()
MY_ROOM_ADMIN_IP = ""

MY_ROOM_USERS_INFO = dict()
COLORS = ["YELLOW", "BLUE", "GREEN", "RED"]
SPECIALS = ["+2", "REVERSE", "BLOCK", ]
UNO_CARDS = list()
IS_MY_TURN= False
LAST_CARD = tuple()
TURN = tuple()
MY_CARDS = list()
GAME_START = False

MUTEX = True

# global GAME_START,MY_CARDS,TURN,LAST_CARD,IS_MY_TURN,UNO_CARDS,SPECIALS,COLORS,MY_ROOM_USERS_INFO,MY_ROOM_ADMIN_IP,AVAILABLE_ROOMS,MY_ROOM_PASSWORD,ROOM_ADMIN,IN_ROOM,ONLINE_USER_LIST,USER_IP

listen_tcp_thread = threading.Thread(target=listen_tcp)
listen_udp_thread = threading.Thread(target=listen_udp)
packet = create_packet(USER_NAME, USER_IP, "DISCOVER", IN_ROOM)
discover_thread = threading.Thread(target=broadcast, args=(packet,))
packet = create_packet(USER_NAME, USER_IP, "REQUEST_ROOMS", IN_ROOM)
request_rooms_thread = threading.Thread(target=broadcast, args=(packet,))

listen_tcp_thread.start()
listen_udp_thread.start()
discover_thread.start()
request_rooms_thread.start()

while True:
    main_menu()

