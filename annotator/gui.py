import tkinter as tk
import os
import ai2thor.controller
from PIL import Image, ImageTk
import keyboard
import threading
import queue
import time
import re
import operator
from tkinter.ttk import *


class Gui():
    """
    Set overall GUI.
    """

    def __init__(self, root):
        """Initialise GUI."""
        # Create queues
        stage_queue = queue.Queue()
        scene_queue = queue.Queue()
        frame_queue = queue.Queue()
        object_queue = queue.Queue()
        input_queue = queue.Queue()

        # Show status
        status = tk.Label(root, text="STATUS: Choosing scene and task...")
        status.pack(side="top", fill="x")

        # Set consistent frame
        container = tk.Frame(root)
        container.pack(side="top", fill="both", expand=True)

        # Instantiate AI2-THOR with queues
        ai2_thor = AI2THOR(stage_queue, scene_queue, frame_queue, object_queue, input_queue)
        ai2_thor_thread = threading.Thread(target=lambda: ai2_thor.run())
        ai2_thor_thread.start()

        # Set initial page to choose task page
        choose_task = ChooseTaskPage(root)
        choose_task.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        choose_task.show(root, container, status, choose_task, None, None, None, stage_queue, scene_queue, frame_queue,
                         object_queue, input_queue)


class ChooseTaskPage(tk.Frame):
    """
    Set choose task page GUI.
    """

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

    def show(self, root, container, status, choose_task, choose_action, do_action, do_input, stage_queue, scene_queue,
             frame_queue, object_queue, input_queue):
        # Clear unused pages
        if choose_action != None:
            choose_action.destroy()
        if do_action != None:
            do_action.destroy()
        if do_input != None:
            do_input.destroy()

        stage_queue.put('choose_task')
        self.scene_queue = scene_queue
        self.frame_queue = frame_queue

        # TODO: Create middle level actions list
        # TODO: Create middle level actions + target list
        # TODO: Create base actions list

        status['text'] = "STATUS: Choosing scene and task...\n"

        # Show initial frame
        self.ai2thor_frame = tk.Label(self)
        self.get_and_set_frame()
        self.ai2thor_frame.pack(side="top")

        # Select scene
        SCENES = [
            "1",
            "2",
            "4",
            "5",
            "7"
        ]
        scene_frame = tk.Frame(self)
        scene_frame.pack(side="top")
        scene_text = tk.Label(self, text="Choose scene:")
        scene_text.pack(in_=scene_frame, side="left")
        self.scene = tk.StringVar(self)
        self.scene.set(SCENES[0])
        self.scene_queue.put(SCENES[0])
        self.scene.trace("w", self.send_scene)
        scene_options = Combobox(self, textvariable=self.scene, state="readonly", values=SCENES)
        scene_options.pack(in_=scene_frame, side="left")

        # Select task
        TASKS = [
            "Make Coffee",
            "Wash dishes",
            "Prepare Slice apple",
            "Toast a bread",
            "Fry an egg",
            "Make tomato soup",
            "Make lettuce soup",
            "Boil water with pot",
            "Throw away cracked egg",
            "Clear the fridge",
            "Boil water with kettle"
        ]
        task_frame = tk.Frame(self)
        task_frame.pack(side="top")
        task_text = tk.Label(self, text="Choose task:")
        task_text.pack(in_=task_frame, side="left")
        task = tk.StringVar(self)
        task.set(TASKS[0])
        task_options = Combobox(self, textvariable=task, state="readonly", values=TASKS)
        task_options.pack(in_=task_frame, side="left")

        # Create start task button
        choose_action = ChooseActionPage(root)
        choose_action.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        start_button = tk.Button(self, text="START TASK",
                                 command=lambda: choose_action.show(root, container, status, task.get(),
                                                                    self.scene.get(), choose_task, choose_action, None,
                                                                    None, stage_queue, scene_queue, frame_queue,
                                                                    object_queue, input_queue,
                                                                    self.ai2thor_frame.image))
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
    """
    Set choose action page GUI.
    """

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

    def show(self, root, container, status, task, scene, choose_task, choose_action, do_action, do_input, stage_queue,
             scene_queue, frame_queue, object_queue, input_queue, initial_frame):
        """Show information for action."""
        # Clear unused pages
        if choose_task != None:
            choose_task.destroy()
        if do_action != None:
            do_action.destroy()
        if do_input != None:
            do_input.destroy()

        stage_queue.put('choose_action')
        scene_queue.put(scene)

        self.object_queue = object_queue
        while True:
            try:
                objects = self.object_queue.get(0)
                break
            except queue.Empty:
                pass

        # Show status
        status['text'] = "TASK:"+task + "' task in scene " + scene + "...\n"

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
            "Boil",
            "Cook",
            "Fry",
            "Heat",
            "Navigate",
            "Robotic Control",
            "Serve",
            "Toast",
            "Wash",
        ]
        mid_actions = tk.StringVar(self)
        mid_actions.set(MID_ACTIONS[0])
        mid_actions_options = Combobox(self, textvariable=mid_actions, state="readonly", values=MID_ACTIONS)
        mid_actions_options.pack(in_=mid_action_frame, side="left")

        # Add text to show this is target object choice
        objects_frame = tk.Frame(self)
        objects_frame.pack(side="top")
        objects_text = tk.Label(self, text="Choose target object:")
        objects_text.pack(in_=objects_frame, side="left")

        f = open("program1.txt", "r")
        contents = f.read()

        instruction = "\nINSTRUCTIONS:" + contents
        instruction_label = tk.Label(self, text=instruction)
        instruction_label.pack(side="top")

        # Show possible target objects
        objects.sort()
        OBJECTS = objects
        objects = tk.StringVar(self)
        objects.set(OBJECTS[0])
        objects_options = Combobox(self, textvariable=objects, state="readonly", values=OBJECTS)
        objects_options.pack(in_=objects_frame, side="left")

        # Create start action button
        do_action = DoActionPage(root)
        do_action.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        start_action_button = tk.Button(self, text="START ACTION",
                                        command=lambda: do_action.show(root, container, status, task, mid_actions.get(),
                                                                       objects.get(), scene, None, choose_action,
                                                                       do_action, None, stage_queue, scene_queue,
                                                                       frame_queue, object_queue, input_queue,
                                                                       initial_frame))
        start_action_button.pack(side="bottom", fill="x", expand=False)

        # Show page
        self.lift()


