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

        csvparser=CsvParser(filename)

        self.attributeNames = csvparser.attributeName
        self.data = csvparser.data
        self.colums = csvparser.colums
        self.rows = csvparser.rows
        self.target = csvparser.target

        self.root=self.ID3(self.colums,self.rows,self.target)

    def ID3(self,colums,rows,target):
        if len(rows)==0:
            return None
        node=TreeNode(-1)
        #print(len(colums))

        Entropy=self.getEntropy(rows,target)
        node.label=self.getMostCommon(target)

        if Entropy==0 or len(colums)==0:
            return node
        else:
            AttributeChosen=self.getAttribute(rows,colums,target,Entropy)
            if AttributeChosen==-1:
                return node
            node.val=AttributeChosen
            #print(AttributeChosen)

            newAttributes = []
            for attribute in colums:
                if attribute != AttributeChosen:
                    newAttributes.append(attribute)
            colums = newAttributes

            branch=self.Separate(rows,target,AttributeChosen)
            node.left=self.ID3(colums,branch[0][0],branch[0][1])
            node.right = self.ID3(colums, branch[1][0], branch[1][1])

            return node



    def getAttribute(self,rows,colums,target,Entropy):
        maxGainRatio = -1
        targetAttribute = -1

        for attribute in colums:

            splitinfo=self.getSepInfo(rows,attribute)
            if splitinfo>0:
                gainRatio=self.getGain(rows,target,Entropy,attribute)/splitinfo
                if gainRatio>maxGainRatio:
                    maxGainRatio=gainRatio
                    targetAttribute=attribute


        return targetAttribute



    def getSepInfo(self,rows,AttributeChosen):
        count=len(rows)
        s0=0
        for i in rows:
            if self.data[i][AttributeChosen]==0:
                s0+=1

        p0=1.0*s0/count
        p1=1-p0
        if p0==0 or p1==0:
            return 0

        return -(p0*math.log(p0,2)+p1*math.log(p1,2))

    def getGain(self,rows,target,Entropy,Attribute):
        count=len(rows)
        branch=self.Separate(rows,target,Attribute)
        e1 = self.getEntropy(branch[0][0],branch[0][1])
        e2 = self.getEntropy(branch[1][0], branch[1][1])

        p1=1.0*len(branch[0][0])/count
        p2=1-p1

        Gain=Entropy-p1*e1-p2*e2
        return Gain

    def Separate(self,rows,target,AttributeChosen):
        new_rows0 = []
        new_rows1 = []
        new_target0 = []
        new_target1 = []

        for i in range(len(rows)):
            if self.data[rows[i]][AttributeChosen]==0:
                new_rows0.append(rows[i])
                new_target0.append(target[i])
            else:
                new_rows1.append(rows[i])
                new_target1.append(target[i])
        return [(new_rows0,new_target0), (new_rows1,new_target1)]



    def getEntropy(self,rows,target):
        num=len(rows)
        count=0
        for i in range(len(rows)):
            if target[i]==1:
                count+=1
        pos=1.0*count/num
        neg=1-pos
        if pos == 0 or neg == 0:
            return 0
        return - (pos * math.log(pos, 2) + neg * math.log(neg, 2))

    def getMostCommon(self,target):
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

    def TreePrint(self,node,count):
        if node==None:
            return
        string = ''
        dep=''
        if count>0:
            for i in range(count):
                dep+='|'
        if node.val > -1:
            curattr = self.attributeNames[node.val]
            string = dep+ curattr + '=0:'
            if node.left.val>0:
                print string
                self.TreePrint(node.left,count+1)
            else:
                string+=str(node.left.label)
                print string

            string = dep+ curattr + '=1:'
            if node.right.val>0:
                print string
                self.TreePrint(node.right,count+1)
            else:
                string+=str(node.right.label)
                print string



