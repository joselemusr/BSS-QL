import numpy as np
from numba import cuda, float32, jit, uint8, int8, uint16, int32
import math
import sys
from numba.cuda.random import create_xoroshiro128p_states, xoroshiro128p_uniform_float32

#cumple reparaSoluciones
#recibe (todos numpy array)
#matriz de n soluciones con m columnas 
#matriz de o restricciones con m columnas
#lista de pesos con m columnas
#retorna
#lista binaria de n x o elementos donde un 1 representa que la solucion n cumple las restricciones, 0 si no

NSOL = 10
MRES = 100
COL = 100



def reparaSoluciones(soluciones, restricciones, pesos, pondRestricciones):
    soluciones = np.array(soluciones, dtype=np.int8)
    restricciones = np.array(restricciones, dtype=np.int8)
    n,m = soluciones.shape
    assert m == restricciones.shape[1], f"numero de columnas distinto en soluciones {m} y restricciones {restricciones.shape[1]}"
    #COL = m
    factibilidad = _procesarFactibilidadGPU(soluciones, restricciones)
    columnas = np.arange(soluciones.shape[0])
    cont = 0
    while (factibilidad == 0).any():        
    
        assert factibilidad.shape[0] == n, f"numero de factibilidades {factibilidad.shape[0]} distinto de numero de soluciones {n}"
        assert factibilidad.shape[1] == restricciones.shape[0], f"numero de restricciones en factibilidades {factibilidad.shape[1]} distinto de numero de restricciones {restricciones.shape[0]}"
        #obtengo matriz que representa la suma de todas las columnas incumplidas de numero soluciones x numero columnas soluciones        
        ponderaciones = _ponderarColsReparar(restricciones, factibilidad, pesos, pondRestricciones)
        ponderaciones[ponderaciones==0] = np.inf
       
        idxSolsInfactibles = np.any(factibilidad==0, axis=1)
        nCols = 10
        colsElegidas = np.argpartition(ponderaciones,nCols,axis=1)[:,:nCols]
        noInf = np.argwhere(colsElegidas != np.inf)
        posNoInf = np.array([np.argwhere(noInf[:,0]==pos).reshape((-1)) for pos in range(soluciones.shape[0])])
        randomNoInf = np.array([np.random.choice(posNoInf[pos]) for pos in range(posNoInf.shape[0])]).T
        noInfidxs = noInf[randomNoInf]

        mejorColumna = np.argmin(ponderaciones[idxSolsInfactibles,colsElegidas.T[:,idxSolsInfactibles]].T, axis=1)

        colRandom = colsElegidas[noInfidxs[:,0], noInfidxs[:,1]]

        if np.random.uniform() < 0.8:
            soluciones[idxSolsInfactibles,colsElegidas[idxSolsInfactibles,mejorColumna]] = 1
        else:
            soluciones[idxSolsInfactibles,colRandom[idxSolsInfactibles]] = 1

        cont += 1

        factibilidad = _procesarFactibilidadGPU(soluciones, restricciones)
    return soluciones
    

def _procesarFactibilidadGPU(soluciones, restricciones):

    restriccionesCumplidas = np.zeros((soluciones.shape[0], restricciones.shape[0]), dtype=np.uint16)
    #iniciar kernel
    threadsperblock = (NSOL, MRES)
    blockspergrid_x = int(math.ceil(soluciones.shape[0] / threadsperblock[0]))
    blockspergrid_y = int(math.ceil(restricciones.shape[0] / threadsperblock[1]))
    blockspergrid = (blockspergrid_x, blockspergrid_y)
    sol_global_mem = cuda.to_device(soluciones)
    rest_global_mem = cuda.to_device(restricciones)
    resultado_global_mem = cuda.to_device(restriccionesCumplidas)

    #llamar kernel
    kernelFactibilidadGPU[blockspergrid, threadsperblock](sol_global_mem,rest_global_mem,resultado_global_mem)

    return resultado_global_mem.copy_to_host()

