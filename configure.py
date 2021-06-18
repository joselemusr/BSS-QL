
# Utils

import sys
import os
import settings
from envs import env
import numpy as np
import time
from pathlib import Path

# SQL
import sqlalchemy as db
import psycopg2
import json

# Definicion Environments Vars
workdir = env('PWD')
db_motor = env('DB_MOTOR')
db_user = env('DB_USER')
db_pass = env('DB_PASS')
db_server = env('DB_SERVER')
db_port = env('DB_PORT')
db_base   = env('DB_BASE')


# Conexión a la DB de resultados
engine = db.create_engine(f'{db_motor}://{db_user}:{db_pass}@{db_server}:{db_port}/{db_base}')
metadata = db.MetaData()

try: 
    connection = engine.connect()

except db.exc.SQLAlchemyError as e:
    exit(str(e.__dict__['orig']))




datosEjecucion = db.Table('datos_ejecucion', metadata, autoload=True, autoload_with=engine)
insertDatosEjecucion = datosEjecucion.insert().returning(datosEjecucion.c.id)

algorithms = [['GWO_SCP_BCL1_CPU_C','SCA_SCP_BCL1_CPU_C','HHO_SCP_BCL1_CPU_C','WOA_SCP_BCL1_CPU_C']
,['GWO_SCP_MIR2_CPU_C','SCA_SCP_MIR2_CPU_C','HHO_SCP_MIR2_CPU_C','WOA_SCP_MIR2_CPU_C']
,['GWO_SCP_QL1_CPU_C','SCA_SCP_QL1_CPU_C','HHO_SCP_QL1_CPU_C','WOA_SCP_QL1_CPU_C']
,['GWO_SCP_QL2_CPU_C','SCA_SCP_QL2_CPU_C','HHO_SCP_QL2_CPU_C','WOA_SCP_QL2_CPU_C']
,['GWO_SCP_QL3_CPU_C','SCA_SCP_QL3_CPU_C','HHO_SCP_QL3_CPU_C','WOA_SCP_QL3_CPU_C']
,['GWO_SCP_QL4_CPU_C','SCA_SCP_QL4_CPU_C','HHO_SCP_QL4_CPU_C','WOA_SCP_QL4_CPU_C']
,['GWO_SCP_QL5_CPU_C','SCA_SCP_QL5_CPU_C','HHO_SCP_QL5_CPU_C','WOA_SCP_QL5_CPU_C']
]

rewardTypes = ['escalatingMultiplicativeAdaptation'
,'escalatingMultiplicativeAdaptation'
,'withPenalty1'
,'withoutPenalty1'
,'globalBest'
,'rootAdaptation'
,'escalatingMultiplicativeAdaptation'
]

instances = ['mscp42','mscp43','mscp44','mscp45','mscp46','mscp47','mscp48','mscp49','mscp410','mscp52','mscp53','mscp54','mscp55','mscp56','mscp57','mscp58','mscp59','mscp510','mscp62','mscp63','mscp64','mscp65','mscpa2','mscpa3','mscpa4','mscpa5','mscpb2','mscpb3','mscpb4','mscpb5','mscpc2','mscpc3','mscpc4','mscpc5','mscpd2','mscpd3','mscpd4','mscpd5']
runs = 5
population  = 40
maxIter = 1000
ql_alpha = 0.1
ql_gamma =  0.4
policy = "softMax-rulette-elitist" #puede ser 'e-greedy', 'greedy', 'e-soft', 'softMax-rulette', 'softMax-rulette-elitist'
qlAlphaType = "static" # Puede ser 'static', 'iteration', 'visits'
repair = 2 # 1:Simple; 2:Compleja; 3:RepairGPU
instance_dir = "MSCP/"
for run in range(runs):
    for instance in instances:
        for algorithm2 in algorithms:
            for algorithm in algorithm2:
                for rewardType in rewardTypes:
                    data = {
                        'nombre_algoritmo' : algorithm,

                        'parametros': json.dumps({
                            'instance_name' : instance,
                            'instance_file': instance+'.txt',
                            'instance_dir': instance_dir,
                            'population': population,
                            'maxIter':maxIter,
                            'discretizationScheme':'V4,Elitist',
                            'ql_alpha': ql_alpha,
                            'ql_gamma': ql_gamma,
                            'repair': repair,
                            'policy': policy,
                            'rewardType': rewardType,
                            'qlAlphaType': qlAlphaType
                    }),
                        'estado' : 'pendiente'
                    }
                    result = connection.execute(insertDatosEjecucion,data)
                    idEjecucion = result.fetchone()[0]
                    print(f'Poblado ID #:{idEjecucion}')

