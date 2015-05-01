class Node:
  def __init__(self, name, result):
    self.name = name
    self.result = result
    self.children = {}

  def addChild(self, value, node):
    self.children[value] = node
    
  def getChild(self, value):
    return self.children[value]

  def getChildren(self):
    return self.children.values()
