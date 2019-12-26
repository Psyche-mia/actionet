from builtins import int

import ai2thor.controller
import re
import time
import glob
import cv2
import os

controller = ai2thor.controller.Controller()
controller.local_executable_path = "/home/user/ai2thor/unity/unity/Builds/linux.x86_64"
controller.start(player_screen_width=1000,
        player_screen_height=500)
event = controller.step(
            dict(action='AddThirdPartyCamera', rotation=dict(x=0, y=0, z=0), position=dict(x=0, z=0, y=0)))
time.sleep(.02)
event.third_party_camera_frames
person= input("ID:")
path = '/home/user/Desktop/actionet/annotator/saved-tasks/'+str(person)+'/*'
files = glob.glob(path)
c=0
for name in files:

    with open(name) as f:

        task=f.read()
        print(name)
# with open('/home/user/Desktop/actionet/annotator/saved-tasks/2/Watch television_FloorPlan203', 'r') as f:
#     task = f.read()

        task = task.replace('][', ',')
        task = task.replace('[','')
        task = task.replace(']','')
        task = task.replace("'", '')
        task_list =  task.split(",")
        task_list = [word.strip() for word in task_list]

        print(task_list[0])
        controller.reset(task_list[1])
        event = controller.step(dict(action='Initialize', gridSize=0.25, renderObjectImage="True"))

        # set initial config for scene
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
        if task_list[0] == config_task_list[0]:
            for obj in event.metadata['objects']:
                if obj['objectType'] == 'Plate' or obj['objectType'] == 'Bowl':
                    target_id = obj['objectId']
                    event = controller.step(
                        dict(action='SpecificToggleSpecificState', StateChange='DirtyObject', objectId=target_id))

        elif task_list[0] == config_task_list[1]:
            for obj in event.metadata['objects']:
                if obj['objectType'] == 'Egg':
                    target_id = obj['objectId']
                    event = controller.step(
                        dict(action='SpecificToggleSpecificState', StateChange='BreakObject', objectId=target_id))

        elif task_list[0] == config_task_list[2]:
            for obj in event.metadata['objects']:
                if obj['objectType'] == 'Apple':
                    target_id = obj['objectId']
                    event = controller.step(
                        dict(action='SpecificToggleSpecificState', StateChange='SliceObject', objectId=target_id))

        elif task_list[0] == config_task_list[3]:
            for obj in event.metadata['objects']:
                if obj['objectType'] == 'Cup':
                    target_id = obj['objectId']
                    event = controller.step(
                        dict(action='SpecificToggleSpecificState', StateChange="FillObjectWithLiquid",
                             objectId=target_id, fillLiquid='coffee'))

        elif task_list[0] == config_task_list[4]:
            for obj in event.metadata['objects']:
                if obj['objectType'] == 'Pot':
                    target_id = obj['objectId']
                    event = controller.step(
                        dict(action='SpecificToggleSpecificState', StateChange="FillObjectWithLiquid",
                             objectId=target_id, fillLiquid='water'))
        elif task_list[0] == config_task_list[5]:
            for obj in event.metadata['objects']:
                if obj['objectType'] == 'Laptop':
                    target_id = obj['objectId']
                    event = controller.step(
                        dict(action='SpecificToggleSpecificState', StateChange="CloseObject", objectId=target_id))

        elif task_list[0] == config_task_list[6]:
            for obj in event.metadata['objects']:
                if obj['objectType'] == 'TissueBox':
                    target_id = obj['objectId']
                    event = controller.step(
                        dict(action='SpecificToggleSpecificState', StateChange="UseUpObject", objectId=target_id))

        elif task_list[0] == config_task_list[7]:
            for obj in event.metadata['objects']:
                if obj['objectType'] == 'DeskLamp':
                    target_id = obj['objectId']
                    event = controller.step(
                        dict(action='SpecificToggleSpecificState', StateChange="ToggleObjectOn", objectId=target_id))

        elif task_list[0] == config_task_list[8]:
            for obj in event.metadata['objects']:
                if obj['objectType'] == 'Blinds':
                    target_id = obj['objectId']
                    event = controller.step(
                        dict(action='SpecificToggleSpecificState', StateChange="CloseObject", objectId=target_id))

        elif task_list[0] == config_task_list[9]:
            for obj in event.metadata['objects']:
                if obj['objectType'] == 'Bed':
                    target_id = obj['objectId']
                    event = controller.step(
                        dict(action='SpecificToggleSpecificState', StateChange='DirtyObject', objectId=target_id))

        elif task_list[0] == config_task_list[10]:
            for obj in event.metadata['objects']:
                if obj['objectType'] == 'Blinds':
                    target_id = obj['objectId']
                    event = controller.step(
                        dict(action='SpecificToggleSpecificState', StateChange="OpenObject", objectId=target_id))

        elif task_list[0] == config_task_list[11]:
            for obj in event.metadata['objects']:
                if obj['objectType'] == 'Candle':
                    target_id = obj['objectId']
                    event = controller.step(
                        dict(action='SpecificToggleSpecificState', StateChange="ToggleObjectOn", objectId=target_id))

        elif task_list[0] == config_task_list[12]:
            for obj in event.metadata['objects']:
                if obj['objectType'] == 'ToiletPaper' or obj['objectType'] == 'SoapBottle':
                    target_id = obj['objectId']
                    event = controller.step(
                        dict(action='SpecificToggleSpecificState', StateChange="UseUpObject", objectId=target_id))

        elif task_list[0] == config_task_list[13]:
            for obj in event.metadata['objects']:
                if obj['objectType'] == 'WateringCan':
                    target_id = obj['objectId']
                    event = controller.step(
                        dict(action='SpecificToggleSpecificState', StateChange="FillObjectWithLiquid",
                             objectId=target_id, fillLiquid='water'))

        elif task_list[0] == config_task_list[14]:
            for obj in event.metadata['objects']:
                if obj['objectType'] == 'Mirror':
                    target_id = obj['objectId']
                    event = controller.step(
                        dict(action='SpecificToggleSpecificState', StateChange="DirtyObject", objectId=target_id))

        elif task_list[0] == config_task_list[15]:
            for obj in event.metadata['objects']:
                if obj['objectType'] == 'FloorLamp':
                    target_id = obj['objectId']
                    event = controller.step(
                        dict(action='SpecificToggleSpecificState', StateChange="ToggleObjectOff", objectId=target_id))

        elif task_list[0] == config_task_list[16]:
            for obj in event.metadata['objects']:
                if obj['objectType'] == 'Cloth':
                    target_id = obj['objectId']
                    event = controller.step(
                        dict(action='SpecificToggleSpecificState', StateChange="DirtyObject", objectId=target_id))


        time.sleep(.02)
        tasks = task_list[0]
        room = task_list[1]
        task_list.pop(0)
        task_list.pop(0)

        newpath = '/home/user/Desktop/actionet/annotator/recorded_video/' +str(person)+'_' + str(tasks) + '_' + str(room)
        if not os.path.exists(newpath):
            # os.remove()
            os.makedirs(newpath)

        # event = controller.step(dict(action='AddThirdPartyCamera', rotation=dict(x=0, y=0, z=0), position=dict(x=-1.0, z=-2.0, y=1.0)))
        # event = controller.step(dict(action='UpdateThirdPartyCamera',thirdPartyCameraId=0, rotation=dict(x=30, y=-240, z=0), position=dict(x=-3.0, z=3, y=2.5)))
        # event.third_party_camera_frames #
        # event.metadata['thirdPartyCameras']
        # print(event.metadata['agent'])# contains metadata about position/rotation of each camera
        a=0
        count=0
        anglehandX = 0.0
        anglehandY = 0.0
        anglehandZ = 0.0
        for i in task_list:

            if not re.search('\d+', i):
                if i == 'PickupObject' or i=='UseUpObject'or i=='EmptyLiquidFromObject' or i =='ToggleObjectOn' or i == 'ToggleObjectOff' or i== 'OpenObject' or i =='CloseObject' or i=='SliceObject' or i== 'BreakObject' or i== 'DirtyObject' or i=='CleanObject':
                    event = controller.step(dict(action=i, objectId=task_list[a+1]))
                    time.sleep(.02)

                elif i == 'PutObject':

                    event = controller.step(dict(action=i, objectId=task_list[a+1], receptacleObjectId=task_list[a+2],forceAction=True))
                    time.sleep(.02)


                elif i=='ThrowObject' or i=='PushObject' or i=='PullObject':
                    event = controller.step(dict(action=i, moveMagnitude=100.0))
                    time.sleep(.02)


                elif i == 'FillObjectWithLiquid':
                    event = controller.step(
                        dict(action=i, objectId=task_list[a + 1], fillLiquid=task_list[a + 2]))
                    print (task_list[a+1])
                    print (task_list[a+2])

                # elif i=='FillObjectWithLiquid':
                #     print (i)
                #     print (task_list[a+1])
                #     print(task_list[a+2])
                #     event = controller.step(dict(action=i, objectId=task_list[a+1], fillLiquid=task_list[a+2]))
                elif i=='DropHandObject' or i=='Crouch' or i=='Stand':
                    event = controller.step(dict(action=i))

                elif i=='RotateHandX':
                    anglehandX=anglehandX+30.0
                    event = controller.step(dict(action='RotateHand', x=anglehandX))
                    time.sleep(.02)

                elif i=='RotateHandY':
                    anglehandY=anglehandY+30.0
                    event = controller.step(dict(action='RotateHand', y=anglehandY))
                    time.sleep(.02)

                elif i=='RotateHandZ':
                    anglehandZ=anglehandZ+30.0
                    event = controller.step(dict(action='RotateHand', z=anglehandZ))
                    time.sleep(.02)


                elif i=='MoveHandAhead' or i=='MoveHandBack' or i =='MoveHandLeft' or i=='MoveHandRight' or i=='MoveHandUp' or i=='MoveHandDown':
                    event = controller.step(dict(action=i, moveMagnitude=0.1))
                    time.sleep(.02)


                elif i == 'MoveRight' or i == 'MoveAhead' or i == 'MoveLeft' or i == 'MoveBack' or i == 'RotateLeft' or i == 'RotateRight' or i == 'LookUp' or i == 'LookDown':

                    event = controller.step(dict(action=i))
                cv2.imwrite(str(newpath)+'/'+str(count)+ '.jpg',event.cv2img)
                count+=1
            a=a+1
        c=c+1
        print(c)


