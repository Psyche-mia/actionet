# ActioNet: An Interactive End-to-End Platform for Task-Based Data Collection and Augmentation in 3D Environments
## Task-Based Dataset
Our dataset can be found in the '_./dataset/{collection_id}_' folders.

Each **data file** has the naming convention of '_./dataset/{collection_id}/{task}\_{floor_plan}_'. In each file, there are **two lists**:
- The **first list** shows the **task** and the **floor plan**
- The **second list** shows the **actions taken to complete the task**

The '_./dataset/resources/task_descriptions_' folder contains the **task descriptions of the tasks for each collection instance**.

The '_./dataset/resources/user_tasks_' folder contains the **collection instances and tasks that each user is in charge of**.

## Dataset Statistics
### Total
Number of tasks: 63

Number of task instances: 3038

Max number of actions: 878

Min number of actions: 3

Mean number of actions: 70.5

Standard deviation for actions: 78.3

Tasks sorted by complexity (number of steps taken):
- Easy: ['Close the shower curtain', 'Fill up the bathtub with water', 'Fill the sink with water', 'Off kitchen light', 'Open Blinds', 'Use the handphone', 'Close the blinds', 'Turn on shower head', 'Turn off the living room light', 'Find the egg in the room', 'Turn on all the floor lamp', 'Turn off all the bedroom light', 'Break shower glass', 'Hand towel on towelholder', 'Turn off the table lamp or desk lamp', 'Make coffee', 'Break the mirror', 'Use laptop', 'Read a book', 'Put off a candle', 'Crack the handphone screen']
- Moderate: ['Check the timing on the watch', 'Clean the bed', 'Throw away cracked egg', 'Fill up cup with water', 'Clear the sofa', 'Pour wine into a cup', 'Crack the window', 'Clean the mirror', 'Pour away coffee in a cup', 'Hide the egg', 'sink towel in water', 'Watch television', 'Toast a bread', 'Prepare sliced apple', 'Throw away used tissuebox', 'Clear the fridge', 'Boil water with a kettle', 'Water the houseplant', 'Wash dirty cloths', 'Pour away water from pot', 'Boil water with pot']
- Complex: ['Keep the laptop', 'Clear the bed', 'Throw away used toilet roll and soap bottle', 'Microwave the sliced potato', 'Keep sporting equipment', 'Throw away unused apple slice', 'Fry an egg', 'Collect dirty cloths', 'Keep box inside safe', 'Wash Dishes', 'Keep valuable items in safe', 'Keep kitchen utensils inside drawer', 'Light up one candle with another', 'Boil Potato', 'Store food into fridge', 'Make a breakfast', 'Make lettuce soup', 'Wash all the utensils', 'Make tomato soup', 'Pack things into the box']

Mean length of mid-level tasks: 2.22

### By Room Category

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
