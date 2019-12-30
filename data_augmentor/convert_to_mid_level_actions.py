tag = False
actions = []
mid_level_actions = []

for i in range(len(actions)):
    action = actions[i]
    if 'Move' not in action and 'Rotate' not in action and 'Look' not in action:
        if tag is True:
            if action == 'DropHandObject':
                # Find target dropped object
                last_pickup_index = len(mid_level_actions) - 1 - mid_level_actions[::-1].index("PickupObject")
                dropped_object_index = last_pickup_index + 1
                dropped_object = mid_level_actions[dropped_object_index]
                # TODO: Find target object using the x and z coordinates by replaying scene in AI2-THOR
                target_object = ""
                # Replace movements with Navigate
                mid_level_actions.append("Navigate" + target_object)
                # Replace DropHandObject with PutObject
                mid_level_actions.append("PutObject")
                mid_level_actions.append(dropped_object)
                mid_level_actions.append(target_object)
            else:
                # TODO: Depends on action type
                # Replace movements with Navigate
                mid_level_actions.append("Navigate" + actions[i+1])
                mid_level_actions.append(action)
        tag = False
    else:
        tag = True