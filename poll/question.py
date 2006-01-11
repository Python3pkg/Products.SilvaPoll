class Question:
    def __init__(self, question, answers):
        self.question = question
        self.answers = answers
        self.votes = len(answers) * [0]

    def vote(self, index):
        self.votes[index] += 1
