
excel_adrs = '/Users/huiyinz/Desktop/UIUC/CS410/CourseProject/Energy_Sector.xlsx'
dir = "/Users/huiyinz/Desktop/UIUC/CS410/CourseProject/"
n_file = 3
end_date = '2022-01-01'

companyFolders = os.path.join(dir, "sec-edgar-filings")
outputLocation = os.path.join(dir, "ProcessedFiles")

file = "/Users/huiyinz/Desktop/UIUC/CS410/CourseProject/sec-edgar-filings/CVX/10-K/0000093410-19-000008/full-submission.txt"
fileType = '10-K'
secFile = open(file,"r")
textString =  secFile.read()
filing, docs = getDocuments(textString, fileType)
company_name, label = getCompanyNameAndTime(textString)

item1APattern = re.compile(r'(>.{0,6}(Part)*.{0,6}I*.{0,6}(I|i)(tem|TEM).{0,6}1.{0,6}(A|a))')
itemRegexPattern = re.compile(r'(>.{0,6}(Part)*.{0,6}I*.{0,6}(I|i)(tem|TEM).{0,6}((1.{0,6}(B|b))|2))')
itemPattern = re.compile(r'>.{0,6}(I|i)(tem|TEM).{0,6}[0-9]{1,2}.{0,6}(A|a|B|b){0,1}.{0,6}<')

riskRegexPattern = r'((R|I|S|K){1,4}\s*FACTOR(S){0,1}|((R|r|i|s|k){1,4}\s*(F|f)actor(s){0,1}))(\.|\s|&#*[a-z0-9]{3,4};)*<\/*'
xmlStartPattern = r'<[A-z]+'
xmlEndPattern = r'[A-z0-9]+(\.)(&(#)*[a-z0-9]{3,4};)*\s*<\/[A-z]+'

if item1APattern.search(filing) is None:
    if re.search(riskRegexPattern, filing) is None:
        print("<data> </data>")
    else:
        itemStarts = sort([e.end() for e in re.finditer(riskRegexPattern, filing)])
else:
    itemStarts = sort([e.end() for e in item1APattern.finditer(filing)])
    itemEnds = sort([e.end() for e in item1APattern.finditer(textString)])


count = 0

while count < len(itemStarts):
    startIndex = itemStarts[count]
    #startIndex = max([e.end() for e in re.finditer(r'</[A-z]+>', textString[:startIndex])])
    riskSection = textString[startIndex:]
    endIndex = itemRegexPattern.search(riskSection).start()
    riskSection = riskSection[:endIndex]
    print(count, '\n\n')
    print(riskSection[:1000])
    count += 1