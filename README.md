# ActioNet: An Interactive End-to-End Platform for Task-Based Data Collection and Augmentation in 3D Environments
## Task-Based Dataset
Our dataset can be found in the '_./dataset/{collection_id}_' folders.

Each **data file** has the naming convention of '_./dataset/{collection_id}/{task}\_{floor_plan}_'. In each file, there are **two lists**:
- The **first list** shows the **task** and the **floor plan**
- The **second list** shows the **actions taken to complete the task**

The '_./dataset/resources/task_descriptions_' folder contains the **task descriptions of the tasks for each collection instance**.

The '_./dataset/resources/user_tasks_' folder contains the **collection instances and tasks that each user is in charge of**.

## Dataset Statistics
The statistics below are obtained from running the '_./get_stats.py_' file.

### Total
Tasks sorted by complexity (number of steps taken):
- Easy: ['Close the shower curtain', 'Fill up the bathtub with water', 'Fill the sink with water', 'Off kitchen light', 'Open Blinds', 'Use the handphone', 'Close the blinds', 'Turn on shower head', 'Turn off the living room light', 'Find the egg in the room', 'Turn on all the floor lamp', 'Turn off all the bedroom light', 'Break shower glass', 'Hand towel on towelholder', 'Turn off the table lamp or desk lamp', 'Make coffee', 'Break the mirror', 'Use laptop', 'Read a book', 'Put off a candle', 'Crack the handphone screen']
- Moderate: ['Check the timing on the watch', 'Clean the bed', 'Throw away cracked egg', 'Fill up cup with water', 'Clear the sofa', 'Pour wine into a cup', 'Crack the window', 'Clean the mirror', 'Pour away coffee in a cup', 'Hide the egg', 'sink towel in water', 'Watch television', 'Toast a bread', 'Prepare sliced apple', 'Throw away used tissuebox', 'Clear the fridge', 'Boil water with a kettle', 'Water the houseplant', 'Wash dirty cloths', 'Pour away water from pot', 'Boil water with pot']
- Complex: ['Keep the laptop', 'Clear the bed', 'Throw away used toilet roll and soap bottle', 'Microwave the sliced potato', 'Keep sporting equipment', 'Throw away unused apple slice', 'Fry an egg', 'Collect dirty cloths', 'Keep box inside safe', 'Wash Dishes', 'Keep valuable items in safe', 'Keep kitchen utensils inside drawer', 'Light up one candle with another', 'Boil Potato', 'Store food into fridge', 'Make a breakfast', 'Make lettuce soup', 'Wash all the utensils', 'Make tomato soup', 'Pack things into the box']

Number of tasks: 63

Number of task instances: 3038

Max number of actions: 878

Min number of actions: 3

Mean number of actions: 70.5

Standard deviation for actions: 78.3

Mean length of mid-level tasks: 2.22

### By Room Category
#### Kitchen
Tasks sorted by complexity (number of steps taken):
- Easy: ['Off kitchen light', 'Find the egg in the room', 'Make coffee', 'Throw away cracked egg', 'Fill up cup with water', 'Pour wine into a cup', 'Pour away coffee in a cup', 'Hide the egg']
- Moderate: ['Toast a bread', 'Prepare sliced apple', 'Clear the fridge', 'Boil water with a kettle', 'Pour away water from pot', 'Boil water with pot', 'Microwave the sliced potato', 'Throw away unused apple slice']
- Complex: ['Fry an egg', 'Wash Dishes', 'Keep kitchen utensils inside drawer', 'Boil Potato', 'Store food into fridge', 'Make a breakfast', 'Make lettuce soup', 'Wash all the utensils', 'Make tomato soup']

Number of tasks: 26

Number of task instances: 1314

Max number of actions: 673

Min number of actions: 5

Mean number of actions: 93.5

Standard deviation for actions: 85

Mean length of mid-level tasks: 6

#### Living Room
Tasks sorted by complexity (number of steps taken):
- Easy: ['Use the handphone', 'Turn off the living room light', 'Turn on all the floor lamp', 'Turn off the table lamp or desk lamp', 'Use laptop', 'Read a book']
- Moderate: ['Crack the handphone screen', 'Check the timing on the watch', 'Clear the sofa', 'Crack the window', 'Watch television', 'Throw away used tissuebox']
- Complex: ['Water the houseplant', 'Keep the laptop', 'Keep box inside safe', 'Keep valuable items in safe', 'Light up one candle with another', 'Pack things into the box']

Number of tasks: 18

Number of task instances: 794

Max number of actions: 878

Min number of actions: 4

Mean number of actions: 58.7

Standard deviation for actions: 72.9

Mean length of mid-level tasks: 4

#### Bedroom
Tasks sorted by complexity (number of steps taken):
- Easy: ['Open Blinds', 'Close the blinds', 'Turn off all the bedroom light']
- Moderate: ['Break the mirror', 'Clean the bed', 'Clear the bed']
- Complex: ['Keep sporting equipment', 'Collect dirty cloths', 'Keep box inside safe', 'Keep valuable items in safe']

Number of tasks: 10

Number of task instances: 404

Max number of actions: 795

Min number of actions: 3

Mean number of actions: 60.7

Standard deviation for actions: 83

Mean length of mid-level tasks: 1.9

#### Bathroom
Tasks sorted by complexity (number of steps taken):
- Easy: ['Close the shower curtain', 'Fill up the bathtub with water', 'Fill the sink with water', 'Turn on shower head']
- Moderate: ['Break shower glass', 'Hand towel on towelholder', 'Put off a candle', 'Clean the mirror']
- Complex: ['sink towel in water', 'Wash dirty cloths', 'Throw away used toilet roll and soap bottle']

Number of tasks: 11

Number of task instances: 526

Max number of actions: 230

Min number of actions: 3

Mean number of actions: 38.4

Standard deviation for actions: 36.9

Mean length of mid-level tasks: 2.5


## Annotation Program
Our **annotation program** can be found in the '_./annotate_' folder.

It can be **run** by running the '_./annotate/gui.py_' file.

We have **made changes** to the '_allenai/ai2thor/unity/Assets/Scripts/PhysicsRemoteFPSAgentController.cs_' file in AI2-THOR to better suit our requirements, and the edited file is '_./annotate/PhysicsRemoteFPSAgentController.cs_'. 

In the '_./annotate/resources_' folder, we have:
- '_demo.mp4_': **tutorial video** displayed for users in our annotation program
- '_initial-scene-settings.txt_': **custom initial scene settings** for some of our tasks, in the '_['index','task','object',...,'actionable_property']_' format
- '_keyboard-control.png_': **keyboard control guide** displayed for users in our annotation program
- '_tasks_': folder containing the **tasks for each collection instance**, and is **used by our annotation program** to track progress and display related information during task annotation

## Data Augmentation


## Creating Videos
The '_./make_videos/replay_and_save_frames.py_' file is used to **replay the actions** in the dataset as a series of frames, and **save the frames**.

The '_./make_videos/create_video_from_frames.py_' file is used to **create videos from the frames saved**.
