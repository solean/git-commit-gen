import markovify

with open('msg.txt') as msgs:
    text = msgs.read()

text_model = markovify.NewlineText(text)

# Generate commit messages from model
for i in range(5):
    print(text_model.make_sentence())