def _ponderarColsReparar(restricciones, factibilidad, pesos, pondRestricciones):
    ponderaciones = np.zeros((factibilidad.shape[0], restricciones.shape[1]), dtype=np.float32)
    #iniciar kernel
    threadsperblock = (NSOL, COL)
    blockspergrid_x = int(math.ceil(factibilidad.shape[0] / threadsperblock[0]))
    blockspergrid_y = int(math.ceil(restricciones.shape[1] / threadsperblock[1]))
    blockspergrid = (blockspergrid_x, blockspergrid_y)
    sol_global_mem = cuda.to_device(restricciones)
    fact_global_mem = cuda.to_device(factibilidad)
    pondRestricciones_mem = cuda.to_device(pondRestricciones)
    pesos_mem = cuda.to_device(pesos)
    resultado_global_mem = cuda.to_device(ponderaciones)

    #llamar kernel
    kernelPonderarGPU[blockspergrid, threadsperblock](sol_global_mem,fact_global_mem,pesos_mem, pondRestricciones_mem, resultado_global_mem)

    return resultado_global_mem.copy_to_host()

def _calcularColsReparar(ponderaciones):
    resultado = np.zeros((ponderaciones.shape[0], ponderaciones.shape[1]), dtype=np.uint8)
    #colsCandidatas = np.zeros((ponderaciones.shape[0], ponderaciones.shape[1]), dtype=np.uint8)
    colsCandidatasGlobal = np.ones((ponderaciones.shape[0], 10), dtype=np.int32) * -1
    rng_states = create_xoroshiro128p_states(COL, seed=1)
    ponderacionMaxima = np.array([np.max(ponderaciones)])
    #print(f"ponderacion maxima {ponderacionMaxima}")
    #iniciar kernel
    threadsperblock = (NSOL, COL)
    blockspergrid_x = int(math.ceil(ponderaciones.shape[0] / threadsperblock[0]))
    blockspergrid_y = int(math.ceil(ponderaciones.shape[1] / threadsperblock[1]))
    blockspergrid = (blockspergrid_x, blockspergrid_y)
    ponderaciones_global_mem = cuda.to_device(ponderaciones)
    resultado_global_mem = cuda.to_device(resultado)
    colsCandidatasGlobal_mem = cuda.to_device(colsCandidatasGlobal)
    poderacionMaxima_mem = cuda.to_device(ponderacionMaxima)
    rng_states_mem = cuda.to_device(rng_states)


    #llamar kernel
    kernelColsCandidatasGPU[blockspergrid, threadsperblock](ponderaciones_global_mem, poderacionMaxima_mem, colsCandidatasGlobal,rng_states_mem, resultado_global_mem)

    return colsCandidatasGlobal_mem.copy_to_host()

@cuda.jit
def kernelFactibilidadGPU(soluciones, restricciones, resultado):
    
    #leer soluciones y restricciones a procesar
    solTmp = cuda.shared.array(shape=(NSOL, COL), dtype=uint8)
    restTmp = cuda.shared.array(shape=(MRES, COL), dtype=uint8)
    resultadoTmp = cuda.shared.array(shape=(NSOL, MRES), dtype=uint8)
    solIdx, restIdx = cuda.grid(2)

    tx = cuda.threadIdx.x
    ty = cuda.threadIdx.y
    
    if solIdx >= soluciones.shape[0]: return
    if restIdx >= restricciones.shape[0]: return
    
    tmp = 0
    numGCols = int(math.ceil(soluciones.shape[1]/COL))
    for gcol in range(numGCols):
        #solTmp = cuda.shared.array(shape=(NSOL,COL), dtype=int8)
        #restTmp = cuda.shared.array(shape=(MRES,COL), dtype=int8)
        colInicio = gcol*COL
        #colFin = colInicio+COL if colInicio+COL < soluciones.shape[1] else soluciones.shape[1]

        #solTmp[tx,:] = soluciones[solIdx,colInicio:colFin]
        #restTmp[ty,:] = restricciones[restIdx,colInicio:colFin]
        #cuda.syncthreads()

        for c in range(COL):
            col = colInicio+c
            if col >= soluciones.shape[1]: break
            #solTmp[tx,col] = soluciones[solIdx,(gcol*COL)+col]
            #restTmp[ty,col] = restricciones[restIdx,(gcol*COL)+col]

            #cuda.syncthreads()
            #tmp += solTmp[tx,col] * restTmp[ty,col]
            #tmp += solTmp[tx,col] * restTmp[ty,col]
            tmp += soluciones[solIdx,col] * restricciones[restIdx, col]
            if tmp > 0: break
        

        cuda.syncthreads()
        if tmp > 0: break

    resultado[solIdx, restIdx] = tmp


