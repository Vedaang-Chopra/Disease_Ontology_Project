# This Code is Used to Create our DATASET(File_Name-Doid_updated.csv)

import csv


with open('CSV Files/doid.csv','r') as csvFile:
    reader=csv.reader(csvFile)
    data=list(reader)
csvFile.close()
list=['Name','Definition','Synonym','Output']
temp_list=[None,None,None,None]
with open('CSV Files/doid_updated.csv', 'w', newline='') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerows([list])
csvFile.close()
jumps=[]
for i in range(0,len(data)):
    if (data[i][0]=='[Term]'):
        jumps.append(i)
    else:
        continue
for j in range(0,len(jumps)):
    if j==len(jumps)-1:
        break
    else:
        for i in range(jumps[j],jumps[j+1]):
            if data[i][0].split(':')[0].strip()=='name':
                # print(data[i][0].split(':')[1].strip())
                temp_list[0]=data[i][0].split(':')[1].strip()
            if data[i][0].split(':')[0].strip()=='def':
                # print(data[i][0].split(':')[1].strip().split('"')[1].strip())
                temp_list[1] = data[i][0].split(':')[1].strip().split('"')[1].strip()
            if data[i][0].split(':')[0].strip() == 'synonym':
                # print(data[i][0].split(':')[1].strip().split('"')[1].strip())
                temp_list[2] = data[i][0].split(':')[1].strip().split('"')[1].strip()
            if data[i][0].split(':')[0].strip() == 'is_a':
                # print(data[i][0].split(':')[2].split('!')[1].strip())
                temp_list[3] = data[i][0].split(':')[2].split('!')[1].strip()
        with open('CSV Files/doid_updated.csv', 'a', newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerows([temp_list])
        csvFile.close()