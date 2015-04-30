def getMajority(records, resultAttr):
  if len(records) == 0:
    return 0
  dictCount = {}
  for record in records:
    result = record[resultAttr]
    if result not in dictCount.keys():
      dictCount[result] = 1
    else:
      dictCount[result] += 1
  Max = 0
  output = 0
  for key in dictCount.keys():
    if dictCount[key] > Max:
      output = key 
      Max = dictCount[key]

  return output

coll1 = {}
coll1['piggy']= 1
coll2 = {}
coll2['piggy']=2 
coll3 = {}
coll3['piggy']=3 
coll4 = {}
coll4['piggy']= 5
coll5 = {}
coll5['piggy']= 5
records = []
records.append(coll1)
records.append(coll2)
records.append(coll3)
records.append(coll4)
records.append(coll5)

#print getMajority(records, 'piggy')

List = []
List.append('1')
List.append('2')
List.append('3')

List.remove('2')
print List

