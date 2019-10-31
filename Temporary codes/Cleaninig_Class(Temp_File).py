class feature_set_words:
    def __init__(self, name, definition, synonym):
        self.name = name
        self.definition = definition
        self.synonym = synonym

    def freq(self, words):
        dict = {
        }
        for i in words:
            dict[i] = words.count(i)
        # print("Dictionary after stopwords removal(no lemmatization)")
        # print(dict)
        return dict

    def pos_to_wordnet(self, pos_tag):
        if pos_tag.startswith('J'):
            return wordnet.ADJ
        elif pos_tag.startswith('N'):
            return wordnet.NOUN
        elif pos_tag.startswith('V'):
            return wordnet.VERB
        # elif pos_tag.startswith('M'):
        #     return wordnet.MODAL
        # elif pos_tag.startswith('R'):
        #     return wordnet.ADVERB
        else:
            return wordnet.NOUN

    def lemmatization(self, part_of_speech, clean_words):
        lemmatized = []
        lemmatizer = WordNetLemmatizer()
        # print pos[2][0]
        # print clean_words[1]
        for i in range(0, len(part_of_speech)):
            for j in range(0, len(clean_words)):
                if part_of_speech[i][0].lower() == clean_words[j]:
                    # print part_of_speech[i][0], clean_words[j], part_of_speech[i][1]
                    lemmatized.append(
                        (lemmatizer.lemmatize(clean_words[j], pos=self.pos_to_wordnet(part_of_speech[i][1]))).lower())
                    break
                else:
                    continue
        # print("After Lemmatization No. of Words:", len(list(set(lemmatized))))
        return list(set(lemmatized))

    def parts_of_speech(self):
        parts_of_speech = pos_tag(word_tokenize(self.definition))  # +' '+self.synonym+ ' ' + self.name))
        # print(parts_of_speech)
        return parts_of_speech

    def freq(self, words):
        dict = {
        }
        for i in words:
            dict[i] = words.count(i)
        # print("Dictionary after stopwords removal(no lemmatization)")
        # print(dict)
        return dict

    def stemming(self, cleaning_words):
        '''
        The process of stemmimng is very dumb. Not always give reslutant output. The information passed through it might result in bad output.
        Stemming is the process of finding the root word of the given word.
        Prefer Lemmatization over it.
        '''
        ps = PorterStemmer()
        # stem_words = ['play', 'playing', 'played', 'player', "happy", 'happier']
        stemmed_words = [ps.stem(w) for w in cleaning_words]
        # print(stem_words)
        return stemmed_words

    def stop_words_removal(self, word_arr):
        # Stopwords and Punctuations.........................................
        stop_words = stopwords.words('english')
        # Stop Words are present of different languages, for papers of different languages.
        # Cleaning words(removing stopwords and punctuations
        # print(stop_words)
        import string
        punctuations = list(string.punctuation)
        # print(string.punctuation)
        stop_words += punctuations
        # print(len(stop_words))
        file_data = []
        with open('stopwords', 'r') as f:
            for line in f:
                for word in line.split():
                    file_data.append(word)
        stop_words += file_data
        stop_words = set(stop_words)
        stop_words = list(stop_words)
        new_word_arr = []
        for i in word_arr:
            new_word_arr.append(i.lower())
        clean_words = [w for w in new_word_arr if not w in stop_words]
        # print((stop_words))
        # print("After cleaning the stopwords, no of words:", len(clean_words))
        return clean_words

    def tokenizing(self, parameters):
        # Tokenising..............................................
        data = '';
        for i in parameters:
            data += i + ' '
        data = data.strip()
        # print(data)
        data = data.split('_')
        # print(data)
        sentence = ''
        for i in data:
            sentence += i
        word_arr = word_tokenize(sentence.lower())
        #  Here lower case is done to remove more stopwords, but some information is lost
        # print word_arr
        return word_arr


import csv

with open('CSV Files/doid_updated.csv','r') as csvFile:
    reader=csv.reader(csvFile)
    data=list(reader)
csvFile.close()

