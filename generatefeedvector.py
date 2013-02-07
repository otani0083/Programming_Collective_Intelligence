#coding:utf-8
import feedparser
import re 
import MeCab

def extractNouns(text):#文字列から名詞を取り出して配列で返す関数
    tagger = MeCab.Tagger('-Ochasen')
    encoded_text = text.encode('utf-8')
    node = tagger.parseToNode(encoded_text)
    nouns= []
    while node:
        if node.posid >=36 and node.posid <=60:
            nouns.append(node.surface)
        node = node.next
    return nouns

def getwordcounts(url):#
    d=feedparser.parse(url)    
    wc={}
    for e in d.entries:
        if 'summary' in e: summary=e.summary
        else: summary=e.description
        words=getwords(e.title+' '+summary)
        for word in words:
            wc.setdefault(word,0)
            wc[word]+=1
        return d.feed.title,wc


def getwords(html):
    txt=re.compile(r'<[^>]+>').sub('',html)
    words=extractNouns(txt)
    return words

apcount={}
wordcounts={}
feedlist=[line for line in file('feedlist.txt')]
for feedurl in feedlist:
    try:
        title,wc=getwordcounts(feedurl)
        wordcounts[title]=wc
        for word,count in wc.items():
            apcount.setdefault(word,0)
            if count>1:
                apcount[word]+=1
    except:
        print 'Failed to parse feed %s' %feedurl

wordlist=[]
for w,bc in apcount.items():
    frac=float(bc)/len(feedlist)
    if frac>0.01 and frac<0.99: wordlist.append(w)

out=file('blogdata.txt','w')
out.write('Blog')
for word in wordlist: out.write('\t%s' % word)
out.write('\n')
for blog,wc in wordcounts.items():
    out.write(blog)
    for word in wordlist:
        if word in wc: out.write('\t%d' % wc[word])
        else: out.write('\t0')
    out.write('\n')