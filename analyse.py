import csv
import heapq #use two heaps to calculate percentile quickly
import re #check if input is formatted right
import sys #quit if something aren't right
import decimal #for accurate rounding
decimal.getcontext().rounding = decimal.ROUND_HALF_UP

percentile_file = open("percentile.txt", "r")

class moneyCounter:
    #used to record sum, count and output percentile for each unique combination of candidate, zip and year
    try:
        percentile = int(percentile_file.read()) #static
    except ValueError as error:
        sys.exit("percentile file has non digit characters")
    def __init__ (self):
        self.sum = decimal.Decimal("0")
        self.count = 0
        self.lower = []
        self.upper = []
        
    def insert (self, amount):
        self.sum += amount
        self.count+=1
        #smallest element of upper should be our percentile, it will not exist if percentile is 100
        if (moneyCounter.percentile == 100):
            heapq.heappush(self.lower, -amount)
            return
        if (self.count == 1 or amount>=self.upper[0]): #see if it fits into upper or lower
            heapq.heappush(self.upper, amount)
        else:
            heapq.heappush(self.lower, -amount)
        #next see if we need to resize lower and upper, adding one element will at most increase the size of lower by one
        if (len(self.lower)>(self.count*moneyCounter.percentile)//100):
            heapq.heappush(self.upper, -self.lower[0])
            heapq.heappop(self.lower)
        elif (len(self.lower)<(self.count*moneyCounter.percentile)//100):
            heapq.heappush(self.lower, -self.upper[0])
            heapq.heappop(self.upper)
        if (len(self.lower)!=(self.count*moneyCounter.percentile)//100):
            raise ValueError('The length is not right after resizing one time')
    
    def output(self, writer, candidate, zipcode, year):
    #write value to disk, shouldn't do it here cause it violates OOP principles. But convenient
        value = -self.lower[0] if moneyCounter.percentile==100 else self.upper[0] # I really miss value = conditon?true:false
        writer.writerow([candidate, zipcode, year, round(value, 0), round(self.sum, 0), self.count])


donor_namezip = {} #matches name and zip against earliest contrib year, used to check for repeat contribs
can_idzipyear = {} #matches candidate, zip and year to their respective records

datafile = open("itcont.txt", "r")
datareader = csv.reader(datafile, delimiter = '|')
outputfile = open("repeat_donors.txt", "w")
writer = csv.writer(outputfile, delimiter = '|')
name_checker = re.compile(r'^[a-zA-Z ]+,[a-zA-Z ]+$')
zip_checker = re.compile(r'^\d{5,9}$')
date_checker = re.compile(r'^\d{8}$')

for row in datareader:
    try:
        donorname = row[7]
        donorzip = row[10]
        other_id = row[15]
        date = row[13]
        recipient = row[0]
        amount = row[14]
    except IndexError as error:
        continue #we probably met an unexpected /n
    if (name_checker.search(donorname) == None or zip_checker.search(donorzip) == None or other_id or date_checker.search(date) == None or len(recipient)==0):
        continue
    try: 
        amount = decimal.Decimal(amount)
    except decimal.InvalidOperation as error:
        continue
    year = date[4:8]
    if year<"2000" or year>"2018":
        continue
    if amount<0:
        continue #should I ignore negative?
    #Finally made it through input check, now check repeat
    namezip = donorname+donorzip[0:5]
    if namezip in donor_namezip and donor_namezip[namezip]<year:
        #we got a repeat, now pick the candidate
        idzipyear = recipient+donorzip[0:5]+year
        if idzipyear not in can_idzipyear:
            can_idzipyear[idzipyear] = moneyCounter()
        can_idzipyear[idzipyear].insert(amount)
        can_idzipyear[idzipyear].output(writer, recipient, donorzip[0:5], year)
    else:
        donor_namezip[namezip]=year

#cleanup
percentile_file.close()
datafile.close()
outputfile.close()
