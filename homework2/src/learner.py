'''
#### Data Structure #####
data : a list of records
record : a json like object ("winpercent":"0.644213", "weather" : "...."})

#### Heuristics #####
@ 1
random choose the attribute

@ 2 
maxmize infomation gain
'''

#from __future__ import print_function
import re
import sys
from random import randint
from node import Node
import math
import numpy

class Learner():
  def __init__(self): 
    
    if len(sys.argv) <= 1:
      #train_file = "../data/origin/btrain.csv"
      train_file = "../data/test.csv"
    else:
      train_file = sys.argv[1]

    f = open(train_file, "r")
    lines = f.readlines()
    lines = lines[:5000]
    
    # get the list of attributes
    attrNames, records, resultAttr, typeList = readData(lines)
    print records
    return 
    process(records, attrNames, typeList)

    print "read " +  str(len(attrNames)) + " attributes"
    print "read " +  str(len(records))   + " records"

    printTree(self.DTL(records, attrNames, resultAttr), -1)

  def DTL(self, records, attrNames, resultAttr):
    resultValues  = [record[resultAttr] for record in records]
    default       = getMajority(records, resultAttr)
    
    # means follow the path, every thing is the same, but the result may still be different
    # therefore return majority
    if len(records) == 0 or len(attrNames) == 1:
      return Node(None, default)

    elif resultValues.count(resultValues[0]) == len(resultValues):
      return Node(None, resultValues[0])
      
    else:
      bestAttr = getBestAttr(records, attrNames, resultAttr)
      print bestAttr
      #print "the chosen attribute is : " + str(bestAttr)
      # construct a 2-dimeinsal array that stores value for bestAttr, and result
      attrResultList = getTwoDimensionArray(records, bestAttr, resultAttr)

      #sort the array based on the best attr value
      newList = sorted(attrResultList, key=lambda x: x[0], reverse=False)
      newDictList = []
      for item in newList:
       
        record = {} 
        record[resultAttr] = item[1]
        newDictList.append(record)

      selectIndex = getSelectVal(newDictList, resultAttr)
      selectVal   = newList[selectIndex][0]

      tree = Node(bestAttr, selectVal)
      
      # No need to remove the bestAttr from the attrNames, since the bestAttr may need to show up again
      #attrNames = getNewAttrNames(attrNames, bestAttr) 
      #print "the new attribute is " + str(newAttrNames)

      # add left and right child
      leftNewRecords, rightNewRecords = getNewRecords(records, bestAttr, selectVal)
      print len(leftNewRecords)
      print len(rightNewRecords)

      leftChild  = self.DTL(leftNewRecords, attrNames, resultAttr)
      rightChild = self.DTL(rightNewRecords, attrNames, resultAttr)
      tree.left  = leftChild
      tree.right = rightChild

    return tree

def process(records, attrNames, typeList):
  # default table hold default value for any attribute, based on the type and records
  defaultTable = {}
  for i in range(len(attrNames)):
    attr = attrNames[i]
    typ  = typeList[i]
    resultValues  = [record[attr] for record in records]
    resultValues = [x for x in resultValues if x != ' ?' and x != '?']
    defaultVal = "none"
    if typ == "numeric":
      defaultVal = numpy.mean(resultValues)
    elif typ == "nominal":
      defaultVal = getMajority(records, attr)
    defaultTable[attr] = defaultVal

  for i in range(len(attrNames)):
    attr = attrNames[i]
    typ  = typeList[i]
    for record in records:
      if record[attr] == '?':
        record[attr] = defaultTable[attr]

def getEntropy(records, resultAttr):
  entropy = 0.0
  freqMap = getFreqMap(records, resultAttr)
  for freq in freqMap.values():
    entropy += (-freq/len(records)) * math.log(freq/len(records), 2) 
  return entropy

def getSelectVal(newDictList, resultAttr):
  maxEntropy = 0.0 
  selectIndex = 0
  #return randint(0, len(newDictList)-1)
  for index in range(len(newDictList)-1):
    # only calculate at the index where the result value changes
    if newDictList[index][resultAttr] != newDictList[index+1][resultAttr]:
      leftEntropy  = getEntropy(newDictList[:index], resultAttr) * len(newDictList[:index])/len(newDictList)
      rightEntropy = getEntropy(newDictList[index:], resultAttr) * len(newDictList[index:])/len(newDictList)
      totalEntropy = leftEntropy + rightEntropy
      if totalEntropy > maxEntropy:
        selectIndex = index
        maxEntropy = totalEntropy

  return selectIndex

def getTwoDimensionArray(records, bestAttr, resultAttr):
  output = []
  for i in range(len(records)):
    inner = []
    record = records[i]
    inner.append(record[bestAttr])
    inner.append(record[resultAttr])
    output.append(inner)
  return output

def printTree(tree, n):
  # if it is a leaf
  if tree.name is None:
    print "----->" + str(tree.value)
    return
  print
  n += 1
  #print left child
  print n * "| ",
  print tree.name + "<" + str(tree.value),
  printTree(tree.left, n)

  #print right child
  print n * "| ",
  print tree.name + ">=" + str(tree.value),
  printTree(tree.right, n)

def getInfoGain(records, attr, resultAttr):
  freqMap = getFreqMap(records, resultAttr)
  entropy = getEntropy(records, resultAttr)
  subEntropy = 0.0
  for key in freqMap.keys():
    valFreq     = freqMap[key]/len(records)
    subRecords  = [record for record in records if record[attr] == key]
    subEntropy += valFreq * getEntropy(subRecords, resultAttr)

  return entropy - subEntropy

def getNewAttrNames(attrNames, bestAttr):
  output = []
  for name in attrNames:
    if name is not bestAttr:
      output.append(name)
  return output

def getNewRecords(records, bestAttr, value):
  leftOutput = []
  rightOutput = []
  for record in records:
    if record[bestAttr] < value:
      leftOutput.append(record)
    if record[bestAttr] >= value:
      rightOutput.append(record)
  return leftOutput, rightOutput

def getAttrValues(records, bestAttr):
  output = []
  for record in records:
    if bestAttr in record.keys():
      output.append(record[bestAttr])
  return output

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

def getBestAttr(records, attrNames, resultAttr):
  # random choose attribute
  
  output   = attrNames[0]
  maxGain = 0.0
  for attr in attrNames:
    if attr == resultAttr:
      continue
    infoGain = getInfoGain(records, attr, resultAttr)
    if infoGain > maxGain:
      output = attr
      maxGain = infoGain
  return output
    
# generate the attribute list and example list
def readData(lines):
  # construct the attrbute name list
  attrList = []
  dividList = lines[0].split(',')
  for attr in dividList:
    print attr
    attr = re.compile(r'[\n\r\t]').sub(' ', attr).strip()
    print "after process: " + attr
    attrList.append(attr)
    
  # construct the type list: noimal and numeric
  typeList = []
  dividList = lines[1].split(',')
  for attr in dividList:
    attr = re.compile(r'[\n\r\t]').sub(' ', attr).strip()
    typeList.append(attr)

  #construct the record list for each attribute
  recordList = []
  for i in range(2, len(lines)):
    line = lines[i]
    dataList = line.split(',')
    record = {}
    for j in range(len(dataList)):
      data = dataList[j]
      data = re.compile(r'[\n\r\t]').sub(' ', data).rstrip()
      if data != '?' and data != ' ?':
        data = float(data) 
      attrName = attrList[j]
      record[attrName] = data
    recordList.append(record)

  return attrList, recordList, attrList[len(attrList)-1], typeList
  
def main():
  learner = Learner()

if __name__== '__main__':
  main()
