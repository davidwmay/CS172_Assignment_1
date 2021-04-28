import re
import os
import zipfile
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd

# Regular expressions to extract data from the corpus
doc_regex = re.compile("<DOC>.*?</DOC>", re.DOTALL)
docno_regex = re.compile("<DOCNO>.*?</DOCNO>")
text_regex = re.compile("<TEXT>.*?</TEXT>", re.DOTALL)


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
        
        for document in result[0:]:
            # Retrieve contents of DOCNO tag
            docno = re.findall(docno_regex, document)[0].replace("<DOCNO>", "").replace("</DOCNO>", "").strip()
            # Retrieve contents of TEXT tag
            text = "".join(re.findall(text_regex, document))\
                      .replace("<TEXT>", "").replace("</TEXT>", "")\
                      .replace("\n", " ")

            # Vectorizer creates a dataframe counting frequency of each word
            vectorizer = CountVectorizer(lowercase=True, stop_words=stopwords)
            matrix = vectorizer.fit_transform([text])
            df = pd.DataFrame(matrix.toarray(), columns=vectorizer.get_feature_names())
            # print(df)

            # step 1 - lower-case words, remove punctuation, remove stop-words, etc. 
            text = text.lower()
            # Regex removes punctuation
            text = re.sub(r'[^\w\s]','',text)
            text = text.split()
            # Nested loops removes stop-words
            for term in stopwords:
                for word in text:
                    if word == term:
                        text.remove(word)

            print(text)


            

            # step 2 - create tokens 

            # step 3 - build index
            