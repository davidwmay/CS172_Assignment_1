# This file should contain code to receive either a document-id or word or both and output the required metrics. See the assignment description for more detail.
import re
import os
import zipfile
import sys
from parsing import get_main_key
from parsing import get_main_val
from parsing import get_doc_key
from parsing import get_doc_val
from parsing import get_map

main_key_list = get_main_key()
main_val_list = get_main_val()

doc_key_list = get_doc_key()
doc_val_list = get_doc_val()

map = get_map()

if len(sys.argv) != (3 or 5): 
    raise ValueError('Please provide a query, either --doc DOCNAME or --term TERM or both.')

if sys.argv[1] == '--doc':
    print("Listing for document: ", sys.argv[2])
    #FIXME: print distinct terms (optional)
    docID = 0
    termCount = 0
    for docname in doc_val_list:
        if sys.argv[2] == docname:
            position = doc_val_list.index(docname)
            docID = doc_key_list[position]
    print("DOCID: ", docID)

    for entry in map:
        if entry[1] == docID:
            termCount += 1 
    print("Total terms: ", termCount)

elif sys.argv[1] == '--term':
    print("Listing for term: ", sys.argv[2])
    #FIXME: print termID, num of docs containing term, term frequency 
    

elif (sys.argv[1] == '--doc' and sys.argv[3] == '--term') or (sys.argv[1] == '--term' and sys.argv[3] == '--doc'):
    print("test")
