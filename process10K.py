# Please download the following libraries if you haven't
# pip install xml-python
# pip install bs4
# pip install numpy

import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from numpy import *
import re
import os

def tickerCheckProcessing(ticker, fileType, outputLocation):
# This function checks if the filing for the company is already processed
    if not os.path.exists(outputLocation):
        os.makedirs(outputLocation)
        return False
    existingFolders = os.listdir(outputLocation)
    if len(existingFolders) == 0: return False
    interestFolder = [x for x in existingFolders if x == ticker]
    if len(interestFolder) == 0: return False
    existingFiles = os.listdir(os.path.join(outputLocation, interestFolder[0]))
    curName = fileType + "_Risk_Factors"
    if curName in existingFiles: return True
    return False

def outputCompletedFiles(txtDict, fileType, ticker, outputLocation):
# This function writes the retrieved sections to designated location
    final_location = os.path.join(outputLocation, ticker, fileType + "_Risk_Factors")
    if not os.path.isdir(final_location):
        os.makedirs(final_location)
    for selection in txtDict.keys():
        text = txtDict[selection]
        fileName = os.path.join(final_location, selection + ".txt")
        textFile = open(fileName, 'w+')
        textFile.write(text)
        textFile.close()

def getCompanyNameAndTime(textString):
# This function gets the company name and filing date
    header = textString[re.search('<SEC-HEADER>', textString).start() : re.search('</SEC-HEADER>', textString).end()]
    name = header[re.search('COMPANY CONFORMED NAME:', header).end() : re.search('CENTRAL INDEX KEY:', header).start()].strip()
    name = re.sub('\.|\/|,', "", name.replace("\\", ""))
    period = header[re.search('CONFORMED PERIOD OF REPORT:', header).end() : re.search('FILED AS OF DATE:', header).start()].strip()
    return name, period

def getDocuments(raw, fileType):
# This function gets the document portion from the filing html
    # Find <DOCUMENT> tags
    doc_start_pattern = re.compile(r'<DOCUMENT>')
    doc_end_pattern = re.compile(r'</DOCUMENT>')

    doc_starts = [x.start() for x in doc_start_pattern.finditer(raw)]
    doc_ends = [x.end() for x in doc_end_pattern.finditer(raw)]

    # Find document type
    type_pattern = re.compile(r'<TYPE>')
    sequence_pattern = re.compile(r'<SEQUENCE>')
    type_starts = [x.end() for x in type_pattern.finditer(raw)]
    type_ends = [x.start() for x in sequence_pattern.finditer(raw)]

    # Find file name
    filename_pattern = re.compile(r'<FILENAME>')
    text_pattern = re.compile(r'<TEXT>')
    filename_starts = [x.end() for x in filename_pattern.finditer(raw)]
    filename_ends = [x.start() for x in text_pattern.finditer(raw)]

    doc10QK = ""
    documents = {}

    for type_start, type_end, filename_start, filename_end, doc_start, doc_end in \
        zip(type_starts, type_ends, filename_starts, filename_ends, doc_starts, doc_ends):
        doc_type = raw[type_start:type_end].strip()
        file_name = re.sub(r'<DESCRIPTION>', "", raw[filename_start:filename_end].strip()).split()[0]
        if (doc_type == fileType) & (re.search('risk factor', raw[doc_start:doc_end]) is not None):
            doc10QK = raw[doc_start:doc_end]
        documents[file_name] = raw[doc_start:doc_end]

    return doc10QK, documents


