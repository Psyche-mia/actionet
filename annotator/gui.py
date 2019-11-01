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
        temp=[]
        temp2=[]

        # Show status
        status = tk.Label(root, text="STATUS: Choosing scene and task...")
        status.pack(side="top", fill="x")

        # Set consistent frame
        container = tk.Frame(root)
        container.pack(side="top", fill="both", expand=True)

        # Instantiate AI2-THOR with queues
        ai2_thor = AI2THOR(stage_queue, scene_queue, frame_queue, object_queue, input_queue,temp,temp2)
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

    def show(self, root, container, status, choose_task, do_action, do_input, review, stage_queue, scene_queue,
             frame_queue, object_queue, input_queue):
        # Clear unused pages
        if do_action != None:
            do_action.destroy()
        if do_input != None:
            do_input.destroy()
        if review != None:
            review.destroy()

        stage_queue.put('choose_task')
        self.scene_queue = scene_queue
        self.frame_queue = frame_queue

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

        # Load all tasks
        with open('resources/tasks.txt') as f:
            TASKS = f.read().split('\n')[:-1]
        
        # Select task
        task_frame = tk.Frame(self)
        task_frame.pack(side="top")
        task_text = tk.Label(self, text="Choose task:")
        task_text.pack(in_=task_frame, side="left")
        task = tk.StringVar(self)
        task.set(TASKS[0])
        task_options = Combobox(self, textvariable=task, state="readonly", values=TASKS)
        task_options.pack(in_=task_frame, side="left")


        # Create start task button
        do_action = DoActionPage(root)
        do_action.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        start_button = tk.Button(self, text="START TASK",
                                 command=lambda: do_action.show(root, container, status, task.get(),
                                                                    self.scene.get(), choose_task, None,
                                                                    None, None, stage_queue, scene_queue, frame_queue,
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
            self.after(1, self.get_and_set_frame)
        except queue.Empty:
            self.after(1, self.get_and_set_frame)


class DoActionPage(tk.Frame):
    """
    Choose do action page GUI.
    """
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

    def show(self, root, container, status, task, scene, choose_task, do_action,
             do_input, review, stage_queue, scene_queue, frame_queue, object_queue, input_queue, initial_frame):
        # Clear unused pages
        if choose_task != None:
            choose_task.destroy()
        if do_input != None:
            do_input.destroy()
        if review != None:
            review.destroy()

        self.frame_queue = frame_queue
        self.object_queue = object_queue
        self.stage_queue = stage_queue

        stage_queue.put('do_action')

        # Show status
        status[
            'text'] = "STATUS: Doing "+ task + " task in scene " + scene + "...\n"

        # Show frame(s)
        self.ai2thor_frame = tk.Label(self)
        self.ai2thor_frame.configure(image=initial_frame)
        self.ai2thor_frame.image = initial_frame
        self.ai2thor_frame.pack(side="top")

        # Instruction description
        f = open("resources/description.txt", "r")
        contents = f.read()
        instruction = "\nINSTRUCTIONS: " + contents
        instruction_label = tk.Label(self, text=instruction,wraplength=700)
        instruction_label.pack(side="top")

        # clock = Label(self)
        # clock.pack(side="bottom")

        # def tick():
        #     global time1
        #     # get the current local time from the PC
        #     time2 = time.strftime('%H:%M:%S')
        #     # if time string has changed, update it
        #     if time2 != time1:
        #         time1 = time2
        #         clock.config(text="Time: "+time2)
        #     # calls itself every 200 milliseconds
        #     # to update the time display as needed
        #     # could use >200 ms, but display gets jerky
        #     clock.after(200, tick)

        # tick()

        # Labels can be text or images
        # keyboard = Image.open("resources/keyboard-control.png")
        # keyboard = keyboard.resize((820,220))
        # keyboard_image = ImageTk.PhotoImage(keyboard)
        # keyboard_label = Label(self, image=keyboard_image)
        # keyboard_label.image = keyboard_image
        # keyboard_label.pack(side="top")

        # Object interaction button
        do_input = DoInputPage(root)
        do_input.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        object_interaction_button = tk.Button(self, text="Interact with an object",
                                              command=lambda: do_input.show(root, container, status, task, scene, None, do_action,
                                                                            do_input, None, stage_queue, scene_queue,
                                                                            frame_queue, object_queue, input_queue,
                                                                            self.ai2thor_frame.image))
        object_interaction_button.pack(side="top", expand=False)

        # Create finish task button
        review = ReviewPage(root)
        review.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        finish_task_button = tk.Button(self, text="FINISH TASK",
                                       command=lambda: review.show(root, container, status, task, scene, None,
                                                                        do_action, do_input, review, stage_queue, scene_queue,
                                                                        frame_queue, object_queue, input_queue))
        finish_task_button.pack(side="bottom", fill="x", expand=False)

        self.lift()

        self.get_and_set_frame()

    def get_and_set_frame(self):
        """Get first frame in the frame_queue, if any, and set the GUI frame to that frame."""
        try:
            frame = self.frame_queue.get(0)
            self.ai2thor_frame.configure(image=frame)
            self.ai2thor_frame.image = frame
            self.after(1, self.get_and_set_frame)
        except queue.Empty:
            self.after(1, self.get_and_set_frame)


class DoInputPage(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

    def show(self, root, container, status, task, scene, choose_task, do_action,
             do_input, review, stage_queue, scene_queue, frame_queue, object_queue, input_queue, initial_frame):
        # Clear unused pages
        if choose_task != None:
            choose_task.destroy()
        if do_action != None:
            do_action.destroy()
        if review != None:
            review.destroy()

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

        # Show initial frame
        self.ai2thor_frame = tk.Label(self)
        self.ai2thor_frame.configure(image=initial_frame)
        self.ai2thor_frame.image = initial_frame
        self.ai2thor_frame.pack(side="top")

        # Instruction description
        f = open("resources/description.txt", "r")
        contents = f.read()
        instruction = "\nINSTRUCTIONS: " + contents
        instruction_label = tk.Label(self, text=instruction,wraplength=700)
        instruction_label.pack(side="top")

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

        # clock = Label(self)
        # clock.pack(side="bottom")

        # def tick():
        #     global time1
        #     # get the current local time from the PC
        #     time2 = time.strftime('%H:%M:%S')
        #     # if time string has changed, update it
        #     if time2 != time1:
        #         time1 = time2
        #         clock.config(text="Time:" + time2)
        #     # calls itself every 200 milliseconds
        #     # to update the time display as needed
        #     # could use >200 ms, but display gets jerky
        #     clock.after(200, tick)

        # tick()
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
                                                                                        scene,
                                                                                        None, do_action, do_input,
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

    def after_input_before_action(self, root, container, status, task, scene, choose_task,
                                  do_action, do_input, stage_queue, scene_queue, frame_queue,
                                  object_queue, input_queue, initial_frame, interaction, input_action,
                                  target_interaction_object, fill_liquid, put_object_location):
        if interaction:
            stage_queue.put('do_input')
            input_queue.put(['interaction', input_action, target_interaction_object, fill_liquid, put_object_location])

        do_action.show(root, container, status, task, scene, None, do_action, do_input, None,
                       stage_queue, scene_queue, frame_queue, object_queue, self.input_queue, initial_frame)

    def send_object_emphasis(self, *args):
        """
        Send objectId to be emphasised and get frame in return.
        """
        self.input_queue.put(['emphasis', self.objects.get()])

    def get_and_set_frame(self):
        try:
            frame = self.frame_queue.get(0)
            self.ai2thor_frame.configure(image=frame)
            self.ai2thor_frame.image = frame
            self.after(1, self.get_and_set_frame)
        except queue.Empty:
            self.after(1, self.get_and_set_frame)

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


class ReviewPage(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

    def show(self, root, container, status, task, scene, choose_task,
            do_action, do_input, review, stage_queue, scene_queue,
            frame_queue, object_queue, input_queue):
        if choose_task != None:
            choose_task.destroy()
        if do_action != None:
            do_action.destroy()
        if do_input != None:
            do_input.destroy()

        self.stage_queue = stage_queue
        self.stage_queue.put("review")
        
        redo_task_button = tk.Button(self, text="REDO TASK",
                                         command=lambda: self.save_or_redo("redo", root, container, status, None,
            None, None, review, self.stage_queue, scene_queue,
            frame_queue, object_queue, input_queue))

        save_task_button = tk.Button(self, text="SAVE TASK",
                                         command=lambda: self.save_or_redo("save", root, container, status, None,
            None, None, review, self.stage_queue, scene_queue,
            frame_queue, object_queue, input_queue))

        save_task_button.pack(side="bottom", fill="x", expand=False)
        redo_task_button.pack(side="bottom", fill="x", expand=False)

        self.lift()

    def save_or_redo(self, state, root, container, status, choose_task,
            do_action, do_input, review, stage_queue, scene_queue,
            frame_queue, object_queue, input_queue):
        if state == "save":
            self.stage_queue.put("save")

        choose_task = ChooseTaskPage(root)
        choose_task.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        choose_task.show(root, container, status, choose_task,
                    None, None, review, stage_queue, scene_queue,
                    frame_queue, object_queue, input_queue)


class AI2THOR():

    def __init__(self, stage_queue, scene_queue, frame_queue, object_queue, input_queue,temp,temp2):
        self.temp = temp
        self.temp2= temp2
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
                self.save = []

                try:
                    scene = self.scene_queue.get(0)

                    controller.reset('FloorPlan' + scene)
                    event = controller.step(dict(action='Initialize', gridSize=0.25, renderObjectImage="True"))

                    # Send frame to GUI
                    ai2thor_frame = ImageTk.PhotoImage(Image.fromarray(event.frame))
                    self.send_frame(ai2thor_frame)
                except queue.Empty:
                    continue
            elif stage == 'do_action':
                # Send frame(s) to GUI

                if keyboard.is_pressed('right'):
                    event = controller.step(dict(action='MoveRight'))
                    ai2thor_frame = ImageTk.PhotoImage(Image.fromarray(event.frame))
                    self.save.append("MoveRight")
                    self.send_frame(ai2thor_frame)
                elif keyboard.is_pressed('up'):
                    event = controller.step(dict(action='MoveAhead'))
                    ai2thor_frame = ImageTk.PhotoImage(Image.fromarray(event.frame))
                    self.save.append("MoveAhead")
                    self.send_frame(ai2thor_frame)
                elif keyboard.is_pressed('down'):
                    event = controller.step(dict(action='MoveBack'))
                    ai2thor_frame = ImageTk.PhotoImage(Image.fromarray(event.frame))
                    self.save.append("MoveBack")
                    self.send_frame(ai2thor_frame)
                elif keyboard.is_pressed('left'):
                    event = controller.step(dict(action='MoveLeft'))
                    ai2thor_frame = ImageTk.PhotoImage(Image.fromarray(event.frame))
                    self.save.append("MoveLeft")
                    self.send_frame(ai2thor_frame)
                elif keyboard.is_pressed('8'):
                    event = controller.step(dict(action='MoveHandAhead', moveMagnitude = 0.1))
                    ai2thor_frame = ImageTk.PhotoImage(Image.fromarray(event.frame))
                    self.save.append("MoveHandAhead")
                    self.send_frame(ai2thor_frame)
                elif keyboard.is_pressed('5'):
                    event = controller.step(dict(action='MoveHandBack', moveMagnitude = 0.1))
                    ai2thor_frame = ImageTk.PhotoImage(Image.fromarray(event.frame))
                    self.save.append("MoveHandBack")
                    self.send_frame(ai2thor_frame)
                elif keyboard.is_pressed('4'):
                    event = controller.step(dict(action='MoveHandLeft', moveMagnitude = 0.1))
                    ai2thor_frame = ImageTk.PhotoImage(Image.fromarray(event.frame))
                    self.save.append("MoveHandLeft")
                    self.send_frame(ai2thor_frame)
                elif keyboard.is_pressed('6'):
                    event = controller.step(dict(action='MoveHandRight', moveMagnitude = 0.1))
                    ai2thor_frame = ImageTk.PhotoImage(Image.fromarray(event.frame))
                    self.save.append("MoveHandRight")
                    self.send_frame(ai2thor_frame)
                elif keyboard.is_pressed('7'):
                    event = controller.step(dict(action='MoveHandUp', moveMagnitude = 0.1))
                    ai2thor_frame = ImageTk.PhotoImage(Image.fromarray(event.frame))
                    self.save.append("MoveHandUp")
                    self.send_frame(ai2thor_frame)
                elif keyboard.is_pressed('9'):
                    event = controller.step(dict(action='MoveHandDown', moveMagnitude = 0.1))
                    ai2thor_frame = ImageTk.PhotoImage(Image.fromarray(event.frame))
                    self.save.append("MoveHandDown")
                    self.send_frame(ai2thor_frame)
                elif keyboard.is_pressed('1'):
                    anglehandx = anglehandx + 30.0
                    event = controller.step(dict(action='RotateHand', x = anglehandx))
                    ai2thor_frame = ImageTk.PhotoImage(Image.fromarray(event.frame))
                    self.save.append("RotateHand X axis")
                    self.send_frame(ai2thor_frame)
                elif keyboard.is_pressed('2'):
                    anglehandy = anglehandy + 30.0
                    event = controller.step(dict(action='RotateHand', y = anglehandy))
                    ai2thor_frame = ImageTk.PhotoImage(Image.fromarray(event.frame))
                    self.save.append("RotateHand Y axis")
                    self.send_frame(ai2thor_frame)
                elif keyboard.is_pressed('3'):
                    anglehandz = anglehandz + 30.0
                    event = controller.step(dict(action='RotateHand', z = anglehandz))
                    ai2thor_frame = ImageTk.PhotoImage(Image.fromarray(event.frame))
                    self.save.append("RotateHand Z axis")
                    self.send_frame(ai2thor_frame)
                elif keyboard.is_pressed('a'):
                    event = controller.step(dict(action='RotateLeft'))
                    # position = event.metadata['agent']['position']
                    # rotation = event.metadata['agent']['rotation']
                    # event = controller.step(
                    #     dict(action='TeleportFull', x=position.get('x'), y=position.get('y'), z=position.get('z'),
                    #          rotation=int(round(rotation.get('y') - 30.0)), horizon=0.0))
                    # time.sleep(.3)
                    # print(rotation)
                    ai2thor_frame = ImageTk.PhotoImage(Image.fromarray(event.frame))
                    self.save.append("RotateLeft")
                    self.send_frame(ai2thor_frame)
                elif keyboard.is_pressed('d'):
                    event = controller.step(dict(action='RotateRight'))
                    # position = event.metadata['agent']['position']
                    # rotation = event.metadata['agent']['rotation']
                    # event = controller.step(
                    #     dict(action='TeleportFull', x=position.get('x'), y=position.get('y'), z=position.get('z'),
                    #          rotation=int(round(rotation.get('y') + 30.0)), horizon=0.0))
                    # time.sleep(.3)
                    # print(rotation)
                    ai2thor_frame = ImageTk.PhotoImage(Image.fromarray(event.frame))
                    self.save.append("RotateRight")
                    self.send_frame(ai2thor_frame)
                elif keyboard.is_pressed('w'):
                    event = controller.step(dict(action='LookUp'))
                    ai2thor_frame = ImageTk.PhotoImage(Image.fromarray(event.frame))
                    self.save.append("LookUp")
                    self.send_frame(ai2thor_frame)
                elif keyboard.is_pressed('s'):
                    event = controller.step(dict(action='LookDown'))
                    ai2thor_frame = ImageTk.PhotoImage(Image.fromarray(event.frame))
                    self.save.append("LookDown")
                    self.send_frame(ai2thor_frame)

            elif stage == 'get_instance_obj':
                # Send list of objects in current instance segmentation frame to GUI
                objects = []
                list1 = []
                list2 = []
                dict2 = {}
                list4 = []
                list5 = []
                # list6=[]
                # list7=[]
                for key, value in event.instance_detections2D.items():
                    list5.append(key)
                for obj_id in event.metadata['objects']:
                    # Remove underscore and characters after underscore
                    # obj_name1 = re.search('^[^_]+', obj_id['name']).group()
                    # if obj_name1 not in objects:
                    for key, value in obj_id.items():
                        if key == 'objectId':
                            list1.append(value)
                            # list6.append(value)
                        if key == 'distance':
                            list2.append(value)
                dict1 = dict(zip(list1, list2))
                # for i, v in dict1.items():
                #     if 'StoveBurner' in i:
                #         dict2.update({i: v})
                # if not len(dict2) == 0:
                #     lowest = min(dict2.items(), key=operator.itemgetter(1))[0]
                #     list4.append(lowest)
                #     dict2.clear()

                # for i, v in dict1.items():
                #     if 'Cabinet' in i:
                #         dict2.update({i: v})
                # if not len(dict2) == 0:
                #     lowest = min(dict2.items(), key=operator.itemgetter(1))[0]
                #     list4.append(lowest)
                #     dict2.clear()

                for i, v in dict1.items():
                    if 'CounterTop' in i:
                        dict2.update({i: v})
                if not len(dict2) == 0:
                    lowest = min(dict2.items(), key=operator.itemgetter(1))[0]
                    list4.append(lowest)
                    dict2.clear()

                for i, v in dict1.items():
                    if 'BreadSliced' in i:
                        dict2.update({i: v})
                if not len(dict2) == 0:
                    lowest = min(dict2.items(), key=operator.itemgetter(1))[0]
                    list4.append(lowest)
                    dict2.clear()

                for i, v in dict1.items():
                    if 'TomatoSliced' in i:
                        dict2.update({i: v})
                if not len(dict2) == 0:
                    lowest = min(dict2.items(), key=operator.itemgetter(1))[0]
                    list4.append(lowest)
                    dict2.clear()

                for i, v in dict1.items():
                    if 'AppleSliced' in i:
                        dict2.update({i: v})
                if not len(dict2) == 0:
                    lowest = min(dict2.items(), key=operator.itemgetter(1))[0]
                    list4.append(lowest)
                    dict2.clear()

                for i, v in dict1.items():
                    if 'LettuceSliced' in i:
                        dict2.update({i: v})
                if not len(dict2) == 0:
                    lowest = min(dict2.items(), key=operator.itemgetter(1))[0]
                    list4.append(lowest)
                    dict2.clear()

                for i, v in dict1.items():
                    if 'PotatoSliced' in i:
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

                # for i, v in dict1.items():
                #     if 'Drawer' in i:
                #         dict2.update({i: v})
                # if not len(dict2) == 0:
                #     lowest = min(dict2.items(), key=operator.itemgetter(1))[0]
                #     list4.append(lowest)
                #     dict2.clear()

                # for i, v in dict1.items():
                #     if 'StoveKnob' in i:
                #         dict2.update({i: v})
                # if not len(dict2) == 0:
                #     lowest = min(dict2.items(), key=operator.itemgetter(1))[0]
                #     list4.append(lowest)
                #     dict2.clear()

                for i, v in dict1.items():
                    if 'TableTop' in i:
                        dict2.update({i: v})
                if not len(dict2) == 0:
                    lowest = min(dict2.items(), key=operator.itemgetter(1))[0]
                    list4.append(lowest)
                    dict2.clear()
                #
                # list1 = [x for x in list1 if not re.search('StoveBurner', x)]
                # list1 = [x for x in list1 if not re.search('StoveKnob', x)]

                # list1 = [x for x in list1 if not re.search('Cabinet', x)]

                list5 = [x for x in list5 if not re.search('CounterTop', x)]
                list5 = [x for x in list5 if not re.search('Shelf', x)]
                list5 = [x for x in list5 if not re.search('TableTop', x)]
                # for i in list6:
                #     if i =="BreadSliced":
                #         list7.append(i)
                # print(list7)
                objects = objects+list5 + list4

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
                            self.save.append("BreakObject")
                            self.save.append(interaction[2])
                        elif interaction[1] == 'Clean':
                            event = controller.step(dict(action='CleanObject', objectId=interaction[2]))
                            self.save.append("CleanObject")
                            self.save.append(interaction[2])
                        elif interaction[1] == 'Close':
                            event = controller.step(dict(action='CloseObject', objectId=interaction[2]))
                            self.save.append("CloseObject")
                            self.save.append(interaction[2])
                        elif interaction[1] == 'Dirty':
                            event = controller.step(dict(action='DirtyObject', objectId=interaction[2]))
                            self.save.append("DirtyObject")
                            self.save.append(interaction[2])
                        elif interaction[1] == 'Drop':
                            event = controller.step(dict(action='DropHandObject'))
                            self.save.append("DropHandObject")
                        elif interaction[1] == 'Empty':
                            event = controller.step(dict(action='EmptyLiquidFromObject', objectId=interaction[2]))
                            self.save.append("EmptyLiquidFromObject")
                            self.save.append(interaction[2])
                        elif interaction[1] == 'Fill':
                            event = controller.step(
                                dict(action='FillObjectWithLiquid', objectId=interaction[2], fillLiquid=interaction[3]))
                            self.save.append("FillObjectWithLiquid")
                            self.save.append(interaction[2])
                            self.save.append(interaction[3])
                        elif interaction[1] == 'Open':
                            event = controller.step(dict(action='OpenObject', objectId=interaction[2]))
                            self.save.append("OpenObject")
                            self.save.append(interaction[2])
                        elif interaction[1] == 'Used up':
                            event = controller.step(dict(action='UseUpObject', objectId=interaction[2]))
                            self.save.append("UseUpObject")
                            self.save.append(interaction[2])
                        elif interaction[1] == 'Pick up':
                            event = controller.step(dict(action='PickupObject', objectId=interaction[2]))
                            self.save.append("PickupObject")
                            self.save.append(interaction[2])
                        elif interaction[1] == 'Pull':
                            event = controller.step(
                                dict(action='PullObject', objectId=interaction[2], moveMagnitude=10.0))
                            self.save.append("PullObject")
                            self.save.append(interaction[2])
                        elif interaction[1] == 'Push':
                            event = controller.step(
                                dict(action='PushObject', objectId=interaction[2], moveMagnitude=10.0))
                            self.save.append("PushObject")
                            self.save.append(interaction[2])
                        elif interaction[1] == 'Put down':
                            event = controller.step(
                                dict(action='PutObject', objectId=interaction[2], receptacleObjectId=interaction[4], forceAction=True))
                            self.save.append("PutObject")
                            self.save.append(interaction[2])
                        elif interaction[1] == 'Slice':
                            event = controller.step(dict(action='SliceObject', objectId=interaction[2]))
                            self.save.append("SliceObject")
                            self.save.append(interaction[2])
                        elif interaction[1] == 'Throw':
                            event = controller.step(dict(action='ThrowObject', moveMagnitude=100.0))
                            self.save.append("ThrowObject")
                        elif interaction[1] == 'Toggle off':
                            event = controller.step(dict(action='ToggleObjectOff', objectId=interaction[2]))
                            self.save.append("ToggleObjectOff")
                            self.save.append(interaction[2])
                        elif interaction[1] == 'Toggle on':
                            event = controller.step(dict(action='ToggleObjectOn', objectId=interaction[2]))
                            self.save.append("ToggleObjectOn")
                            self.save.append(interaction[2])

                        # Send frame to GUI
                        ai2thor_frame = ImageTk.PhotoImage(Image.fromarray(event.frame))
                        self.send_frame(ai2thor_frame)
                except queue.Empty:
                    pass
            elif stage == 'review':
                pass
            elif stage == 'save':
                # save user inputs
                with open("actions.txt", "w") as output:
                    # output.write(str(name_list))
                    output.write(str(self.save))
                # with open("object.txt", "w") as output1:
                #     output1.write(str(self.temp2))

                stage = 'choose_task'

    def send_frame(self, frame):
        """Send frame to the frame_queue."""
        self.frame_queue.put(frame)

    def send_current_objects(self, current_objects):
        """Send all object choices to the object_queue."""
        self.object_queue.put(current_objects)


if __name__ == "__main__":
    root = tk.Tk()
    root.wm_geometry("820x800")
    time1 = ''
    # Instantiate GUI
    gui = Gui(root)
    root.mainloop()
