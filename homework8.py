############################################################
# CIS 521: Homework 8
############################################################

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import math
import random
import string

############################################################

student_name = "Xinyuan Quan"

############################################################
# Section 1: Ngram Models
############################################################


def tokenize(text):
    tokens = []
    current = []

    for char in text:
        if char.isspace():
            if current:
                tokens.append("".join(current))
                current = []
        elif char in string.punctuation:
            if current:
                tokens.append("".join(current))
                current = []
            tokens.append(char)
        else:
            current.append(char)
    
    if current:
        tokens.append("".join(current))
    return tokens


def ngrams(n, tokens):
    start = ["<START>"] * (n - 1)
    sum_token = start + list(tokens) + ["<END>"]
    result = []

    for index, token in enumerate(sum_token[n - 1:], start=n - 1):
        context = tuple(sum_token[index - n + 1 : index])
        result.append((context, token))
    return result


class NgramModel(object):

    def __init__(self, n):
        self.n = n
        self.ngram_counts = {}
        self.context_counts = {}

    def update(self, sentence):
        for context, token in ngrams(self.n, tokenize(sentence)):
            self.ngram_counts[(context, token)] = (
                self.ngram_counts.get((context, token), 0) + 1
            )
            self.context_counts[context] = (
                self.context_counts.get(context, 0) + 1
            )

    def prob(self, context, token):
        context_count = self.context_counts.get(context, 0)
        if context_count == 0:
            return 0.0
        return self.ngram_counts.get((context, token), 0) / context_count

    def random_token(self, context):
        possible_tokens = sorted(
            token for (saved_context, token) in self.ngram_counts
            if saved_context == context
        )
        if not possible_tokens:
            return None
        random_value = random.random()
        cumulative = 0.0
        for token in possible_tokens:
            cumulative += self.prob(context, token)
            if random_value < cumulative:
                return token
        return possible_tokens[-1]

    def random_text(self, token_count):
        context = ("<START>",) * (self.n - 1)
        result = []

        for _ in range(token_count):
            token = self.random_token(context)
            if token is None:
                break
            result.append(token)

            if token == "<END>":
                context = ("<START>",) * (self.n - 1)
            elif self.n > 1:
                context = context[1:] + (token,)

        return " ".join(result)

    def perplexity(self, sentence):
        sentence_ngrams = ngrams(self.n, tokenize(sentence))
        log_probability = 0.0

        for context, token in sentence_ngrams:
            probability = self.prob(context, token)
            if probability == 0:
                return float("inf")
            log_probability += math.log(probability)

        return math.exp(-log_probability / len(sentence_ngrams))

def create_ngram_model(n, path):
    model = NgramModel(n)
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            model.update(line)
    return model

############################################################
# Section 2: Feedback
############################################################


# Just an approximation is fine.
feedback_question_1 = """
7
"""

feedback_question_2 = """
The synatax of token and gram.
"""

feedback_question_3 = """
Clear structure.
"""
