import tkinter as tk
import os
import ai2thor.controller
from PIL import Image, ImageTk
import keyboard
import threading
import queue
import time

class Gui():
    """
    Set overall GUI.
    """
    def __init__(self, root):
        """Initialise GUI."""
        # Create queues
        # TODO: Create remaining queues
        scene_queue = queue.Queue()
        frame_queue = queue.Queue()
        metadata_queue = queue.Queue()

        # Show status
        status = tk.Label(root, text="STATUS: Choosing scene and task...")
        status.pack(side="top", fill="x")

        # Set consistent frame
        container = tk.Frame(root)
        container.pack(side="top", fill="both", expand=True)

        # Instantiate AI2-THOR with queues
        ai2_thor = AI2THOR(scene_queue, frame_queue, metadata_queue)
        ai2_thor_thread = threading.Thread(target=lambda: ai2_thor.run())
        ai2_thor_thread.start()

        # Set initial page to choose task page
        choose_task = ChooseTaskPage(root)
        choose_task.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        choose_task.show(root, container, status, choose_task, None, None, None, scene_queue, frame_queue, metadata_queue)


class ChooseTaskPage(tk.Frame):
    """
    Set choose task page GUI.
    """
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

    def show(self, root, container, status, choose_task, choose_action, do_action, do_input, scene_queue, frame_queue, metadata_queue):
        # Clear unused pages
        if choose_action != None:
            choose_action.destroy()
        if do_action != None:
            do_action.destroy()
        if do_input != None:
            do_input.destroy()

        self.scene_queue = scene_queue
        self.frame_queue = frame_queue

        # TODO: Create middle level actions list
        # TODO: Create middle level actions + target list
        # TODO: Create base actions list

        status['text'] = "STATUS: Choosing scene and task..."

        # Show initial frame
        self.ai2thor_frame = tk.Label(self)
        self.get_and_set_frame()
        self.ai2thor_frame.pack(side="top")

        # Select scene
        SCENES = [
            "1",
            "2",
            "3"
        ]
        scene_frame = tk.Frame(self)
        scene_frame.pack(side="top")
        scene_text = tk.Label(self, text="Choose scene:")
        scene_text.pack(in_=scene_frame, side="left")
        self.scene = tk.StringVar(self)
        self.scene.set(SCENES[0])
        self.scene_queue.put(SCENES[0])
        self.scene.trace("w",self.send_scene)
        scene_options = tk.OptionMenu(self, self.scene, *SCENES)
        scene_options.pack(in_=scene_frame, side="left")

        # Select task
        TASKS = [
            "Make Coffee"
        ]
        task_frame = tk.Frame(self)
        task_frame.pack(side="top")
        task_text = tk.Label(self, text="Choose task:")
        task_text.pack(in_=task_frame, side="left")
        task = tk.StringVar(self)
        task.set(TASKS[0])
        task_options = tk.OptionMenu(self, task, *TASKS)
        task_options.pack(in_=task_frame, side="left")

        # Create start task button
        choose_action = ChooseActionPage(root)
        choose_action.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        start_button = tk.Button(self, text="START TASK", command= lambda: choose_action.show(root, container, status, task.get(), 'START_'+self.scene.get(), choose_task, choose_action, None, None, scene_queue, frame_queue, metadata_queue, self.ai2thor_frame.image))
        start_button.pack(side="bottom", fill="x", expand=False)

        self.lift()

    def send_scene(self, *args):
        """Get scene in the scene options and send to scene_queue."""
        self.scene_queue.put(self.scene.get())

    def get_and_set_frame(self):
        """Get first frame in the frame_queue, if any, and set the GUI frame to that frame."""
        try:
            frame = self.frame_queue.get(0)
            self.ai2thor_frame.configure(image=frame)
            self.ai2thor_frame.image = frame
            self.after(100, self.get_and_set_frame)
        except queue.Empty:
            self.after(100, self.get_and_set_frame)


