import math
import random
import copy
from collections import deque
from csvparser import CsvParser
from validation import Validator

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
        self.root=self.ID3(self.colums,self.rows)

    def ID3(self,colums,rows):
        if len(rows)==0:
            return None
        node=TreeNode(-1)
        #print(len(colums))

        Entropy=self.getEntropy(rows)
        node.label=self.getMostCommon(rows)

        if Entropy==0 or len(colums)==0:
            return node

        else:
            AttributeChosen=self.getAttribute(rows,colums,Entropy)
            if AttributeChosen==-1:
                return node
            node.val=AttributeChosen
            #print(AttributeChosen)

            newAttributes = []
            for attribute in colums:
                if attribute != AttributeChosen:
                    newAttributes.append(attribute)
            colums = newAttributes

            branch=self.Separate(rows,AttributeChosen)
            node.left=self.ID3(colums,branch[0])
            node.right = self.ID3(colums, branch[1])

            return node



    def getAttribute(self,rows,colums,Entropy):
        maxGainRatio = -1
        targetAttribute = -1

        for attribute in colums:

            splitinfo=self.getSepInfo(rows,attribute)
            if splitinfo>0:
                gainRatio=self.getGain(rows,Entropy,attribute)/splitinfo
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

    def getGain(self,rows,Entropy,Attribute):
        count=len(rows)
        branch=self.Separate(rows,Attribute)
        e1 = self.getEntropy(branch[0])
        e2 = self.getEntropy(branch[1])

        p1=1.0*len(branch[0])/count
        p2=1-p1

        Gain=Entropy-p1*e1-p2*e2
        return Gain

    def Separate(self,rows,AttributeChosen):
        new_rows0 = []
        new_rows1 = []

        for i in rows:
            if self.data[i][AttributeChosen]==0:
                new_rows0.append(i)

            else:
                new_rows1.append(i)

        return [new_rows0,new_rows1]



    def getEntropy(self,rows):
        num=len(rows)
        count=0
        for i in rows:
            if self.data[i][-1]==1:
                count+=1
        pos=1.0*count/num
        neg=1-pos
        if pos == 0 or neg == 0:
            return 0
        return - (pos * math.log(pos, 2) + neg * math.log(neg, 2))

    def getMostCommon(self,rows):
        if len(rows)==1:
            return self.data[rows[0]][-1]
        count = 0
        for i in rows:
            if self.data[i][-1]==1:
                count += 1
        if count>=len(rows)/2:
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



