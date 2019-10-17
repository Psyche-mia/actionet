import tkinter as tk
import os
import ai2thor.controller
from PIL import Image, ImageTk
import keyboard
import threading

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
        scene_frame = tk.Frame(self)
        scene_frame.pack(side="top", fill="both")
        scene_text = tk.Label(self, text="Choose scene:")
        scene_text.pack(in_=scene_frame, side="left", fill="x")
        self.scene = tk.StringVar(self)
        self.scene.set(SCENES[0])
        scene_options = tk.OptionMenu(self, self.scene, *SCENES)
        scene_options.pack(in_=scene_frame, side="left")

        # Select task
        TASKS = [
            "Make coffee"
        ]
        task_frame = tk.Frame(self)
        task_frame.pack(side="top", fill="both")
        task_text = tk.Label(self, text="Choose task:")
        task_text.pack(in_=task_frame, side="left", fill="x")
        self.task = tk.StringVar(self)
        self.task.set(TASKS[0])
        task_options = tk.OptionMenu(self, self.task, *TASKS)
        task_options.pack(in_=task_frame, side="left")

class ControllerPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

    # Start running user_controller.py
    def start(self, scene, task, status):
        # Instruction
        instruction = "\nINSTRUCTIONS:\n "\
               "Use arrows keys to move, 'WASD' to look around, 'esc' to abort a new action\n " \
               "'end'-to enter a new action | 'o'-open an object | 'u'-pick up an object\n" \
               "'p'-put an object down | 't'-toggle on an object | 'f'-toggle off an object.\n" \
               "'c'-close object | 'k'-throw object | 'i'-drop object\n" \
               "'l' -push object | 'r' -pull object | 'z' -slice object\n" \
               "'b' -break object | 'm' -dirty object | 'y' -clean object\n" \
               "'g' -empty object | 'h' -fill object\n"
        instruction_label = tk.Label(self, text=instruction)
        instruction_label.pack(side="top")

        # Show middle level tasks
        middle_level_tasks ="\nMIDDLE LEVEL TASKS:\n " \
                "0.Navigate 1.Toast 2.Boil\n" \
                "3.Wash     4.Fry   5.Heat\n" \
                "6.Serve    7.Cook  8.Finish    9.Robotic Control\n "
        middle_level_tasks_label = tk.Label(self, text=middle_level_tasks)
        middle_level_tasks_label.pack(side="top")

        # Show status
        status['text'] = "STATUS: Task '" + task + "' in progress..."

        # Show page
        self.show()

        # Instantiate AI2-THOR
        ai2_thor_thread = threading.Thread(target=self.ai2_thor(scene), args=[])
        ai2_thor_thread.start()

        # TODO: https://www.oreilly.com/library/view/python-cookbook/0596001673/ch09s07.html
        # ai2thor_frame = ImageTk.PhotoImage(Image.fromarray(event.frame))
        # ai2thor_label = tk.Label(self, image=ai2thor_frame)
        # ai2thor_label.image=ai2thor_frame
        # ai2thor_label.pack(side="top")
    
    def ai2_thor(self,scene):
        controller = ai2thor.controller.Controller()
        controller.start(player_screen_width=300,
                player_screen_height=300)
        # controller1 = ai2thor.controller.Controller()
        # controller1.start()

        controller.reset('FloorPlan'+scene)
        event = controller.step(dict(action='Initialize', gridSize=0.25,renderObjectImage="True"))

        # Record user data
        action_list = []
        midtasks = []

        while True:
            # Add mid-level actions
            anglehand=0
            temp1 =[]
            midtask=['Navigate','Toast','Boil','Wash','Fry','Heat','Serve','Cook','Nill','Robotic control']
            
            name = input("Name your action (enter 'Finish' if you have completed your task): ")
            target =input("Target of your action: ")
            middleleveltask= midtask[int(name)]
            temp1.append(middleleveltask)
            temp1.append(target)

            print("Middle level Task: "+middleleveltask +target)
            # Task complete
            if name == '8':
                with open("program1.txt","w") as output:
                    # output.write(str(name_list))
                    output.write(str(action_list))
                with open("program2.txt","w") as output:
                    output.write(str(midtasks))
                print("Task complete.")
                break

            temp = []
            while True:
                anglehand=anglehand+30.0
                if keyboard.is_pressed('right'):
                    event = controller.step(dict(action='MoveRight'))
                    # event = controller1.step(dict(action='MoveRight'))
                    ai2thor_frame = ImageTk.PhotoImage(Image.fromarray(event.frame))
                    # ai2thor_label.configure(image=ai2thor_frame)
                    # ai2thor_label.image=ai2thor_frame
                    temp.append('MoveRight')

class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        startconfig = StartConfigPage(self)
        controller = ControllerPage(self)

        # Show status
        status = tk.Label(self, text="STATUS: Task not started.")
        status.pack(side="top", fill="x")

        # Set consistent frame
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        
        # Set pages in frame
        startconfig.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        controller.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        # Create start button
        start_button = tk.Button(startconfig, text="START TASK", command= lambda: controller.start(startconfig.scene.get(),startconfig.task.get(), status))
        start_button.pack(side="bottom", fill="x", expand=False)

        startconfig.show()

    def check_not_default(self):
        pass

if __name__ == "__main__":
    root = tk.Tk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("600x600")
    root.mainloop()