@cuda.jit
def kernelPonderarGPU(restricciones, factibilidad, pesos, pondRestricciones, cReparar):
    
    #leer soluciones y restricciones a procesar
    #solTmp = cuda.shared.array(shape=(NSOL, COL), dtype=uint8)
    restTmp = cuda.shared.array(shape=(COL), dtype=float32)
    pesosTmp = cuda.shared.array(shape=(COL), dtype=float32)
    infactTmp = cuda.shared.array(shape=(NSOL), dtype=float32)
    pondRestriccionesTmp = cuda.shared.array(shape=(1), dtype=float32)
    #resultadoTmp = cuda.shared.array(shape=(NSOL, MRES), dtype=uint8)
    solIdx, colIdx = cuda.grid(2)

    tx = cuda.threadIdx.x
    ty = cuda.threadIdx.y
    bx = cuda.blockIdx.x
    by = cuda.blockIdx.y
    
    if solIdx >= cReparar.shape[0]: return
    if colIdx >= cReparar.shape[1]: return

    #if factibilidad[solIdx, restIdx] == 0: return
    tmp = 0

    if tx == 0:
        pesosTmp[ty] = pesos[colIdx] 
    cuda.syncthreads()

    for res in range(restricciones.shape[0]):
        if tx == 0 and ty == 0:
            pondRestriccionesTmp[0] = pondRestricciones[res]

        if tx == 0:
            restTmp[ty] = restricciones[res,colIdx]
            
        if ty == 0:
            infactTmp[tx] = factibilidad[solIdx,res]

        #print(restTmp[0:])
        cuda.syncthreads()

        if infactTmp[tx] == 0:
            tmp += restTmp[ty] * pondRestriccionesTmp[0]
            #tmp += restTmp[ty]

        cuda.syncthreads()
    if tmp > 0:
        cReparar[solIdx,colIdx] = ( pesosTmp[ty] / tmp )
        #cReparar[solIdx,colIdx] = 1 / tmp


