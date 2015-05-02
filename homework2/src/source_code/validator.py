from node import Node
from learner import Learner
from datareader import Datareader
import helper

import sys

class Validator():
  def __init__(self, datapath, tree):
    # decision tree get from the learner
    self.DT = tree

    if datapath != "None":
      validate_file = datapath
    elif len(sys.argv) <= 1:
      validate_file = "bvalidate.csv"
    else:
      validate_file = sys.argv[1]


    f = open(validate_file, "r")
    lines = f.readlines()

    # get the list of attributes
    readInput  = Datareader(lines)
    attrNames  = readInput.attrNames
    records    = readInput.records
    resultAttr = readInput.resultAttr
    typeList   = readInput.typeList

    helper.process(records, attrNames, typeList) 
    print 
    print "---> Using the validation set, the prediction accuracy is : "
    print(self.validate(records, self.DT, resultAttr))
    print 

  def validate(self, records, tree, resultAttr):
    total   = len(records)
    count   = 0
    for record in records:
      if self.check(record, tree, resultAttr):  
        count += 1
    return float(count)/float(total)

  def check(self, record, tree, resultAttr):
    if tree.name is None:
      return record[resultAttr] == tree.value
    else:
      valHere = record[tree.name]
      if valHere < tree.value:
        return self.check(record, tree.left, resultAttr)
      else:
        return self.check(record, tree.right, resultAttr)
        
def main():
  learner   = Learner()
  validator = Validator(learner.tree)

if __name__== '__main__':
  main()
      
