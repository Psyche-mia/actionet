# ActioNet: An Interactive End-to-End Platform for Task-Based Data Collection and Augmentation in 3D Environments
## Task-Based Dataset
Our dataset can be found in the '_./dataset/{collection_id}_' folders.

Each **data file** has the naming convention of '_./dataset/{collection_id}/{task}\_{floor_plan}_'. In each file, there are **two lists**:
- The **first list** shows the **task** and the **floor plan**
- The **second list** shows the **actions taken to complete the task**

The '_./dataset/resources/task_descriptions_' folder contains the **task descriptions of the tasks for each collection instance**.

The '_./dataset/resources/user_tasks_' folder contains the **collection instances and tasks that each user is in charge of**.

## Dataset Statistics

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
