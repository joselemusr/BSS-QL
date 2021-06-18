
# Utils

import sys
import os
import settings
from envs import env
import numpy as np
import time
from datetime import datetime
from pathlib import Path

# SQL
import sqlalchemy as db
import psycopg2
import json
import pickle
import zlib

import Database.Database as Database


### Buscamos experimentos pendientes
connect = Database.Database()


# Algorithms

from Metaheuristics.GWO_SCP import GWO_SCP
from Metaheuristics.GWOQL_SCP import GWOQL_SCP
from Metaheuristics.SCA_SCP import SineCosine_SCP
from Metaheuristics.SCAQL_SCP import SineCosineQL_SCP
from Metaheuristics.HHO_SCP import HHO_SCP
from Metaheuristics.HHOQL_SCP import HHOQL_SCP
from Metaheuristics.WOA_SCP import WOA_SCP
from Metaheuristics.WOAQL_SCP import WOAQL_SCP


flag = True
while flag:

    id, algorithm, params = connect.getLastPendingAlgorithm('pendiente')
    
    if id == 0:
        print('No hay más ejecuciones pendientes')
        break
        
       
    print("------------------------------------------------------------------------------------------------------------------\n")
    print(f'Id Execution: {id} -  {algorithm}')
    print(json.dumps(params,indent=4))
    print("------------------------------------------------------------------------------------------------------------------\n")

    if(algorithm == 'GWO_SCP_BCL1' or algorithm == 'GWO_SCP_MIR2' or algorithm == 'GWO_SCP_BCL1_CPU_S' or algorithm == 'GWO_SCP_MIR2_CPU_S' or algorithm == 'GWO_SCP_BCL1_CPU_C' or algorithm == 'GWO_SCP_MIR2_CPU_C'):
        if  GWO_SCP(id,
                params['instance_file'],
                params['instance_dir'],
                params['population'],
                params['maxIter'],
                params['discretizationScheme'],
                params['repair']
                ) == True:
            print(f'Ejecución {id} completada ')

    if(algorithm == 'GWO_SCP_QL1' or algorithm =='GWO_SCP_QL2' or algorithm == 'GWO_SCP_QL3' or algorithm == 'GWO_SCP_QL4' or algorithm == 'GWO_SCP_QL5' or algorithm == 'GWO_SCP_QL1_CPU_S' or algorithm =='GWO_SCP_QL2_CPU_S' or algorithm == 'GWO_SCP_QL3_CPU_S' or algorithm == 'GWO_SCP_QL4_CPU_S' or algorithm == 'GWO_SCP_QL5_CPU_S' or algorithm == 'GWO_SCP_QL1_CPU_C' or algorithm =='GWO_SCP_QL2_CPU_C' or algorithm == 'GWO_SCP_QL3_CPU_C' or algorithm == 'GWO_SCP_QL4_CPU_C' or algorithm == 'GWO_SCP_QL5_CPU_C'):
        if  GWOQL_SCP(id,
                params['instance_file'],
                params['instance_dir'],
                params['population'],
                params['maxIter'],
                params['discretizationScheme'],
                params['ql_alpha'],
                params['ql_gamma'],
                params['repair'],
                params['policy'],
                params['rewardType'],
                params['qlAlphaType']
                ) == True:
            print(f'Ejecución {id} completada ')

    if(algorithm == 'SCA_SCP_BCL1' or algorithm == 'SCA_SCP_MIR2' or algorithm == 'SCA_SCP_BCL1_CPU_S' or algorithm == 'SCA_SCP_MIR2_CPU_S' or algorithm == 'SCA_SCP_BCL1_CPU_C' or algorithm == 'SCA_SCP_MIR2_CPU_C'):
        if  SineCosine_SCP(id,
                params['instance_file'],
                params['instance_dir'],
                params['population'],
                params['maxIter'],
                params['discretizationScheme'],
                params['repair']
                ) == True:
            print(f'Ejecución {id} completada ')
  
    if(algorithm == 'SCA_SCP_QL1' or algorithm =='SCA_SCP_QL2' or algorithm == 'SCA_SCP_QL3' or algorithm == 'SCA_SCP_QL4' or algorithm == 'SCA_SCP_QL5' or algorithm == 'SCA_SCP_QL1_CPU_S' or algorithm =='SCA_SCP_QL2_CPU_S' or algorithm == 'SCA_SCP_QL3_CPU_S' or algorithm == 'SCA_SCP_QL4_CPU_S' or algorithm == 'SCA_SCP_QL5_CPU_S' or algorithm == 'SCA_SCP_QL1_CPU_C' or algorithm =='SCA_SCP_QL2_CPU_C' or algorithm == 'SCA_SCP_QL3_CPU_C' or algorithm == 'SCA_SCP_QL4_CPU_C' or algorithm == 'SCA_SCP_QL5_CPU_C'):
        if  SineCosineQL_SCP(id,
                params['instance_file'],
                params['instance_dir'],
                params['population'],
                params['maxIter'],
                params['discretizationScheme'],
                params['ql_alpha'],
                params['ql_gamma'],
                params['repair'],
                params['policy'],
                params['rewardType'],
                params['qlAlphaType']
                ) == True:
            print(f'Ejecución {id} completada ')


    if(algorithm == 'HHO_SCP_BCL1' or algorithm == 'HHO_SCP_MIR2' or algorithm == 'HHO_SCP_BCL1_CPU_S' or algorithm == 'HHO_SCP_MIR2_CPU_S' or algorithm == 'HHO_SCP_BCL1_CPU_C' or algorithm == 'HHO_SCP_MIR2_CPU_C'):
        if  HHO_SCP(id,
                params['instance_file'],
                params['instance_dir'],
                params['population'],
                params['maxIter'],
                params['discretizationScheme'],
                params['repair']
                ) == True:
            print(f'Ejecución {id} completada ')

    if(algorithm == 'HHO_SCP_QL1' or algorithm =='HHO_SCP_QL2' or algorithm == 'HHO_SCP_QL3' or algorithm == 'HHO_SCP_QL4' or algorithm == 'HHO_SCP_QL5' or algorithm == 'HHO_SCP_QL1_CPU_S' or algorithm =='HHO_SCP_QL2_CPU_S' or algorithm == 'HHO_SCP_QL3_CPU_S' or algorithm == 'HHO_SCP_QL4_CPU_S' or algorithm == 'HHO_SCP_QL5_CPU_S' or algorithm == 'HHO_SCP_QL1_CPU_C' or algorithm =='HHO_SCP_QL2_CPU_C' or algorithm == 'HHO_SCP_QL3_CPU_C' or algorithm == 'HHO_SCP_QL4_CPU_C' or algorithm == 'HHO_SCP_QL5_CPU_C'):
        if  HHOQL_SCP(id,
                params['instance_file'],
                params['instance_dir'],
                params['population'],
                params['maxIter'],
                params['discretizationScheme'],
                params['ql_alpha'],
                params['ql_gamma'],
                params['repair'],
                params['policy'],
                params['rewardType'],
                params['qlAlphaType']
                ) == True:
            print(f'Ejecución {id} completada ')


    if(algorithm == 'WOA_SCP_BCL1' or algorithm == 'WOA_SCP_MIR2' or algorithm == 'WOA_SCP_BCL1_CPU_S' or algorithm == 'WOA_SCP_MIR2_CPU_S' or algorithm == 'WOA_SCP_BCL1_CPU_C' or algorithm == 'WOA_SCP_MIR2_CPU_C'):
        if  WOA_SCP(id,
                params['instance_file'],
                params['instance_dir'],
                params['population'],
                params['maxIter'],
                params['discretizationScheme'],
                params['repair']
                ) == True:
            print(f'Ejecución {id} completada ')

    if(algorithm == 'WOA_SCP_QL1' or algorithm =='WOA_SCP_QL2' or algorithm == 'WOA_SCP_QL3' or algorithm == 'WOA_SCP_QL4' or algorithm == 'WOA_SCP_QL5' or algorithm == 'WOA_SCP_QL1_CPU_S' or algorithm =='WOA_SCP_QL2_CPU_S' or algorithm == 'WOA_SCP_QL3_CPU_S' or algorithm == 'WOA_SCP_QL4_CPU_S' or algorithm == 'WOA_SCP_QL5_CPU_S' or algorithm == 'WOA_SCP_QL1_CPU_C' or algorithm =='WOA_SCP_QL2_CPU_C' or algorithm == 'WOA_SCP_QL3_CPU_C' or algorithm == 'WOA_SCP_QL4_CPU_C' or algorithm == 'WOA_SCP_QL5_CPU_C'):
        if  WOAQL_SCP(id,
                params['instance_file'],
                params['instance_dir'],
                params['population'],
                params['maxIter'],
                params['discretizationScheme'],
                params['ql_alpha'],
                params['ql_gamma'],
                params['repair'],
                params['policy'],
                params['rewardType'],
                params['qlAlphaType']
                ) == True:
            print(f'Ejecución {id} completada ')