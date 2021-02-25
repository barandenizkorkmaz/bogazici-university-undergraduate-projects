import re
import string

"""
    Declaration of regex patterns required for parsing the data within SGM files.
    Reference:
        https://dzlab.github.io/nlp/2018/11/17/parsing-xml-into-dataframe/
"""
document_pattern = re.compile(r"<REUTERS.*?<\/REUTERS>", re.S)
newid_pattern = re.compile(r"NEWID=.*?>", re.S)
body_pattern = re.compile(r"<BODY>.*?<\/BODY>", re.S)
title_pattern = re.compile(r"<TITLE>.*?<\/TITLE>", re.S)

"""
    Appends the content of stopwords text into a list.
    Arguments:
        file_name: 
            Type: String
            Desc: Name of file.
    Returns:
        Type: List<String>
        Desc: List of stopwords.
"""
def get_stopwords(file_name='stopwords.txt'):
    stopwords = list()
    with open(file_name,'r') as f:
        stopwords = f.read().split()
    return stopwords

"""
    Parses every article in SGM files.
    Arguments:
        file_name_template:
            Type: String
            Desc: Name template for SGM files that will be parsed.
    Returns:
        Type: List<Dict>
        Desc: A list of dictionary which holds the data of NEWID, TITLE, and BODY within every article.
        Each article has been represented as a single dictionary within the list.
        Dictionary:
            - Keys:
                Type: String
                Description: Tags in SGM file that are to be processed, i.e. NEWID, TITLE, BODY.
            - Values:
                Type: String
                Description: Values of NEWID, TITLE, and BODY.
            - Example:
                { 'NEWID' : '1',
                  'TITLE' : 'TITLE of Article 1',
                  'BODY' : 'BODY of Article 1'
                  }
"""
def get_articles(file_name_template='reuters21578/reut2-'):
    articles = list()
    for index in range(22):
        file_name = file_name_template + '{}.sgm'.format(str(index).zfill(3))
        with open(file_name,'r',encoding='latin-1',errors='ignore') as f:
            file_content = f.read()
            documents = document_pattern.findall(file_content)
            for article in documents:
                new_id = newid_pattern.search(article)
                body = body_pattern.search(article)
                title = title_pattern.search(article)
                new_id = new_id.group()[7:-2]
                body = body.group()[6:-7] if body else ""
                title = title.group()[7:-8] if title else ""
                articles.append({'NEWID': new_id,
                                 'TITLE': title,
                                 'BODY': body
                                 })
    return articles

"""
    Tokenizes the title and body of each article.
    Arguments:
        articles:
            Type: List<Dict>
            Desc: List of articles which are represented as separate dictionaries.
            Format:
                [ { 'NEWID' : '1',
                  'TITLE' : 'TITLE of Article 1',
                  'BODY' : 'BODY of Article 1'
                  },
                  { 'NEWID' : '2',
                  'TITLE' : 'TITLE of Article 2',
                  'BODY' : 'BODY of Article 2'
                  },
                  ...
                  { 'NEWID' : '21578',
                  'TITLE' : 'TITLE of Article 21578',
                  'BODY' : 'BODY of Article 21578'
                  }
                ]
    Returns:
        Type: Dictionary
        Desc: A dictionary that keeps newid and postings list pairs.
        Dictionary:
            - Keys:
                Type: String
                Description: NEWID of article.
            - Values:
                Type: List<String>
                Description: List of tokens.
            - Format:
                { '1' : ['token1_1','token1_2',...,'token1_a'],
                  '2' : ['token2_1','token2_2',...,'token2_b'],
                  ...
                  '21578' : ['token21578_1','token21578_2',...,'token21578_c']
                  }
"""
def tokenize(articles):
    tokenized_articles = dict()
    for article_dict in articles:
        title = article_dict['TITLE']
        body = article_dict['BODY']
        token_list = title.split() + body.split()
        tokenized_articles[article_dict['NEWID']] = token_list
    return tokenized_articles

"""
    Normalizes the tokens of each article. It applies the following operations in the given order:
        1. Case-Folding
        2. Punctuation Removal
        3. Stopword Removal
    Arguments:
        tokenized_articles:
            Type: Dictionary
            Desc: A dictionary that keeps newid and postings list pairs.
            Format:
                { '1' : ['token1_1','token1_2',...,'token1_a'],
                  '2' : ['token2_1','token2_2',...,'token2_b'],
                  ...
                  '21578' : ['token21578_1','token21578_2',...,'token21578_c']
                  }
    Returns:
        Type: Dictionary
        Desc: A dictionary that keeps newid and postings list pairs where each token is normalized.
        Dictionary:
            - Keys:
                Type: String
                Description: NEWID of article.
            - Values:
                Type: List<String>
                Description: List of tokens.
            - Format:
                { '1' : ['normalized_token1_1','normalized_token1_2',...,'normalized_token1_a'],
                  '2' : ['normalized_token2_1','normalized_token2_2',...,'normalized_token2_b'],
                  ...
                  '21578' : ['normalized_token21578_1','normalized_token21578_2',...,'normalized_token21578_c']
                  }
    Reference:
        https://stackoverflow.com/questions/34860982/replace-the-punctuation-with-whitespace
"""
def normalize(tokenized_articles):
    stopwords = get_stopwords()
    translator = str.maketrans(string.punctuation, ' ' * len(string.punctuation))  # map punctuation to space
    for newid in tokenized_articles.keys():
        tokens = tokenized_articles[newid]
        tokens = [x.lower() for x in tokens] # Case-Folding
        tokens = [x.translate(translator) for x in tokens]  # Punctuation Removal
        tmp = " ".join(x for x in tokens) # Retokenize the tokens that include any whitespaces after punctuation removal.
        tokens = tmp.split()
        tokens = [x for x in tokens if x not in stopwords] # Stopword Removal
        tokenized_articles[newid] = tokens
    return tokenized_articles