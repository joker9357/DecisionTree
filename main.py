import sys
from DecisionTree import DecisionTree

def main():
    decisionTree=DecisionTree('./data_sets1/training_set.csv')

    print "finish construct tree"

    decisionTree.TreePrint(decisionTree.root,0)




if __name__=="__main__":main()