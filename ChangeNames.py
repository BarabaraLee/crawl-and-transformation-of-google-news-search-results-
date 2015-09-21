# -*- coding: utf-8 -*-
'''
from nltk import word_tokenize,pos_tag,ne_chunk
import re
text1="After his remarks Paul told reporters, 'It's not only the way that he has built them [casinos], but he's on record saying that the Kelo case, he's 100 percent for it. You won't find one conservative in America that knows what the Kelo case is and is for it. It is an anathema to those in the Tea Party. It is an anathema to those who are property rights advocates. And he say's he's 100 percent for it. Things like that will add up. Ultimately people will say that he can call people fat and stupid, but he also doesn't support property rights."
tokenized=word_tokenize(text1)
tagged=pos_tag(tokenized)
namedEnt=ne_chunk(tagged,binary=False)
entities=re.findall(r'PERSON\s(.*?)/',str(namedEnt))
entities
# The NER routine is not necessary for solving the problem
'''
import re
import urllib2
import pandas as pd

# The NameConvertTable() creates a table which includes the candiates' FirstName, 
# LastName, Year (of birth) and Female (most popular girl name)
def NameConvertTable(directory):
    fhand=urllib2.urlopen('https://en.wikipedia.org/wiki/Republican_Party_presidential_candidates,_2016')
    lines=[]
    names=[]
    dbirths=[]
    for line in fhand:
        a=line.strip()
        lines.append(a)
        regex1='<b><big><span class="sortkey">(.+?)</span>'
        pattern1=re.compile(regex1)
        name=re.findall(pattern1,a)
        regex2='<span style="white-space:nowrap">(.+?)</span><br />'
        pattern2=re.compile(regex2)
        dbirth=re.findall(pattern2,a)
        if(len(name)>=1):
            names.append(name[0])
        if(len(dbirth)>=1):
            dbirths.append(int(dbirth[0].split()[2]))
    dbirths=dbirths[:-4]
    names_df=pd.DataFrame(names,columns=['CandidName'])
    names_df['LastName']=map(lambda x:x.split(', ')[0],names)
    names_df['FirstName']=map(lambda x:x.split(', ')[1],names)
    del names_df['CandidName']
    names_df['Year']=pd.DataFrame(dbirths)
    babynames=pd.read_csv(directory+"1915-2014.csv")
    babynames=babynames.ix[:,0:2] #take the 'Year' and 'Rank1' columns
    babynames.columns=['Year','Female']
    filt=map(lambda x: x in list(names_df['Year']),list(babynames['Year']))
    baby_names=babynames[filt]
    #innor join the two names_df table and the baby_names table on 'Year'
    #which creates a code book with candidates' name and girls' name
    return names_df.merge(baby_names,how='inner')

# The ReplaceNames() replace candidates' name with their corresponding girl name.
#Table.ix[i,4] contains FullName
#Table.ix[i,0] contains LastName
#Table.ix[i,1] contains FirstName
#Table.ix[i,3] contains Female (most popular girl name of the year given by ix[i,2])
def ReplaceNames(directory,text1):
    Table=NameConvertTable(directory)
    Table['FullName']=map(lambda x,y:y+' '+x,list(Table['LastName']),list(Table['FirstName']))
    for i in range(len(Table)):
        text1=text1.replace(Table.ix[i,4],Table.ix[i,3]).replace(Table.ix[i,0],Table.ix[i,3]).replace(Table.ix[i,1],Table.ix[i,3])
    return text1.replace('Mary Perry','Rick Perry')

#The titles.txt file contains the url, title and content. This function extracts the titles.
def ExtractTitle(directory,titlefile):
    fp = open(directory+titlefile, 'r')
    titles=[]
    regex1='title\t-> (.+)'
    pattern1=re.compile(regex1)
    for line in fp:
        a=line.strip('\n')
        title=re.findall(pattern1,a)
        if (len(title)>0):
            a=title[0].replace('</b>','').replace('<b>','').replace('\xe2\x80\x9c','"').replace('\xe2\x80\x9d','"').replace('\xe2\x80\x93','-')
            titles.append(a)
    return titles

#The ReWriteTitles() executes the ExtractTitle() and ReplaceNames(), and output the rewritten titles into output.txt.
def ReWriteTitles(directory,titlefile):
    texts= ExtractTitle(directory,titlefile)
    string=''
    for i in range(len(texts)):
        string=string+str(i+1)+'. '+ReplaceNames(directory,texts[i])+'\n'
    with open(directory+"Output.txt", "w") as text_file:
        text_file.write("%s" % string)

if __name__ == "__main__":     
    ReWriteTitles('/Users/linjunli/Desktop/temp/Change Names/','titles.txt')