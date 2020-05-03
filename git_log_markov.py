from typing import List
import re
import subprocess
import sys
import markovify

class GitCommitGenerator:
    def __init__(self, repo: str, author: str):
        self.repo = repo
        self.author = author
        self.model = None

    def build_model(self):
        # Build command to pull git log commits
        cmd = 'git'
        if self.repo:
            cmd += ' --git-dir ' + self.repo + '/.git'
        cmd += ' log --pretty=format:"%s"'
        if self.author:
            cmd += ' --author=' + self.author
        cmd += ' | cat'


        raw_glg_output = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True)
        raw_glg_output_lines = raw_glg_output.stdout.decode('utf-8').split('\n')


        # Parse out branch/PR merges so that we only have actual commit messages
        parsedLines = []
        for line in raw_glg_output_lines:
            if not re.match(r'Merge ', line) and not re.match(r'\[bamboo\]', line):
                parsedLines.append(line)


        self.model = markovify.NewlineText(parsedLines)
        return self.model

    # Generate commit messages from model
    def generate(self, num_lines: int) -> List[str]:
        if not self.model:
            self.build_model()

        msgs = []
        for i in range(num_lines):
            msgs.append(self.model.make_sentence())
        return msgs


# TODO: accept these as named params
# Parse params:
#   - OPTIONAL: directory of git repo (if not supplied, use current dir)
#   - OPTIONAL: commit author
#   - OPTIONAL: number of sentences to generate (default = 1)
if __name__ == '__main__':
    args = sys.argv
    repo_dir = None
    author = None
    num_sentences = 1

    if len(args) > 1:
        repo_dir = args[1]
    if len(args) > 2:
        author = args[2]
    if len(args) > 3:
        num_sentences = int(args[3])

    g = GitCommitGenerator(repo_dir, author)
    commit_msgs = g.generate(num_sentences)
    for msg in commit_msgs:
        print(msg)

