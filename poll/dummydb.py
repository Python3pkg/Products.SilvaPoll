from question import Question

class DB:
    def __init__(self, context):
        # we don't need the context here, it's only useful in situations
        # where we want to actually get stuff from the ZODB (like SQL
        # connections)
        self.db = []

    def create(self, question, answers):
        q = Question(question, answers)
        self.db.append(q)
        return self.db.index(q)

    def get(self, id):
        return self.db[id]

    def update(self, id, question, answers):
        try:
            current = self.get(id)
        except IndexError:
            current = None
        q = Question(question, answers)
        # note that if the number of answers doesn't match, we blatantly throw
        # away any existing votes (since we can't really know much about what
        # votes to keep)
        if current and len(current.votes) == len(answers):
            q.votes = current.votes

    def vote(self, id, index):
        q = self.get(id)
        q.vote(index)
