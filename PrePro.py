import re


def read_stopwords(stopwords_file):
    stopwords_set = set()
    with open(stopwords_file, "r", encoding="utf-8") as file:
        for line in file:
            stopword = line.strip().lower()
            stopwords_set.add(stopword)
    return stopwords_set


def process_file(input_file, output_file, stopwords_set):
    tokens_set = set()
    with open(input_file, "r", encoding="utf-8") as file_in, open(
        output_file, "w", encoding="utf-8"
    ) as file_out:
        for line in file_in:
            tokens = re.split(r"\s*[^a-zA-Z']+\s*", line.strip())
            for token in tokens:
                token = token.lower()
                if token and token not in stopwords_set and token not in tokens_set:
                    tokens_set.add(token)
                    file_out.write(token + "\n")
    return tokens_set


def stem_words(input_file, output_file):
    from nltk.stem import PorterStemmer

    stemmer = PorterStemmer()
    with open(input_file, "r", encoding="utf-8") as file_in, open(
        output_file, "w", encoding="utf-8"
    ) as file_out:
        for line in file_in:
            word = line.strip()
            stemmed_word = stemmer.stem(word)
            file_out.write(stemmed_word + "\n")


def main():
    stopwords_set = read_stopwords("stopwords.txt")
    tokens_set = process_file("input.txt", "ToStem.txt", stopwords_set)
    stem_words("ToStem.txt", "Stemmed.txt")


if __name__ == "__main__":
    main()
