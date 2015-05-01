from __future__ import print_function

print ('this is a test', end='')
print ('this is a test', end='')
print ('this is a test', end='')
print ('this is a test', end='')

def getFreqMap(records, resultAttr):

  output = {}

  for record in records:
    result = record[resultAttr]
    if result not in output.keys():
      output[result] = 1.0
    else:
      output[result] += 1.0

  return output

def getMajority(records, resultAttr):
  if len(records) == 0:
    return 0
  dictCount = getFreqMap(records, resultAttr)
  Max = 0
  for key in dictCount.keys():
    if dictCount[key] > Max:
      output = key 
      Max = dictCount[key]

  return output

coll1 = {}
coll1['piggy']= 1
coll2 = {}
coll2['piggy']=3
coll3 = {}
coll3['piggy']=3 
coll4 = {}
coll4['piggy']= 5
coll5 = {}
coll5['piggy']= 4
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
#print List

def getNewAttrNames(attrNames, bestAttr):
  output = []
  for name in attrNames:
    if name is not bestAttr:
      output.append(name)
  return output
attrNames = ['1', '2', '3']
bestAttr  = '2'
#print getNewAttrNames(attrNames, bestAttr)

