import nltk
import os

class Analyzer():
    """Implements sentiment analysis."""

    def __init__(self, positives, negatives):
        """Initialize Analyzer."""
        self.positive = set()
        file1 = open(positives, "r")
        for line in file1:
            if line.startswith(";") == False:
                self.positive.add(line.rstrip("\n"))
        file1.close()
        self.negative = set()
        file2 = open(negatives, "r")
        for line in file2:
            if line.startswith(";") == False:
                self.negative.add(line.rstrip("\n"))
        file2.close()


    def analyze(self, text):
        """Analyze text for sentiment, returning its score."""
        tokenizer = nltk.tokenize.TweetTokenizer()
        tokens = tokenizer.tokenize(text)
        score = 0
        for word in tokens:
            if word.lower() in self.positive:
                score += 1
            elif word.lower() in self.negative:
                score -= 1
            else:
                continue
        return score







