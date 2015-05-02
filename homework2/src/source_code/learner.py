'''
#### Data Structure #####
data : a list of records
record : a json like object ("winpercent":"0.644213", "weather" : "...."})

#### Heuristics #####
@
maxmize infomation gain

'''
import re
import sys
from random import randint
from node import Node
from datareader import Datareader
import helper
import math
import numpy

class Learner():
  def __init__(self, datapath): 
    
    if datapath != "None":
      train_file = datapath

    elif len(sys.argv) <= 1:
      train_file = "btrain.csv"
      #train_file = "../data/test.csv"
    else:
      train_file = sys.argv[1]

    f = open(train_file, "r")
    lines = f.readlines()
    lines = lines[:16000]
    
    # get the list of attributes
    readInput  = Datareader(lines)
    attrNames  = readInput.attrNames
    records    = readInput.records
    resultAttr = readInput.resultAttr
    typeList   = readInput.typeList
    print typeList

    helper.process(records, attrNames, typeList)

    print "read " +  str(len(attrNames)) + " attributes"
    print "read " +  str(len(records))   + " records"
    print 

    self.tree = self.DTL(records, attrNames, resultAttr)
    
    print "-----> Printing DNF of the decision tree ..."
    helper.printDNF(self.tree)
    print 

  def DTL(self, records, attrNames, resultAttr):

    # basecase 1) no record or no new attributes
    default = helper.getMajority(records, resultAttr)
    if len(records) == 0 or len(attrNames) == 1:
      return Node(None, default)

    # basecase 2) all the record left endup with same result
    resultValues  = [record[resultAttr] for record in records]

    if resultValues.count(resultValues[0]) == len(resultValues):
      return Node(None, resultValues[0])
      
    else:
      bestAttr = helper.getBestAttr(records, attrNames, resultAttr)
      #print bestAttr
        
        
      #print "the chosen attribute is : " + str(bestAttr)
      # construct a 2-dimeinsal array that stores value for bestAttr, and result
      attrResultList = helper.getTwoDimensionArray(records, bestAttr, resultAttr)

      #sort the array based on the best attr value
      newList = sorted(attrResultList, key=lambda x: x[0], reverse=False)
      newDictList = []
      for item in newList:
       
        record = {} 
        record[resultAttr] = item[1]
        newDictList.append(record)

      selectIndex = helper.getSelectVal(newDictList, resultAttr)
      selectVal   = newList[selectIndex][0]

      tree = Node(bestAttr, selectVal)
      attrNames = helper.getNewAttrNames(attrNames, bestAttr)

      # add left and right child
      leftNewRecords, rightNewRecords = helper.getNewRecords(records, bestAttr, selectVal)
      #print len(leftNewRecords)
      #print len(rightNewRecords)

      leftChild  = self.DTL(leftNewRecords, attrNames, resultAttr)
      rightChild = self.DTL(rightNewRecords, attrNames, resultAttr)
      tree.left  = leftChild
      tree.right = rightChild

    return tree
  
def main():
  learner = Learner("None")

if __name__== '__main__':
  main()
