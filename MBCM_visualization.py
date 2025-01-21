import tkinter as tk
from time import time
from webbrowser import open as web_open
from MultyBaseComputingMachine import *

class PNM_visualisation:

    def __init__(self):
        self.UI = None
        self.machine = None
        self.console_status = False # False - instructions, True - console
        self.instr_text = ''
        self.console_text = ''
        self.instr_console_locking = False
        self.console_locking = True
        self.text_state = {False: 'normal', True: 'disabled'}
        self.current_step = -1

        self.is_step = True
        self.time_executing = 0
        self.time_measuring = False
        self.start_time = 0

        self.lang = "Укр"
        self.text = {
            'Укр': {
                'info': [
                    "Основа чисел",
                    "Кількість слів в пам'яті",
                    "Місткість слова",
                    ["Час виконання програми", "сек"],
                    "Введіть інформацію про БЕОМ та інструкції"
                ],
                'another_lang': "Eng",
                'btn': {
                    'lang': "Eng",
                    'step': "Крок",
                    'instr': 'Інструкції',
                    'end': 'Кінець',
                    'mem': "Пам'ять",
                    'cnsl': 'Консоль',
                    'execute': 'Створити',
                    'prog': 'Програма',
                },
                'header': 'Багатоосновна обчислювальна електронна машина',
                'mem': {
                    0: 'Бат',
                    1: '',
                    2: '',
                    3: '',
                }
            },
            'Eng': {
                'info': [
                    "Base of number",
                    "Quantity words in memory",
                    "Capacity of word",
                    ["Executing program time", "s"],
                    "Input MBCM's parameters and instructions"
                ],
                'another_lang': "Укр",
                'btn': {
                    'lang': "Укр",
                    'step': "Step",
                    'instr': 'Instructions',
                    'end': 'End',
                    'mem': "Memory",
                    'cnsl': 'Console',
                    'execute': 'Create',
                    'prog': 'Program',
                },
                'header': 'Multy-base computing machine',
                'mem': {
                    0: 'Batt',
                    1: '',
                    2: '',
                    3: '',
                }
            }
        }
        self.create_visualisation()

    def show_memory_matrix(self):
        self.update_matrix('memory')

    def show_instructions_matrix(self):
        self.update_matrix('instructions')

    def show_actual_console(self):
        if not self.console_status:
            self.show_instr()
        else:
            self.show_console()

    def highlight_line(self):
        self.editable_text.tag_remove("highlight", "1.0", "end")
        if self.current_step != -1 and self.console_status == False:
            start = f"{self.current_step + 2}.0"
            end = f"{self.current_step + 2}.end"
            self.editable_text.tag_add("highlight", start, end)
            self.editable_text.tag_config("highlight", background="#0073e6")

    def show_instr(self):
        if self.console_status == False:
            self.instr_text = self.editable_text.get("1.0", "end-1c")
        if self.console_locking == True:
            self.editable_text.configure(state='normal')
            if self.console_status == True:
                self.console_text = self.editable_text.get("1.0", "end-1c")
            self.editable_text.delete(1.0, "end")
            self.editable_text.insert(1.0, self.instr_text)
            self.console_status = False
            self.highlight_line()
            self.editable_text.configure(state=self.text_state[self.instr_console_locking])

    def show_console(self):
        self.editable_text.configure(state='normal')
        if not self.console_status:
            self.instr_text = self.editable_text.get("1.0", "end-1c")
        self.editable_text.delete(1.0, "end")
        self.editable_text.insert(1.0, self.console_text)
        self.console_status = True
        self.highlight_line()
        self.editable_text.configure(state=self.text_state[self.console_locking])

    def update_console_text(self, recipient_status, text:str):
        if recipient_status == self.console_status:
            self.editable_text.insert("end", text)

    def update_info(self, text=''):
        if text != '':
            self.static_text.config(text=text)
            return
        if self.UI is not None:
            sep = ': '
            new_text = self.text[self.lang]['info'][0] + sep + str(self.machine.NS) + '\n' + \
                       self.text[self.lang]['info'][1] + sep + str(self.machine.const['main']['word']['amount']) + '\n' + \
                       self.text[self.lang]['info'][2] + sep + str(self.machine.const['main']['word']['capacity'])
            if self.time_executing != 0:
                new_text += '\n' + self.text[self.lang]['info'][3][0] + sep + str(self.time_executing) + ' ' + self.text[self.lang]['info'][3][1]
            self.static_text.config(text=new_text)
        else:
            self.static_text.config(text=self.text[self.lang]['info'][-1])

    def update_text(self):
        self.update_info()
        self.show_memory_matrix()
        self.root.title(self.text[self.lang]['header'])
        self.btn_prog.config(text=self.text[self.lang]['btn']['prog'])
        self.btn_end.config(text=self.text[self.lang]['btn']['end'])
        self.btn_instr.config(text=self.text[self.lang]['btn']['instr'])
        self.btn_mem.config(text=self.text[self.lang]['btn']['mem'])
        self.btn_cnsl.config(text=self.text[self.lang]['btn']['cnsl'])
        self.btn_execute.config(text=self.text[self.lang]['btn']['execute'])
        self.btn_step.config(text=self.text[self.lang]['btn']['step'])
        self.btn_lang.config(text=self.text[self.lang]['btn']['lang'])
        self.header_label.config(text=self.text[self.lang]['header'])

    def change_language(self):
        self.lang = self.text[self.lang]['another_lang']
        self.update_text()

    def open_info(self, event):
        web_open('https://docs.google.com/document/d/14ImVzvMt15tfGAmMM6jdkcK9DQwH5IlnJNKutn1MR8Q/edit?tab=t.0')

    def create_visualisation(self):
        self.scale = 1.5

        window_width = int(600 * self.scale)
        window_height = int(400 * self.scale)
        button_height = int(30 * self.scale)
        matrix_size = int(340 * self.scale)
        button_spacing_x = int(10 * self.scale)
        button_spacing_y = int(10 * self.scale)
        editable_text_width = int(225 * self.scale)
        editable_text_height = int(100 * self.scale)
        button_1_width = (editable_text_width - 2 * button_spacing_x) // 3
        button_1_height = int(40 * self.scale)
        info_text_width = editable_text_width
        info_text_height = int(80 * self.scale)
        button_width = (editable_text_width - button_spacing_x) // 2
        button_bottom_width = button_1_width // 1.5
        button_bottom_height = button_1_height // 1.5

        self.root = tk.Tk()
        self.root.geometry(f"{window_width}x{window_height}")
        self.root.option_add("*Font", f"Arial {int(10 * self.scale)}")
        self.root.config(bg="#99ccff")
        self.root.resizable(False, False)
        self.input_value = tk.StringVar()
        self.to_continue = tk.BooleanVar()


        self.header_label = tk.Label(self.root, text="", bg="#99ccff", font=("Arial", int(10 * self.scale)))
        self.header_label.place(x=button_spacing_x, y=button_spacing_y, width=matrix_size, height=int(20 * self.scale))

        matrix_frame = tk.Frame(self.root, bg="#002080")
        matrix_frame.place(x=button_spacing_x, y=button_spacing_y + int(20 * self.scale) + button_spacing_y,
                           width=matrix_size, height=matrix_size)

        v_scrollbar = tk.Scrollbar(matrix_frame, orient=tk.VERTICAL)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        h_scrollbar = tk.Scrollbar(matrix_frame, orient=tk.HORIZONTAL)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        self.canvas = tk.Canvas(matrix_frame, bg="#002080", yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.config(command=self.canvas.yview)
        h_scrollbar.config(command=self.canvas.xview)

        self.inner_frame = tk.Frame(self.canvas, bg="#002080")
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        self.show_memory_matrix()

        self.inner_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

        self.btn_mem = tk.Button(self.root, text="", bg="#3366ff", command=self.show_memory_matrix, fg="white")
        self.btn_mem.place(x=button_spacing_x + matrix_size + button_spacing_x, y=button_spacing_y, width=button_width,
                          height=button_height)

        self.btn_instr = tk.Button(self.root, text="", bg="#3366ff", command=self.show_instructions_matrix, fg="white")
        self.btn_instr.place(x=button_spacing_x + matrix_size + button_spacing_x + button_width + button_spacing_x,
                          y=button_spacing_y, width=button_width, height=button_height)

        self.btn_prog = tk.Button(self.root, text="", bg="#3366ff", command=self.show_instr, fg="white")
        self.btn_prog.place(x=button_spacing_x + matrix_size + button_spacing_x,
                          y=button_spacing_y + button_height + button_spacing_y, width=button_width,
                          height=button_height)

        self.btn_cnsl = tk.Button(self.root, text="", bg="#3366ff", command=self.show_console, fg="white")
        self.btn_cnsl.place(x=button_spacing_x + matrix_size + button_spacing_x + button_width + button_spacing_x,
                          y=button_spacing_y + button_height + button_spacing_y, width=button_width,
                          height=button_height)

        editable_text_frame = tk.Frame(self.root, bg="gray")
        editable_text_frame.place(x=button_spacing_x + matrix_size + button_spacing_x,
                                  y=button_spacing_y + 2 * (button_height + button_spacing_y),
                                  width=editable_text_width, height=editable_text_height)

        self.editable_text = tk.Text(editable_text_frame, bg="#00134d", fg="white", wrap=tk.WORD,
                                font=("Arial", int(10 * self.scale)))
        self.editable_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        text_scrollbar = tk.Scrollbar(editable_text_frame, orient=tk.VERTICAL, command=self.editable_text.yview)
        text_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.editable_text.config(yscrollcommand=text_scrollbar.set, insertbackground="white")

        self.btn_execute = tk.Button(self.root, text="", bg="#3366ff", fg="white",
                                   command=self.launch_PNM)
        self.btn_execute.place(x=button_spacing_x + matrix_size + button_spacing_x,
                             y=button_spacing_y + 2 * (
                                     button_height + button_spacing_y) + editable_text_height + button_spacing_y,
                             width=button_1_width, height=button_1_height)

        self.btn_step = tk.Button(self.root, text="", bg="#3366ff", fg="white",
                                   command=self.next_step)
        self.btn_step.place(
            x=button_spacing_x + matrix_size + button_spacing_x + button_1_width + button_spacing_x,
            y=button_spacing_y + 2 * (button_height + button_spacing_y) + editable_text_height + button_spacing_y,
            width=button_1_width, height=button_1_height)

        self.btn_end = tk.Button(self.root, text="", bg="#3366ff", fg="white",
                                   command=self.execute_to_end)
        self.btn_end.place(
            x=button_spacing_x + matrix_size + button_spacing_x + 2 * (button_1_width + button_spacing_x),
            y=button_spacing_y + 2 * (button_height + button_spacing_y) + editable_text_height + button_spacing_y,
            width=button_1_width, height=button_1_height)

        self.static_text = tk.Label(self.root, text="", bg="#002080", fg="white", font=("Arial", int(10 * self.scale)), anchor="nw", justify="left", wraplength=info_text_width - button_spacing_x)
        self.static_text.place(x=button_spacing_x + matrix_size + button_spacing_x,
                          y=button_spacing_y + 2 * (
                                  button_height + button_spacing_y) + editable_text_height + button_spacing_y + button_1_height + button_spacing_y,
                          width=info_text_width, height=info_text_height)


        self.btn_lang = tk.Button(self.root, text=self.text[self.lang]['another_lang'], bg="#3366ff", fg="white",
                                   command=self.change_language)
        self.btn_lang.place(x=matrix_size + editable_text_width - button_bottom_width - button_bottom_height + button_spacing_x,
                y=button_spacing_y + 2 * (
                button_height + button_spacing_y) + editable_text_height + 2 * button_spacing_y + button_1_height + button_spacing_y + info_text_height,
                width=button_bottom_width, height=button_bottom_height)

        canvas = tk.Canvas(self.root, width=button_bottom_width, height=button_bottom_height, highlightthickness=0)
        canvas.config(background='#99ccff')
        canvas.place(x=matrix_size + editable_text_width - button_spacing_x,
                y=button_spacing_y + 2 * (
                button_height + button_spacing_y) + editable_text_height + 2 * button_spacing_y + button_1_height + button_spacing_y + info_text_height,
                width=button_bottom_height + 5 * self.scale, height=button_bottom_height + 5*self.scale)

        circle = canvas.create_oval(0, 0, button_bottom_height, button_bottom_height, fill="#3366ff", outline="black", width=0)
        text = canvas.create_text(button_bottom_height // 2, button_bottom_height // 2, text="i", fill="white", font=("Times New Roman", 30, "bold"))
        canvas.tag_bind(circle, "<Button-1>", self.open_info)
        canvas.tag_bind(text, "<Button-1>", self.open_info)

        self.update_text()
        self.show_actual_console()
        self.update_info()

        self.editable_text.bind("<Return>", self.handle_input)
        self.editable_text.bind("<BackSpace>", self.handle_backspace)

        self.root.mainloop()

    def update_matrix(self, source_str:str):
        if self.machine is None:
            return
        if source_str == 'memory':
            source = self.machine.MB
            memory = self.machine.memory_size
            word = self.machine.word
        else:
            source = self.machine.IB
            memory = self.machine.instr_stack_size
            word = self.machine.instr_word
        for widget in self.inner_frame.winfo_children():
            widget.destroy()
        for i in range(memory):
            row = []
            if source_str == 'memory' and i < 4:
                row_label = tk.Label(self.inner_frame, text=self.text[self.lang]['mem'][i], bg="#002080", fg="white",
                                     font=("Arial", int(7 * self.scale)))
            else:
                if source_str == 'memory':
                    row_label = tk.Label(self.inner_frame, text=str(i - self.machine.const['mem']['reserved']), bg="#002080", fg="white",
                                         font=("Arial", int(10 * self.scale)))
                else:
                    row_label = tk.Label(self.inner_frame, text=str(i),
                                         bg="#002080", fg="white",
                                         font=("Arial", int(10 * self.scale)))
            row_label.grid(row=i, column=0, padx=2, pady=2)
            for j in range(word):
                value = source.read(Unit(self.param, i * word + j)).val
                label = tk.Label(self.inner_frame, text=str(value), bg="white", relief="solid")
                label.grid(row=i, column=j + 1, padx=2, pady=2, sticky="nsew")
                row.append(label)
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def handle_backspace(self, event):
        if self.console_status == True and self.console_locking == False:
                input_index = self.editable_text.search(">>>", "end-1c", backwards=True)
                if self.editable_text.index("insert") > str(float(input_index) + 0.4):
                    return
        if self.console_status == False:
            return
        return 'break'

    def handle_input(self, event):
        if (self.console_status == True) and (self.console_locking == False):
            input_index = self.editable_text.search(">>>", "end-1c", backwards=True)
            input_value = self.editable_text.get(f"{input_index}+4c", "end-1c").strip()
            self.console_text += input_value
            self.input_value_lst = input_value.split()
            self.machine.const['console']['stream'] = self.input_value_lst
            self.console_locking = True
            self.console_text += '\n'
            self.show_console()
            self.input_value.set(input_value)

    def next_step(self):
        self.to_continue.set(True)

    def launch_PNM(self):
        if self.console_status == False:
            self.instr_text = self.editable_text.get("1.0", "end-1c")
        self.time_executing = 0
        self.console_text = ''
        self.console_status = False
        self.instr_console_locking = True
        self.console_locking = True
        self.to_continue.set(False)
        self.is_step = True
        rows = self.instr_text.split('\n')
        try:
            self.UI = UI(rows[0].split(), {'pause': self.pause})
            self.machine = self.UI.machine
            self.UI.update_console_interface(self.input_f, self.print_f)
            self.param = [self.machine.NS, self.UI.machine.const['main']['word']['size']]
            for i in range(1, len(rows)):
                command = rows[i].split()
                if len(command) <= 0: continue
                command_lst = command + ['0'] * (3 - len(command))
                self.UI.add_instruction(command_lst[2], command_lst[0], command_lst[1])
        except Exception as ex:
            self.update_info(str(ex))
        else:
            self.execute()

    def execute(self, is_beginning = True):
        self.show_actual_console()
        if is_beginning:
            self.show_memory_matrix()
            self.update_info()
        exception_text = ''

        try:
            self.UI.execute()
        except Exception as ex:
            exception_text = ex
        if self.time_measuring:
            self.time_executing = round(time() - self.start_time, 3)

        self.time_measuring = False
        self.instr_console_locking = False
        self.show_instr()
        self.show_memory_matrix()
        self.update_info(exception_text)
        self.time_executing = 0

    def execute_to_end(self):
        if self.UI != None:
            self.time_measuring = True
            self.start_time = time()
            self.is_step = False
            self.to_continue.set(True)
            self.instr_console_locking = False
            self.show_memory_matrix()


    def print_f(self, text):
        self.console_text += str(text)
        self.show_console()

    def input_f(self):
        if not (self.console_text.endswith('\n') or self.console_text == ''):
            self.print_f('\n')
        self.print_f('>>> ')
        self.editable_text.mark_set("insert", "end")
        self.console_locking = False
        self.show_console()
        self.root.wait_variable(self.input_value)

    def pause(self, current_step):
        if self.is_step:
            self.current_step = current_step
            self.highlight_line()
            self.show_memory_matrix()
            self.to_continue.set(False)
            self.root.wait_variable(self.to_continue)


if __name__ == '__main__':
    StartVisualisation = PNM_visualisation()