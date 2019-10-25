import socket
import threading
import time

def fa_one_second(udp_socket,recv_ip,recv_data):
    # 3 发送信息
    while True:
        time.sleep(1)
        data01 = 'mess01 send'
        # data_require = input('请输入要发送的数据')
        udp_socket.sendto(data01.encode("utf-8"),(recv_ip,recv_data))
# def fa_require(udp_socket,recv_ip,recv_data):
#     # 3 发送信息
#     while True:
#         data02 = input('请输入数据')
#         udp_socket.sendto(data02.encode("utf-8"),(recv_ip,recv_data))
def shou(udp_socket):
    # 4接收数据
    while True:

        user_data = udp_socket.recvfrom(1024)
        a = user_data[0]
        b = user_data[1]
        print("用户:%s发来的数据为:%s" % (str(b), a.decode("utf-8")))
def main():
    # １创建套接字
    udp_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    # 2 绑定本地信息
    udp_socket.bind(("192.168.1.79",25599))  #IP地址换为自己电脑的IP
    recv_ip = "192.168.1.79"
    recv_data = 25566

    client1 = threading.Thread(target=fa_one_second,args=(udp_socket,recv_ip,recv_data))
    # client2 = threading.Thread(target=fa_require, args=(udp_socket, recv_ip, recv_data))
    client3 = threading.Thread(target=shou,args=(udp_socket,))
    client1.start()
    # client2.start()
    client3.start()

if __name__ == '__main__':
    main()
