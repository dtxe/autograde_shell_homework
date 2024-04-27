import pandas as pd
import os.path
import os

github_step_output = os.environ['GITHUB_STEP_SUMMARY']

# score table
s = []

# load script
with open('homework.sh', 'r') as f:
    script = f.readlines()

with open('output.txt', 'r') as f:
    output = f.readlines()

# step 1: check if required directories exist
isdir = [os.path.isdir(f'dir{i}') for i in range(1, 4)]
if all(isdir):
    s.append({'question': 1, 'grade': 'correct'})
else:
    s.append({'question': 1, 'grade': 'incorrect', 'comment': 'missing required directories'})

# step 2: check that the ls command was run
# if output contains "+ ls" followed by a line containing homework.sh, then correct
indx = [i for i, x in enumerate(output) if '+ ls' in x]
if len(indx) > 0:
    if any(['homework.sh' in output[i+1] for i in indx]):
        s.append({'question': 2, 'grade': 'correct'})
    else:
        s.append({'question': 2, 'grade': 'incorrect'})

# step 3: check that the 5 specified files were created in dir2
file_exists = [os.path.isfile(f'dir2/file{i}.txt') for i in range(1, 6)]
if all(file_exists):
    s.append({'question': 3, 'grade': 'correct'})
else:
    s.append({'question': 3, 'grade': 'incorrect', 'comment': 'missing required files in dir2'})

# output the score table
df = pd.DataFrame(s)
df.to_markdown(github_step_output)
