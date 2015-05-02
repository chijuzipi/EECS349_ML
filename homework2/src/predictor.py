from node import Node
from learner import Learner
from datareader import Datareader
import helper

import sys

class Predictor():
  def __init__(self, tree):
    # decision tree get from the learner
    self.DT = tree

    if len(sys.argv) <= 1:
      test_file = "../data/origin/test.csv"
    else:
      test_file = sys.argv[1]

    f = open(test_file, "r")
    lines = f.readlines()
    lines = lines[:20]

    # get the list of attributes
    readInput  = Datareader(lines)
    attrNames  = readInput.attrNames
    records    = readInput.records
    resultAttr = readInput.resultAttr
    typeList   = readInput.typeList

    helper.process(records, attrNames[:len(attrNames)-1], typeList) 
    self.predict(records, tree, resultAttr)
  
  # the predict function update the "winner" filed in the records
  def predict(self, records, tree, resultAttr):
    for record in records:
      record[resultAttr] = self.determine(record, tree, resultAttr)

  def determine(self, record, tree, resultAttr):
    if tree.name is None:
      return tree.value
    else:
      valHere = record[tree.name]
      if valHere < tree.value:
        return self.determine(record, tree.left, resultAttr)
      else:
        return self.determine(record, tree.right, resultAttr)

def main():
  learner   = Learner()
  predictor = Predictor(learner.tree)

if __name__== '__main__':
  main()
      