class DoActionPage(tk.Frame):
    """
    Choose do action page GUI.
    """

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

    def show(self, root, container, status, task, action, target_object, scene, choose_task, choose_action, do_action,
             do_input, stage_queue, scene_queue, frame_queue, object_queue, input_queue, initial_frame):
        # Clear unused pages
        if choose_action != None:
            choose_action.destroy()
        if choose_task != None:
            choose_task.destroy()
        if do_input != None:
            do_input.destroy()

        self.frame_queue = frame_queue
        self.object_queue = object_queue
        self.stage_queue = stage_queue

        stage_queue.put('do_action')

        # Show status
        status[
            'text'] = "TASK:"+ task + " task in scene " + scene + "...\n"

        # Show frame(s)
        self.ai2thor_frame = tk.Label(self)
        self.ai2thor_frame.configure(image=initial_frame)
        self.ai2thor_frame.image = initial_frame
        self.ai2thor_frame.pack(side="top")

        # Instruction
        f = open("program1.txt", "r")
        contents = f.read()

        instruction = "\nINSTRUCTIONS:" + contents
        instruction_label = tk.Label(self, text=instruction)
        instruction_label.pack(side="top")
        load = Image.open("keyboard control.png")
        load = load.resize((820,230))
        render = ImageTk.PhotoImage(load)

        # labels can be text or images
        img = Label(self, image=render)
        img.image = render
        img.place(x=0, y=460)


        # Object interaction button
        do_input = DoInputPage(root)
        do_input.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        object_interaction_button = tk.Button(self, text="Interact with an object",
                                              command=lambda: do_input.show(root, container, status, task, action,
                                                                            target_object, scene, None, None, do_action,
                                                                            do_input, stage_queue, scene_queue,
                                                                            frame_queue, object_queue, input_queue,
                                                                            self.ai2thor_frame.image))
        object_interaction_button.pack(side="top", expand=False)

        # Create finish task button
        choose_task = ChooseTaskPage(root)
        choose_task.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        finish_task_button = tk.Button(self, text="--------------- FINISH TASK ---------------",
                                       command=lambda: choose_task.show(root, container, status, choose_task, None,
                                                                        do_action, do_input, stage_queue, scene_queue,
                                                                        frame_queue, object_queue, input_queue))
        finish_task_button.pack(side="bottom", fill="x", expand=False)

        # Create finish action button --> TODO: make sure at least one action in middle level action
        choose_action = ChooseActionPage(root)
        choose_action.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        finish_action_button = tk.Button(self, text="FINISH ACTION",
                                         command=lambda: choose_action.show(root, container, status, task, scene,
                                                                            choose_task, choose_action, do_action,
                                                                            do_input, stage_queue, scene_queue,
                                                                            frame_queue, object_queue, input_queue,
                                                                            self.ai2thor_frame.image))
        finish_action_button.pack(side="bottom", fill="x", expand=False)

        self.lift()

        self.get_and_set_frame()

    def get_and_set_frame(self):
        """Get first frame in the frame_queue, if any, and set the GUI frame to that frame."""
        try:
            frame = self.frame_queue.get(0)
            self.ai2thor_frame.configure(image=frame)
            self.ai2thor_frame.image = frame
            self.after(5, self.get_and_set_frame)
        except queue.Empty:
            self.after(5, self.get_and_set_frame)


