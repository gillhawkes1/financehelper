#TO DO
    #change self.groceriesKeys from list to self.purchaseKeys.grocery. 
    #ensure you can iterate correctly on list to dictionary change in groceries()



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
import time
from datetime import datetime

class banking():
    testfile = '/Users/gillhawkes1/Documents/cc/ccstatement.csv'
    shorttestfile = '/Users/gillhawkes1/Documents/cc/ccstatement2.csv'
    mypath = '/Users/gillhawkes1/Documents/cc/'

    #
    tasks = ['Calculate Groceries','Calculate Utilities','Greet','Calculate Expenses','Other']

    #nested dictionary for all locations, built into different default groups for calculating spending
    #key-values are only for searching through csv files-displaying messages to user
    #accessing by: self.purchaseKeys['grocery']['aldi'] would == 'Aldi'
    purchaseKeys = {
        'grocery': {'aldi':'Aldi','publix':'Publix','trader':"Trader Joe's",'foods':"Lowe's Foods"},
        'drink': {'brewery','brewing'},
        'medical': {'dermatology'},
        'gas' : {'eleven':'7-Eleven','exxon':'Exxon','bp':'BP','shell':'Shell'},
        'subs': {'netflix'},
        'shopping': {'target','Target'},
        'utilities': {'water'}
    }
    groceriesKeys = ['aldi','publix']


    #get a unique list of locations from a file and return the top occurring words
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

    #may need to delete this as i don't use it anymore
    #could come up with a new way of doing this?
    #it was supposed to be for parsing order numbers appended to end of amazon orders 
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

    def parseDates(self,file):
        format = ''
        fname = os.path.basename(file)
        fname = os.path.splitext(fname)[0]
        

        #myformat = '%Y-%m-%d'
        #newformat = '%d %B, %Y'
        #dateobj = datetime.strptime(mydate,myformat).strftime(newformat)

        #get formatting from file name
        if 'ally' in fname:
            format = '%Y-%m-%d'
            filecols = ['Date', 'Time', 'Amount', 'Type', 'Description']
            file = pd.read_csv(file,names=filecols,usecols=filecols,header=0,parse_dates={'date':['Date']})
            #file['Datet'] = pd.to_datetime(file.Date,infer_datetime_format=False)
            print(file)
            mydatecol = 'Date'
        elif 'wells' in fname:
            format = '%m/%d/%Y'
            colnames = ['date','amt','star','NaN','location']
        elif 'secu' in fname:
            format = ''
        elif 'discover' in fname:
            format = ''
        else:
            print('File does not specify where it was downloaded from.')
            return False
        myformat = '%d %B, %Y'
        #for i,j in file.iterrows():
            #thisdate = datetime.strptime(j[mydatecol],format).strftime(myformat)
            #print(j.date)

            #mydate = '2022-03-25'
            #myformat = '%Y-%m-%d'
            #newformat = '%d %B, %Y'
            #dateobj = datetime.strptime(mydate,myformat).strftime(newformat)
            #print(dateobj)

        
    #get the most recent edited/downloaded csv file. will work as long as an older file is not edited
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
            
    #get a file, and make sure it exists
    def getFile(self,filename):
        fpath = self.mypath+filename+'.csv'
        return pd.read_csv(fpath) if os.path.isfile(fpath) else False

    #perform the grocery task for spending
    def groceries(self):
        print('---------------------------------------------')
        print('Your current grocery keys are: [' + ', '.join(self.groceriesKeys) + ']')
        print('Would you like to add any keys to search for? y/n')
        morekeys = input()
        if morekeys.lower() == 'y':
            print('Type your additional key(s) separated by a comma.')
            mykeywords = input()
            if ',' in mykeywords:
                mykeywords = mykeywords.lower().split(',')
                mykeywords = [i.lstrip() for i in mykeywords]

                self.groceriesKeys += mykeywords
            else:

                self.groceriesKeys.append(mykeywords)
        else:
            mykeywords = self.groceriesKeys

        myfile = self.getRecent()
        print('Detected the most recent file as: '+ myfile)
        print('Run this file? y/n')
        runfile = input()
        while runfile not in ('y','n'):
            util.clear()
            print('----------------------------------')
            print('You must type a y/n response. Please try again.')
            time.sleep(1)
            print('----------------------------------')
            print('Detected the most recent file as: '+ myfile)
            print('Run this file (y) or pick another file (n) y/n')
            runfile = input()
        if runfile == 'n':
            print('The current file path is ' + self.mypath)
            time.sleep(1)
            print('Files in this path (please choose one):')
            cc_files = glob.glob(self.mypath + '*.csv')
            files_nopath = []
            for file in cc_files:
                fname = os.path.basename(file)
                fname = os.path.splitext(fname)[0]
                files_nopath.append(fname)
            print(files_nopath)
            newfile = input() + '.csv'
            while os.path.isfile(self.mypath + newfile) == False:
                print('Please type a valid file. Choose from this list:')
                print(files_nopath)
                newfile = input() + '.csv'
            if newfile:
                print('newfile has been selected: '+ newfile)
                #myfile = newfile
                myfile = '/Users/gillhawkes1/Documents/cc/'+newfile
            
        headerList = ['date','amt','star','NaN','location']
        myfile = pd.read_csv(myfile,names=headerList,usecols=['date','amt','location'])
        total = 0

        #datetime.strptime(d1, "%Y-%m-%d")
        mindate = datetime.strptime(min(myfile.date),'%m/%d/%Y')
        maxdate = datetime.strptime(max(myfile.date),'%m/%d/%Y')
        dayspan = abs(maxdate-mindate).days
        weeks = round(dayspan/7,1)
        print(weeks)
        
        

        for i,j in myfile.iterrows():
            j.amt = abs(j.amt)
            j.location = j.location.lower()

            if re.search('|'.join(self.groceriesKeys),j.location):
                total += j.amt
        print('----------------------------------')
        print('Your total spending for this file for [' + ','.join(self.groceriesKeys) + '] is: ')
        print('$' + str(round(total,2)))
        print('You spent an average of $' + str(round(total/weeks,2)) + ' per week, over a span of ' + str(weeks) + ' weeks on groceries.')

    def utilities(self):
        recentfile = self.getRecent()
        rfile = pd.read_csv(recentfile)
        self.parseDates(recentfile)

    #calculate spending from a list of your choosing
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

    #ask user what task they would like to perform from a numbered list
    def callTask(self):
        print('----------------------------------')
        print('What would you like to do? Type the number and press enter.')
        for t in self.tasks:
            i = self.tasks.index(t)+1
            print(str(i)+'. '+t)
        res = input('number: ')
        res = int(res)-1
        return res

    #from a list of tasks
    def doTask(self,task):
        if task == 'Calculate Groceries':
            self.groceries()
        elif task == 'Calculate Utilities':
            self.utilities()
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
        util.clear()
        chosentask = self.callTask()
        while chosentask >= len(self.tasks):
            util.clear()
            print('----------------------------------')
            print('You must type a number in range. Please try again.')
            time.sleep(2)
            return self.main()
        else:
            chosentask = self.tasks[chosentask]

        self.doTask(chosentask)

    


#-------------------------------------------------------------------------#

test = banking()
test.main()
#print(test.readLocations(test.testfile))
