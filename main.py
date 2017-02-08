import sys
from DecisionTree import DecisionTree
from validation import Validator

def main():


    decisionTree=DecisionTree('./data_sets1/training_set.csv')

    print "finish construct tree"

    validator=Validator('./data_sets1/test_set.csv')

    validator.validation(decisionTree.root)


    #decisionTree.TreePrint(decisionTree.root,0)




if __name__=="__main__":main()