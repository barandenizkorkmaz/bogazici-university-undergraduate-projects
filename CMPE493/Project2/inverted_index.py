import os

"""
    Constructs an inverted index structure.
    Arguments:
        normalized_articles: A dictionary that keeps the normalized words for each article.
            - Keys:
                Type: String
                Description: Documents ids.
            - Values:
                Type: List<String>
                Description: List of normalized words.
            - Example:
                { '1' : [word1_1, word1_2, ... , word1_a],
                  '2' : [word2_1, word2_2, ... , word2_b],
                  ...
                  'n' : [wordn_1, wordn_2, ... , wordn_c]
                  }
    Returns:
        A dictionary.
        - Keys:
            Type: String
            Description: Strings of words.
        - Values:
            Type: List<String>
            Description: Postings lists of document IDs.
        - Example:
            { 'word1' : [id1_1, id1_2, ... , id1_a],
              'word2' : [id2_1, id2_2, ... , id2_b],
              ...
              'wordm' : [idn_1, idn_2, ... , idn_c]
              }
"""
def construct_inverted_index(normalized_articles):
    inverted_index = dict()
    for newid in normalized_articles.keys():
        normalized_tokens = normalized_articles[newid]
        for token in normalized_tokens:
            if token in inverted_index:
                if newid not in inverted_index[token]:
                    inverted_index[token].append(newid)
            else:
                inverted_index[token] = [newid]
    return inverted_index

"""
    Searches whether a previously saved inverted index (.json) file exists in the given name.
    Arguments:
        file_name: Name of file to be searched.
    Returns:
        Boolean
"""
def search_inverted_index(file_name):
    return os.path.exists(file_name)