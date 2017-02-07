import math
import random
import copy
from collections import deque
from csvparser import CsvParser

class TreeNode:
    def __init__(self,val,left=None,right=None):
        self.val=val
        self.label=-1
        self.left=left
        self.right=right

class DecisionTree:
    def __init__(self,filename):

        csvparser=CsvParser()
        attributeNames = csvparser.attributeName
        data = csvparser.data
        colums = csvparser.colums
        rows = csvparser.rows
        target = csvparser.target


    def ID3(self,colums,rows,target):
        if len(rows)==0:
            return None
        node=TreeNode(-1)

        Entropy=self.getEntropy(rows,target)
        node.label=self.getMostCommon(target)

        if Entropy==0 or len(colums)==0:
            return node
        else:
            AttributeChosen=self.getAttribute(rows,colums,target,Entropy)
            if AttributeChosen==-1:
                return node
            node.val=AttributeChosen

            newAttributes = []
            for attribute in colums:
                if attribute != AttributeChosen:
                    newAttributes.append(attribute)
            colums = newAttributes

            branch=self.separate(rows,target,AttributeChosen)
            node.left=self.ID3(colums,branch[0][0],branch[0][1])
            node.right = self.ID3(colums, branch[1][0], branch[1][1])

            return node



    def getAttribute(self,rows,colums,target,Entropy):
        maxGainRatio = -1
        targetAttribute = -1

    def separate(self,rows,target,AttributeChosen):
        new_rows0 = []
        new_rows1 = []
        new_target0 = []
        new_target1 = []

        for i in range(len(rows)):
            if self.data[rows[i]][AttributeChosen]==1:
                new_rows0.append(rows[i])
                new_target0.append(target[i])
            else:
                new_rows1.append(rows[i])
                new_target1.append(target[i])
        return [(new_rows0,new_target0), (new_rows1,new_target1)]



    def getEntropy(rows,target):
        num=len(rows)
        count=0
        for i in range(len(target)):
            if i==1:
                count+=1
        pos=1.0*count/num
        neg=1-pos
        if pos == 0 or neg == 0:
            return 0
        return - (pos * math.log(pos, 2) + neg * math.log(neg, 2))

    def getMostCommon(target):
        if len(target)==1:
            return target[0]
        count = 0
        for i in range(len(target)):
            if i == 1:
                count += 1
        if count>=len(target)/2:
            return 1
        else:
            return 0

