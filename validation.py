from csvparser import CsvParser

class Validator:
    def __init__(self,filename):
        csvparser=CsvParser(filename)
        self.data=csvparser.data


        #print "finish construct validator"

    def validation(self,root):
        if root==None or self.data==None:
            return 0

        count=0
        #print "begin validation"
        for i in range(len(self.data)):
            node =root
            instance =self.data[i]
            while node.val!=-1:
                if instance[node.val]==0:
                    node=node.left
                else:
                    node=node.right

            if node.label==instance[-1]:
                count+=1

        self.accuracy=1.0*count/len(self.data)
        print self.accuracy
