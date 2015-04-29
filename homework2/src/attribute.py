class Attr:
  def __init__(self, name):
    self.name = name 
    self.data = []

  def test(self):
    print "this is a " + self.name

class Exam:
  def __init__(self, name):
    self.name = name 
    self.data = []

class Node:
  #the value is its parent's value that lead to her
  def __init__(self, name, value):
    self.name     = name 
    self.value    = value
    self.children = []

  def addChild(node):
    self.children.append(node)
