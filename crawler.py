import urllib2
import sys
import re
from HTMLParser import HTMLParser

def loaderUrl(url):
    try:
        content = urllib2.urlopen(url).read()
        #print content
        return content
    except urllib2.HTTPError:
        print "Unable to connect web"
        return False
def parserStockq(content):
    for a in list(re.finditer("USD",content)):
        line = content[a.start()-5:a.end()+60]
        if not "/USD.php" in line:
            if "USD" in line:
                end=line.find(".php")
                print line[end-6:end]
    return

class parserCurrency(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.matchdata = False
        self.matchgold = False
        self.matchcountry = False
        self.lasttag = None
        self.lastcountry = None
        self.currencydict = {}

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for name, value in attrs:
                if name == 'href' and "/commodity/COMMGOLD.php" in value:
                    self.matchgold = True

                if name == 'href' and "USD" in value and not "/USD.php" in value:
                    end=value.find(".php")
                    #print value[end-6:end]
                    self.lastcountry = value[end-6:end]
                    self.matchdata = True
        self.lasttag = tag

    def handle_data(self, data):
        if self.lasttag == 'td':
            if self.matchgold and data.strip():
                # USD equal to how much gold (mg)
                self.currencydict["USD"] = 1/float(data) * 1000000
                #print ("USD", self.currencydict["USD"])
                self.matchgold = False

            if self.matchdata and data.strip():
                if self.lastcountry.find("USD") == 0:
                    self.currencydict[self.lastcountry[3:]] = self.currencydict["USD"]/float(data)
                    #print (self.lastcountry[3:],self.currencydict[self.lastcountry[3:]])
                else:
                    self.currencydict[self.lastcountry[:3]] = self.currencydict["USD"]*float(data)
                    #print (self.lastcountry[:3],self.currencydict[self.lastcountry[:3]])
                self.matchdata = False

#content = loaderUrl("http://www.stockq.org/")
content = open("stockq.html",'rb').read()

parser = parserCurrency()
parser.feed(content)
parser.close()
currencydict = parser.currencydict
print currencydict
#parserStockq(content)