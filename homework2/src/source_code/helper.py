import re
from random import randint
import math
import numpy
import sys

def process(records, attrNames, typeList):
  # default table hold default value for any attribute, based on the type and records
  defaultTable = {}
  for i in range(len(attrNames)):
    attr = attrNames[i]
    typ  = typeList[i]
    resultValues  = [record[attr] for record in records]
    resultValues = [x for x in resultValues if x != '?']
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
  minEntropy = sys.maxint
  selectIndex = 0
  #return randint(0, len(newDictList)-1)
  for index in range(1, len(newDictList)):
    # only calculate at the index where the result value changes
    
    if index+1 < len(newDictList) and newDictList[index][resultAttr] != newDictList[index+1][resultAttr]:
      leftEntropy  = getEntropy(newDictList[:index], resultAttr) * len(newDictList[:index])/len(newDictList)
      rightEntropy = getEntropy(newDictList[index:], resultAttr) * len(newDictList[index:])/len(newDictList)

      totalEntropy = leftEntropy + rightEntropy
      #print str(index) + " " + str(leftEntropy) + " " + str(rightEntropy) + " " + str(totalEntropy)
      if totalEntropy < minEntropy:
        selectIndex = index
        minEntropy = totalEntropy

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

def getInfoGain(records, attr, resultAttr):
  freqMap = getFreqMap(records, attr)
  entropy = getEntropy(records, resultAttr)
  subEntropy = 0.0
  for key in freqMap.keys():
    valFreq     = freqMap[key]/len(records)
    subRecords  = [record for record in records if record[attr] == key]
    subEntropy += valFreq * getEntropy(subRecords, resultAttr)

  output =  entropy - subEntropy
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

def printDNF(tree):
  stat = []
  count = []
  count.append(0)

  buildstat(tree, stat, count)

def buildstat(tree, stat, count):
  if count[0] > 16:
    return 
  if tree.name is None:
    count[0] += 1
    if float(tree.value) == 0.0:
      print "[NOT(" + " AND ".join(stat) + ")]" + " OR "
    else:
      print "(" + " AND ".join(stat) + ")" + " OR "
    return
  
  stat.append(tree.name + " < " + str(tree.value))
  buildstat(tree.left, stat, count)
  stat.pop()
  stat.append(tree.name + " >= " + str(tree.value))
  buildstat(tree.right, stat, count)
  stat.pop()
  return




