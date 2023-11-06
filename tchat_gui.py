import curses
import tchat_message
import math


class Gui():
    def __init__(self, stdscr):
        curses.use_default_colors()
        curses.start_color()
        curses.init_pair(tchat_message.TEXT_COLOR_DEFAULT, -1, -1)
        curses.init_pair(tchat_message.TEXT_COLOR_GREEN, curses.COLOR_GREEN, -1)
        curses.init_pair(tchat_message.TEXT_COLOR_RED, curses.COLOR_RED, -1)
        curses.init_pair(tchat_message.TEXT_COLOR_YELLOW, curses.COLOR_YELLOW, -1)
        curses.init_pair(tchat_message.TEXT_COLOR_BLUE, curses.COLOR_BLUE, -1)

        self.stdscr = stdscr
        self.sidebar_width = 24
        self.user_input_message = ""
        self.relative_cursor_string_x = 0
        self.cursor_x = 3
        self.user_input_offset = 0
        self.chat_scroll_index = 0
        self.chatbox_messages = []
        self.sidebar_data = None

        self.screen_height = -1
        self.screen_width = -1
        self.sidebar = None
        self.sidebar_border = None
        self.inputfield_border = None
        self.inputfield = None
        self.chatbox_border = None
        self.chatbox = None

    def dimensions_changed(self):
        height, width = self.stdscr.getmaxyx()
        if self.screen_height != height or self.screen_width != width:
            return True
        return False
    
    def update_dimensions(self):
        self.screen_height, self.screen_width = self.stdscr.getmaxyx()

    def console_message_success(self, message):
        object = tchat_message.GeneralMessage(tchat_message.CONSOLE_SUCCESS, tchat_message.CONSOLE_SEPERATOR, message, tchat_message.TEXT_COLOR_GREEN)
        self.chatbox_messages.append(object)
        self.win_draw_semi()

    def console_message_fail(self, message):
        object = tchat_message.GeneralMessage(tchat_message.CONSOLE_FAIL, tchat_message.CONSOLE_SEPERATOR, message, tchat_message.TEXT_COLOR_RED)
        self.chatbox_messages.append(object)
        self.win_draw_semi()

    def console_message_info(self, message):
        object = tchat_message.GeneralMessage(tchat_message.CONSOLE_INFO, tchat_message.CONSOLE_SEPERATOR, message, tchat_message.TEXT_COLOR_YELLOW)
        self.chatbox_messages.append(object)
        self.win_draw_semi()

    def new_message(self, sender_name, seperator, message, color=tchat_message.TEXT_COLOR_DEFAULT):
        object = tchat_message.GeneralMessage(sender_name, seperator, message, color)
        self.chatbox_messages.append(object)
        self.win_draw_semi()

    def handle_enter(self):
        self.user_input_message = ""
        self.relative_cursor_string_x = 0
        self.user_input_offset = 0

    def win_draw_semi(self):
        self.win_draw_chatbox()
        self.win_draw_inputfield()


    def update_window_dimensions(self):
        sidebar_height = self.screen_height - 5
        sidebar_width = self.sidebar_width - 4
        inputfield_height = 1
        inputfield_width = self.screen_width - 5
        chatbox_height = self.screen_height - 5
        chatbox_width = self.screen_width - self.sidebar_width - 3

        sidebar_border_hwyx = (sidebar_height + 2, sidebar_width + 2, 0, 1)
        sidebar_hwyx = (sidebar_height, sidebar_width, 1, 2)
        self.sidebar_border = curses.newwin(*sidebar_border_hwyx)
        self.sidebar = curses.newwin(*sidebar_hwyx)

        inputfield_border_hwyx = (inputfield_height + 2, inputfield_width + 3, chatbox_height + 2, 1)
        inputfield_hwyx = (inputfield_height, inputfield_width, chatbox_height + 3, 3)
        self.inputfield_border = curses.newwin(*inputfield_border_hwyx)
        self.inputfield = curses.newwin(*inputfield_hwyx)

        chatbox_border_hwyx = (chatbox_height + 2, chatbox_width + 2, 0, self.sidebar_width)
        chatbox_hwyx = (chatbox_height, chatbox_width, 1, 1 + self.sidebar_width)
        self.chatbox_border = curses.newwin(*chatbox_border_hwyx)
        self.chatbox = curses.newwin(*chatbox_hwyx)


    def win_draw_global(self):
        self.stdscr.erase()

        if self.dimensions_changed():
            self.update_dimensions()
            try:
                self.update_window_dimensions()
            except:
                curses.beep()

        try:
            self.stdscr.refresh()
            self.win_draw_chatbox()
            self.win_draw_sidebar()
            self.win_draw_inputfield()
        except:
            curses.beep()

    # was very tired and lazy when i made this abomination
    def win_draw_sidebar(self, message_object=None):
        def br():
            return 20 * "~"
        
        self.sidebar_border.border()
        self.sidebar.erase()

        if message_object:
            object = tchat_message.message_decode(message_object)
            self.sidebar_data = [br(), f" Name : {object.server_name}",
                         f" Users: {object.connected_clients}/{object.max_clients}", br()
                         ]
            for connected in object.clients_info_dict:
                if connected.user_id == connected.username:
                    self.sidebar_data.append(f" {connected.user_id}")
                else:
                    self.sidebar_data.append(f" {connected.user_id} ~ {connected.username}")

            for i in range(min(len(self.sidebar_data), self.screen_height - 5)):
                try:
                    if str(self.sidebar_data[i]) == str(br()):
                        self.sidebar.addstr(i, 0, self.sidebar_data[i], curses.color_pair(tchat_message.TEXT_COLOR_YELLOW))
                    else:
                        self.sidebar.addstr(i, 0, self.sidebar_data[i][:self.sidebar_width-5])
                except:
                    pass
        else:
            if self.sidebar_data:
                for i in range(min(len(self.sidebar_data), self.screen_height - 5)):
                    try:
                        if self.sidebar_data[i] == br():
                            self.sidebar.addstr(i, 0, self.sidebar_data[i], curses.color_pair(tchat_message.TEXT_COLOR_YELLOW))
                        else:
                            self.sidebar.addstr(i, 0, self.sidebar_data[i][:self.sidebar_width-4 -8])
                    except:
                        pass
            
        self.sidebar_border.refresh()
        self.sidebar.refresh()
        self.inputfield.refresh()


    def win_draw_inputfield(self):
        self.inputfield.erase()
        self.inputfield_border.border()

        inputfield_width = self.screen_width - 5
        user_input_display = self.user_input_message[self.user_input_offset:inputfield_width + self.user_input_offset - 1]
        if len(user_input_display) > inputfield_width:
            curses.beep()
        self.inputfield.addstr(0, 0, user_input_display, curses.color_pair(1))
        
        
        self.inputfield_border.addch(1,1, ">")
        self.inputfield_border.refresh()
        self.inputfield.refresh()

    def win_draw_chatbox(self):
        self.chatbox.erase()
        chatbox_height = self.screen_height - 5
        chatbox_width = self.screen_width - self.sidebar_width  - 3

        temp_lines_offset = sum([self.calc_lines_needed(msg.total_length, chatbox_width) for msg in self.chatbox_messages])
        if temp_lines_offset <= chatbox_height:
            self.shows_first_message = True
            cursor_y = 0
            for msg in self.chatbox_messages:
                complete_message = msg.sender_name + msg.separator + msg.message
                self.chatbox.addstr(cursor_y, 0, complete_message, curses.color_pair(msg.text_color))
                cursor_y = self.chatbox.getyx()[0] + 1
        else:
            total_lines_offset = 0
            self.shows_first_message = False
            for i in range(min(chatbox_height, len(self.chatbox_messages))):
                try:
                    recent_message = self.chatbox_messages[len(self.chatbox_messages) - i - 1 - self.chat_scroll_index]
                    total_lines_offset += self.calc_lines_needed(recent_message.total_length, chatbox_width)
                    complete_message = recent_message.sender_name + recent_message.separator + recent_message.message
                    self.chatbox.addstr(chatbox_height - total_lines_offset, 0, complete_message, curses.color_pair(recent_message.text_color))
                    if recent_message == self.chatbox_messages[0]:
                        self.shows_first_message = True
                except Exception as e:
                    continue
        
        self.chatbox_border.border()
        self.chatbox_border.refresh()
        self.chatbox.refresh()

    def remove_char_in_input(self):
        string1 = self.user_input_message[:self.relative_cursor_string_x]
        string2 = self.user_input_message[self.relative_cursor_string_x + 1:]
        self.user_input_message = string1 + string2

    def handle_resize(self):
        self.win_draw_global()
        inputfield_width = self.screen_width - 5
        if len(self.user_input_message) >= inputfield_width:
            self.user_input_offset = len(self.user_input_message) - (inputfield_width - 1)
            self.relative_cursor_string_x = len(self.user_input_message)
            self.win_draw_inputfield()
        else:
            self.user_input_offset = 0

    def handle_character_input(self, user_input):
        self.user_input_message += chr(user_input)
        self.update_dimensions()
        if self.inputfield.getyx()[1] == self.screen_width - 6:
            self.user_input_offset += 1
        self.win_draw_inputfield()
        self.relative_cursor_string_x += 1


    def handle_backspace(self):
        if self.relative_cursor_string_x != 0:
            if self.user_input_offset > 0:
                self.user_input_offset -= 1
            self.relative_cursor_string_x -= 1
            self.remove_char_in_input()
            self.win_draw_inputfield()
        else:
            curses.beep()

    def get_user_input(self):
        return self.user_input_message

    def calc_lines_needed(self, text_length, chatbox_width):
        return math.ceil(text_length / chatbox_width)