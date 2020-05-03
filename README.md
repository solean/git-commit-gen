# git-commit-gen

git-commit-gen is a fun tool that builds a markov model (using the fantastic [markovify](https://github.com/jsvine/markovify) module) of a git repo's log and use it to generate commit messages. The more commits in a repo, the more real the generated messages seem.

## Example outputs:
- "Removed extraneous comments before code complete with functional tests to work in two stages."
- "Began building out test case for testing values"
- "Removed extra comma that broke some validation on submit"
- "Updated and preliminary-ly working before some refactoring of the new procedure utility"
- "Fixed two integration tests for query list"

## Usage

command line:
```
python3 git_commit_gen.py --repo=~/my_project --author=satoshi@gmail.com --n=5
```

as a module:
```python
from git_commit_gen import GitCommitGenerator

g = GitCommitGenerator('~/my_project', 'satoshi@gmail.com')
# Optional, otherwise it will build every time you call .generate()
g.build_model()
messages = g.generate(2)
for x in messages:
    print(x)
```