def cleanText(text):
# Some tags are not closed, they need to be removed or else beautiful soup won't work
# and parsing will not be successful
    text = re.sub(r'(\&\#[0-9]{3,4};)|(\&[a-z]{4};)', '', text)
    text = re.sub('(<br>)|(<br(\s)*>)', '\n', text)

    while True:
        if re.search(r'<[A-z]+:[A-z]+ ', text) == None: break
        s = re.search(r'<[A-z]+:[A-z]+ ', text).start()
        contentStart = s + re.search(r'>', text[s:]).end()
        contentEnd = contentStart + re.search(r'<', text[contentStart:]).start()
        e = contentEnd + re.search(r'>', text[contentEnd:]).end()
        text = text[:s] + text[contentStart:contentEnd] + text[e:]

    if re.search(r'</hr>', text) == None:
        while True:
            if re.search(r'<hr', text) == None: break
            s = re.search(r'<hr', text).start()
            e = s + re.search(r'>', text[s:]).end()
            text = text[:s] + text[e:]

    while True:
        if re.search(r'<img', text) == None: break
        s = re.search(r'<img', text).start()
        e = s + re.search(r'>', text[s:]).end()
        text = text[:s] + text[e:]

    if re.search(r'<a', text) == None: text = re.sub("</a>", "", text)
    return text

def treeToText(tree):
# Iteratively extract text from nodes in html tree, a newline is added after certain
# punctuation marks
    textList = []
    for child in tree:
        line = ''.join(list(child.itertext())).strip()
        line = ' '.join(line.split())
        if line != None and len(line) > 10:
            if re.search('[:punct:]', line.strip()[-1]) is None and len(line) < 100 and re.search('[a-z]', line[0]) is None:
                textList.append("\n\n" + line + '\n\n')
            else:
                if line.strip()[-1] in ['.', ':']:
                    line += '\n'
                if line.strip()[-1] in [',', ';']:
                    line = line.rstrip() + " "
                if re.search('[a-z]', line[0]) is not None and len(textList) != 0:
                    textList[-1] = textList[-1].rstrip()
                    line = " " + line
                textList.append(line)
    completeText = "".join(textList)
    
    # Remove some unnecessary text (like item 1 business) accidentally extracted
    completeText = re.sub('(Table of Contents)|(TABLE OF CONTENTS)', '', completeText)
    start_pattern = re.compile(r'(I|i)(tem|TEM)\s*1\s*(A|a)\.\s*((R|I|S|K){4}\s*FACTOR(S){0,1}|((R|r|i|s|k){4}\s*(F|f)actor(s){0,1}))')
    if re.search(start_pattern, completeText) is not None:
        section_start = re.search(start_pattern, completeText).start()
        completeText = completeText[section_start:]

    return completeText

def tagsToLower(text):
# Standardize tags to lowercase to avoid possible parsing errors
    tags = list(re.finditer(r'(<A-z]+ )|(</[A-z]+>)|(<[A-z]+>)', text))
    for t in tags:
        text = text[:t.start()] + text[t.start():t.end()].lower() + text[t.end():]
    return text

