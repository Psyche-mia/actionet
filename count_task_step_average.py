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
        task_name = task.split('/')[-1].split('_')[0]

        task_count[task_name] += 1

        with open(task) as f:
            data = f.read()

        data = data.replace('][', ',')
        data = data.replace('[','')
        data = data.replace(']','')
        data = data.replace("'", '')
        task_list =  data.split(",")

        step_count[task_name] += len(task_list) - 2

print("\nAverage steps per task: " + str(sum(step_count.values()) / sum(task_count.values())))
print("\n")
for task in step_count.keys():
    print("Average steps per task for " + str(task) + ": " + str(step_count[task] / task_count[task]))