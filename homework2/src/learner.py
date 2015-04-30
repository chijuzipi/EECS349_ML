'''
#### Data Structure #####
data : a list of records
record : a json like object ("winpercent":"....", "weather" : "...."})

#### Heuristics #####
@ 1
random choose the attribute

@ 2 
maxmize infomation gain
'''

import re
import sys
from random import randint
import math

class Learner():
  def __init__(self): 
    
    if len(sys.argv) <= 1:
      train_file = "../data/train_test2.csv"
    else:
      train_file = sys.argv[1]

    f = open(train_file, "r")
    lines = f.readlines()
    
    # get the list of attributes
    attrNames, records, resultAttr = readData(lines)
    print "read " +  str(len(attrNames)) + " attributes"
    print "read " +  str(len(records))   + " records"
    #print getEntropy(records, resultAttr)
    print self.DTL(records, attrNames, resultAttr, 1)

  def DTL(self, records, attrNames, resultAttr, fitFunction):
    resultValues  = [record[resultAttr] for record in records]
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

      newAttrNames = getNewAttrNames(attrNames, bestAttr) 
      print newAttrNames
      for value in attrValues:
        newRecords   = getNewRecords(records, bestAttr, value)
        child = self.DTL(newRecords, newAttrNames, resultAttr, fitFunction)
        tree[bestAttr][value] = child

    return tree

def getInfoGain(records, attr, resultAttr):
  freqMap = getFreqMap(records, resultAttr)
  entropy = getEntropy(records, resultAttr)
  subEntropy = 0.0
  for key in freqMap.keys():
    valFreq     = freqMap[key]/len(records)
    subRecords  = [record for record in records if record[attr] == key]
    subEntropy += valFreq * getEntropy(subRecords, resultAttr)

  return entropy - subEntropy

def getEntropy(records, resultAttr):
  entropy = 0.0
  freqMap = getFreqMap(records, resultAttr)
  for freq in freqMap.values():
    entropy += (-freq/len(records)) * math.log(freq/len(records), 2) 
  return entropy

def getNewAttrNames(attrNames, bestAttr):
  output = []
  for name in attrNames:
    if name is not bestAttr:
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
    return output

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
