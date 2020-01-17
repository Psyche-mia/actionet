import argparse
import os
import ai2thor.controller
from collections import defaultdict

parser = argparse.ArgumentParser()
parser.add_argument('--task_path')
parser.add_argument('--target_path')
args = parser.parse_args()
task_path = args.task_path
target_path = args.target_path

task_dict = defaultdict(lambda: 0)

user_paths = [os.path.join(task_path, d) for d in os.listdir(task_path) 
                    if os.path.isdir(os.path.join(task_path, d))]

controller = ai2thor.controller.Controller()
controller.local_executable_path = "/home/user/ai2thor/unity/unity/Builds/linux.x86_64"
controller.start(player_screen_width=1000,
        player_screen_height=500)

for user_path in user_paths:
    user_id = user_path.split('/')[-1]

    if not os.path.exists(target_path + '/' + user_id):
        os.makedirs(target_path + '/' + user_id)

    user_tasks = [os.path.join(user_path, d) for d in os.listdir(user_path) 
                    if os.path.isfile(os.path.join(user_path, d))]

    for user_task in user_tasks:
        with open(user_task) as f:
            task = f.read()
        task = task.replace('][', ',')
        task = task.replace('[','')
        task = task.replace(']','')
        task = task.replace("'", '')
        task_list =  task.split(",")
        task_list = [word.strip() for word in task_list]

        # Get information from task text files and set initial config for AI2-THOR
        task_name = task_list[0]
        # Check if there are repeated tasks
        done = False
        for t in task_dict.keys():
            # If task value in dictionaries is already the shortest and is repeated
            if len(t) <= len(task_name):
                length = len(t)
                if task_name[:length] == t:
                    task_name = t
                    done = True
                    break
            # If task value in dictionaries is not the shortest and is repeated
            else:
                length = len(task_name)
                if t[:length] == task_name:
                    del task_dict[t]
                    done = True
                    break
        if not done:
            task_dict[task_name] = 0

        scene = task_list[1]
        controller.reset(scene)
        event = controller.step(dict(action='Initialize', gridSize=0.25, renderObjectImage="True"))

        config_task_list = [
            'Wash Dishes',
            'Throw away cracked egg',
            'Throw away unused apple slice',
            'Pour away coffee in a cup',
            'Pour away water from pot',
            'Use laptop',
            'Throw away used tissuebox',
            'Turn off the table lamp or desk lamp',
            'Open Blinds',
            'Clean the bed',
            'Close the blinds',
            'Put off a candle',
            'Throw away used toilet roll and soap bottle',
            'Water the houseplant',
            'Clean the mirror',
            'Turn on all the floor lamp',
            'Wash dirty cloths'
        ]

        if task_name == config_task_list[0]:
            for obj in event.metadata['objects']:
                if obj['objectType'] == 'Plate' or obj['objectType'] == 'Bowl':
                    target_id = obj['objectId']
                    event = controller.step(
                        dict(action='SpecificToggleSpecificState', StateChange='DirtyObject', objectId=target_id))

        elif task_name == config_task_list[1]:
            for obj in event.metadata['objects']:
                if obj['objectType'] == 'Egg':
                    target_id = obj['objectId']
                    event = controller.step(
                        dict(action='SpecificToggleSpecificState', StateChange='BreakObject', objectId=target_id))

        elif task_name == config_task_list[2]:
            for obj in event.metadata['objects']:
                if obj['objectType'] == 'Apple':
                    target_id = obj['objectId']
                    event = controller.step(
                        dict(action='SpecificToggleSpecificState', StateChange='SliceObject', objectId=target_id))

        elif task_name == config_task_list[3]:
            for obj in event.metadata['objects']:
                if obj['objectType'] == 'Cup':
                    target_id = obj['objectId']
                    event = controller.step(
                        dict(action='SpecificToggleSpecificState', StateChange="FillObjectWithLiquid",
                             objectId=target_id, fillLiquid='coffee'))

        elif task_name == config_task_list[4]:
            for obj in event.metadata['objects']:
                if obj['objectType'] == 'Pot':
                    target_id = obj['objectId']
                    event = controller.step(
                        dict(action='SpecificToggleSpecificState', StateChange="FillObjectWithLiquid",
                             objectId=target_id, fillLiquid='water'))
        elif task_name == config_task_list[5]:
            for obj in event.metadata['objects']:
                if obj['objectType'] == 'Laptop':
                    target_id = obj['objectId']
                    event = controller.step(
                        dict(action='SpecificToggleSpecificState', StateChange="CloseObject", objectId=target_id))

        elif task_name == config_task_list[6]:
            for obj in event.metadata['objects']:
                if obj['objectType'] == 'TissueBox':
                    target_id = obj['objectId']
                    event = controller.step(
                        dict(action='SpecificToggleSpecificState', StateChange="UseUpObject", objectId=target_id))

        elif task_name == config_task_list[7]:
            for obj in event.metadata['objects']:
                if obj['objectType'] == 'DeskLamp':
                    target_id = obj['objectId']
                    event = controller.step(
                        dict(action='SpecificToggleSpecificState', StateChange="ToggleObjectOn", objectId=target_id))

        elif task_name == config_task_list[8]:
            for obj in event.metadata['objects']:
                if obj['objectType'] == 'Blinds':
                    target_id = obj['objectId']
                    event = controller.step(
                        dict(action='SpecificToggleSpecificState', StateChange="CloseObject", objectId=target_id))

        elif task_name == config_task_list[9]:
            for obj in event.metadata['objects']:
                if obj['objectType'] == 'Bed':
                    target_id = obj['objectId']
                    event = controller.step(
                        dict(action='SpecificToggleSpecificState', StateChange='DirtyObject', objectId=target_id))

        elif task_name == config_task_list[10]:
            for obj in event.metadata['objects']:
                if obj['objectType'] == 'Blinds':
                    target_id = obj['objectId']
                    event = controller.step(
                        dict(action='SpecificToggleSpecificState', StateChange="OpenObject", objectId=target_id))

        elif task_name == config_task_list[11]:
            for obj in event.metadata['objects']:
                if obj['objectType'] == 'Candle':
                    target_id = obj['objectId']
                    event = controller.step(
                        dict(action='SpecificToggleSpecificState', StateChange="ToggleObjectOn", objectId=target_id))

        elif task_name == config_task_list[12]:
            for obj in event.metadata['objects']:
                if obj['objectType'] == 'ToiletPaper' or obj['objectType'] == 'SoapBottle':
                    target_id = obj['objectId']
                    event = controller.step(
                        dict(action='SpecificToggleSpecificState', StateChange="UseUpObject", objectId=target_id))

        elif task_name == config_task_list[13]:
            for obj in event.metadata['objects']:
                if obj['objectType'] == 'WateringCan':
                    target_id = obj['objectId']
                    event = controller.step(
                        dict(action='SpecificToggleSpecificState', StateChange="FillObjectWithLiquid",
                             objectId=target_id, fillLiquid='water'))

        elif task_name == config_task_list[14]:
            for obj in event.metadata['objects']:
                if obj['objectType'] == 'Mirror':
                    target_id = obj['objectId']
                    event = controller.step(
                        dict(action='SpecificToggleSpecificState', StateChange="DirtyObject", objectId=target_id))

        elif task_name == config_task_list[15]:
            for obj in event.metadata['objects']:
                if obj['objectType'] == 'FloorLamp':
                    target_id = obj['objectId']
                    event = controller.step(
                        dict(action='SpecificToggleSpecificState', StateChange="ToggleObjectOff", objectId=target_id))

        elif task_name == config_task_list[16]:
            for obj in event.metadata['objects']:
                if obj['objectType'] == 'Cloth':
                    target_id = obj['objectId']
                    event = controller.step(
                        dict(action='SpecificToggleSpecificState', StateChange="DirtyObject", objectId=target_id))

        prev_is_movement = None
        actions = task_list[2:]
        mid_level_actions = []

        for i in range(len(actions)):
            action = actions[i]
            if 'Move' not in action and 'Rotate' not in action and 'Look' not in action:
                if prev_is_movement:
                    # Previous action is movement-related action
                    target_object = actions[i+1]
                    mid_level_actions.append("Navigate" + target_object)
                if action == 'DropHandObject':
                    # Find target dropped object
                    last_pickup_index = len(mid_level_actions) - 1 - mid_level_actions[::-1].index("PickupObject")
                    dropped_object_index = last_pickup_index + 1
                    dropped_object = mid_level_actions[dropped_object_index]

                    # Get closest object (using y coordinate) that is below hand (using x and z coordinates)
                    possible_objects = {}
                    # TODO: Get x and z coordinate bounds for suggested object and check if hand's x and z coordinates are within bounds
                    # Using 'isPickedUp'
                    distance = 0
                    possible_objects[obj] = distance
                    sorted_possible_objects = [k for k, v in sorted(possible_objects.items(), key=lambda item: item[1])]
                    target_object = sorted_possible_objects[0]

                    # Replace DropHandObject with PutObject
                    mid_level_actions.append("PutObject")
                    mid_level_actions.append(dropped_object)
                    mid_level_actions.append(target_object)
                else:
                    mid_level_actions.append(action)
                prev_is_movement = False
            else:
                prev_is_movement = True

        # Write new mid-level action list to target path
        with open(target_path + '/' + user_id + '/' + task_name + '_' + scene, 'w') as f:
            task_scene_list = [task_name, scene]
            f.write(str(task_scene_list))
            f.write(str(mid_level_actions))