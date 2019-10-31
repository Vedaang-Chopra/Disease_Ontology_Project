# -*- coding: utf-8 -*-
"""Ontology Code.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1KEnruOhrmyRvTdT0WlwCrKSm4qioh_bP
"""

import csv, nltk

# nltk.download()
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import preprocessing
from sklearn.preprocessing import OneHotEncoder

# from google.colab import files
# uploaded = files.upload()
# from google.colab import files
# uploaded = files.upload()



with open('CSV Files/doid_updated.csv', 'r', encoding='latin1') as csvFile:
    reader = csv.reader(csvFile)
    data = list(reader)
csvFile.close()
feature_set = []
dataset = []




class feature_set_words:

    def __init__(self, list_of_indices):
        self.list_of_indices = list_of_indices

    def building_dataset(self, words, multiple_inputs):
        dataset = []
        output_class = str(multiple_inputs[0])
        print(output_class)
        temp = {}
        index = multiple_inputs[1]
        for j in index:
            temp = {}
            tokens = (self.tokenizing([data[j][1]]))
            for i in range(0, len(tokens)):
                if tokens[i] in words:
                    temp[tokens[i]] = True
                else:
                    continue
            if data[j][3] == output_class:
                dataset.append((temp, output_class))
            else:

                dataset.append((temp, "Not " + str(output_class)))
        return dataset

    def changing_for_count_vectorization(self, words):
        temp = []
        sent = ''
        for i in words:
            for j in i:
                sent = sent + ' ' + str(j)
            temp.append(sent.strip())
            sent = ' '
        return temp

    def feature_set_formation_for_incorrect_words(self):
        final_words_for_count_vectorization = []
        for i in range(1, len(data)):
            if i in self.list_of_indices:
                continue
            else:
                word_arr = self.tokenizing([data[i][1]])
                stopwords_remove = self.stop_words_removal(word_arr)
                parts_of_speech = self.parts_of_speech(data[i][1])
                words = self.lemmatization(parts_of_speech, stopwords_remove)
                final_words_for_count_vectorization.append(words)

        temp = self.changing_for_count_vectorization(final_words_for_count_vectorization)
        # print(len(temp))
        count_vec = CountVectorizer(max_features=30)
        x_train_features = count_vec.fit_transform(temp[:])
        # print(len(count_vec.get_feature_names()))
        print((count_vec.get_feature_names()))
        # print(x_train_features.todense())
        return count_vec.get_feature_names()

    def feature_set_formation_for_correct_words(self):
        final_words_for_count_vectorization = []
        for i in range(1, len(self.list_of_indices)):
            word_arr = self.tokenizing([data[i][1]])
            stopwords_remove = self.stop_words_removal(word_arr)
            parts_of_speech = self.parts_of_speech(data[i][1])
            words = self.lemmatization(parts_of_speech, stopwords_remove)
            final_words_for_count_vectorization.append(words)
        # print(final_words_for_count_vectorization)
        temp = self.changing_for_count_vectorization(final_words_for_count_vectorization)
        count_vec = CountVectorizer(max_features=15)
        x_train_features = count_vec.fit_transform(temp)
        # print(len(count_vec.get_feature_names()))
        # print((count_vec.get_feature_names()))
        # print(x_train_features.todense())
        return count_vec.get_feature_names()

    def feature_set_for_formation_complete_data(self):
        final_words_for_count_vectorization = []
        for i in range(0, len(self.list_of_indices)):
            word_arr = self.tokenizing([data[i][1]])
            stopwords_remove = self.stop_words_removal(word_arr)
            parts_of_speech = self.parts_of_speech(data[i][1])
            words = self.lemmatization(parts_of_speech, stopwords_remove)
            final_words_for_count_vectorization.append(words)
        temp = self.changing_for_count_vectorization(final_words_for_count_vectorization)
        # print(len(temp))
        count_vec = CountVectorizer(max_features=2000)
        x_train_features = count_vec.fit_transform(temp)
        # print(len(count_vec.get_feature_names()))
        # print((count_vec.get_feature_names()))
        # print(x_train_features.todense())
        return count_vec.get_feature_names(),x_train_features

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

    def parts_of_speech(self, definition):
        parts_of_speech = pos_tag(word_tokenize(definition))  # +' '+self.synonym+ ' ' + self.name))
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


