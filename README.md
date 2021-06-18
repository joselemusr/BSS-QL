# BSS-QL
Work repository "Q-Learnheuristics: towards data-driven ambidextrous metaheuristics"

## Links

[PostgresSQL database with results](https://drive.google.com/drive/folders/18wT7QR2sTjM_nvYwLpn9t8XUiuRxlN0w?usp=sharing)


[Graphics](https://drive.google.com/drive/folders/1-kS78-j46xKqI2g6m4lqyvDTyHhM-OLB?usp=sharing)


## Instructions

#### 1) Create PostgreSQL Database with the structure of Database/Table_DB_mh_result_mh_result.sql

#### 2) Update ".env" with the credentials corresponding to the created database.

#### 3) Populate database with the experiments to be performed in "configure.py".
```
python configure.py
```

#### 4) Running experiments
```
python main.py
```
