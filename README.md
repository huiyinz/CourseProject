# Market Risk Analyzer

## Description
This application targets to computationally analyze the market risk in certain economic sectors to help user make more informed investment decisions. There are three main components:

1. Extract text description of risk from company 10-K filings
2. Uncover shared topics from text descriptions of risk in companies within the same economic sector
3. Analyze sentiments of text descriptions 

## Presentation
Please click [here](https://drive.google.com/file/d/1mkZ1n0QFDNkURG7WZ6eF9rHspblquq4v/view?usp=sharing) for the presentation :) 

## Pipeline
For users / contributers, please follow these steps to test the application.
- Please create a working directory. You can also use your desktop.
- Please copy and paste your interested companies [here](https://finviz.com/screener.ashx?v=111&f=geo_usa,sec_energy&o=-marketcap).
You can change to a different economic sector. Please save in an excel file under your working directory. An example is Energy_Sector.xlsx
- If you have not done so, please download necessary libraries (note: I was using python 3.8.2 for testing the implementation):
```
    pip install sec-edgar-downloader
    pip install pandas
    pip install xml-python
    pip install bs4
    pip install numpy
```
- After you have completed the steps above, please go to your working directory and paste **main.py**, **load10K.py**, and **process10K.py** for testing the information retrieval process. Now you should have the code files as well as Energy_Sector.xlsx (or some other excel sheet with company ticker code) in your working directory
- Please go to **main.py** and specify the `dir` as well as `excel_adrs`
- You can run **main.py** now, results will be saved in **ProcessedFiles** under your working directory
- You can upload **Filings.csv** and **Filings_Text.txt** to a shared location (e.g. github) and follow the steps in **[Topic Modeling Demo.ipynb](https://colab.research.google.com/drive/1x5Oyph2zefFCchmTH6R0a_YtmoyYqDDt?usp=sharing)** and **[Sentiment Analysis Demo.ipynb](https://colab.research.google.com/drive/1XbBkVJdI6wFgnxXKx3g4ZZ-L0OIe7wfW?usp=sharing)** for text mining

## Documentation
- **main.py** is used to execute the pipeline
- **load10K.py** is the first part of the information retrieval task to download 10-K filings of companies listed in the excel file from SEC with edgar downloader into the specified location
- **process10K.py** performs the second part of the information task to extract the risk factors section from the downloaded html filings of companies. There are 9 functions in this file:
    - tickerCheckProcessing
        - Function: checks if the filing for the company is already processed
        - Inputs: company ticker (string), file type (string, e.g. '10-K')
        - Outputs: boolean
    - outputCompletedFiles
        - Function: writes the retrieved sections to designated location
        - Inputs: extracted risk factors of all companies (dictionary of texts), file type (string, e.g. '10-K'), company ticker (string)
        - Outputs: N/A
    - getCompanyNameAndTime
        - Function: extracts the company name and filing date
        - Inputs: text string of company filing (string)
        - Outputs: company name (string), period (string)
    - getDocuments
        - Function: extracts the actual body content from the filing html
        - Inputs: text string of company filing (string), file type (string, e.g. '10-K')
        - Outputs: body content (string), individual financial documents (dictionary)
    - cleanText
        - Function: extracts the company name and filing date
        - Inputs: body content (string)
        - Outputs: cleaned body content (string)
    - treeToText
        - Function: iteratively extract text from nodes in element tree, a newline is added after certain punctuations
        - Inputs: root element of parsed tree (Element)
        - Outputs: standardized xml selection (string)
    - tagsToLower
        - Function: standardize tags to lowercase to avoid possible parsing errors
        - Inputs: unformatted xml selection (string)
        - Outputs: cleaned text (string)
    - getRiskSectionXML
        - Function: Extract the Item 1A (Risk Factors) section from filing
        - Inputs: text string of company filing (string), filing type (string)
        - Outputs: xml-structured text for Item 1A (string)
    - processFiles
        - Function: Wrapper function for extracting the Item 1A (Risk Factors) section from each company's filing in the download folder and save the results in a txt file
        - Inputs: output location (path), company filings main folder location (path), filing type (string)
        - Outputs: None

## References
#### **Edgar Downloader**
- https://sec-edgar-downloader.readthedocs.io/en/latest/

#### **Sentiment Analysis**
- https://www.digitalocean.com/community/tutorials/how-to-perform-sentiment-analysis-in-python-3-using-the-natural-language-toolkit-nltk
- https://realpython.com/python-nltk-sentiment-analysis/

#### **Topic Modeling**
- https://github.com/MilaNLProc/contextualized-topic-models