# CMPE 493: Introduction to Information Retrieval - Assignment 3

## Requirements

* Python3 
* The program has been tested in Python 3.6.9.



## Execution

The program execution has two steps:

1. Preprocessing the data and constructing the required data structures. In order to execute the first step, please enter the following command in terminal:

   `python3 main.py [path_to_file]`

   Example:

   `python3 main.py books.txt`

   I would like to mention that, in my local run, this stage lasted approximately `3 hours` with the provided file consisting of 1800 URLs.

2. After the first step has been successfully done, you can request a query by entering the following command in terminal:

   `python3 main.py [query_url]`

   Arguments:

   1. query_url: String of url.

   Example:

   `python3 main.py https://www.goodreads.com/book/show/18050143-zero-to-one`