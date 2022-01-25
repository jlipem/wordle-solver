import math


def get_words(path="words.txt"):
    f = open(path, "r")
    raw_words = f.readlines()
    words_ls = [word.strip() for word in raw_words]
    return words_ls


def get_letter_frequency(words_ls):
    letters = dict()
    for word in words_ls:
        for index, letter in enumerate(word):
            if index not in letters.keys():
                letters[index] = dict()
            if letter not in letters[index].keys():
                letters[index][letter] = 1
            else:
                letters[index][letter] += 1
    return letters


def get_word_scores(letter_scores):
    word_scores = dict()
    for word in words:
        score = 0
        for index, letter in enumerate(word):
            score += letter_scores[index][letter]
        divider = len(words) / len(set(word))
        word_scores[word] = score / divider
    return word_scores


def get_top_words_and_scores(word_scores, n=10):
    top_words = [(word, word_scores[word]) for word in word_scores.keys()]
    return sorted(top_words, key=lambda word_score: word_score[1], reverse=True)[:n]


def get_top_words(word_scores, n=10):
    top_words = [(word, word_scores[word]) for word in word_scores.keys()]
    sorted_words = sorted(top_words, key=lambda word_score: word_score[1], reverse=True)[:n]
    return [word_tuple[0] for word_tuple in sorted_words]


def get_letter_count(word1, word2):
    penalty = 0
    letters_ls = [letter for letter in word1]
    letters_ls.extend([letter for letter in word2])
    for index, letter in enumerate(word1):
        if word2[index] == letter:
            penalty -= 1
    return len(set(letters_ls)) + penalty


def get_double_scores(word_scores):
    double_scores = dict()
    top_words = get_top_words(word_scores, 2000)
    halfway = math.ceil(len(top_words) / 2)

    for word1 in top_words[:halfway]:
        for word2 in top_words[halfway:]:
            if word1 == word2:
                pass
            else:
                unique_letter_count = get_letter_count(word1, word2)
                initial_score = word_scores[word1] + word_scores[word2]
                double_scores[word1 + ', ' + word2] = (unique_letter_count * (initial_score-2500)) / 10000
    return double_scores


def get_top_doubles(doubles, n=10):
    top_doubles = [(double, doubles[double]) for double in doubles.keys()]  # if scores[word] >= min_score
    return sorted(top_doubles, key=lambda double_score: double_score[1], reverse=True)[:n]


def guess_word(guess, result, words_ls, guesses):
    """guess is the guess as a str. result is a str, x for miss, o is for make, - is for wrong spot"""
    for index, letter in enumerate(guess):
        if result == 'ooooo':
            print('Guesses: ' + str(guesses))
        if result[index] == 'o':
            words_ls = [word for word in words_ls if word[index] == letter]
        elif result[index] == 'x':
            words_ls = [word for word in words_ls if letter not in word]
        else:
            words_ls = [word for word in words_ls if letter in word and letter != word[index]]
    return words_ls


if __name__ == '__main__':
    words = get_words()
    guesses = 1
    while guesses < 6:
        letters = get_letter_frequency(words)
        scores = get_word_scores(letters)
        print(get_top_words_and_scores(scores, 10))
        guess = input('Enter your guess: ')
        result = input('Enter the result: ')
        words = guess_word(guess, result, words, guesses)
        if len(words) == 1:
            print(words)
            guesses = 6
        else:
            guesses += 1

    # letters = get_letter_frequency(words)
    # scores = get_word_scores(letters)
    # print(get_top_words_and_scores(scores))
    # double_word_scores = get_double_scores(scores)
    # top_double_scores = get_top_doubles(double_word_scores, 40)