def getRiskSectionXML(filing):
# Extract risk section from the company filing (xml)
    item1APattern = re.compile(r'(>.{0,6}(Part)*.{0,6}I*.{0,6}(I|i)(tem|TEM).{0,6}1.{0,6}(A|a))')
    itemRegexPattern = re.compile(r'(>.{0,6}(Part)*.{0,6}I*.{0,6}(I|i)(tem|TEM).{0,6}((1.{0,6}(B|b))|2))')
    itemPattern = re.compile(r'>.{0,6}(I|i)(tem|TEM).{0,6}[0-9]{1,2}.{0,6}(A|a|B|b){0,1}.{0,6}<')

    riskRegexPattern = r'((R|I|S|K){1,4}\s*FACTOR(S){0,1}|((R|r|i|s|k){1,4}\s*(F|f)actor(s){0,1}))(\.|\s|&#*[a-z0-9]{3,4};)*<\/*'
    xmlStartPattern = r'<[A-z]+'
    xmlEndPattern = r'[A-z0-9]+(\.)(&(#)*[a-z0-9]{3,4};)*\s*<\/[A-z]+'
    
    # Test multiple rounds to extract the correct portion
    if item1APattern.search(filing) is None:
        if re.search(riskRegexPattern, filing) is None:
            return "<data> </data>"
        else:
            itemStarts = sort([e.end() for e in re.finditer(riskRegexPattern, filing)])
    else:
        itemStarts = sort([e.end() for e in item1APattern.finditer(filing)])

    count = 0
    errors = True
    while errors and count < len(itemStarts):
        errors = False
        startIndex = itemStarts[count]
        try:
            # Try cropping out the portion with complete xml tags
            startIndex = max([e.end() for e in re.finditer(r'</[A-z]+>', filing[:startIndex])])
            riskSection = filing[startIndex:]
            endIndex = itemRegexPattern.search(riskSection).start()
            riskSection = riskSection[:endIndex]
            riskSection = tagsToLower(riskSection)
            starts = re.search(xmlStartPattern, riskSection).start()
            ends = max([e.end() for e in re.finditer(xmlEndPattern, riskSection)])
            ends = ends + min([s.start() for s in re.finditer(xmlStartPattern, riskSection[ends:])])
            if re.search(riskRegexPattern, riskSection[starts:ends]) is None: errors = True
            if len(list(itemPattern.finditer(riskSection[starts:ends]))) >= 2: errors = True
        except Exception as e: errors = True
        if not errors: break
        count += 1
    # Return empty string if nothing is found
    if errors: return "<data> </data>"
    # Prepare cropped xml portion for parsing into text
    xmlToParse = "<data>" + riskSection[starts:ends] + "</data>"
    xmlToParse = cleanText(xmlToParse)
    xmlToParse = str(BeautifulSoup(xmlToParse, features="lxml").prettify())
    s = re.search(r'<data>', xmlToParse).start()
    e = re.search(r'</data>', xmlToParse).end()
    xmlToParse = re.sub('\n', ' ', xmlToParse[s:e])
    return xmlToParse

def processFiles(outputLocation, companyFolders, fileType = '10-K'):
    if fileType not in ["10-K"]: return
    # Process filings for each company
    for folder in [os.path.join(companyFolders, x) for x in os.listdir(companyFolders)]:
        print(folder)
        # Process 10-K
        interestFolder = os.path.join(folder, fileType)
        # Skip folders do not contain filings
        if os.path.basename(folder) == ".DS_Store": continue
        ticker = os.path.basename(folder)
        # Skip already processed filings
        # if (tickerCheckProcessing(ticker, fileType, outputLocation)): continue
        # Skip if the desired filing type is not present
        if interestFolder not in [os.path.join(folder, x)  for x in os.listdir(folder)]: continue
        else:
            # Processing interested filing type for a company
            print(ticker + ": being processed")
            subFolders = [os.path.join(interestFolder, x) for x in os.listdir(interestFolder)]
            txtForThisCusip = {}
            errors = False
            # Process interested filing type for the company in each year
            for subF in subFolders:
                if os.path.basename(subF) == ".DS_Store": continue
                print("Processing ", os.path.basename(subF))
                folderFiles = [os.path.join(subF, x) for x in os.listdir(subF)]
                # Loop through downloaded files for that year
                for file in folderFiles:
                    # Only process full-submission.txt which is the text version of
                    # the filing's html
                    if os.path.basename(file) == "full-submission.txt":
                        secFile = open(file,"r")
                        textString =  secFile.read()
                        filing, docs = getDocuments(textString, fileType)
                        company_name, label = getCompanyNameAndTime(textString)
                        try:
                            xmlToParse = getRiskSectionXML(filing)
                            treeToParse = ET.fromstring(xmlToParse)
                        except Exception as e:
                            errors = True
                            print(f"Error in : {ticker}    :   {os.path.basename(subF)}\n{str(e)}")
                        if not errors:
                            textOut = treeToText(treeToParse)
                            txtForThisCusip[label] = textOut
                if not errors:
                    outputCompletedFiles(txtForThisCusip, fileType,
                    ticker + '-' + re.sub('\s', '-', company_name), outputLocation)