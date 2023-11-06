import pickle

TEXT_COLOR_DEFAULT = 1
TEXT_COLOR_GREEN = 2
TEXT_COLOR_RED = 3
TEXT_COLOR_YELLOW = 4
TEXT_COLOR_BLUE = 5
CONSOLE_SUCCESS = "[+]"
CONSOLE_FAIL = "[-]"
CONSOLE_INFO = "[~]"
CONSOLE_SEPERATOR = " "
MESSAGE_GENERAL = 0
MESSAGE_INFO = 1


class InfoMessage():
    def __init__(self, server_name, max_clients, connected_clients, clients_info_dict, server_end):
        self.server_name = server_name
        self.message_type = MESSAGE_INFO
        self.max_clients = max_clients
        self.connected_clients = connected_clients
        self.clients_info_dict = clients_info_dict
        self.server_end = server_end


class GeneralMessage():
    def __init__(self, sender_name, separator, message, text_color):
        self.message_type = MESSAGE_GENERAL
        self.sender_name = sender_name
        self.separator = separator
        self.message = message
        self.text_color = text_color
        self.total_length = len(sender_name + separator + message) 


def general_message_encode(sender_name, separator, message, text_color):
    return pickle.dumps(GeneralMessage(sender_name, separator, message, text_color))

def info_message_encode(server_name, max_clients, connected_clients, clients_info_dict, server_end):
    return pickle.dumps(InfoMessage(server_name, max_clients, connected_clients, clients_info_dict, server_end))

def message_decode(message_object):
    return pickle.loads(message_object)

