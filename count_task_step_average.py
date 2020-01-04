import argparse
import os
from collections import defaultdict

parser = argparse.ArgumentParser()
parser.add_argument("--task_path")
args = parser.parse_args()

task_path = args.task_path

task_count = defaultdict(lambda: 0)
step_count = defaultdict(lambda: 0)

task_dir = [os.path.join(task_path, d) for d in os.listdir(task_path) 
                    if os.path.isdir(os.path.join(task_path, d)) and d.split('/')[-1].isdigit()]

for user_dir in task_dir:
    user_tasks = [os.path.join(user_dir, d) for d in os.listdir(user_dir) 
                    if os.path.isfile(os.path.join(user_dir, d))]
                    
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
        for t in task_count.keys():
            # If task value in dictionaries is already the shortest and is repeated
            if len(t) <= len(task_name):
                length = len(t)
                if task_name[:length] == t:
                    step_count[t] += len(task_list) - 2
                    task_count[t] += 1
                    done = True
                    break
            # If task value in dictionaries is not the shortest and is repeated
            else:
                length = len(task_name)
                if t[:length] == task_name:
                    step_count[task_name] += step_count[t]
                    step_count[task_name] += len(task_list) - 2
                    task_count[task_name] += task_count[t]
                    task_count[task_name] += 1
                    del task_count[t]
                    del step_count[t]
                    done = True
                    break
        if not done:
            step_count[task_name] += len(task_list) - 2
            task_count[task_name] += 1

print("\nAvg steps for all tasks: " + str(sum(step_count.values()) / sum(task_count.values())) + "\n")

for task in step_count.keys():
    print("Avg steps for '" + str(task) + "': " + str(step_count[task] / task_count[task]))