class DoInputPage(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

    def show(self, root, container, status, task, action, target_object, scene, choose_task, choose_action, do_action,
             do_input, stage_queue, scene_queue, frame_queue, object_queue, input_queue, initial_frame):
        # Clear unused pages
        if choose_action != None:
            choose_action.destroy()
        if choose_task != None:
            choose_task.destroy()
        if do_action != None:
            do_action.destroy()

        # Send stage update to AI2-THOR
        stage_queue.put('get_instance_obj')

        self.frame_queue = frame_queue
        self.object_queue = object_queue
        while True:
            try:
                object_list = self.object_queue.get(0)
                break
            except queue.Empty:
                pass

        self.input_queue = input_queue

        # Change status
        status[
            'text'] = "STATUS: Interacting with object for '" + action + target_object + "' action for '" + task + "' task in scene " + scene + "...\n"

        # Show initial frame
        self.ai2thor_frame = tk.Label(self)
        self.ai2thor_frame.configure(image=initial_frame)
        self.ai2thor_frame.image = initial_frame
        self.ai2thor_frame.pack(side="top")

        # Show interaction action choices
        input_action_frame = tk.Frame(self)
        input_action_frame.pack(side="top")
        input_action_text = tk.Label(self, text="Choose interaction:")
        input_action_text.pack(in_=input_action_frame, side="left")

        INPUT_ACTIONS = [
            "Break",
            "Clean",
            "Close",
            "Dirty",
            "Drop",
            "Empty",
            "Fill",
            "Open",
            "Pick up",
            "Used up",
            "Pull",
            "Push",
            "Put down",
            "Slice",
            "Throw",
            "Toggle off",
            "Toggle on",
        ]
        self.input_actions = tk.StringVar(self)
        self.input_actions.set(INPUT_ACTIONS[0])
        self.input_actions.trace("w", self.configure_buttons)
        input_actions_options = Combobox(self, textvariable=self.input_actions, state="readonly", values=INPUT_ACTIONS)
        input_actions_options.pack(in_=input_action_frame, side="left")

        # Show possible target objects
        self.target_object_frame = tk.Frame(self)
        self.target_object_frame.pack(side="top")
        self.target_object_text = tk.Label(self, text="Choose target object:")
        self.target_object_text.pack(in_=self.target_object_frame, side="left")



        # Show possible target objects to PUT DOWN
        self.put_down_target_object_frame = tk.Frame(self)
        self.put_down_target_object_frame.pack(side="top")
        self.put_down_target_object_text = tk.Label(self, text="Choose location:")
        self.put_down_target_object_text.pack(in_=self.put_down_target_object_frame, side="left")
        self.put_down_target_object_frame.pack_forget()
        f = open("program1.txt", "r")
        contents = f.read()

        instruction = "\nINSTRUCTIONS:" + contents
        instruction_label = tk.Label(self, text=instruction)
        instruction_label.pack(side="bottom")
        LIQUIDS = [
            'coffee',
            'water',
            'wine'
        ]

        # Show possible liquids to FILL a target object with
        self.fill_target_object_frame = tk.Frame(self)
        self.fill_target_object_frame.pack(side="top")
        self.fill_target_object_text = tk.Label(self, text="Choose liquid:")
        self.fill_target_object_text.pack(in_=self.fill_target_object_frame, side="left")
        self.fill_target_object_frame.pack_forget()

        liquids = tk.StringVar(self)
        liquids.set(LIQUIDS[0])
        liquid_options = Combobox(self, textvariable=liquids, state="readonly", values=LIQUIDS)
        liquid_options.pack(in_=self.fill_target_object_frame, side="left")

        # Get list of objects from AI2-THOR instance segmentation for target objects
        object_list.sort()
        OBJECTS = object_list
        self.objects = tk.StringVar(self)
        self.objects.set(OBJECTS[0])
        self.objects.trace("w", self.send_object_emphasis)
        objects_options = Combobox(self, textvariable=self.objects, state="readonly", values=OBJECTS)
        objects_options.pack(in_=self.target_object_frame, side="left")

        # Also use list of objects from AI2-THOR instance segmentation for put down
        object_list.sort()
        OBJECTS = object_list
        self.object_locations = tk.StringVar(self)
        self.object_locations.set(OBJECTS[0])
        objects_location_options = Combobox(self, textvariable=self.object_locations, state="readonly", values=OBJECTS)
        objects_location_options.pack(in_=self.put_down_target_object_frame, side="left")

        # Create finish interaction button
        do_action = DoActionPage(root)
        do_action.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        finish_action_button = tk.Button(self, text="FINISH INTERACTION",
                                         command=lambda: self.after_input_before_action(root, container, status, task,
                                                                                        action, target_object, scene,
                                                                                        None, None, do_action, do_input,
                                                                                        stage_queue, scene_queue,
                                                                                        frame_queue, object_queue,
                                                                                        self.input_queue, initial_frame,
                                                                                        True, self.input_actions.get(),
                                                                                        self.objects.get(),
                                                                                        liquids.get(),
                                                                                        self.object_locations.get()))
        finish_action_button.pack(side="bottom", fill="x", expand=False)

        self.get_and_set_frame()

        self.lift()

    def after_input_before_action(self, root, container, status, task, action, target_object, scene, choose_task,
                                  choose_action, do_action, do_input, stage_queue, scene_queue, frame_queue,
                                  object_queue, input_queue, initial_frame, interaction, input_action,
                                  target_interaction_object, fill_liquid, put_object_location):
        if interaction:
            stage_queue.put('do_input')
            input_queue.put(['interaction', input_action, target_interaction_object, fill_liquid, put_object_location])

        do_action.show(root, container, status, task, action, target_object, scene, None, None, do_action, do_input,
                       stage_queue, scene_queue, frame_queue, object_queue, self.input_queue, initial_frame)

    def send_object_emphasis(self, *args):
        """
        Send objectId to be emphasised and get frame in return.
        """
        # Show emphasis on selected object to let user know which object is selected
        self.input_queue.put(['emphasis', self.objects.get()])

    def get_and_set_frame(self):
        try:
            frame = self.frame_queue.get(0)
            self.ai2thor_frame.configure(image=frame)
            self.ai2thor_frame.image = frame
            self.after(5, self.get_and_set_frame)
        except queue.Empty:
            self.after(5, self.get_and_set_frame)

    def configure_buttons(self, *args):
        """
        Hide or show buttons depending on needs.
        """
        interaction = self.input_actions.get()
        if interaction == 'Drop' or interaction == 'Throw':
            self.target_object_frame.pack_forget()
            self.put_down_target_object_frame.pack_forget()
            self.fill_target_object_frame.pack_forget()
        elif interaction == 'Fill':
            self.target_object_frame.pack()
            self.put_down_target_object_frame.pack_forget()
            self.fill_target_object_frame.pack()
        elif interaction == 'Put down':
            self.target_object_frame.pack()
            self.put_down_target_object_frame.pack()
            self.fill_target_object_frame.pack_forget()
        else:
            self.target_object_frame.pack()
            self.put_down_target_object_frame.pack_forget()
            self.fill_target_object_frame.pack_forget()


class AI2THOR():
    def __init__(self, stage_queue, scene_queue, frame_queue, object_queue, input_queue):
        self.stage_queue = stage_queue
        self.scene_queue = scene_queue
        self.frame_queue = frame_queue
        self.object_queue = object_queue
        self.input_queue = input_queue

    def run(self):
        """Run AI2-THOR."""
        controller = ai2thor.controller.Controller()
        controller.start(player_screen_width=700,
                         player_screen_height=350)
        anglehandx = 0.0
        anglehandy = 0.0
        anglehandz = 0.0
        # Set initial stage to None
        stage = None

        while True:
            # Check which stage the user is at

            # Sleep to prevent this from being too fast
            time.sleep(0.005)

            # Try to get stage from stage_queue
            try:
                stage = self.stage_queue.get(0)
            except queue.Empty:
                pass

            if stage == 'choose_task':
                try:
                    scene = self.scene_queue.get(0)

                    controller.reset('FloorPlan' + scene)
                    event = controller.step(dict(action='Initialize', gridSize=0.25, renderObjectImage="True"))

                    # Send frame to GUI
                    ai2thor_frame = ImageTk.PhotoImage(Image.fromarray(event.frame))
                    self.send_frame(ai2thor_frame)
                except queue.Empty:
                    continue
            elif stage == 'choose_action':
                # Send list of all objects to GUI
                objects = []
                for obj in event.metadata['objects']:
                    # Remove underscore and characters after underscore
                    obj_name = re.search('^[^_]+', obj['name']).group()
                    if obj_name not in objects:
                        objects.append(obj_name)
                self.object_queue.put(objects)
                stage = 'pause'
            elif stage == 'do_action':
                # Send frame(s) to GUI

                if keyboard.is_pressed('right'):
                    event = controller.step(dict(action='MoveRight'))
                    ai2thor_frame = ImageTk.PhotoImage(Image.fromarray(event.frame))
                    self.send_frame(ai2thor_frame)
                elif keyboard.is_pressed('up'):
                    event = controller.step(dict(action='MoveAhead'))
                    ai2thor_frame = ImageTk.PhotoImage(Image.fromarray(event.frame))
                    self.send_frame(ai2thor_frame)
                elif keyboard.is_pressed('down'):
                    event = controller.step(dict(action='MoveBack'))
                    ai2thor_frame = ImageTk.PhotoImage(Image.fromarray(event.frame))
                    self.send_frame(ai2thor_frame)
                elif keyboard.is_pressed('left'):
                    event = controller.step(dict(action='MoveLeft'))
                    ai2thor_frame = ImageTk.PhotoImage(Image.fromarray(event.frame))
                    self.send_frame(ai2thor_frame)
                elif keyboard.is_pressed('8'):
                    event = controller.step(dict(action='MoveHandAhead', moveMagnitude = 0.1))
                    ai2thor_frame = ImageTk.PhotoImage(Image.fromarray(event.frame))
                    self.send_frame(ai2thor_frame)
                elif keyboard.is_pressed('5'):
                    event = controller.step(dict(action='MoveHandBack', moveMagnitude = 0.1))
                    ai2thor_frame = ImageTk.PhotoImage(Image.fromarray(event.frame))
                    self.send_frame(ai2thor_frame)
                elif keyboard.is_pressed('4'):
                    event = controller.step(dict(action='MoveHandLeft', moveMagnitude = 0.1))
                    ai2thor_frame = ImageTk.PhotoImage(Image.fromarray(event.frame))
                    self.send_frame(ai2thor_frame)
                elif keyboard.is_pressed('6'):
                    event = controller.step(dict(action='MoveHandRight', moveMagnitude = 0.1))
                    ai2thor_frame = ImageTk.PhotoImage(Image.fromarray(event.frame))
                    self.send_frame(ai2thor_frame)
                elif keyboard.is_pressed('7'):
                    event = controller.step(dict(action='MoveHandUp', moveMagnitude = 0.1))
                    ai2thor_frame = ImageTk.PhotoImage(Image.fromarray(event.frame))
                    self.send_frame(ai2thor_frame)
                elif keyboard.is_pressed('9'):
                    event = controller.step(dict(action='MoveHandDown', moveMagnitude = 0.1))
                    ai2thor_frame = ImageTk.PhotoImage(Image.fromarray(event.frame))
                    self.send_frame(ai2thor_frame)
                elif keyboard.is_pressed('1'):
                    anglehandx = anglehandx + 30.0
                    event = controller.step(dict(action='RotateHand', x = anglehandx))
                    ai2thor_frame = ImageTk.PhotoImage(Image.fromarray(event.frame))
                    self.send_frame(ai2thor_frame)
                elif keyboard.is_pressed('2'):
                    anglehandy = anglehandy + 30.0
                    event = controller.step(dict(action='RotateHand', y = anglehandy))
                    ai2thor_frame = ImageTk.PhotoImage(Image.fromarray(event.frame))
                    self.send_frame(ai2thor_frame)
                elif keyboard.is_pressed('3'):
                    anglehandz = anglehandz + 30.0
                    event = controller.step(dict(action='RotateHand', z = anglehandz))
                    ai2thor_frame = ImageTk.PhotoImage(Image.fromarray(event.frame))
                    self.send_frame(ai2thor_frame)
                elif keyboard.is_pressed('a'):
                    event = controller.step(dict(action='RotateLeft'))
                    # position = event.metadata['agent']['position']
                    # rotation = event.metadata['agent']['rotation']
                    # event = controller.step(
                    #     dict(action='TeleportFull', x=position.get('x'), y=position.get('y'), z=position.get('z'),
                    #          rotation=rotation.get('y') - 45.0, horizon=0.0))
                    ai2thor_frame = ImageTk.PhotoImage(Image.fromarray(event.frame))
                    self.send_frame(ai2thor_frame)
                elif keyboard.is_pressed('d'):
                    event = controller.step(dict(action='RotateRight'))
                    # position = event.metadata['agent']['position']
                    # rotation = event.metadata['agent']['rotation']
                    # event = controller.step(
                    #     dict(action='TeleportFull', x=position.get('x'), y=position.get('y'), z=position.get('z'),
                    #          rotation=rotation.get('y') + 45.0, horizon=0.0))
                    ai2thor_frame = ImageTk.PhotoImage(Image.fromarray(event.frame))
                    self.send_frame(ai2thor_frame)
                elif keyboard.is_pressed('w'):
                    event = controller.step(dict(action='LookUp'))
                    ai2thor_frame = ImageTk.PhotoImage(Image.fromarray(event.frame))
                    self.send_frame(ai2thor_frame)
                elif keyboard.is_pressed('s'):
                    event = controller.step(dict(action='LookDown'))
                    ai2thor_frame = ImageTk.PhotoImage(Image.fromarray(event.frame))
                    self.send_frame(ai2thor_frame)
            elif stage == 'get_instance_obj':
                # Send list of objects in current instance segmentation frame to GUI
                objects = []
                list1 = []
                list2 = []
                dict2 = {}
                list4 = []
                list5 = []
                for obj_id in event.metadata['objects']:
                    # Remove underscore and characters after underscore
                    # obj_name1 = re.search('^[^_]+', obj_id['name']).group()
                    # if obj_name1 not in objects:
                    for key, value in obj_id.items():
                        if key == 'objectId':
                            list1.append(value)
                        if key == 'distance':
                            list2.append(value)
                dict1 = dict(zip(list1, list2))
                for i, v in dict1.items():
                    if 'StoveBurner' in i:
                        dict2.update({i: v})
                if not len(dict2) == 0:
                    lowest = min(dict2.items(), key=operator.itemgetter(1))[0]
                    list4.append(lowest)
                    dict2.clear()

                for i, v in dict1.items():
                    if 'Cabinet' in i:
                        dict2.update({i: v})
                if not len(dict2) == 0:
                    lowest = min(dict2.items(), key=operator.itemgetter(1))[0]
                    list4.append(lowest)
                    dict2.clear()

                for i, v in dict1.items():
                    if 'CounterTop' in i:
                        dict2.update({i: v})
                if not len(dict2) == 0:
                    lowest = min(dict2.items(), key=operator.itemgetter(1))[0]
                    list4.append(lowest)
                    dict2.clear()

                for i, v in dict1.items():
                    if 'Shelf' in i:
                        dict2.update({i: v})
                if not len(dict2) == 0:
                    lowest = min(dict2.items(), key=operator.itemgetter(1))[0]
                    list4.append(lowest)
                    dict2.clear()

                for i, v in dict1.items():
                    if 'Drawer' in i:
                        dict2.update({i: v})
                if not len(dict2) == 0:
                    lowest = min(dict2.items(), key=operator.itemgetter(1))[0]
                    list4.append(lowest)
                    dict2.clear()

                for i, v in dict1.items():
                    if 'StoveKnob' in i:
                        dict2.update({i: v})
                if not len(dict2) == 0:
                    lowest = min(dict2.items(), key=operator.itemgetter(1))[0]
                    list4.append(lowest)
                    dict2.clear()

                for i, v in dict1.items():
                    if 'TableTop' in i:
                        dict2.update({i: v})
                if not len(dict2) == 0:
                    lowest = min(dict2.items(), key=operator.itemgetter(1))[0]
                    list4.append(lowest)
                    dict2.clear()

                list1 = [x for x in list1 if not re.search('StoveBurner', x)]
                list1 = [x for x in list1 if not re.search('StoveKnob', x)]
                list1 = [x for x in list1 if not re.search('TableTop', x)]
                list1 = [x for x in list1 if not re.search('Cabinet', x)]
                list1 = [x for x in list1 if not re.search('Drawer', x)]
                list1 = [x for x in list1 if not re.search('CounterTop', x)]
                list1 = [x for x in list1 if not re.search('Shelf', x)]
                objects = objects+list1 + list4
                self.object_queue.put(objects)
                stage = 'do_input'
            elif stage == 'do_input':
                try:
                    interaction = self.input_queue.get(0)

                    if interaction[0] == 'emphasis':
                        event = controller.step({"action": "EmphasizeObject", "objectId": interaction[1]})
                        # event = controller.step({"action": "EmphasizeObject", "receptacleObjectId": interaction[1]})
                        # Send frame to GUI
                        ai2thor_frame = ImageTk.PhotoImage(Image.fromarray(event.frame))
                        self.send_frame(ai2thor_frame)
                    elif interaction[0] == 'interaction':
                        event = controller.step({"action": "UnemphasizeAll"})

                        if interaction[1] == 'Break':
                            event = controller.step(dict(action='BreakObject', objectId=interaction[2]))
                        elif interaction[1] == 'Clean':
                            event = controller.step(dict(action='CleanObject', objectId=interaction[2]))
                        elif interaction[1] == 'Close':
                            event = controller.step(dict(action='CloseObject', objectId=interaction[2]))
                        elif interaction[1] == 'Dirty':
                            event = controller.step(dict(action='DirtyObject', objectId=interaction[2]))
                        elif interaction[1] == 'Drop':
                            event = controller.step(dict(action='DropHandObject'))
                        elif interaction[1] == 'Empty':
                            event = controller.step(dict(action='EmptyLiquidFromObject', objectId=interaction[2]))
                        elif interaction[1] == 'Fill':
                            event = controller.step(
                                dict(action='FillObjectWithLiquid', objectId=interaction[2], fillLiquid=interaction[3]))
                        elif interaction[1] == 'Open':
                            event = controller.step(dict(action='OpenObject', objectId=interaction[2]))
                        elif interaction[1] == 'Used up':
                            event = controller.step(dict(action='UseUpObject', objectId=interaction[2]))
                        elif interaction[1] == 'Pick up':
                            event = controller.step(dict(action='PickupObject', objectId=interaction[2]))
                        elif interaction[1] == 'Pull':
                            event = controller.step(
                                dict(action='PullObject', objectId=interaction[2], moveMagnitude=10.0))
                        elif interaction[1] == 'Push':
                            event = controller.step(
                                dict(action='PushObject', objectId=interaction[2], moveMagnitude=10.0))
                        elif interaction[1] == 'Put down':
                            event = controller.step(
                                dict(action='PutObject', objectId=interaction[2], receptacleObjectId=interaction[4]))
                        elif interaction[1] == 'Slice':
                            event = controller.step(dict(action='SliceObject', objectId=interaction[2]))
                        elif interaction[1] == 'Throw':
                            event = controller.step(dict(action='ThrowObject', moveMagnitude=100.0))
                        elif interaction[1] == 'Toggle off':
                            event = controller.step(dict(action='ToggleObjectOff', objectId=interaction[2]))
                        elif interaction[1] == 'Toggle on':
                            event = controller.step(dict(action='ToggleObjectOn', objectId=interaction[2]))

                        # Send frame to GUI
                        ai2thor_frame = ImageTk.PhotoImage(Image.fromarray(event.frame))
                        self.send_frame(ai2thor_frame)
                except queue.Empty:
                    pass
            elif stage == 'pause':
                pass

    def send_frame(self, frame):
        """Send frame to the frame_queue."""
        self.frame_queue.put(frame)

    def send_current_objects(self, current_objects):
        """Send all object choices to the object_queue."""
        self.object_queue.put(current_objects)


if __name__ == "__main__":
    root = tk.Tk()
    root.wm_geometry("820x800")

    # Instantiate GUI
    gui = Gui(root)
    root.mainloop()
