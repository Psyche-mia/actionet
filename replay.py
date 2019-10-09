import ai2thor.controller
from sortedcontainers import SortedList
import ast
import time
controller = ai2thor.controller.Controller()
controller.start(player_screen_width=1280,
        player_screen_height=640)
print("Floorplan:")
floorplan= input('')
controller.reset('FloorPlan'+floorplan)
event = controller.step(dict(action='Initialize', gridSize=0.25,renderObjectImage="True"))
# event = controller.step(dict(action='AddThirdPartyCamera', rotation=dict(x=0, y=0, z=0), position=dict(x=-1.0, z=-2.0, y=1.0)))
# event = controller.step(dict(action='UpdateThirdPartyCamera',thirdPartyCameraId=0, rotation=dict(x=30, y=220, z=0), position=dict(x=-0.5, z=2.5, y=2.5)))
# event.third_party_camera_frames #
# event.metadata['thirdPartyCameras'] # contains metadata about position/rotation of each camera
with open('program1.txt', 'r') as f:
    task = eval(f.read())
print(task)
print (type(task))

for a in range(len(task)):
    for i in range(len(task[a])):
        action= task[a][i]
        print(action)
        if action == "OpenObject":
            for z in event.instance_detections2D:
                if task[a][i+1] in z:
                    event = controller.step(dict(action='OpenObject', objectId=z))
                    time.sleep(1)

        elif action == 'CloseObject':
            for z in event.instance_detections2D:
                if task[a][i + 1] in z:
                    event = controller.step(dict(action='CloseObject', objectId=z))
                    time.sleep(1)

        elif action == 'SliceObject':
            for z in event.instance_detections2D:
                if task[a][i + 1] in z:
                    event = controller.step(dict(action='SliceObject', objectId=z))
                    time.sleep(1)

        elif action == 'BreakObject':
            for z in event.instance_detections2D:
                if task[a][i + 1] in z:
                    event = controller.step(dict(action='BreakObject', objectId=z))
                    time.sleep(1)

        elif action == 'DirtyObject':
            for z in event.instance_detections2D:
                if task[a][i + 1] in z:
                    event = controller.step(dict(action='DirtyObject', objectId=z))
                    time.sleep(1)

        elif action == 'CleanObject':
            for z in event.instance_detections2D:
                if task[a][i + 1] in z:
                    event = controller.step(dict(action='CleanObject', objectId=z))
                    time.sleep(1)

        elif action == 'EmptyLiquidFromObject':
            for z in event.instance_detections2D:
                if task[a][i + 1] in z:
                    event = controller.step(dict(action='EmptyLiquidFromObject', objectId=z))
                    time.sleep(1)



        elif action == 'ToggleObjectOn':
            for z in event.instance_detections2D:
                if task[a][i+1] in z:
                    event = controller.step(dict(action='ToggleObjectOn', objectId=z))
                    time.sleep(1)

        elif action == "ToggleObjectOff":
            for z in event.instance_detections2D:
                if task[a][i+1] in z:
                    event = controller.step(dict(action='ToggleObjectOff', objectId=z))
                    time.sleep(1)

        elif action == "PickupObject":
            for z in event.instance_detections2D:
                if task[a][i + 1] in z:
                    event = controller.step(dict(action='PickupObject', objectId=z))
                    time.sleep(1)

        elif action == "FillObjectWithLiquid":
            for z in event.instance_detections2D:
                if task[a][i + 1] in z:
                    event = controller.step(dict(action='FillObjectWithLiquid', objectId=z, filledLiquid=task[a][i+2]))
                    time.sleep(1)

        elif action == "PutObject":
            for z in event.instance_detections2D:
                for b in event.instance_detections2D:
                    if task[a][i +1] in z and task[a][i +2] in b:
                        event = controller.step(dict(action='PutObject', objectId=z, receptacleObjectId=b))
                        time.sleep(1)

        elif action == "PushObject":
            for z in event.instance_detections2D:
                if task[a][i+1] in z:
                    event = controller.step(dict(action='PushObject', objectId=z, moveMagnitude=10.0))
                    time.sleep(1)

        elif action == "PullObject":
            for z in event.instance_detections2D:
                if task[a][i+1] in z:
                    event = controller.step(dict(action='PullObject', objectId=z, moveMagnitude=10.0))
                    time.sleep(1)

        elif action == 'DropHandObject':
            event = controller.step(dict(action='DropHandObject'))
            time.sleep(1)

        elif action == 'ThrowObject':
            event = controller.step(dict(action='ThrowObject', moveMagnitude= 100.0))
            time.sleep(1)

        movement=["RotateRight","RotateLeft","MoveAhead","MoveLeft","MoveRight","MoveBack","LookDown","LookUp"]
        for item in movement:
            if action == item:
                event = controller.step(dict(action=action))