def encoding_y_train():
    encoding_output = {}
    c = 1
    for i in range(1, len(data)):
        if data[i][3] in encoding_output.keys():
            continue
        else:
            encoding_output[data[i][3]] = c
            c = c + 1
    # print(len(encoding_output))
    # print(encoding_output)
    y_train_test = []
    for i in range(1, len(data)):
        y_train_test.append(encoding_output[data[i][3]])
    # print(y_train_test)
    return y_train_test, encoding_output


def encoding_y_train():
    encoding_output = {}
    c = 1
    for i in range(1, len(data)):
        if data[i][3] in encoding_output.keys():
            continue
        else:
            encoding_output[data[i][3]] = c
            c = c + 1
    # print(len(encoding_output))
    # print(encoding_output)
    y_train_test = []
    for i in range(1, len(data)):
        y_train_test.append(encoding_output[data[i][3]])
    # print(y_train_test)
    return y_train_test, encoding_output

def creating_feature_set_for_ontology_based_NLP(output_class):
    y_train_test, encoding_output = encoding_y_train()
    # print(encoding_output)
    temp_data = []
    # print(encoding_output['drug allergy'])
    for i in encoding_output:
        if i == str(output_class):
            for j in range(0, len(data)):
                if i == data[j][3]:
                    temp_data.append(j)
                else:
                    continue
            # print(temp_data)
        else:
            continue
    obj = feature_set_words(temp_data)
    words_correct = obj.feature_set_formation_for_correct_words()
    words_incorrect = obj.feature_set_formation_for_incorrect_words()
    incorrect_rows = []
    words_incorrect = set(words_incorrect)
    for j in range(0, len(data)):
        tokens = (obj.tokenizing([data[j][1]]))
        for i in range(0, len(tokens)):
            if tokens[i] in words_incorrect:
                incorrect_rows.append(j)
                break
            else:
                continue
    # print((incorrect_rows))
    indices = temp_data + incorrect_rows
    words = list(words_incorrect) + words_correct
    dataset = obj.building_dataset(words, ['drug allergy', indices])
    # print(dataset)
    return dataset


def creating_dataset_for_Normal_Text_classification():

    # Encoding All Classes
    le = preprocessing.LabelEncoder()
    le.fit([data[i][3] for i in range(1,len(data))])
    y_train_test = (le.transform([data[i][3] for i in range(1,len(data))]))
    print(len(y_train_test))

    # print(list(y_train_test))
    # enc = OneHotEncoder(handle_unknown='ignore')
    # enc.fit()
    # enc.fit_transform(final_y)
    # print(final_y)

    # Creating Keywords for dataset
    obj =feature_set_words([i for i in range(1,len(data))])
    feature_names,dataset=(obj.feature_set_for_formation_complete_data())
    print((dataset).shape)
    return dataset,y_train_test





data_input = ['patent blue V allergy','A drug allergy that has_allergic_trigger patent blue V.', 'allergic contact dermatitis to DNP']
data_x,data_y=creating_dataset_for_Normal_Text_classification()
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.model_selection import train_test_split
# x_train,x_test,y_train,y_test=train_test_split(data_x,data_y,random_state=1)
# clf=DecisionTreeClassifier()
# clf.fit(x_train,y_train)
# y_pred_train=clf.predict(x_train)
# y_pred_test=clf.predict(x_test)
# print()
# from sklearn.metrics import confusion_matrix,accuracy_score
# a=confusion_matrix(y_train,y_pred_train)
# b=confusion_matrix(y_test,y_pred_test)
# c=accuracy_score(y_pred_test,y_test)
# print(a)
# print(b)
# print(c)


