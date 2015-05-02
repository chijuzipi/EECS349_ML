# generate the attribute list and example list
import re

class Datareader():
  def __init__(self, lines):
    self.attrNames   = []
    self.records     = []
    self.resultAttr  = ''
    self.typeList    = []
    self.readData(lines)
    
  def readData(self,lines):
    # construct the attrbute name list
    attrList = []
    dividList = lines[0].split(',')
    for attr in dividList:
      attr = re.compile(r'[\n\r\t]').sub(' ', attr).strip()
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
        data = re.compile(r'[\n\r\t]').sub(' ', data).strip()
        if data != '?':
          data = float(data) 
        attrName = attrList[j]
        record[attrName] = data
      recordList.append(record)

    self.attrNames   =  attrList
    self.records     =  recordList
    self.resultAttr  =  attrList[len(attrList)-1]
    self.typeList    =  typeList
