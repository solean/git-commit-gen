import re
import subprocess
import sys
import markovify


# TODO: accept these as named params
# Parse params:
#   - OPTIONAL: directory of git repo (if not supplied, use current dir)
#   - OPTIONAL: commit author
#   - OPTIONAL: number of sentences to generate (default = 1)
args = sys.argv

if len(args) > 1:
    repo_dir = args[1]
if len(args) > 2:
    author = args[2]
if len(args) > 3:
    num_sentences = int(args[3])


# Build command to pull git log commits
cmd = ''
if repo_dir:
    cmd = 'cd ' + repo_dir + '; '
cmd += 'git log --pretty=format:"%s"'
if author:
    cmd += ' --author=' + author
cmd += ' | cat'


raw_glg_output = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True)
raw_glg_output = raw_glg_output.stdout.decode('utf-8').split('\n')


# Parse out branch/PR merges so that we only have actual commit messages
parsedLines = []
for line in raw_glg_output:
    if not re.match(r'Merge ', line) and not re.match(r'\[bamboo\]', line):
        parsedLines.append(line)


text_model = markovify.NewlineText(parsedLines)

# Generate commit messages from model
for i in range(num_sentences):
    print(text_model.make_sentence())
