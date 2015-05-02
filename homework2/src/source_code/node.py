class Node:
 def __init__(self, name, value):
    self.name = name
    self.value = value
    self.left = None  # < value
    self.right = None # >= value
  
'''
  def addChild(self, value, node):
    self.children[value] = node
    
  def getChild(self, value):
    return self.children[value]

  def getChildren(self):
    return self.children.values()
'''
