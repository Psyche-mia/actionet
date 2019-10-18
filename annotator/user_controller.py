import ai2thor.controller
import keyboard
import time
import argparse

# Get arguments
parser = argparse.ArgumentParser()
parser.add_argument('-scene')
parser.add_argument('-task')
args = parser.parse_args()

# Instantiate AI2-THOR
controller = ai2thor.controller.Controller()
controller.start(player_screen_width=640,
        player_screen_height=640)
# controller1 = ai2thor.controller.Controller()
# controller1.start()

controller.reset('FloorPlan'+args.scene)
event = controller.step(dict(action='Initialize', gridSize=0.25,renderObjectImage="True"))
# controller1.reset('FloorPlan'+floorplan)
# event = controller1.step(dict(action='Initialize', gridSize=0.25,renderObjectImage="True"))
# Show user task details
# event = controller1.step(dict(action='ToggleMapView'))

# Record user data
action_list = []
midtasks = []

while True:
    # Add mid-level actions
    anglehand=0
    temp1 =[]
    midtask=['Navigate','Toast','Boil','Wash','Fry','Heat','Serve','Cook','Nill','Robotic control']
    
    target =input("Target of your action: ")
    # temp1.append(middleleveltask)
    temp1.append(target)

    # print("Middle level Task: "+middleleveltask +target)
    # # Task complete
    # if name == '8':
    #     with open("program1.txt","w") as output:
    #         # output.write(str(name_list))
    #         output.write(str(action_list))
    #     with open("program2.txt","w") as output:
    #         output.write(str(midtasks))
    #     print("Task complete.")
    #     break

    temp = []
    while True:
        anglehand=anglehand+30.0
        if keyboard.is_pressed('right'):
            event = controller.step(dict(action='MoveRight'))
            # event = controller1.step(dict(action='MoveRight'))
            temp.append('MoveRight')
        elif keyboard.is_pressed('up'):
            event = controller.step(dict(action='MoveAhead'))
            # event = controller1.step(dict(action='MoveAhead'))
            temp.append('MoveAhead')

        elif keyboard.is_pressed('down'):
            event = controller.step(dict(action='MoveBack'))
            # event = controller1.step(dict(action='MoveBack'))
            temp.append('MoveBack')

        elif keyboard.is_pressed('left'):
            event = controller.step(dict(action='MoveLeft'))
            # event = controller1.step(dict(action='MoveLeft'))
            temp.append('MoveLeft')

        elif keyboard.is_pressed('a'):
            # event = controller.step(dict(action='RotateLeft'))
            # event = controller1.step(dict(action='RotateLeft'))
            position=event.metadata['agent']['position']
            rotation= event.metadata['agent']['rotation']
            angle = rotation.get('y')
            print(angle)
            rotate=angle-30.0
            x= position.get('x')
            y= position.get('y')
            z= position.get('z')
            event = controller.step(dict(action='TeleportFull', x=x, y=y, z=z, rotation=rotate, horizon=0.0))

            temp.append('RotateLeft')
        elif keyboard.is_pressed('d'):
            # event = controller.step(dict(action='RotateRight'))
            # event = controller1.step(dict(action='RotateRight'))
            position = event.metadata['agent']['position']
            rotation = event.metadata['agent']['rotation']
            angle = rotation.get('y')
            print(angle)
            rotate = angle + 30.0
            x = position.get('x')
            y = position.get('y')
            z = position.get('z')
            event = controller.step(dict(action='TeleportFull', x=x, y=y, z=z, rotation=rotate, horizon=0.0))

            temp.append('RotateRight')
        elif keyboard.is_pressed('w'):
            event = controller.step(dict(action='LookUp'))
            temp.append('LookUp')
        elif keyboard.is_pressed('s'):
            event = controller.step(dict(action='LookDown'))
            temp.append('LookDown')
        elif keyboard.is_pressed('8'):
            event = controller.step(dict(action='MoveHandAhead', moveMagnitude = 0.1))
            temp.append('MoveHandAhead')
        elif keyboard.is_pressed('5'):
            event = controller.step(dict(action='MoveHandBack', moveMagnitude=0.1))
            temp.append('MoveHandBack')
        elif keyboard.is_pressed('4'):
            event = controller.step(dict(action='MoveHandLeft', moveMagnitude=0.1))
            temp.append('MoveHandLeft')
        elif keyboard.is_pressed('6'):
            event = controller.step(dict(action='MoveHandRight', moveMagnitude=0.1))
            temp.append('MoveHandBack')
        elif keyboard.is_pressed('9'):
            event = controller.step(dict(action='MoveHandUp', moveMagnitude=0.1))
            temp.append('MoveHandUp')
        elif keyboard.is_pressed('3'):
            event = controller.step(dict(action='MoveHandDown', moveMagnitude=0.1))
            temp.append('MoveHandDown')
        elif keyboard.is_pressed('7'):
            event = controller.step(dict(action='RotateHand', x =anglehand))
            temp.append('RotateHandX')
        elif keyboard.is_pressed('1'):
            event = controller.step(dict(action='RotateHand', z =anglehand))
            temp.append('RotateHandZ')
        elif keyboard.is_pressed('0'):
            event = controller.step(dict(action='RotateHand', y =anglehand))
            temp.append('RotateHandY')

        elif keyboard.is_pressed('o'):
            target_obj = input("\nName your target object to OPEN: ")
            for i in event.instance_detections2D:
                print(i)
                if target_obj in i:
                    event = controller.step(dict(action='OpenObject', objectId=i))
                    temp.append('OpenObject')
                    temp.append(target_obj)
                    break
        elif keyboard.is_pressed('c'):
            target_obj = input("\nName your target object to CLOSE: ")
            for i in event.instance_detections2D:
                print(i)
                if target_obj in i:
                    event = controller.step(dict(action='CloseObject', objectId=i))
                    temp.append('CloseObject')
                    temp.append(target_obj)
                    break
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
        elif keyboard.is_pressed('u'):
            target_obj = input("\nName your target object to PICK UP: ")
            for i in event.instance_detections2D:
                if target_obj in i:
                    event = controller.step(dict(action='PickupObject', objectId=i))
                    temp.append('PickupObject')
                    temp.append(target_obj)
                    break
        elif keyboard.is_pressed('p'):
            target_obj = input("\nName your target object to PUT DOWN: ")
            recep_obj = input("\nName your location to PUT DOWN: ")
            for i in event.instance_detections2D:
                for b in event.instance_detections2D:
                    if target_obj in i and recep_obj in b:
                        event = controller.step(dict(action='PutObject', objectId=i, receptacleObjectId= b))
                        temp.append('PutObject')
                        temp.append(target_obj)
                        temp.append(recep_obj)
                        break
        elif keyboard.is_pressed('t'):
            target_obj = input("\nName your target object to TOGGLE ON: ")
            for i in event.instance_detections2D:
                if target_obj in i:
                    event = controller.step(dict(action='ToggleObjectOn', objectId=i))
                    temp.append('ToggleObjectOn')
                    temp.append(target_obj)
                    break
        elif keyboard.is_pressed('f'):
            target_obj = input("\nName your target object to TOGGLE OFF: ")
            for i in event.instance_detections2D:
                if target_obj in i:
                    event = controller.step(dict(action='ToggleObjectOff', objectId=i))
                    temp.append('ToggleObjectOff')
                    temp.append(target_obj)
                    break
        elif keyboard.is_pressed('i'):
            target_obj = input("\nName your target object to DROP: ")
            event = controller.step(dict(action='DropHandObject'))
            temp.append('DropHandObject')

        elif keyboard.is_pressed('k'):
            target_obj = input("\nName your target object to THROW: ")
            event = controller.step(dict(action='ThrowObject', moveMagnitude= 100.0))
            temp.append('ThrowObject')

        elif keyboard.is_pressed('l'):
            target_obj = input("\nName your target object to PUSH: ")
            for i in event.instance_detections2D:
                if target_obj in i:
                    event = controller.step(dict(action='PushObject', objectId=i, moveMagnitude=10.0))
                    temp.append('PushObject')
                    temp.append(target_obj)
                    break

        elif keyboard.is_pressed('r'):
            target_obj = input("\nName your target object to PULL: ")
            for i in event.instance_detections2D:
                if target_obj in i:
                    event = controller.step(dict(action='PullObject', objectId=i, moveMagnitude=10.0))
                    temp.append('PullObject')
                    temp.append(target_obj)
                    break

        elif keyboard.is_pressed('z'):
            target_obj = input("\nName your target object to SLICE: ")
            for i in event.instance_detections2D:
                if target_obj in i:
                    event = controller.step(dict(action='SliceObject', objectId=i))
                    temp.append('SliceObject')
                    temp.append(target_obj)
                    break

        elif keyboard.is_pressed('b'):
            target_obj = input("\nName your target object to BREAK: ")
            for i in event.instance_detections2D:
                if target_obj in i:
                    event = controller.step(dict(action='BreakObject', objectId=i))
                    temp.append('BreakObject')
                    temp.append(target_obj)
                    break

        elif keyboard.is_pressed('m'):
            target_obj = input("\nName your target object to DIRTY: ")
            for i in event.instance_detections2D:
                if target_obj in i:
                    event = controller.step(dict(action='DirtyObject', objectId=i))
                    temp.append('DirtyObject')
                    temp.append(target_obj)
                    break

        elif keyboard.is_pressed('y'):
            target_obj = input("\nName your target object to CLEAN: ")
            for i in event.instance_detections2D:
                if target_obj in i:
                    event = controller.step(dict(action='CleanObject', objectId=i))
                    temp.append('CleanObject')
                    temp.append(target_obj)
                    break

        elif keyboard.is_pressed('g'):
            target_obj = input("\nName your target object to EMPTY: ")
            for i in event.instance_detections2D:
                if target_obj in i:
                    event = controller.step(dict(action='EmptyLiquidFromObject', objectId=i))
                    temp.append('EmptyLiquidFromObject')
                    temp.append(target_obj)
                    break

        elif keyboard.is_pressed('h'):
            target_obj = input("\nName your target object to FILL: ")
            item_obj = input("\nName the liquid to fill object with: ")
            for i in event.instance_detections2D:
                if target_obj in i:
                    event = controller.step(dict(action='FillObjectWithLiquid', objectId=i, fillLiquid= item_obj))
                    temp.append('FillObjectWithLiquid')
                    temp.append(target_obj)
                    temp.append(item_obj)
                    break
