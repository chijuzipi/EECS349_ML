'''
#### Data Structure #####
data : a list of records
record : a json like object ("winpercent":"....", "weather" : "...."})
'''

from attribute import Attr
import re
import sys
from random import randint

class Learner():
  def __init__(self): 
    
    if len(sys.argv) <= 1:
      train_file = "../data/train_test.csv"
    else:
      train_file = sys.argv[1]

    f = open(train_file, "r")
    lines = f.readlines()
    
    # get the list of attributes
    attrNames, records, resultAttr = readData(lines)
    print len(attrNames)
    print len(records)

    print self.DTL(records, attrNames, resultAttr, 5)

  def DTL(self, records, attrNames, resultAttr, fitFunction):
    resultValues = [record[resultAttr] for record in records]
    default       = getMajority(records, resultAttr)
    
    # means follow the path, every thing is the same, but the result may still be different
    # therefore return majority
    if len(records) == 0 or len(attrNames) == 0:
      return default

    elif resultValues.count(resultValues[0]) == len(resultValues):
      return resultValues[0]
    
    else:
      bestAttr = getBestAttr(records, attrNames, resultAttr, fitFunction)
      print "the chosen attribute is : " + str(bestAttr)
      tree = {bestAttr:{}}

      # get unique values from the record corresponding to bestAttr
      attrValues = getAttrValues(records, bestAttr)

      for value in attrValues:
        newRecords   = getNewRecords(records, bestAttr, value)
        newAttrNames = getNewAttrNames(attrNames, bestAttr) 
        child = self.DTL(newRecords, newAttrNames, resultAttr, fitFunction)
        tree[bestAttr][value] = child

    return tree

def getNewAttrNames(attrNames, bestAttr):
  output = []
  for name in attrNames:
    if name != bestAttr:
      output.append(name)
  return output

def getNewRecords(records, bestAttr, value):
  output = []
  for record in records:
    if record[bestAttr] == value:
      output.append(record)
  return output

def getAttrValues(records, bestAttr):
  output = []
  for record in records:
    if bestAttr in record.keys():
      output.append(record[bestAttr])
  return output

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

def getBestAttr(records, attrNames, resultAttr, fitFunction):
  # random choose attribute
  if fitFunction == 5:
    index = randint(0, len(attrNames)-1)
    return attrNames[index]
  else:
    # TODO  implement the entropy 
    return 0
    
# generate the attribute list and example list
def readData(lines):
  # construct the attrbute name list
  dividList = lines[0].split(',')
  attrList = []
  for attr in dividList:
    attr = re.compile(r'[\n\r\t]').sub(' ', attr).rstrip()
    attrList.append(attr)
    
  recordList = []
  
  #construct the record list for each attribute
  for i in range(1, len(lines)):
    line = lines[i]
    dataList = line.split(',')
    record = {}
    for j in range(len(dataList)):
      data = dataList[j]
      data = re.compile(r'[\n\r\t]').sub(' ', data).rstrip()
      attrName = attrList[j]
      record[attrName] = data
    recordList.append(record)

  return attrList[:len(attrList)-1], recordList, attrList[len(attrList)-1]
  
def main():
  learner = Learner()

if __name__== '__main__':
  main()
