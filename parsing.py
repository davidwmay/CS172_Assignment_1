import re
import os
import zipfile
import sys

# Regular expressions to extract data from the corpus
doc_regex = re.compile("<DOC>.*?</DOC>", re.DOTALL)
docno_regex = re.compile("<DOCNO>.*?</DOCNO>")
text_regex = re.compile("<TEXT>.*?</TEXT>", re.DOTALL)
termIndexMap = {}
docIndexMap = {}
termIndexMapCount = 1
docIndexCount = 1
map = [] 
termInfo = {}


with zipfile.ZipFile("ap89_collection_small.zip", 'r') as zip_ref:
    zip_ref.extractall()
   
# Retrieve the names of all files to be indexed in folder ./ap89_collection_small of the current directory
for dir_path, dir_names, file_names in os.walk("ap89_collection_small"):
    allfiles = [os.path.join(dir_path, filename).replace("\\", "/") for filename in file_names if (filename != "readme" and filename != ".DS_Store")]
    
for file in allfiles:
    with open(file, 'r', encoding='ISO-8859-1') as f:
        filedata = f.read()
        result = re.findall(doc_regex, filedata)  # Match the <DOC> tags and fetch documents
        # Creates a list of stopwords
        stop_file = open("stopwords.txt", "r")
        temp_stopwords = stop_file.readlines()
        stopwords = []
        for word in temp_stopwords:
            stopwords.append(word.replace("\n", ""))

        stop_file.close()
        

        
        for document in result[0:3]:
            # Retrieve contents of DOCNO tag
            docno = re.findall(docno_regex, document)[0].replace("<DOCNO>", "").replace("</DOCNO>", "").strip()
            # print(docno)
            # if (docno != "AP890101-0001"): # FIXME FOR TESTING ONLY
            #     continue
            # Retrieve contents of TEXT tag
            text = "".join(re.findall(text_regex, document))\
                      .replace("<TEXT>", "").replace("</TEXT>", "")\
                      .replace("\n", " ")

            # step 1 - lower-case words, remove punctuation, remove stop-words, etc. 
            text = text.lower()
            # Regex removes punctuation
            text = re.sub(r'[^\w\s]','',text)
            text = text.split()
            # Nested loops remove stop-words
            for term in stopwords:
                for word in text:
                    if word == term:
                        text.remove(word)
            # print(text)

            # step 2 - create tokens 
            #Add document ID and name to docIndexMap
            docIndexMap[docIndexCount] = docno

            locationCount = 1
            for word in text:
                if word not in termIndexMap.values():
                    termIndexMap[termIndexMapCount] = word
                    termIndexMapCount += 1
            
                key_list = list(termIndexMap.keys())
                val_list = list(termIndexMap.values())
                position = val_list.index(word)
                newEntry = [key_list[position], docIndexCount, locationCount]
                locationCount += 1
                map.append(newEntry)

                # keyval = map[0][0]
                # print(termIndexMap[keyval])

            docIndexCount += 1 

            # print(map)
key_list = list(termIndexMap.keys())
val_list = list(termIndexMap.values())
        # Creates posting list for each term in map
for key in key_list:
    termInfo[key] = []
    tempDict = {}
    for entry in map:
        if entry[0] == key:
            if entry[1] not in tempDict:
                tempDict[entry[1]] = [1, [entry[2]]]
            else:
                frequency = tempDict[entry[1]][0]
                frequency += 1
                tempDict[entry[1]][0] = frequency
                tempDict[entry[1]][1].append(entry[2])
    termInfo[key].append(tempDict)
    print(termInfo[key])
        # step 3 - build index
