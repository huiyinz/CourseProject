import os
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize.treebank import TreebankWordDetokenizer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize
from nltk.sentiment import SentimentIntensityAnalyzer
import re

dir = "/Users/huiyinz/Desktop/UIUC/CS410/CourseProject/"
outputLocation = os.path.join(dir, "ProcessedFiles")

company_filings = {}
for folder in [os.path.join(outputLocation, x) for x in os.listdir(outputLocation)]:
    company = os.path.basename(folder)
    if company == '.DS_Store': continue
    folder_10K = os.path.join(folder, '10-K_Risk_Factors')
    company_records = {}
    for txts in [os.path.join(folder_10K, x) for x in os.listdir(folder_10K)]:
        risk_factors = open(txts,"r")
        risk_factors_string =  risk_factors.read()
        company_records[os.path.basename(txts)[:-4]] = risk_factors_string
    company_filings[company] = company_records


example_company = list(company_filings.keys())[0]
example_filing = list(company_filings[example_company].keys())[0]
corpus = company_filings[example_company][example_filing]

# Sentiment Analysis Demo

SIA = SentimentIntensityAnalyzer()
sentiment_analysis_results = SIA.polarity_scores(corpus)


for index, row in df_subset.iterrows():
    scores = sid.polarity_scores(row[1])
    for key, value in scores.items():
        temp = [key,value,row[0]]
        df1['row_id']=row[0]
        df1['sentiment_type']=key
        df1['sentiment_score']=value
        t_df=t_df.append(df1)


# Topic Modeling Demo

from contextualized_topic_models.models.ctm import CombinedTM
from contextualized_topic_models.utils.data_preparation import TopicModelDataPreparation
from contextualized_topic_models.utils.data_preparation import bert_embeddings_from_file
from contextualized_topic_models.models.ctm import ZeroShotTM

all_filings = [company_filings[i][j] for i in company_filings.keys() for j in company_filings[i].keys()]

stop_words = stopwords.words('english')
corp = [str(x).lower() for x in all_filings]
text_for_contextual = [re.sub('\n',' ', x).strip() for x in corp]

token_list = [word_tokenize(x) for x in text_for_contextual]
text_for_bow = []
for tokens in token_list:
    cur_words = [t for t in tokens if t not in stop_words]
    cur_string = TreebankWordDetokenizer().detokenize(cur_words)
    text_for_bow.append(cur_string)

qt = TopicModelDataPreparation("all-mpnet-base-v2")
training_dataset = qt.fit(text_for_contextual=text_for_contextual, 
                          text_for_bow=text_for_bow)
ctm = CombinedTM(bow_size=len(qt.vocab), contextual_size=768, n_components=15) # 15 topics

import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

ctm.fit(training_dataset) # run the model
ctm.get_topics(5)

