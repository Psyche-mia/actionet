import ai2thor.controller
import re
import time
controller = ai2thor.controller.Controller()
controller.start(player_screen_width=640,
        player_screen_height=640)
with open('Make Coffee_FloorPlan1', 'r') as f:
    task = f.read()

    task = task.replace('][', ',')
    task = task.replace('[','')
    task = task.replace(']','')
    task = task.replace("'", '')
    task_list =  task.split(",")
    task_list = [word.strip() for word in task_list]

print(task_list[0])


controller.reset(task_list[1])
event = controller.step(dict(action='Initialize', gridSize=0.25,renderObjectImage="True"))

task_list.pop(0)
task_list.pop(0)

# event = controller.step(dict(action='AddThirdPartyCamera', rotation=dict(x=0, y=0, z=0), position=dict(x=-1.0, z=-2.0, y=1.0)))
# event = controller.step(dict(action='UpdateThirdPartyCamera',thirdPartyCameraId=0, rotation=dict(x=30, y=-240, z=0), position=dict(x=-3.0, z=3, y=2.5)))
# event.third_party_camera_frames #
# event.metadata['thirdPartyCameras']
# print(event.metadata['agent'])# contains metadata about position/rotation of each camera
a=0
anglehandX = 0.0
anglehandY = 0.0
anglehandZ = 0.0
for i in task_list:

    if not re.search('\d+', i):
        if i == 'PickupObject' or i=='UseUpObject'or i=='EmptyLiquidFromObject' or i =='ToggleObjectOn' or i == 'ToggleObjectOff' or i== 'OpenObject' or i =='CloseObject' or i=='SliceObject' or i== 'BreakObject' or i== 'DirtyObject' or i=='CleanObject':
            event = controller.step(dict(action=i, objectId=task_list[a+1]))
            time.sleep(.1)

        elif i == 'PutObject':

            event = controller.step(dict(action=i, objectId=task_list[a+1], receptacleObjectId=task_list[a+2]))
            time.sleep(.1)
        elif i=='ThrowObject' or i=='PushObject' or i=='PullObject':
            event = controller.step(dict(action=i, moveMagnitude=100.0))
            time.sleep(.1)



        # elif i=='FillObjectWithLiquid':
        #     print (i)
        #     print (task_list[a+1])
        #     print(task_list[a+2])
        #     event = controller.step(dict(action=i, objectId=task_list[a+1], fillLiquid=task_list[a+2]))

        elif i=='RotateHandX':
            anglehandX=anglehandX+30.0
            event = controller.step(dict(action='RotateHand', x=anglehandX))
            time.sleep(.1)
        elif i=='RotateHandY':
            anglehandY=anglehandY+30.0
            event = controller.step(dict(action='RotateHand', y=anglehandY))
            time.sleep(.1)
        elif i=='RotateHandZ':
            anglehandZ=anglehandZ+30.0
            event = controller.step(dict(action='RotateHand', z=anglehandZ))
            time.sleep(.1)

        elif i=='MoveHandAhead' or i=='MoveHandBack' or i =='MoveHandLeft' or i=='MoveHandRight' or i=='MoveHandUp' or i=='MoveHandDown':
            event = controller.step(dict(action=i, moveMagnitude=0.01))
            time.sleep(.1)

        else:
            event = controller.step(dict(action=i))
            time.sleep(.1)


    a=a+1


