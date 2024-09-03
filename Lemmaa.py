import nltk
from nltk.stem import WordNetLemmatizer

# Initialize the WordNet lemmatizer
lemmatizer = WordNetLemmatizer()

# Open the input file for reading
with open("ToStem.txt", "r", encoding="utf-8") as input_file:
    # Read the contents of the file into a list of words
    words = input_file.read().split()

# Lemmatize each word
lemmatized_words = [lemmatizer.lemmatize(word) for word in words]

# Open the output file for writing
with open("Lemma.txt", "w", encoding="utf-8") as output_file:
    # Write the lemmatized words to the output file, separated by newlines
    output_file.write("\n".join(lemmatized_words))

