from typing import List
import re
import subprocess
import argparse
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

        raw_glg_output = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True)
        raw_glg_output_lines = raw_glg_output.stdout.decode('utf-8').split('\n')

        # Parse out branch/PR merges so that we only have actual commit messages
        parsed_lines = []
        for line in raw_glg_output_lines:
            if not re.match(r'Merge ', line) and not re.match(r'\[bamboo\]', line):
                parsed_lines.append(line)

        self.model = markovify.NewlineText(parsed_lines)
        return self.model

    # Generate commit messages from model
    def generate(self, num_msgs: int) -> List[str]:
        if not self.model:
            self.build_model()

        msgs = [self.model.make_sentence() for i in range(num_msgs)]
        return msgs


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', help='Directory of the git repo to build the git log model from', type=str)
    parser.add_argument('--author', help='Filter git log by author', type=str)
    parser.add_argument('--n', help='Number of commit messages to generate (default = 1)', type=int, default=1)
    args = parser.parse_args()

    repo = args.repo
    author = args.author
    num_msgs = args.n

    g = GitCommitGenerator(repo, author)
    commit_msgs = g.generate(num_msgs)
    [print(msg) for msg in commit_msgs]

