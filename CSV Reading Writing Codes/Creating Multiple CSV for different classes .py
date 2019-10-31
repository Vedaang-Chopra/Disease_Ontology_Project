import csv

with open('D:\Development\Minor Project-Ontology Based\Sample_Doctor_Dataset\CSV Files\doid_updated.csv','r') as csvFile:
    reader=csv.reader(csvFile)
    data=list(reader)
csvFile.close()

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
    return y_train_test,encoding_output

y_train_test,encoding_output=encoding_y_train()

print(encoding_output)

# for (key,val) in encoding_output.items():
#     list = ['Name', 'Definition', 'Synonym', 'Output']
#     temp_list = [None, None, None, None]
#     with open('CSV Files/Multiple_Datasets/'+ str(key) + '_dataset.csv', 'w', newline='') as csvFile:
#         writer = csv.writer(csvFile)
#         writer.writerows([list])
#         # print(val)
#         for j in range(0,len(data)):
#             if key==data[j][3]:
#                 temp_list=[str(data[j][0]),str(data[j][1]),str(data[j][2]),str(data[j][3])]
#                 # print(len(temp_list))
#                 writer.writerows([temp_list])
#             else:
#                 continue
#     csvFile.close()