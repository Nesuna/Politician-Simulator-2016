# cdf and choice code taken from 
# http://stackoverflow.com/questions/4113307/pythonic-way-to-select-list-elements-with-different-probability
import random
import bisect
import collections
import string

def cdf(weights):
    total = sum(weights)
    result = []
    cumsum = 0
    for w in weights:
        cumsum += w
        result.append(cumsum / total)
    return result

def choice(population, weights):
    assert len(population) == len(weights)
    cdf_vals = cdf(weights)
    x = random.random()
    idx = bisect.bisect(cdf_vals, x)
    return population[idx]

# readFile and writeFile taken from CMU 15-112 file I/O notes
def readFile(filename, mode="rt"):
    # rt = "read text"
    with open(filename, mode) as fin:
        return fin.read()

def writeFile(filename, contents, mode="wt"):
    # wt = "write text"
    with open(filename, mode) as fout:
        fout.write(contents)

def getCounts(text):
    # returns dictionary of dictionaries 
    # first level dictionary maps each word to a word that follows it
    # inner level dictionary maps each word to the number of occurrences 
    counts = dict()
    text = text.lower()
    punctuation = string.punctuation
    wordlist = text.split()

    for i in range(len(wordlist) - 1):
        first_word = wordlist[i]
        second_word = wordlist[i + 1]

        if first_word in counts:
            counts[first_word][second_word] = counts[first_word].get(second_word, 0) + 1

        else:
            counts[first_word] = {second_word: 1}

    return counts

def getProbabilities(counts):
    # returns dictionary of dictionaries 
    # first level dictionary maps each word to a word that follows it
    # inner level dictionary maps each word to probability it will occur after 
    # the first word
    prob = dict()

    for first_word in counts:
        summ = 0 
        second_word_counts = counts[first_word]
        for second_word in second_word_counts:
            summ += second_word_counts[second_word]

        second_word_probs = dict()
        for second_word in second_word_counts:
            second_word_probs[second_word] = (second_word_counts[second_word]/summ)

        prob[first_word] = second_word_probs

    return prob

def processText(filename):
    text = readFile(filename)
    counts = getCounts(text)
    probs = getProbabilities(counts)
    return probs

def get_next_word(word_probs):
    # given probabilities each word will occur, it will generate the next word
    words = []
    probs = []
    for word in word_probs:
        words.append(word)
        probs.append(word_probs[word]) 

    return choice(words, probs)


def createSentence():
    # make sure speech.txt is in the same folder as markovchains.py
    probs = processText("speech.txt")
    first = "the"
    sentence = ["The"]
    while True:
        raw = input("Press q to quit, r to reset your sentence, or any key to continue: ")

        if raw == "q":
            break
        if raw == "r":
            first = "the"
            sentence = ["The"]

        next_word_probs = probs.get(first, dict())
        next_word = get_next_word(next_word_probs)
        first = next_word
        sentence += [next_word]
        print(" ".join(sentence) +".")


