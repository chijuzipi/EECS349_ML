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
      #train_file = "../data/train_test3.csv"
      train_file = "../data/train_test.csv"
    else:
      train_file = sys.argv[1]

    f = open(train_file, "r")
    lines = f.readlines()
    
    # get the list of attributes
    attrNames, records, resultAttr = readData(lines)
    print "read " +  str(len(attrNames)) + " attributes"
    print "read " +  str(len(records))   + " records"
    #print getEntropy(records, resultAttr)
    #self.DTL(records, attrNames, resultAttr, 1)
    printTree(self.DTL(records, attrNames, resultAttr, 1), -1)

  def DTL(self, records, attrNames, resultAttr, fitFunction):
    resultValues  = [record[resultAttr] for record in records]
    default       = getMajority(records, resultAttr)
    
    # means follow the path, every thing is the same, but the result may still be different
    # therefore return majority
    if len(records) == 0 or len(attrNames) == 0:
      return Node(None, default)

    elif resultValues.count(resultValues[0]) == len(resultValues):
      return Node(None, resultValues[0])
      
    else:
      bestAttr, split = getBestAttr(records, attrNames, resultAttr, fitFunction)
      if split == 0:
        return Node(None, default)
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
      newAttrNames = getNewAttrNames(attrNames, bestAttr) 
      #print "the new attribute is " + str(newAttrNames)

      # add left and right child
      leftNewRecords, rightNewRecords = getNewRecords(records, bestAttr, selectVal)
      #print len(leftNewRecords)
      #print len(rightNewRecords)

      leftChild  = self.DTL(leftNewRecords, newAttrNames, resultAttr, fitFunction)
      rightChild = self.DTL(rightNewRecords, newAttrNames, resultAttr, fitFunction)
      tree.left  = leftChild
      tree.right = rightChild

    return tree

def getEntropy(records, resultAttr):
  entropy = 0.0
  freqMap = getFreqMap(records, resultAttr)
  for freq in freqMap.values():
    entropy += (-freq/len(records)) * math.log(freq/len(records), 2) 
  return entropy

def getSelectVal(newDictList, resultAttr):
  maxEntropy = 0.0 
  selectIndex = 0
  for index in range(len(newDictList)):
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
  print tree.name + "<" + tree.value,
  printTree(tree.left, n)

  #print right child
  print n * "| ",
  print tree.name + ">=" + tree.value,
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

def getBestAttr(records, attrNames, resultAttr, heu):
  # random choose attribute
  if heu == 0:
    index = randint(0, len(attrNames)-1)
    return attrNames[index]
  elif heu == 1:
    output   = attrNames[0]
    maxGain = 0.0
    for attr in attrNames:
      infoGain = getInfoGain(records, attr, resultAttr)
      if infoGain > maxGain:
        output = attr
        maxGain = infoGain
    if maxGain == 0.0:
      return output, 0
    else:
      return output, 1

  return ''
    
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
