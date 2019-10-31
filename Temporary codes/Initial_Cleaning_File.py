
import random

def encoding_y_train():
    encoding_output={}
    for i in range(1,len(data)):
        if data[i][3] in encoding_output.keys():
            continue
        else:
            encoding_output[data[i][3]]=i
    print(len(encoding_output))
    # print(encoding_output)
    y_train_test=[]
    for i in range(1,len(data)):
        y_train_test.append(encoding_output[data[i][3]])
    # print(y_train_test)
    return y_train_test



with open('CSV Files/doid_updated.csv','r',encoding='latin1') as csvFile:
    reader=csv.reader(csvFile)
    data=list(reader)
csvFile.close()
feature_set=[]
dataset=[]
# print(data)
random.shuffle(data)

i=2

print(data)
# temp_y= [data[i][3] for i in range(0,len(data))]
# temp_y=list(set(temp_y))
# print(len(temp_y))
temp_y_dict={}
# for i in range(0,len(temp_y)):
#     temp_y_dict[temp_y[i]]=i
y_train_test=[]
# print(temp_y_dict)
for i in range(1,len(data)):
    # print(i)
    if not data[i][0]:
        continue
    elif not data[i][1]:
        continue
    elif not data[i][2]:
        continue
    else:

        # dict_freq = obj.keywords_process_for_dictionary()
        words = obj.feature_set_formation()
        sent = ''
        for j in words:
            sent += j + " "
        sent = sent.strip()
        feature_set.append(sent)
        # print(data[i][3])
        y_train_test.append(data[i][3])


# # print(feature_set)
# # # # c=0
# # # # for i in feature_set:
# # # #     c+=len(i.split(' '))

x_test_features=count_vec.transform(feature_set[170:])

# print(y_train_test)
# print(x_train_features.shape)
# print(x_test_features.shape)
# print(type(x_test_features))
# print(final_y.shape)


from sklearn.ensemble import RandomForestClassifier
rf=RandomForestClassifier()
rf.fit(x_train_features,y_train_test[:170])
y_pred=rf.predict(x_test_features)

from sklearn.ensemble import RandomForestClassifier
rf=RandomForestClassifier()
rf.fit(x_train_features,y_train_test[:170])
y_pred=rf.predict(x_test_features)


from sklearn.metrics import accuracy_score
from  sklearn.metrics import confusion_matrix,classification_report
print(classification_report(y_train_test[170:],y_pred))
print(confusion_matrix(y_train_test[170:],y_pred))
print(accuracy_score(y_pred,y_train_test[170:]))


# from sklearn.linear_model import LogisticRegression
# lr=LogisticRegression()
# lr.fit(x_train_features,y_train_test[:170])
# print(lr.predict(x_test_features))
# print(lr.score(y_train_test[:170],lr.predict(x_test_features)))
