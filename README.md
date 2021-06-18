# BSS-QL
Work repository "Q-Learnheuristics: towards data-driven ambidextrous metaheuristics"

## Links

[PostgresSQL database with results](https://drive.google.com/drive/folders/18wT7QR2sTjM_nvYwLpn9t8XUiuRxlN0w?usp=sharing)


[Graphics](https://drive.google.com/drive/folders/1-kS78-j46xKqI2g6m4lqyvDTyHhM-OLB?usp=sharing)


## Instrucciones

#### 1) Crear Base de Datos PostgreSQL con la estructura de database/Table_DB_mh_resultados.sql

#### 2) Actualizar .env con las credenciales correspondiente a la base de datos creada.

#### 3) Poblar base de datos con los experimentos a realizar en configure.py
```
python configure.py
```

#### 4) Correr experimentos
```
python main.py
```