dataset=creating_feature_set_for_ontology_based_NLP('drug allergy')
import random
random.shuffle(dataset)
x_train = dataset[:3000]
x_test = dataset[3000:]
y_test=[]
y_train=[]
for i in x_train:
    y_test.append(i[1])

for i in x_test:
    y_test.append(i[1])

# print(y_test)


from nltk.classify import SklearnClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB,BernoulliNB
from sklearn.linear_model import LogisticRegression,SGDClassifier
from sklearn.svm import SVC, LinearSVC


testing_set=x_test
training_set=x_train


from nltk import NaiveBayesClassifier
classifier = NaiveBayesClassifier.train(x_train)
print(nltk.classify.accuracy(classifier, x_test))
print("Original Naive Bayes Algo accuracy percent:", (nltk.classify.accuracy(classifier, testing_set))*100)
classifier.show_most_informative_features(15)

Random_Forest_Classifier=SklearnClassifier(RandomForestClassifier())
Random_Forest_Classifier.train(training_set)
# Random_Forest_Classifier_Normal=RandomForestClassifier()
# Random_Forest_Classifier_Normal.fit(x_train)
print("Random Forest Classifier After Ontology Matching percent:", (nltk.classify.accuracy(Random_Forest_Classifier, testing_set))*100)
print("Random Forest Classifier :", (nltk.classify.accuracy(Random_Forest_Classifier, testing_set))*100)

MNB_classifier = SklearnClassifier(MultinomialNB())
MNB_classifier.train(training_set)
print("MNB_classifier accuracy After Ontology Matching percent:", (nltk.classify.accuracy(MNB_classifier, testing_set))*100)
print("MNB_classifier accuracy percent:", (nltk.classify.accuracy(MNB_classifier, testing_set))*100)

BernoulliNB_classifier = SklearnClassifier(BernoulliNB())
BernoulliNB_classifier.train(training_set)
print("BernoulliNB_classifier accuracy After Ontology Matching percent:", (nltk.classify.accuracy(BernoulliNB_classifier, testing_set))*100)
print("BernoulliNB_classifier accuracy percent:", (nltk.classify.accuracy(BernoulliNB_classifier, testing_set))*100)

LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
LogisticRegression_classifier.train(training_set)
print("LogisticRegression_classifier accuracy After Ontology Matching percent:", (nltk.classify.accuracy(LogisticRegression_classifier, testing_set))*100)
print("LogisticRegression_classifier accuracy percent:", (nltk.classify.accuracy(LogisticRegression_classifier, testing_set))*100)

SGDClassifier_classifier = SklearnClassifier(SGDClassifier())
SGDClassifier_classifier.train(training_set)
print("SGDClassifier_classifier accuracy After Ontology Matching percent :", (nltk.classify.accuracy(SGDClassifier_classifier, testing_set))*100)
print("SGDClassifier_classifier accuracy percent :", (nltk.classify.accuracy(SGDClassifier_classifier, testing_set))*100)

SVC_classifier = SklearnClassifier(SVC())
SVC_classifier.train(training_set)
print("SVC_classifier accuracy After Ontology Matching percent:", (nltk.classify.accuracy(SVC_classifier, testing_set))*100)
print("SVC_classifier accuracy percent:", (nltk.classify.accuracy(SVC_classifier, testing_set))*100)

LinearSVC_classifier = SklearnClassifier(LinearSVC())
LinearSVC_classifier.train(training_set)
print("LinearSVC_classifier accuracy After Ontology Matching percent:", (nltk.classify.accuracy(LinearSVC_classifier, testing_set))*100)
print("LinearSVC_classifier percent:", (nltk.classify.accuracy(LinearSVC_classifier, testing_set))*100)

# from  sklearn.metrics import confusion_matrix,classification_report
# print(classification_report(y_test,y_pred))
# print(confusion_matrix(y_test,y_pred))

