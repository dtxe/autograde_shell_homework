import pandas as pd
import os.path
import os

# get environment variables for output
github_step_output = os.environ['GITHUB_STEP_SUMMARY']

status_c = '✅'
status_i = '❌'

# score table
s = []

# load script
with open('.autograder/output.txt', 'r') as f:
    script_rslt = f.read()

script_rslt = script_rslt.split('\n+')
script_rslt = [{'command': x.split('\n')[0][1:].strip(), 'output': x.split('\n')[1:]} for x in script_rslt]

print(script_rslt)

############################################################################################################
############################################################################################################
# step 1: check if required directories exist
isdir = [os.path.isdir(f'dir{i}') for i in range(1, 4)]
if all(isdir):
    s.append({'question': 1, 'status': 1})
else:
    s.append({'question': 1, 'status': 0, 'comment': 'missing required directories'})

############################################################################################################
# step 2: check that the ls command was run
# if output contains "+ ls" followed by a line containing homework.sh, then correct
indx = [i for i, x in enumerate(script_rslt) if x['command'].startswith('ls')]
if len(indx) > 0:
    if any(['homework.sh' in script_rslt[i]['output'] for i in indx]):
        s.append({'question': 2, 'status': 1})
    else:
        s.append({'question': 2, 'status': 0, 'comment': '`ls` command run in the wrong directory'})
else:
    s.append({'question': 2, 'status': 0, 'comment': '`ls` command not run'})

############################################################################################################
# step 3: check that the 5 specified files were created in dir2
file_exists = [os.path.isfile(f'dir2/file{i}') for i in range(1, 6)]
if all(file_exists):
    s.append({'question': 3, 'status': 1})
else:
    s.append({'question': 3, 'status': 0, 'comment': 'missing required files in dir2'})

############################################################################################################
############################################################################################################

### Postprocessing ###
df = pd.DataFrame(s)
df.fillna('', inplace=True)

# compute percentage correct
correct = df['status'].sum()
total = df.shape[0]

# output the score table
df['status'].replace({1: status_c, 0: status_i}, inplace=True)
df.to_markdown(github_step_output, index=False)

if correct == total:
    exit(0)
else:
    exit(1)
