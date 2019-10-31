import csv,nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk import  pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from operator import itemgetter, attrgetter


def ontology_matching(words):

    keywords=[]
    words = sorted(words, key=itemgetter(1, 2), reverse=True)
    for i in range(0, len(words)):
        keywords.append(words[i][0])
    lst_id = []
    import json
    f = open('Ontology Matching Files/doid_final.json')
    data = json.load(f)

    for (k, v) in data.items():
        d = v['desc']
        n = v['name']
        desc = d.split()
        name = n.split()
        if (keywords[0] in desc or keywords[0] in name):
            lst_id.append(k)

    # print(lst_id)
    # in keyword
    # in lst of doid
    # iterate over the entire json object
    f = 0

    for i in range(1, 2):
        for j in range(0, len(lst_id)):
            if lst_id[j] == 1:
                continue
            else:
                # print('list[j]  ' + lst[j])
                for k, v in data.items():
                    f = 0

                    if lst_id[j] == k:
                        d = v['desc']
                        n = v['name']
                        desc = d.split();
                        name = n.split();
                        if (keywords[i] in desc or keywords[i] in name):
                            f = 1;
                            # print('found in desc or name')
                            # print(lst[j] , k )
                            break;
                        else:
                            f = 0
                            # print('not found sorry ')

                if f == 0:
                    # print("removed")
                    # lst.remove(lst[j])
                    lst_id[j] = 1

    def remove_values_from_list(the_list, val):
        return [value for value in the_list if value != val]

    lst = remove_values_from_list(lst_id, 1)
    print(lst)


class cleaning_nlp_processes:

    def __init__(self, name, definition, synonym):
        self.name = name
        self.definition = definition
        self.synonym = synonym

    def same_frequency_words_priority(self,word_list):
        final_list=[]
        parts_of_speech = self.parts_of_speech()
        for i in range(0,len(word_list)):
            words = self.lemmatization(parts_of_speech, [word_list[i][0]])
            if len(words)==0 or word_list[i][0]==words[0]:
                # print(words,word_list[i],"Flag=1")
                final_list.append((word_list[i][0],word_list[i][1],1))
            else:
                # print(words,word_list[i]," Flag=0")
                final_list.append((word_list[i][0],word_list[i][1],0))
        return final_list


    def priority_provide(self, stop_words_remove,freq_dict):
        final_priority_list=[]
        # print(freq_dict)
        import operator
        sorted_x = sorted(freq_dict.items(), key=operator.itemgetter(1),reverse=True)
        import collections
        sorted_dict = dict(collections.OrderedDict(sorted_x))
        sorted_list = [(k, v) for k, v in sorted_dict.items()]
        # print(sorted_list)
        splice_index=[]
        for i in range(1,len(sorted_list)):
            if sorted_list[i-1][1]==sorted_list[i][1]:
                continue
            else:
                splice_index.append(i)
        # print(splice_index)
        if len(splice_index)==0:
            pass
        elif len(splice_index)==1:
            list_1=(sorted_list[:splice_index[0]])
            list_2=(sorted_list[splice_index[0]:])
            final_priority_list = self.same_frequency_words_priority(list_1)
            final_priority_list += self.same_frequency_words_priority(list_2)

        else:
            list_1=(sorted_list[:splice_index[0]])
            final_priority_list=self.same_frequency_words_priority(list_1)

            for i in range(1,len(splice_index)):
                list_i=(sorted_list[splice_index[i-1]:splice_index[i]])
                final_priority_list+=self.same_frequency_words_priority(list_i)
            list_end=(sorted_list[splice_index[len(splice_index)-1]:])
            final_priority_list += self.same_frequency_words_priority(list_end)

        # print(final_priority_list)
        # sorted_x = sorted(freq_dict.items(), key=operator.itemgetter(1), reverse=True)
        return final_priority_list

    def keywords_formation(self):
        word_arr = self.tokenizing([self.definition,self.synonym,self.name])
        stopwords_remove = self.stop_words_removal(word_arr)
        # print(stopwords_remove)
        count = self.freq(stopwords_remove)
        final_prority_array=self.priority_provide(stopwords_remove,count)
        return final_prority_array

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
            sentence += i+' '
        sentence=sentence.strip()
        word_arr = word_tokenize(sentence.lower())
        #  Here lower case is done to remove more stopwords, but some information is lost
        # print word_arr
        return word_arr

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
        # print(len(stop_words))
        # print("After cleaning the stopwords, no of words:", len(clean_words))
        # print(clean_words)
        return clean_words

    def freq(self, words):
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
        # print(lemmatized)
        return list(set(lemmatized))

    def parts_of_speech(self):
        parts_of_speech = pos_tag(word_tokenize(self.definition))  # +' '+self.synonym+ ' ' + self.name))
        # print(parts_of_speech)
        return parts_of_speech

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




    def stemming(self, cleaning_words):
        '''
        The process of stemmimng is very dumb. Not always give reslutant output. The information passed through it might result in bad output.
        Stemming is the process of finding the root word of the given word.
        Prefer Lemmatization over it.
        '''
        ps = PorterStemmer()
        # stem_words = ['play', 'playing', 'played', 'player', "happy", 'happier']
        stemmed_words = [ps.stem(w) for w in cleaning_words]
        # print(len(stemmed_words))
        # print(stemmed_words)
        return stemmed_words



# i=0
# data_input=[['acute hemorrhagic conjunctivitis',
#              'A viral infectious disease that results in inflammation located in conjunctiva',
#              "Epidemic hemorrhagic conjunctivitis"]]
# data_input=[['pterygium',
#              'A corneal disease that is characterized by a triangular tissue growth located_in cornea of the eye that is the result of collagen degeneration and fibrovascular proliferation',
#              "surfer's eye"]]
# data_input=[['isocyanates allergic asthma','An allergic asthma that has_allergic_trigger isocyanates.',"allergic asthma to HMDI"]]
# data_input=[["A malignant Vascular tumor that results_in rapidly proliferating, extensively infiltrating anaplastic cells derives_from blood vessels and derived_from the lining of irregular blood-filled spaces.",
#              "angiosarcoma",
#              "malignant Vascular tumor"]]



with open('CSV Files/doid_updated.csv','r') as csvFile:
    reader=csv.reader(csvFile)
    data=list(reader)
csvFile.close()
data_input=data
for i in range(1,200):#len(data_input)):
    obj=cleaning_nlp_processes(data_input[i][0],data_input[i][1],data_input[i][2])
    words=obj.keywords_formation()
    print(words)
    # ontology_matching(words)