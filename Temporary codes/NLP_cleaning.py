import csv,nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk import  pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from sklearn.feature_extraction.text import CountVectorizer

class cleaning_nlp:

    def __init__(self,name,definition,synonym):
        self.name=name
        self.definition=definition
        self.synonym=synonym

    def freq(self,words):
        dict = {
        }
        for i in words:
            dict[i] = words.count(i)
        # print("Dictionary after stopwords removal(no lemmatization)")
        # print(dict)
        return dict


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



    def keywords_process_for_dictionary(self):
        word_arr = self.tokenizing([self.definition,self.synonym,self.name])
        stopwords_remove = self.stop_words_removal(word_arr)
        count = self.freq(stopwords_remove)
        return count

    def pos_to_wordnet(self,pos_tag):
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

    def lemmatization(self,part_of_speech,clean_words):
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
        parts_of_speech = pos_tag(word_tokenize(self.definition))#+' '+self.synonym+ ' ' + self.name))
        # print(parts_of_speech)
        return parts_of_speech

    def freq(self,words):
        dict = {
        }
        for i in words:
            dict[i] = words.count(i)
        # print("Dictionary after stopwords removal(no lemmatization)")
        # print(dict)
        return dict


    def stemming(self,cleaning_words):
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

    def stop_words_removal(self,word_arr):
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

    def tokenizing(self,parameters):
        # Tokenising..............................................
        data='';
        for i in parameters:
            data+=i +' '
        data=data.strip()
        # print(data)
        data=data.split('_')
        # print(data)
        sentence=''
        for i in data:
            sentence+=i
        word_arr =word_tokenize(sentence.lower())
        #  Here lower case is done to remove more stopwords, but some information is lost
        # print word_arr
        return word_arr

with open('CSV Files/doid_updated.csv','r') as csvFile:
    reader=csv.reader(csvFile)
    data=list(reader)
csvFile.close()

feature_set=[]
dataset=[]
# i=77
# obj=cleaning_nlp(data[i][0],data[i][1],data[i][2])
# dict_freq=obj.keywords_process_for_dictionary()
# words=obj.feature_set_formation()
# print(words)
# print(dict_freq)
# print(words)


for i in range(1,200):#len(data)):
    # print(i)
    obj=cleaning_nlp(data[i][0],data[i][1],data[i][2])
    dict_freq=obj.keywords_process_for_dictionary()
    words = obj.feature_set_formation()
    feature_set+=[i for i in words]
    dataset+=[(dict_freq,data[i][3])]
feature_set=list(set(feature_set))

for i in feature_set:
#     print(i)
    for j in range(0,len(dataset)):
        # print(list((dataset[j][0]).keys()))
        if i in list(dataset[j][0].keys()):
            # dataset[j][0][i]= True
            continue
        else:
            dataset[j][0][i] = False
            # print(dataset[j][0].get(i))

# # for i in dataset:
# #     print(i)

# from nltk import NaiveBayesClassifier
# x_y_train, x_y_test=dataset[0:170],dataset[170:]
# classifier=NaiveBayesClassifier.train(x_y_train)
# print('Accuracy:',nltk.classify.accuracy(classifier,x_y_test))
# print(classifier.show_most_informative_features(15))
#
#
# # from nltk import DecisionTreeClassifier
# # classifier=DecisionTreeClassifier.train(x_y_train)
# # print('Accuracy:',nltk.classify.accuracy(classifier,x_y_test))
# # # #print(classifier.show_most_informative_features(15))
#
#
