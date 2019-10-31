# from operator import itemgetter, attrgetter
# def ontology_matching(words):
#
#     keywords=[]
#     words = sorted(words, key=itemgetter(1, 2), reverse=True)
#     for i in range(0, len(words)):
#         keywords.append(words[i][0])
#     lst_id = []
#     import json
#     f = open('Ontology Matching Files/doid_final.json')
#     data = json.load(f)
#
#     for (k, v) in data.items():
#         d = v['desc']
#         n = v['name']
#         desc = d.split()
#         name = n.split()
#         if (keywords[0] in desc or keywords[0] in name):
#             lst_id.append(k)
#
#     # print(lst_id)
#     # in keyword
#     # in lst of doid
#     # iterate over the entire json object
#     f = 0
#
#     for i in range(1, 2):
#         for j in range(0, len(lst_id)):
#             if lst_id[j] == 1:
#                 continue
#             else:
#                 # print('list[j]  ' + lst[j])
#                 for k, v in data.items():
#                     f = 0
#
#                     if lst_id[j] == k:
#                         d = v['desc']
#                         n = v['name']
#                         desc = d.split();
#                         name = n.split();
#                         if (keywords[i] in desc or keywords[i] in name):
#                             f = 1;
#                             # print('found in desc or name')
#                             # print(lst[j] , k )
#                             break;
#                         else:
#                             f = 0
#                             # print('not found sorry ')
#
#                 if f == 0:
#                     # print("removed")
#                     # lst.remove(lst[j])
#                     lst_id[j] = 1
#
#     def remove_values_from_list(the_list, val):
#         return [value for value in the_list if value != val]
#
#     lst = remove_values_from_list(lst_id, 1)
#     print(lst)

from pronto import Ontology

cl = Ontology("CSO.owl")
print(cl)
