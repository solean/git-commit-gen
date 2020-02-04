import re


# Pipe commit messages to a file
#   $ git log --author=<email/name> --pretty=format:"%s" > msg.txt

#msgs = open('msg.txt', 'r')
with open('msg.txt', 'r') as f:
    msgs = f.read().split('\n')

# Parse out branch/PR merges so that we only have actual commit messages
parsedLines = []
for line in msgs:
    if not re.match('Merge ', line) and not re.match('\[bamboo\]', line):
        parsedLines.append(line)

msgs = open('msg.txt', 'w')
msgs.write('\n'.join(parsedLines))
msgs.close()

