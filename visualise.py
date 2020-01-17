import argparse
import os
from collections import defaultdict
import re
import statistics

parser = argparse.ArgumentParser()
parser.add_argument("--task_path")
args = parser.parse_args()

task_path = args.task_path

task_dir = [os.path.join(task_path, d) for d in os.listdir(task_path) 
                    if os.path.isdir(os.path.join(task_path, d))]


# 1. Total number of tasks
tasks = []
task_instances = 0

for user_dir in task_dir:
    user_batches = [os.path.join(user_dir, d) for d in os.listdir(user_dir) 
                    if os.path.isdir(os.path.join(user_dir, d))]

    for user_batch in user_batches:
        user_tasks = [os.path.join(user_batch, d) for d in os.listdir(user_batch) 
                    if os.path.isfile(os.path.join(user_batch, d))]
                    
        for task in user_tasks:
            task_instances += 1

            with open(task) as f:
                data = f.read()

            data = data.replace('][', ',')
            data = data.replace('[','')
            data = data.replace(']','')
            data = data.replace("'", '')
            task_list =  data.split(",")

            task_name = task_list[0]

            # Check if there are repeated tasks
            done = False
            for t in tasks:
                # If task value in dictionaries is already the shortest and is repeated
                if len(t) <= len(task_name):
                    length = len(t)
                    if task_name[:length] == t:
                        done = True
                        break
                # If task value in dictionaries is not the shortest and is repeated
                else:
                    length = len(task_name)
                    if t[:length] == task_name:
                        tasks.append(task_name)
                        tasks.remove(t)
                        done = True
                        break
            if not done:
                tasks.append(task_name)

print("\n")
print("Total number of tasks: " + str(len(tasks)))
print("Total number of tasks (instances): " + str(task_instances))
print("\n")


# 2. Number of tasks by category
tasks_by_category = defaultdict(lambda: [])
task_instances_by_category = defaultdict(lambda: 0)

for user_dir in task_dir:
    user_batches = [os.path.join(user_dir, d) for d in os.listdir(user_dir) 
                    if os.path.isdir(os.path.join(user_dir, d))]

    for user_batch in user_batches:
        user_tasks = [os.path.join(user_batch, d) for d in os.listdir(user_batch) 
                    if os.path.isfile(os.path.join(user_batch, d))]
                    
        for task in user_tasks:
            with open(task) as f:
                data = f.read()

            data = data.replace('][', ',')
            data = data.replace('[','')
            data = data.replace(']','')
            data = data.replace("'", '')
            task_list =  data.split(",")

            task_name = task_list[0]
            floor_plan = task_list[1]
            floor_plan = int(re.findall('\d+', floor_plan)[0])

            if floor_plan < 200:
                scene = 'kitchen'
            elif floor_plan > 200 and floor_plan < 300:
                scene = 'living_room'
            elif floor_plan > 300 and floor_plan < 400:
                scene = 'bedroom'
            else:
                scene = 'bathroom'

            task_instances_by_category[scene] += 1

            # Check if there are repeated tasks
            done = False
            for t in tasks_by_category[scene]:
                # If task value in dictionaries is already the shortest and is repeated
                if len(t) <= len(task_name):
                    length = len(t)
                    if task_name[:length] == t:
                        done = True
                        break
                # If task value in dictionaries is not the shortest and is repeated
                else:
                    length = len(task_name)
                    if t[:length] == task_name:
                        tasks_by_category[scene].append(task_name)
                        tasks_by_category[scene].remove(t)
                        done = True
                        break
            if not done:
                tasks_by_category[scene].append(task_name)

tasks_by_category_count = defaultdict(lambda: 0)
for s in tasks_by_category.keys():
    tasks_by_category_count[s] = len(tasks_by_category[s])

print("\n")
print("Number of tasks by category: " + str(tasks_by_category_count))
print("Number of tasks by category (instances): " + str(task_instances_by_category))
print("\n")


# 3. Find max n min for each category and its median
task_steps_by_category = defaultdict(lambda: [])

for user_dir in task_dir:
    user_batches = [os.path.join(user_dir, d) for d in os.listdir(user_dir) 
                    if os.path.isdir(os.path.join(user_dir, d))]

    for user_batch in user_batches:
        user_tasks = [os.path.join(user_batch, d) for d in os.listdir(user_batch) 
                    if os.path.isfile(os.path.join(user_batch, d))]
                    
        for task in user_tasks:
            with open(task) as f:
                data = f.read()

            data = data.replace('][', ',')
            data = data.replace('[','')
            data = data.replace(']','')
            data = data.replace("'", '')
            task_list =  data.split(",")

            task_name = task_list[0]
            floor_plan = task_list[1]
            floor_plan = int(re.findall('\d+', floor_plan)[0])

            if floor_plan < 200:
                scene = 'kitchen'
            elif floor_plan > 200 and floor_plan < 300:
                scene = 'living_room'
            elif floor_plan > 300 and floor_plan < 400:
                scene = 'bedroom'
            else:
                scene = 'bathroom'

            task_steps_by_category[scene].append(len(task_list) - 2)

max_dict = defaultdict(lambda: 0)
min_dict = defaultdict(lambda: 0)
median_dict = defaultdict(lambda: 0)

for s in task_steps_by_category.keys():
    max_dict[s] = max(task_steps_by_category[s])
    min_dict[s] = min(task_steps_by_category[s])
    median_dict[s] = statistics.median(task_steps_by_category[s])

