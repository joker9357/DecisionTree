import csv
class CsvParser:
    def __init__(self,filename):

        self.data=[]
        with open(filename,'rb') as csvfile:
            csvreader=csv.reader(csvfile,delimiter=',')
            count=0
            for row in csvreader:
                if count==0:
                    self.attributeName=row[:-1]
                else:
                    self.data.append([int(i) for i in row])
                count+=1

        self.colums = range(len(self.attributeName))
        self.rows = range(len(self.data))
        self.target = [row[-1] for row in self.data]
