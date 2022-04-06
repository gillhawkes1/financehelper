
from ensurepip import version
import numpy
import pandas as pd
import glob
import os
import sys
import re
from threading import Timer
from difflib import SequenceMatcher
import operator
import util

class banking():
    testfile = '/Users/gillhawkes1/Documents/cc/ccstatement.csv'
    shorttestfile = '/Users/gillhawkes1/Documents/cc/ccstatement2.csv'
    mypath = '/Users/gillhawkes1/Documents/cc/'
    tasks = ['Calculate Groceries','Greet','Calculate Expenses','Other']

    purchaseKeys = {
        'grocery': {'aldi', 'publix', 'trader', 'foods'},
        'drink': {'brewery','brewing'},
        'medical': {'dermatology'},
        'gas' : {'eleven','exxon','bp','shell'},
        'subs': {'netflix'},
        'shopping': {'target'}
    }
    groceriesKeys = ['aldi','publix']


    def readLocations(self,myfile):
        headerList = ['date','amt','star','NaN','location']
        myfile = pd.read_csv(myfile,names=headerList,usecols=['date','amt','location'])
        locations = myfile['location'].tolist()
        locwords = []
        for loc in locations:
            lsplit = loc.split()
            for l in lsplit:
                locwords.append(l)
        #aldis = { i:locwords.count(i) for i in locwords if i.lower() == 'aldi' }
        locwords = { i:locwords.count(i) for i in locwords if len(i) > 3 }
        locwords = dict(sorted(locwords.items(), key=lambda item: item[1],reverse=True))
        print(locwords)
        #return self.parseLocations(locwords)

    def parseLocations(self,locations):
        substr_cts={}
        for i in range(0, len(locations)):
            for j in range(i+1,len(locations)):
                loc1 = locations[i]
                loc2 = locations[j]
                match = SequenceMatcher(lambda x: x in ' ', loc1, loc2).find_longest_match(0, len(loc1), 0, len(loc2))
                substr_match=loc1[match.a:match.a+match.size]
                if len(substr_match) > 3:
                    if(substr_match not in substr_cts):
                        substr_cts[substr_match]=1
                    else:
                        substr_cts[substr_match]+=1
        substr_cts = dict(sorted(substr_cts.items(), key=lambda item: item[1],reverse=True))
        return substr_cts
        
    def getRecent(self):
        hasfiles = os.listdir(self.mypath)
        if len(hasfiles) > 0:
            cc_files = glob.glob(self.mypath + '*.csv')
        else:
            print(self.mypath + ' has no files.')
            return False
        
        if not cc_files:
            print('Directory empty. Please download a .csv file into the directory: ' + self.mypath)
            return False
        else:
            recent_file = max(cc_files,key=os.path.getctime)
            return recent_file
            
    def getFile(self,filename):
        fpath = '/Users/gillhawkes1/Documents/cc/'+filename+'.csv'
        return pd.read_csv(fpath) if os.path.isfile(fpath) else False

    def groceries(self):
        print('---------------------------------------------')
        print('Your current grocery keys are: [' + ', '.join(self.groceriesKeys) + ']')
        print('Would you like to add any keys to search for? y/n')
        morekeys = input()
        if morekeys.lower() == 'y':
            print('Type your additional key(s) separated by a comma.')
            mykeywords = input()
            if len(mykeywords.lower().split(',')) > 1:
                mykeywords = mykeywords.lower().split(',')
                self.groceriesKeys += mykeywords
            else:
                self.groceriesKeys.append(mykeywords)
            print(self.groceriesKeys)

        myfile = self.getRecent()
        print('Detected the most recent file as: '+ myfile)
        print('Run this file? y/n')
        runfile = input()
        if runfile == 'n':
            print('Type the file name from path ' + self.mypath)
            newfile = input() + '.csv'
            while os.path.isfile(self.mypath + newfile) == False:
                print('Please type a valid file.')
                newfile = input() + '.csv'
        elif runfile == 'y':
            headerList = ['date','amt','star','NaN','location']
            myfile = pd.read_csv(myfile,names=headerList,usecols=['date','amt','location'])
            total = 0

            for i,j in myfile.iterrows():
                j.amt = abs(j.amt)
                j.location = j.location.lower()

                if re.search('|'.join(mykeywords),j.location):
                    total += j.amt
            print('----------------------------------')
            print('Your total spending for this file for [' + ','.join(mykeywords) + '] is: ')
            print('$' + total)


        else:
            print('Please enter either y/n. Would you like to run this file?')


    def calcFromList(self,myfile,keywords=[],dateRange=False):
        headerList = ['date','amt','star','NaN','location']
        myfile = pd.read_csv(myfile,names=headerList,usecols=['date','amt','location'])
        total = 0

        for i,j in myfile.iterrows():
            j.amt = abs(j.amt)
            j.location = j.location.lower()

            if re.search('|'.join(keywords),j.location):
                total += j.amt
            #if(len(keywords) > 0):
            #    keyfound = keywords.find(j.location)
            #    if keyfound:
            #        print(j.location, j.amt)
        print('----------------------------------')
        print('Your total spending for this file for [' + ','.join(keywords) + '] is: ')
        #print('$'+total)
        print(total)

    def callTask(self):
        print('----------------------------------')
        print('What would you like to do? Type the number and press enter.')
        for t in self.tasks:
            i = self.tasks.index(t)+1
            print(str(i)+'. '+t)
        res = input('number: ')
        res = int(res)-1
        return res

    def doTask(self,task):
        if task == 'Calculate Groceries':
            self.groceries()
        elif task == 'Greet':
            self.greet()
        elif task == 'Calculate Expenses':
            myfile = self.getRecent()
            print('Is this the file you wish to choose: ' + myfile + '? y/n')
            choice = input()
            if choice == 'y':
                print('These are all of the keys listed for this file: ')
                uniquekeys = self.readLocations(myfile)
                print(uniquekeys)
                print('Please type your keys for calculation separated by commas:')
                searchkeys = input()
                searchkeys = searchkeys.lower().split(',')
            self.calcFromList()
        elif task == 'Other':
            print('other has not been written yet!')

    def greet(self):
        who = input('Who would you like to greet? ')
        print('Hello, ' + who.capitalize() + '!')

    def main(self):
        task = self.callTask()
        if task >= len(self.tasks):

            print('----------------------------------')
            print('You must type a number in range. Please try again.')
            return self.main()
        else:
            task = self.tasks[task]

        self.doTask(task)

    


#-------------------------------------------------------------------------#

test = banking()
#test.main()
print(test.readLocations(test.testfile))
