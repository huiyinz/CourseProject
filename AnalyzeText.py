# Please download the nltk library
# pip install --user -U nltk
def PreprocessText():
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    from nltk.stem import WordNetLemmatizer

    # Please run the following commented code if you have not downloaded
    #nltk.download([
    #     "names",
    #     "stopwords",
    #     "vader_lexicon",
    #     "punkt",
    #     "perluniprops"
    # ])

    lemma = WordNetLemmatizer()
    stop_words = stopwords.words('english')


    corp = str(x).lower()
    corp = re.sub('[^a-zA-Z]+',' ', corp).strip()
    tokens = word_tokenize(corp)
    words = [t for t in tokens if t not in stop_words]
    lemmatize = [lemma.lemmatize(w) for w in words]


def SentimentAnalysis():
    from nltk.sentiment import SentimentIntensityAnalyzer

    SIA = SentimentIntensityAnalyzer()
    sia.polarity_scores("Wow, NLTK is really powerful!")


    for index, row in df_subset.iterrows():
        scores = sid.polarity_scores(row[1])
        for key, value in scores.items():
            temp = [key,value,row[0]]
            df1['row_id']=row[0]
            df1['sentiment_type']=key
            df1['sentiment_score']=value
            t_df=t_df.append(df1)

def ContextualTopicModeling():
    from contextualized_topic_models.models.ctm import CombinedTM
    from contextualized_topic_models.utils.data_preparation import TopicModelDataPreparation
    from contextualized_topic_models.utils.data_preparation import bert_embeddings_from_file

    qt = TopicModelDataPreparation("all-mpnet-base-v2")
    training_dataset = qt.fit(text_for_contextual=list_of_unpreprocessed_documents, text_for_bow=list_of_preprocessed_documents)
    ctm = CombinedTM(bow_size=len(qt.vocab), contextual_size=768, n_components=50) # 50 topics
    ctm.fit(training_dataset) # run the model
    ctm.get_topics(5)