@cuda.jit()
def kernelColsCandidatasGPU(ponderacion, ponderacionMax, colsCandidatasGlobal, rng_states, resultado):
    #if(cuda.threadIdx.x==0 and cuda.threadIdx.y==0):
    #    print(cuda.blockIdx)
    #    print(cuda.blockDim)
    #return

    ponderacionTmp = cuda.shared.array(shape=(NSOL,COL), dtype=float32)
    colsCandidatasBloque = cuda.shared.array(shape=(NSOL, COL), dtype=int32)
    pondCandidatasBloque = cuda.shared.array(shape=(NSOL, COL), dtype=float32)
    colsCandidatasGlobalTmp = cuda.shared.array(shape=(NSOL, 10), dtype=int32)
    pondCandidatasGlobalTmp = cuda.shared.array(shape=(NSOL, 10), dtype=float32)
    #hilosvivos = cuda.shared.array(shape=(NSOL,COL), dtype=uint8)
    #ponderacionMaxTmp = cuda.shared.array(shape=(1), dtype=float32)
    
    #tmpColsCandidatas = cuda.shared.array(shape=(NSOL, 10), dtype=uint8)
    
    

    solIdx, colIdx = cuda.grid(2)

    tx = cuda.threadIdx.x
    ty = cuda.threadIdx.y

    if solIdx >= ponderacion.shape[0]: return
    if colIdx >= ponderacion.shape[1]: return

    #if tx==0 and ty==0: ponderacionMaxTmp[0] = ponderacionMaxima[0]

    #ponderacionTmp[tx,ty] = ponderacion[solIdx,colIdx]
    #cuda.syncthreads()
    #hilosvivos[tx,ty] = 1

    min = -1
    for i in range(int(ponderacion.shape[1]/COL)):
        #if tx==0 and ty ==0:
        #    print(ponderacionTmp.shape)
        #    print(ponderacion.shape)
        #return
        ponderacionTmp[tx,ty] = ponderacion[solIdx, ty+i*COL]
        if ponderacionTmp[tx,ty] == 0: 
            resultado[solIdx,ty+i*COL] = 0
            #hilosvivos[tx,ty] = 0
            continue
        cuda.syncthreads()

        #for j in range(COL):
        #    if minId == -1 or ponderacionTmp[tx,j] < ponderacionTmp[tx,minId]:
        #        minId = ty
        #random = xoroshiro128p_uniform_float32(rng_states, tx)
        #print(f"random {random} < {ponderacionTmp[tx, ty]/ponderacionMaxTmp[0]}")
        if min == -1 or ponderacionTmp[tx, ty] < ponderacionTmp[tx, min]:
            min = colIdx
    
    colsCandidatasBloque[tx,ty] = min
    pondCandidatasBloque[tx,ty] = ponderacionTmp[tx, min]
    

    #if ty!=0: return
    #cuda.syn
    if ty < 10:
        colsCandidatasGlobalTmp[tx, ty] = colsCandidatasGlobal[solIdx, ty]
        pondCandidatasGlobalTmp[tx,ty] = ponderacion[solIdx, colsCandidatasGlobalTmp[tx, ty]]

    cuda.syncthreads()

    if ty==0 and tx==0:
        #print(ponderacionTmp)
        return
    if ty == 0:
        
        for i in range(COL):
            #para cada minimo del bloque
            for j in range(pondCandidatasGlobalTmp.shape[1]):
                #comparado con cada valor de minimos globales
                if pondCandidatasGlobalTmp[tx,j] == -1 or pondCandidatasBloque[tx,i] < pondCandidatasGlobalTmp[tx,j]:
                    #si el minimo global no esta asignado o es mayor al minimo del bloque se inserta el minimo del bloque en 
                    #la posicion del global
                    for a in range(pondCandidatasGlobalTmp.shape[1]-1, j, -1):
                        colsCandidatasGlobalTmp[tx, a] = colsCandidatasGlobalTmp[tx, a-1] 
                        pondCandidatasGlobalTmp[tx, a] = pondCandidatasGlobalTmp[tx, a-1] 
                    colsCandidatasGlobalTmp[tx, j] = colsCandidatasBloque[tx, i] 
                    pondCandidatasGlobalTmp[tx, j] = pondCandidatasBloque[tx, i] 
                    
            
        for i in range(pondCandidatasGlobalTmp.shape[1]):
            colsCandidatasGlobal[tx, i] = colsCandidatasGlobalTmp[tx, i]

        cuda.syncthreads()







        
        #hilosvivos[tx,ty] = 1
        #cuda.syncthreads()
        #tmp = 0
        #for j in range(COL):
        #    tmp += hilosvivos[tx,j]

        #if tmp <= 10:
        #    resultado[solIdx,colIdx] = 1
        #    continue

    #resultado[solIdx,colIdx] = res




