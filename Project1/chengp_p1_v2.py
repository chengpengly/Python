import string
import re
def main():
    dict={}
    title=''
# read file
    file_grimms=open("grimms.txt","r")
    file_stopwords=open("stopwords.txt","r")
    lines=file_grimms.readlines()
    stopwords_=stopwords(file_stopwords)
    count=0
#create dictionary
    for line_num in range(123,9183):
         if re.match(r'^[A-Z]+[^a-z0-9]*$',lines[line_num]):
                title=lines[line_num].strip()
         else:
            words=remove_punctuation_lower(lines[line_num])
            for word in words:
                if word not in stopwords_ and word != '':
                     dict.setdefault(word,{}).setdefault(title,[]).append(line_num+1)
#Search query
    query=input("Please enter your query:")
    while query!="q quit":
       print("query =", query)
       search(query,dict,lines)
       query = input("Please enter your query:")
    exit()


#close file
    file_stopwords.close()
    file_grimms.close()

#remove punctuation and lower words
def remove_punctuation_lower(line):
    clean_words=[]
    line=line.strip()
    words=line.split()
    for word in words:
        item=re.sub(r'[^a-zA-Z0-9]','',word).lower()
        clean_words.append(item)
    return clean_words
# get stopwords list
def stopwords(file_stopwords):
    file_stopword=file_stopwords.readlines()
    stopwords=[]
    for line in file_stopword:
        stopwords.append(line.strip())
    return stopwords

#search query function
def search(query,dict,lines):
    #get the number of words
    query=query.split()
    number_words=len(query)
    if "or" in query:
       results_or(query,dict,lines)

    #only have one word
    elif number_words==1:
       results_oneword(query[0],dict,lines)
    elif "and" in query or number_words==2:
      search_and(query,dict,lines)
    else:
        search_contain_words(query,dict,lines)

# highlight the keyword
def highlight(line,key):
   line=remove_punctuation_lower(line)
   for word in line:
       if word==key:
           print("**",word.upper(),"**",end=" ")
       else:
           print(word,end=" ")

#display the results when query only contains one word
def results_oneword(keyword,dict,lines):
        results = dict.get(keyword, 0)
        if results == 0:
            print("\t--")
        else:
            for (k, v) in results.items():
                print("\t", k)
                for line in v:
                    print("\t\t", line, end=" ")
                    highlight(lines[line - 1], keyword)
                    print()

# display the results when query contains or
def results_or(keyword,dict,lines):
   results1=dict.setdefault(keyword[0],{})
   results2=dict.setdefault(keyword[2],{})

   for (k,v ) in results1.items():
       flag=True
       for(k2,v2) in results2.items():
            if k==k2:
                print("\t",k)
                print("\t",keyword[0])
                for line in v:
                    print("\t\t", line, end=" ")
                    highlight(lines[line - 1], keyword[0])
                    print()
                print("\t",keyword[2])
                for line in v2:
                    print("\t\t", line, end=" ")
                    highlight(lines[line - 1], keyword[2])
                    print()
                flag=False
                break;
       if flag:
           print("\t", k)
           print("\t", keyword[0])
           for line in v:
               print("\t\t", line, end=" ")
               highlight(lines[line - 1], keyword[0])
               print()
           print("\t", keyword[2])
           print("\t\t--")

   for(k2,v2) in results2.items():
       list_keys=list(results1.keys())
       if k2 not in list_keys:
           print("\t", k2)
           print("\t", keyword[2])
           for line in v2:
               print("\t\t", line, end=" ")
               highlight(lines[line - 1], keyword[2])
               print()
           print("\t",keyword[0])
           print("\t\t--")

# query has and or query length ==2
def search_and(keyword,dict,lines):
    flag=True
    if(len(keyword)==2):
        results1 = dict.setdefault(keyword[0], {})
        results2 = dict.setdefault(keyword[1], {})
        for (k, v) in results1.items():
            flag=True
            for (k2, v2) in results2.items():
                if k == k2:
                    print("\t", k)
                    print("\t", keyword[0])
                    for line in v:
                        print("\t\t", line, end=" ")
                        highlight(lines[line - 1], keyword[0])
                        print()
                    print("\t", keyword[1])
                    for line in v2:
                        print("\t\t", line, end=" ")
                        highlight(lines[line - 1], keyword[1])
                        print()
                    flag = False
        if flag:
               print("\t--")
    else:
        results1 = dict.setdefault(keyword[0], {})
        results2 = dict.setdefault(keyword[2], {})

        for (k, v) in results1.items():
            flag = True
            for (k2, v2) in results2.items():
                if k == k2:
                    print("\t", k)
                    print("\t", keyword[0])
                    for line in v:
                        print("\t\t", line, end=" ")
                        highlight(lines[line - 1], keyword[0])
                        print()
                    print("\t", keyword[2])
                    for line in v2:
                        print("\t\t", line, end=" ")
                        highlight(lines[line - 1], keyword[2])
                        print()
                    flag = False
        if flag:
            print("\t--")
#query must contain multiple words
def search_contain_words(keyword,dict,lines):
   title=set()
   title_final_set=set()
   for num in range(len(keyword)):
       if num==0:
           title_final_set=set(dict.setdefault(keyword[0],{}))
       else:
           results=dict.setdefault(keyword[num],{})
           title=set(results)
           title_final_set=title_final_set.intersection(title)
   for title in title_final_set:
       print("\t",title)
       for word in keyword:
          lines_title=dict.get(word).get(title)
          for line in lines_title:
              print("\t\t", line, end=" ")
              highlight(lines[line - 1], word)
              print()

   if len(title_final_set)==0:
       print("\t--")


main()



