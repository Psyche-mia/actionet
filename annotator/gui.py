import tkinter as tk
import os
import socket, pickle
import threading
import subprocess

class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()

class StartConfigPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        # Select scene
        SCENES = [
            "1"
        ]

        self.scene = tk.StringVar(self)
        self.scene.set("(CHOOSE SCENE)")
        scene_options = tk.OptionMenu(self, self.scene, *SCENES)
        scene_options.pack()

        # Select task
        TASKS = [
            "Make coffee"
        ]

        self.task = tk.StringVar(self)
        self.task.set("(CHOOSE TASK)")
        task_options = tk.OptionMenu(self, self.task, *TASKS)
        task_options.pack()

        # Instruction
        instruction = "Use arrows keys to move, 'WASD' to look around, 'esc' to abort a new action\n " \
               "'end'-to enter a new action | 'o'-open an object | 'u'-pick up an object\n" \
               "'p'-put an object down | 't'-toggle on an object | 'f'-toggle off an object.\n" \
               "'c'-close object | 'k'-throw object | 'i'-drop object\n" \
               "'l' -push object | 'r' -pull object | 'z' -slice object\n" \
               "'b' -break object | 'm' -dirty object | 'y' -clean object\n" \
               "'g' -empty object | 'h' -fill object\n"

        label = tk.Label(self, text=instruction)
        label.pack(side="top", fill="both", expand=True)

class ControllerPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

    # Start running user_controller.py
    def start(self, scene, task):
        label = tk.Label(self, text="AI2-THOR Metadata")
        label.pack(side="left", fill="both", expand=True)
        self.show()

        subprocess.Popen(["python3","user_controller.py","-scene",scene,"-task",task])

class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        startconfig = StartConfigPage(self)
        controller = ControllerPage(self)

        # Show server status
        server_status = tk.Label(self, text="(SERVER STATUS)")
        server_status.pack(side="top", fill="x")

        # Set solid frame
        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)
        
        # Set pages in frame
        startconfig.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        controller.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        start_button = tk.Button(startconfig, text="START TASK", command= lambda: controller.start(startconfig.scene.get(),startconfig.task.get()))
        start_button.pack(side="bottom", fill="x", expand=False)

        startconfig.show()

    def check_not_default(self):
        pass

# Server socket
class Server:
    clients = []

    def __init__(self, server_status):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.HOST = '127.0.0.1'
        self.PORT = 65432
        self.server_status = server_status

    # Set up connection to client
    def connect(self):
        self.s.bind((self.HOST, self.PORT))
        self.server_status.configure(text="Date: {}\nConnected.\n".format("GGG"))
        self.s.listen()
        self.condition()

    def accept(self):
        c, addr = self.s.accept()
        self.clients.append((c, addr))

    def receive(self):
        for i in self.clients:

            def f():
                data = str(i[0].recv(1024))[1:]

            t1_2_1 = threading.Thread(target=f)
            t1_2_1.start()

    def condition(self):
        while True:
            t1_1 = threading.Thread(target=self.accept)
            t1_1.daemon = True
            t1_1.start()
            t1_1.join(1)
            t1_2 = threading.Thread(target=self.receive)
            t1_2.daemon = True
            t1_2.start()
            t1_2.join(1)

    def send(self):
        pass
        # respond = str(entry.get())
        # now = str(datetime.now())[:-7]
        # entry.delete("0", "end")
        # try:
        #     for i in self.clients:
        #         i.sendall(bytes(respond.encode("utf-8")))
        #     text.insert("insert", "\nDate: {}\nServer: {}\n".format(now, respond))
        # except BrokenPipeError:
        #     text.insert("insert", "\nDate: {}\nClient has been disconnected.\n".format(now))

if __name__ == "__main__":
    root = tk.Tk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("600x600")
    root.mainloop()

# command=os.system("python3 /home/samson/Documents/github/SamsonYuBaiJian/actionnet/user_controller.py")