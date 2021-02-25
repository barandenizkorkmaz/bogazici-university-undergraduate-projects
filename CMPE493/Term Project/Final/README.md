# CMPE493: Introduction to Information Retrieval - Term Project (Final)

## Project Collaborators

* Baran Deniz Korkmaz
* Bekir Yıldırım
* Mahir Efe Kaya



## Requirements

* Python3

* The packages used in the project are listed in `requirements.txt` which are derived by the following command:

  ```
  pip freeze > requirements.txt
  ```

* The following files must be provided for running the notebook:
  * `metadata.csv`
  * `topics-rnd5.xml`
  * `qrels-covid_d5_j0.5-5.txt`
  * `keywords.txt`



## Execution

1. The information retrieval system retrieves ranked documents based on cosine similarity. In order to obtain the `RESULTS` file that is formatted as the `official trec evaluation` tool requires, run the notebook called `TermProject.ipynb`.

2. Finally you can enter the following command in `official trec evaluation` tool to evaluate our system by entering:

   `./trec_eval -m map -m ndcg -m P.10 qrels-covid_d5_j0.5-5.txt RESULTS`

   Below our evaluation results can be observed.

   | Metric | Value  |
   | :----: | :----: |
   |  map   | 0.5184 |
   |  P_10  | 0.6620 |
   |  ndcg  | 0.8390 |