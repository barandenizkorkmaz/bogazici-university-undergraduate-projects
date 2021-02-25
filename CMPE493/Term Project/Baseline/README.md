# CMPE493: Introduction to Information Retrieval - Term Project (Baseline)

## Project Collaborators

* Baran Deniz Korkmaz
* Bekir Yıldırım
* Mahir Efe Kaya



## Requirements

* Python3

* The packages used in the project can be installed by `requirements.txt` into a virtual environment. Please make sure that inside the virtual environment `pip` is referenced to `pip3` and it is updated.

  `pip3 install -r requirements.txt`

* The project has been tested in Ubuntu 18.04 using Python 3.6.9.

* The following files must be located inside the directory where the files provided by collaborators reside:
  * `metadata.csv`
  * `topics-rnd5.xml`
  * `qrels-covid_d5_j0.5-5.txt`



## Execution

1. The information retrieval system retrieves ranked documents based on cosine similarity. In order to obtain the `RESULTS` file that is formatted as the `official trec evaluation` tool requires, enter the following command in terminal:

   `python3 main.py`

2. The program will output `RESULTS` file that you can use to evaluate. The file contains the ranked results for the queries with even ids since they are predetermined as test queries. In order to obtain the relevance judgements for test queries, please enter the following command in terminal:

   `python3 prepareQueryRels.py`

   This command will output the relevance judgements for test queries in a `txt` file called `qrels-covid_d5_j0.5-5_test.txt`.

3. Finally you can enter the following command in `official trec evaluation` tool to evaluate our system by entering:

   `./trec_eval -m map -m ndcg -m P.10 qrels-covid_d5_j0.5-5_test.txt RESULTS`

   Below our evaluation results can be observed.

   | Metric | Value  |
   | :----: | :----: |
   |  map   | 0.2537 |
   |  P_10  | 0.5920 |
   |  ndcg  | 0.7353 |