# CMPE 493: Introduction to Information Retrieval - Assignment 2

## Requirements

* Python3 
* The program has been tested in Python 3.6.9.



## Execution

The program execution has two steps:

1. Preprocessing the data and constructing the required data structures, namely inverted index and trie. In order to execute the first step, please enter the following command in terminal:

   `python3 main.py`

   Please note that, this step assumes that the required data, namely`reuters21578` and `stopwords.txt` are provided in the working directory. Plus, the entire execution assumes that the files that stores the saved data structures, namely `inverted_index.json` and `trie.pickle` will not be touched.

2. After the first step has been successfully done, you can request a valid query by entering the following command in terminal:

   `python3 main.py [query]`

   Arguments:

   1. query: String of single-word or prefix query.

   Examples:

   1. `python3 main.py information`
   2. `python3 main.py retrieva*`