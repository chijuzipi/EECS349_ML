from attribute import Attr
import re

class Learner():
  def __init__(self): 
    
    f = open("../data/btrain.csv", "r")
    lines = f.readlines()

    # a object list, that each object is a attribute
    examList, attrList = readData(lines)

  #TODO what is default for?
  def DTL(self, examList, attrList, default, value):
    if len(examList) == 0:
      return None
    
    if hasSameValue(examList):
      return getValue(examList[0])

    if len(attrList) == 0:
      #TODO what is Mode for?
      return Mode(examList)
    
    bestAttr, bestAttrIndex = getBest(examList, attrList)
    root = Node(bestAttr, value)
    for item in bestAttr.data:
      newExamList = buildExamList(examList, item, bestAttrIndex)
      root.addChild(self.DTL(newExamList, remove(attrList, bestAttrIndex), Mode(examples), item))
    return root


def getBest(examList, attrList):

def remove(attrList, bestAttrIndex):
  return del attrList[bestAttrIndex]

def hasSameValue(examList):
  result = getResult(examList[0])
  for exam in examList:
    if result != getResult(exam):
      return False
  return True

def getResult(exam):
  divid = exam.split(',')
  return divid[len(divid)-1]

def readData(lines):
  attrNameList = lines[0].split(',')
  attrList = []
  examList = []
  
  # construct the attribute object list
  for item in attrNameList:
    attrList.append(Attr(item)) 
  
  #construct the data list for each attribute
  for i in range(1, len(lines)):
    line = lines[i]
    examList.append(line)
    dataList = line.split(',')
    for j in range(len(dataList)):
      data = dataList[j]
      data = re.compile(r'[\n\r\t]').sub(' ', data) 
      attrList[j].data.append(data)

  return examList, attrList
  
def main():
  learner = Learner()

if __name__== '__main__':
  main()