print("\n")
print("Max step by category: " + str(max_dict))
print("Min step by category: " + str(min_dict))
print("Median step by category: " + str(median_dict))
print("\n")


# 4. Classify each task by complex/moderate/easy this can be determine using the SD of the disturbation
task_count = defaultdict(lambda: 0)
step_count = defaultdict(lambda: 0)
avg_step = defaultdict(lambda: 0)

for user_dir in task_dir:
    user_batches = [os.path.join(user_dir, d) for d in os.listdir(user_dir) 
                    if os.path.isdir(os.path.join(user_dir, d))]

    for user_batch in user_batches:
        user_tasks = [os.path.join(user_batch, d) for d in os.listdir(user_batch) 
                    if os.path.isfile(os.path.join(user_batch, d))]
                    
        for task in user_tasks:
            with open(task) as f:
                data = f.read()

            data = data.replace('][', ',')
            data = data.replace('[','')
            data = data.replace(']','')
            data = data.replace("'", '')
            task_list =  data.split(",")

            task_name = task_list[0]

            # Check if there are repeated tasks
            done = False
            for t in tasks:
                # If task value in dictionaries is already the shortest and is repeated
                if len(t) <= len(task_name):
                    length = len(t)
                    if task_name[:length] == t:
                        task_count[t] += 1
                        step_count[t] += len(task_list) - 2
                        done = True
                        break
                # If task value in dictionaries is not the shortest and is repeated
                else:
                    length = len(task_name)
                    if t[:length] == task_name:
                        task_count[task_name] += 1
                        step_count[task_name] += len(task_list) - 2
                        del task_count[t]
                        del step_count[t]
                        done = True
                        break
            if not done:
                task_count[task_name] += 1
                step_count[task_name] += len(task_list) - 2

for t in task_count.keys():
    avg_step[t] = step_count[t] / task_count[t]
task_sorted_by_steps = [k for k, v in sorted(avg_step.items(), key=lambda item: item[1])]
task_by_complexity = defaultdict(lambda:[])
task_by_complexity['easy'] = task_sorted_by_steps[0:21]
task_by_complexity['moderate'] = task_sorted_by_steps[21:42]
task_by_complexity['complex'] = task_sorted_by_steps[42:63]
print('\n')
print("Tasks sorted by complexity: " + str(task_by_complexity))
print('\n')


task_by_category_count = defaultdict(lambda: defaultdict(lambda: 0))
step_by_category_count = defaultdict(lambda: defaultdict(lambda: 0))
avg_step_by_category = defaultdict(lambda: defaultdict(lambda: 0))
task_sorted_by_steps_and_category = defaultdict(lambda: [])
task_by_category_and_complexity = defaultdict(lambda: defaultdict(lambda:[]))

for user_dir in task_dir:
    user_batches = [os.path.join(user_dir, d) for d in os.listdir(user_dir) 
                    if os.path.isdir(os.path.join(user_dir, d))]

    for user_batch in user_batches:
        user_tasks = [os.path.join(user_batch, d) for d in os.listdir(user_batch) 
                    if os.path.isfile(os.path.join(user_batch, d))]
                    
        for task in user_tasks:
            with open(task) as f:
                data = f.read()

            data = data.replace('][', ',')
            data = data.replace('[','')
            data = data.replace(']','')
            data = data.replace("'", '')
            task_list =  data.split(",")

            task_name = task_list[0]
            floor_plan = task_list[1]
            floor_plan = int(re.findall('\d+', floor_plan)[0])

            if floor_plan < 200:
                scene = 'kitchen'
            elif floor_plan > 200 and floor_plan < 300:
                scene = 'living_room'
            elif floor_plan > 300 and floor_plan < 400:
                scene = 'bedroom'
            else:
                scene = 'bathroom'

            # Check if there are repeated tasks
            done = False
            for t in tasks:
                # If task value in dictionaries is already the shortest and is repeated
                if len(t) <= len(task_name):
                    length = len(t)
                    if task_name[:length] == t:
                        task_by_category_count[scene][t] += 1
                        step_by_category_count[scene][t] += len(task_list) - 2
                        done = True
                        break
                # If task value in dictionaries is not the shortest and is repeated
                else:
                    length = len(task_name)
                    if t[:length] == task_name:
                        task_by_category_count[scene][task_name] += 1
                        step_by_category_count[scene][task_name] += len(task_list) - 2
                        del task_by_category_count[scene][t]
                        del step_by_category_count[scene][t]
                        done = True
                        break
            if not done:
                task_by_category_count[scene][task_name] += 1
                step_by_category_count[scene][task_name] += len(task_list) - 2

for s in task_by_category_count.keys():
    for t in task_by_category_count[s].keys():
        avg_step_by_category[s][t] = step_by_category_count[s][t] / task_by_category_count[s][t]
for s in avg_step_by_category.keys():
    task_sorted_by_steps_and_category[s] = [k for k, v in sorted(avg_step_by_category[s].items(), key=lambda item: item[1])]
    length = len(task_sorted_by_steps_and_category[s])
    size = round(length / 3)
    task_by_category_and_complexity[s]['easy'] = task_sorted_by_steps_and_category[s][0:size]
    task_by_category_and_complexity[s]['moderate'] = task_sorted_by_steps_and_category[s][size:size * 2]
    task_by_category_and_complexity[s]['complex'] = task_sorted_by_steps_and_category[s][size * 2:length]
print('\n')
print("Tasks sorted by complexity and category: " + str(task_by_category_and_complexity))
print('\n')