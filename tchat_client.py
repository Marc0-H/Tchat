import socket
import select
import tchat_message

INTERVAL = 0.4
DATA_SIZE = 1024
CONNECTION_TIMEOUT = 4

class Client():
    def __init__(self, gui, server_ip, server_port):
        self.gui = gui
        self.server_ip = server_ip
        self.server_port = server_port

        self.is_running = False

    def start_connection(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.settimeout(CONNECTION_TIMEOUT)
        self.client_socket.connect((self.server_ip, self.server_port))

    def run_client(self):
        self.is_running = True

        while self.is_running:
            readable, _, _ = select.select([self.client_socket,], [], [], INTERVAL)
            for node in readable:
                try:
                    data = node.recv(DATA_SIZE)
                    if data:
                        
                        object = tchat_message.message_decode(data)

                        if object.message_type == tchat_message.MESSAGE_INFO:
                            self.gui.win_draw_sidebar(data)
                        else:
                            self.gui.new_message(object.sender_name, object.separator, object.message, object.text_color)

                except Exception as e:
                    pass

    def send_message(self, message_object):
        try:
            self.client_socket.send(message_object)
        except:
            self.gui.new_message(tchat_message.CONSOLE_FAIL, tchat_message.CONSOLE_SEPERATOR, "Error sending message, maybe the server is down...", tchat_message.TEXT_COLOR_RED)
    def stop_client(self):
        self.is_running = False
        self.client_socket.close()
        self.gui.new_message(tchat_message.CONSOLE_INFO, tchat_message.CONSOLE_SEPERATOR, "You disconnected from the server...", tchat_message.TEXT_COLOR_YELLOW)