print("Todo poblado")

algorithms = [['GWO_SCP_BCL1_CPU_S','SCA_SCP_BCL1_CPU_S','HHO_SCP_BCL1_CPU_S','WOA_SCP_BCL1_CPU_S']
,['GWO_SCP_MIR2_CPU_S','SCA_SCP_MIR2_CPU_S','HHO_SCP_MIR2_CPU_S','WOA_SCP_MIR2_CPU_S']
,['GWO_SCP_QL1_CPU_S','SCA_SCP_QL1_CPU_S','HHO_SCP_QL1_CPU_S','WOA_SCP_QL1_CPU_S']
,['GWO_SCP_QL2_CPU_S','SCA_SCP_QL2_CPU_S','HHO_SCP_QL2_CPU_S','WOA_SCP_QL2_CPU_S']
,['GWO_SCP_QL3_CPU_S','SCA_SCP_QL3_CPU_S','HHO_SCP_QL3_CPU_S','WOA_SCP_QL3_CPU_S']
,['GWO_SCP_QL4_CPU_S','SCA_SCP_QL4_CPU_S','HHO_SCP_QL4_CPU_S','WOA_SCP_QL4_CPU_S']
,['GWO_SCP_QL5_CPU_S','SCA_SCP_QL5_CPU_S','HHO_SCP_QL5_CPU_S','WOA_SCP_QL5_CPU_S']
]

rewardTypes = ['escalatingMultiplicativeAdaptation'
,'escalatingMultiplicativeAdaptation'
,'withPenalty1'
,'withoutPenalty1'
,'globalBest'
,'rootAdaptation'
,'escalatingMultiplicativeAdaptation'
]

instances = ['mscp42','mscp43','mscp44','mscp45','mscp46','mscp47','mscp48','mscp49','mscp410','mscp52','mscp53','mscp54','mscp55','mscp56','mscp57','mscp58','mscp59','mscp510','mscp62','mscp63','mscp64','mscp65','mscpa2','mscpa3','mscpa4','mscpa5','mscpb2','mscpb3','mscpb4','mscpb5','mscpc2','mscpc3','mscpc4','mscpc5','mscpd2','mscpd3','mscpd4','mscpd5']
runs = 5
population  = 40
maxIter = 1000
ql_alpha = 0.1
ql_gamma =  0.4
policy = "softMax-rulette-elitist" #puede ser 'e-greedy', 'greedy', 'e-soft', 'softMax-rulette', 'softMax-rulette-elitist'
qlAlphaType = "static" # Puede ser 'static', 'iteration', 'visits'
repair = 1 # 1:Simple; 2:Compleja; 3:RepairGPU
instance_dir = "MSCP/"
for run in range(runs):
    for instance in instances:
        for algorithm2 in algorithms:
            for algorithm in algorithm2:
                for rewardType in rewardTypes:
                    data = {
                        'nombre_algoritmo' : algorithm,

                        'parametros': json.dumps({
                            'instance_name' : instance,
                            'instance_file': instance+'.txt',
                            'instance_dir': instance_dir,
                            'population': population,
                            'maxIter':maxIter,
                            'discretizationScheme':'V4,Elitist',
                            'ql_alpha': ql_alpha,
                            'ql_gamma': ql_gamma,
                            'repair': repair,
                            'policy': policy,
                            'rewardType': rewardType,
                            'qlAlphaType': qlAlphaType
                    }),
                        'estado' : 'pendiente'
                    }
                    result = connection.execute(insertDatosEjecucion,data)
                    idEjecucion = result.fetchone()[0]
                    print(f'Poblado ID #:{idEjecucion}')

print("Todo poblado")