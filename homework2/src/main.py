from learner import Learner 
from validator import Validator
from predictor import Predictor
import sys

def main():
  if len(sys.argv) != 4:
    print "Please specify input files"
    return
  learn = sys.argv[1]
  valid = sys.argv[2]
  pred  = sys.argv[3]
  learner   = Learner(learn)
  validator = Validator(valid, learner.tree)
  predictor = Predictor(pred, learner.tree)

if __name__== '__main__':
  main()