class ChooseActionPage(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

    def show(self, root, container, status, task, scene, choose_task, choose_action, do_action, do_input, scene_queue, frame_queue, metadata_queue, initial_frame):
        # Clear unused pages
        if choose_task != None:
            choose_task.destroy()
        if do_action != None:
            do_action.destroy()
        if do_input != None:
            do_input.destroy()
        
        """Show information for action."""
        scene_queue.put(scene)
        scene = scene[6:]

        # Show status
        status['text'] = "STATUS: Choosing new middle level action for '" + task + "' task for scene " + scene + "..."

        # Show initial frame
        ai2thor_frame = tk.Label(self)
        ai2thor_frame.configure(image=initial_frame)
        ai2thor_frame.image = initial_frame
        ai2thor_frame.pack(side="top")

        # Add text to show this is action choice
        mid_action_frame = tk.Frame(self)
        mid_action_frame.pack(side="top")
        mid_action_text = tk.Label(self, text="Choose action:")
        mid_action_text.pack(in_=mid_action_frame, side="left")

        # Show middle level actions
        MID_ACTIONS = [
            "Navigate",
            "Toast",
            "Boil",
            "Wash",
            "Fry",
            "Heat",
            "Serve",
            "Cook",
            "Robotic Control",
            "Finish"
        ]
        mid_actions = tk.StringVar(self)
        mid_actions.set(MID_ACTIONS[0])
        mid_actions_options = tk.OptionMenu(self, mid_actions, *MID_ACTIONS)
        mid_actions_options.pack(in_=mid_action_frame, side="left")

        # Add text to show this is target object choice
        objects_frame = tk.Frame(self)
        objects_frame.pack(side="top")
        objects_text = tk.Label(self, text="Choose target object:")
        objects_text.pack(in_=objects_frame, side="left")

        # Show possible target objects
        OBJECTS = [
            "Coffee"
        ]
        objects = tk.StringVar(self)
        objects.set(OBJECTS[0])
        objects_options = tk.OptionMenu(self, objects, *OBJECTS)
        objects_options.pack(in_=objects_frame, side="left")

        # Create start action button
        do_action = DoActionPage(root)
        do_action.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        start_action_button = tk.Button(self, text="START ACTION", command= lambda: do_action.show(root, container, status, task, mid_actions.get(), objects.get(), scene, None, choose_action, do_action, None, scene_queue, frame_queue, metadata_queue, initial_frame))
        start_action_button.pack(side="bottom", fill="x", expand=False)

        # Show page
        self.lift()


class DoActionPage(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

    def show(self, root, container, status, task, action, target_object, scene, choose_task, choose_action, do_action, do_input, scene_queue, frame_queue, metadata_queue, initial_frame):
        # Clear unused pages
        if choose_action != None:
            choose_action.destroy()
        if choose_task != None:
            choose_task.destroy()
        if do_input != None:
            do_input.destroy()

        self.frame_queue = frame_queue
        self.metadata_queue = metadata_queue

        # Show status
        status['text'] = "STATUS: Doing middle level action '" + action + target_object + "' for '" + task + "' task..."

        # Show frame(s)
        self.ai2thor_frame = tk.Label(self)
        self.ai2thor_frame.configure(image=initial_frame)
        self.ai2thor_frame.image = initial_frame
        self.ai2thor_frame.pack(side="top")

        # Instruction
        instruction = "\nINSTRUCTIONS: Use arrows keys to move, 'WASD' to look around\n"
        instruction_label = tk.Label(self, text=instruction)
        instruction_label.pack(side="top")

        # Show metadata
        self.ai2thor_metadata = tk.Label(self)
        self.ai2thor_metadata.pack(side="top")

        # Create finish task button --> make sure at least one action in middle level action
        choose_task = ChooseTaskPage(root)
        choose_task.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        self.finish_task_button = tk.Button(self, text="--------------- FINISH TASK ---------------", command= lambda: choose_task.show(root, container, status, choose_task, None, do_action, None, scene_queue, frame_queue, metadata_queue))
        self.finish_task_button.pack(side="bottom", fill="x", expand=False)

        # Create finish action button
        choose_action = ChooseActionPage(root)
        choose_action.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        self.finish_action_button = tk.Button(self, text="FINISH ACTION", command= lambda: choose_action.show(root, container, status, task, scene, choose_task, choose_action, do_action, None, scene_queue, frame_queue, metadata_queue, self.ai2thor_frame.image))
        self.finish_action_button.pack(side="bottom", fill="x", expand=False)

        # TODO: Create abort action button
        # self.abort_action_button = tk.Button(self, text="ABORT ACTION", command= lambda: do_action())
        # self.abort_action_button.pack(side="bottom", fill="x", expand=False)
        
        self.lift()

        self.get_and_set_frame()
        self.get_and_set_metadata()

    def get_and_set_frame(self):
        """Get first frame in the frame_queue, if any, and set the GUI frame to that frame."""
        try:
            frame = self.frame_queue.get(0)
            self.ai2thor_frame.configure(image=frame)
            self.ai2thor_frame.image = frame
            self.after(5, self.get_and_set_frame)
        except queue.Empty:
            self.after(5, self.get_and_set_frame)

    def get_and_set_metadata(self):
        """Get first metadata in the metadata_queue, if any, and set the GUI metadata to that metadata."""
        try:
            metadata = self.metadata_queue.get(0)
            self.ai2thor_metadata['text'] = metadata
            self.after(5, self.get_and_set_metadata)
        except queue.Empty:
            self.after(5, self.get_and_set_metadata)
        

class DoInputPage(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

    def show(self, root, action_type):
        # TODO: Show all appropriate buttons
        #  'o'-open an object | 'u'-pick up an object\n" \
        #        "'p'-put an object down | 't'-toggle on an object | 'f'-toggle off an object.\n" \
        #        "'c'-close object | 'k'-throw object | 'i'-drop object\n" \
        #        "'l' -push object | 'r' -pull object | 'z' -slice object\n" \
        #        "'b' -break object | 'm' -dirty object | 'y' -clean object\n" \
        #        "'g' -empty object | 'h' -fill object\n"

        # TODO: Show appropriate object choices in OptionsMenu
        # TODO: Pause keyboard
        
        self.lift()

    def get_and_set_choices(self):
        # Show list of object choices
        pass


class AI2THOR():
    def __init__(self, scene_queue, frame_queue, metadata_queue):
        self.scene_queue = scene_queue
        self.frame_queue = frame_queue
        self.metadata_queue = metadata_queue

    def run(self):
        """Run AI2-THOR."""
        controller = ai2thor.controller.Controller()
        controller.start(player_screen_width=300,
                player_screen_height=300)

        choose_task = True
        choose_action = False
        do_action = False
        do_input = False

        # Check for conditions
        while choose_task:
            try:
                scene = self.scene_queue.get(0)

                if scene.startswith('START_'):
                    choose_task = False
                    # Ignore the characters 'START_'
                    scene = scene[6:]
                    controller.reset('FloorPlan'+scene)
                    event = controller.step(dict(action='Initialize', gridSize=0.25,renderObjectImage="True"))
                
                    # Send frame to GUI
                    ai2thor_frame = ImageTk.PhotoImage(Image.fromarray(event.frame))
                    self.send_frame(ai2thor_frame)
                elif scene != None:
                    controller.reset('FloorPlan'+scene)
                    event = controller.step(dict(action='Initialize', gridSize=0.25,renderObjectImage="True"))
                
                    # Send frame to GUI
                    ai2thor_frame = ImageTk.PhotoImage(Image.fromarray(event.frame))
                    self.send_frame(ai2thor_frame)
            except queue.Empty:
                continue

        # Record user data
        action_list = []
        midtasks = []

        # while True:
        #     # Add mid-level actions
        #     anglehand=0
        #     temp1 =[]
            
        #     # Wait for action input
        #     # target =input("Target of your action: ")
        #     # temp1.append(middleleveltask)
        #     # temp1.append(target)

        #     # print("Middle level Task: "+middleleveltask +target)
        #     # # Task complete
        #     # if name == '8':
        #     #     with open("program1.txt","w") as output:
        #     #         # output.write(str(name_list))
        #     #         output.write(str(action_list))
        #     #     with open("program2.txt","w") as output:
        #     #         output.write(str(midtasks))
        #     #     print("Task complete.")
        #     #     break

        temp = []
        while True:
            # Sleep to prevent this from being too fast
            time.sleep(0.005)

            if keyboard.is_pressed('right'):
                event = controller.step(dict(action='MoveRight'))
                ai2thor_frame = ImageTk.PhotoImage(Image.fromarray(event.frame))
                # Send frame to GUI
                self.send_metadata(event.metadata['objects'])
                self.send_frame(ai2thor_frame)
                temp.append('MoveRight')
            elif keyboard.is_pressed('up'):
                event = controller.step(dict(action='MoveAhead'))
                ai2thor_frame = ImageTk.PhotoImage(Image.fromarray(event.frame))
                # Send frame to GUI
                self.send_metadata(event.metadata['objects'])
                self.send_frame(ai2thor_frame)
                temp.append('MoveAhead')
            elif keyboard.is_pressed('down'):
                event = controller.step(dict(action='MoveBack'))
                ai2thor_frame = ImageTk.PhotoImage(Image.fromarray(event.frame))
                # Send frame to GUI
                self.send_metadata(event.metadata['objects'])
                self.send_frame(ai2thor_frame)
                temp.append('MoveBack')
            elif keyboard.is_pressed('left'):
                event = controller.step(dict(action='MoveLeft'))
                ai2thor_frame = ImageTk.PhotoImage(Image.fromarray(event.frame))
                # Send frame to GUI
                self.send_metadata(event.metadata['objects'])
                self.send_frame(ai2thor_frame)
                temp.append('MoveLeft')
            # Finish mid-level action
            elif keyboard.is_pressed('end'):
                if len(temp) > 0:
                    action_list.append(temp)
                    midtasks.append(temp1)
                    break
                else:
                    break
            # Abort mid-level action
            elif keyboard.is_pressed('esc'):
                # TODO: Revert to original attributes
                break

    def send_frame(self, frame):
        """Send frame to the frame_queue."""
        self.frame_queue.put(frame)

    def send_metadata(self, metadata):
        """Send metadata to the metadata_queue."""
        self.metadata_queue.put(metadata)


if __name__ == "__main__":
    root = tk.Tk()
    root.wm_geometry("600x600")

    # Instantiate GUI
    gui = Gui(root)
    root.mainloop()