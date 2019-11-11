import ai2thor.controller
import random
import networkx as nx
import math
import numpy as np
import time

def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'"""
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

def object_centering(agent_pos, origin_vector, target_vector):
    # Make position and angle align with each other according the world coordinates
    agent_vector = [agent_pos['x'], 0, agent_pos['z']]
    direction = origin_vector[0] * agent_vector[2] - origin_vector[2] * agent_vector[0]
    if direction > 0:
        start_rot = -angle_between(origin_vector, agent_vector) * 180 / math.pi
    else:
        start_rot = angle_between(origin_vector, agent_vector) * 180 / math.pi

    # Make agent rotate to face object
    direction_vector = [target_vector[0] - agent_vector[0], 0, target_vector[2] - agent_vector[2]]
    direction = agent_vector[0] * direction_vector[2] - agent_vector[2] * direction_vector[0]
    if direction > 0:
        rotation = start_rot - (angle_between(agent_vector, direction_vector) * 180 / math.pi)
    else:
        rotation = start_rot + (angle_between(agent_vector, direction_vector) * 180 / math.pi)
    event = controller.step(
        dict(action='TeleportFull', x=agent_pos['x'], y=agent_pos['y'], z=agent_pos['z'], rotation=rotation, horizon=0))

    return event

# configurations
rotation_degree = 30
seed = 42
random.seed(seed)
origin_vector = [0,0,1]

# start controller
img_width = 500
img_height = 500
controller = ai2thor.controller.BFSController(grid_size=0.25)
controller.start()
controller.reset('FloorPlan1')
controller.local_executable_path = "/home/samson/Documents/github/allenai/ai2thor/unity/Builds/linux.x86_64"
controller.search_all_closed('FloorPlan1') # provide the scene name you want a grid for here
graph = controller.build_graph()
event = controller.step(dict(action='Initialize', gridSize=0.25, renderObjectImage=True))
agent = event.metadata['agent']
for obj in event.metadata['objects']:
    target = obj
    print(target['name'])
    break

# find location with minimum distance from target object
distance_list = []
node_list = list(graph.nodes)
for i in node_list:
    target_pos = i.split('|')
    distance_list.append(math.sqrt((target['position']['x'] - float(target_pos[0]))**2 + (target['position']['z'] - float(target_pos[1]))**2))
min_node = distance_list.index(min(distance_list))

# save target object location
target_vector = [target['position']['x'],0,target['position']['z']]

# change target location to nearest moveable location to object
target['position']['x'] = float(node_list[min_node].split('|')[0])
target['position']['z'] = float(node_list[min_node].split('|')[1])

shortest_path = nx.shortest_path(graph, controller.key_for_point(agent['position']), controller.key_for_point(target['position']))
shortest_path = list(shortest_path)

# change to topdown view
event = controller.step(dict(action='ToggleMapView'))
for p in shortest_path:
    event = controller.step(dict(action='Teleport', x=float(p.split('|')[0]), y=agent['position']['y'], z=float(p.split('|')[1])))
    time.sleep(0.1)

agent_pos = event.metadata['agent']['position']
event = controller.step(dict(action='ToggleMapView'))
event = object_centering(agent_pos, origin_vector, target_vector)

# check if object is visible
if target['objectId'] not in event.instance_detections2D.keys():
    event = controller.step(dict(action='LookDown'))

while True:
    pass