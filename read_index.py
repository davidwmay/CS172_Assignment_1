# This file should contain code to receive either a document-id or word or both and output the required metrics. See the assignment description for more detail.
import re
import os
import zipfile
import sys
from parsing import get_term_key
from parsing import get_term_val
from parsing import get_main_key
from parsing import get_main_val
from parsing import get_doc_key
from parsing import get_doc_val
from parsing import get_map
from parsing import get_termInfo

term_key_list = get_term_key()
term_val_list = get_term_val()

main_key_list = get_main_key()
main_val_list = get_main_val()

doc_key_list = get_doc_key()
doc_val_list = get_doc_val()

map = get_map()

termInfo = get_termInfo()

# FIXME: throwing error on correct --term and --doc query
# if len(sys.argv) != (3 or 5): 
#     raise ValueError('Please provide a query, either --term TERM or --doc DOCNAME or both.')

# FIXME: print distinct terms (optional), auto-uppercase the document argument
if sys.argv[1] == '--doc' and len(sys.argv) <= 2:
    print("Listing for document: ", sys.argv[2])
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

# FIXME: stem term
elif sys.argv[1] == '--term' and len(sys.argv) <= 2:
    print("Listing for term: ", sys.argv[2])
    termID = 0
    for term in term_val_list:
        if(sys.argv[2] == term):
            position = term_val_list.index(term)
            termID = term_key_list[position]
    print("TERMID: ", termID)
    # print(termInfo[termID])
    print("Number of documents containing term: ", termInfo[termID][0][1])
    print("Term frequency in corpus: ", termInfo[termID][0][0])

# FIXME: auto-uppercase doc argument, create valuerror outputs for incorrect inputs
elif (sys.argv[1] == '--doc' and sys.argv[3] == '--term') or (sys.argv[1] == '--term' and sys.argv[3] == '--doc'):
    if sys.argv[1] == '--doc' and sys.argv[3] == '--term':
        print("Please put your query in the order --term TERM --doc DOCNAME")
        sys.exit()
    termID = 0 
    docID = 0
    print("Listing for term: ", sys.argv[2])
    print("In document: ", sys.argv[4])
    for term in term_val_list:
        if(sys.argv[2] == term):
            position = term_val_list.index(term)
            termID = term_key_list[position]
    print("TERMID: ", termID)
    for docname in doc_val_list:
        if sys.argv[4] == docname:
            position = doc_val_list.index(docname)
            docID = doc_key_list[position]
    print("DOCID: ", docID)

    smallList = termInfo[termID][0][2].items()
    # FIXME: not sure if this works, finds matching key to docID and puts the key and value in that dictionary entry into a tuple
    for key,freq in smallList:
       if key == docID:
           newTuple = (key,freq)
    # print(newTuple)

    print("Term frequency in document: ", newTuple[1][0])
    print("Positions: ", newTuple[1][1])