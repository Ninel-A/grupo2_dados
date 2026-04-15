"""
simulacion.py — Modos de demostración del Juego 21 con Dados
============================================================

Este módulo conecta los algoritmos con la práctica del informe.

SEGÚN EL INFORME (Practica PP IA 1.pdf), la evaluación comparativa
requiere comparar DOS metodologías de búsqueda:

  ► Metodología 1: EXPECTIMINIMAX (expectiminimax.py)
      - Considera nodos de azar (CHANCE) para un modelo probabilístico completo.
      - Muy costoso en tiempo de ejecución.

  ► Metodología 2: PODA ALFA-BETA (minimax.py)
      - Adaptación usando abstracción determinista y poda.
      - Más rápida y produce el MISMO resultado que Minimax Puro.

La comparación demuestra empíricamente que la Poda Alfa-Beta
es más eficiente: evalúa MENOS nodos para llegar a la MISMA decisión.

MODOS DE USO:
  mostrar_decision()      → Analiza un par concreto con ambos algoritmos
  modo_todos_los_pares()  → Tabla completa de los 36 pares (evaluación comparativa)
  simular_turno_completo()→ Simula un turno usando el mejor algoritmo (Alfa-Beta)
  simular_partida()       → Simula una partida completa J1 vs J2
"""

import random
import time

try:
    from grupo2_dados.juego import (
        utilidad, mostrar_tabla_utilidades, TODOS_LOS_RESULTADOS,
        MAX_LANZAMIENTOS, UTILIDAD_21,
    )
    from grupo2_dados.expectiminimax  import decidir_accion_expectiminimax
    from grupo2_dados.minimax       import decidir_accion_minimax
except ModuleNotFoundError:
    from juego import (
        utilidad, mostrar_tabla_utilidades, TODOS_LOS_RESULTADOS,
        MAX_LANZAMIENTOS, UTILIDAD_21,
    )
    from expectiminimax  import decidir_accion_expectiminimax
    from minimax       import decidir_accion_minimax



# ─────────────────────────────────────────────
# FUNCIÓN AUXILIAR
# ─────────────────────────────────────────────

def lanzar_dados() -> tuple:
    """
    Simula el lanzamiento de dos dados de 6 caras.
    Cada resultado (d1, d2) es igualmente probable.
    """
    return (random.randint(1, 6), random.randint(1, 6))


# ─────────────────────────────────────────────
# MODO 1: ANALIZAR UN PAR CONCRETO
# Relacionado con: Prototipo + Evaluación Comparativa del informe
# ─────────────────────────────────────────────

def mostrar_decision(dados: tuple, lanzamientos_usados: int):
    """
    Muestra la decisión de AMBOS algoritmos para un par de dados dado.

    PROPÓSITO EN EL INFORME:
      Sirve para generar los 'screenshots de la aplicación' que pide
      la sección de Prototipo. También demuestra la Evaluación Comparativa
      al mostrar cuántos nodos usa cada metodología para la misma decisión.

    COLUMNAS DE LA TABLA:
      Algoritmo     → nombre del método (Minimax Puro o Poda Alfa-Beta)
      Acción        → la recomendación: LANZAR o PLANTARSE
      V(plantarse)  → utilidad si se planta ahora (valor del par actual)
      V(lanzar)     → valor esperado calculado si lanza una vez más
      Nodos         → cuántos nodos del árbol se evaluaron
      T(ms)         → tiempo de ejecución en milisegundos

    Parámetros:
        dados              (tuple): Par (d1, d2) a analizar.
        lanzamientos_usados (int): Lanzamientos ya realizados [0..2].
    """
    u_actual = utilidad(*dados)

    # ── Estado actual ──────────────────────────────────────────────────
    print(f"\n{'─'*64}")
    print(f"  Dados actuales        : {dados[0]}  y  {dados[1]}")
    print(f"  Utilidad U({dados[0]},{dados[1]})       : {u_actual}")
    print(f"  Lanzamientos usados   : {lanzamientos_usados} de {MAX_LANZAMIENTOS}")
    print(f"  Lanzamientos restantes: {MAX_LANZAMIENTOS - lanzamientos_usados}")
    print(f"{'─'*64}")

    # ── Ejecutar Metodología 1: EXPECTIMINIMAX ──────────────────────────
    t0 = time.perf_counter()
    res_puro = decidir_accion_expectiminimax(dados, lanzamientos_usados)
    t_puro   = (time.perf_counter() - t0) * 1000

    # ── Ejecutar Metodología 2: PODA ALFA-BETA ────────────────────────
    t0 = time.perf_counter()
    res_ab   = decidir_accion_minimax(dados, lanzamientos_usados)
    t_ab     = (time.perf_counter() - t0) * 1000

    # ── Tabla comparativa ──────────────────────────────────────────────
    print(f"\n  {'Metodologia':<26} {'Accion':<12} {'V(plantarse)':<15}"
          f" {'V(lanzar)':<11} {'Nodos':<8} {'T(ms)'}")
    print(f"  {'─'*78}")
    print(
        f"  {'Expectiminimax':<26} "
        f"{res_puro['accion']:<12} "
        f"{str(res_puro['valor_plantarse']):<15} "
        f"{res_puro['valor_lanzar']:<11} "
        f"{res_puro['nodos_evaluados']:<8} "
        f"{t_puro:.3f}"
    )
    print(
        f"  {'Minimax + Poda Alfa-Beta':<26} "
        f"{res_ab['accion']:<12} "
        f"{str(res_ab['valor_plantarse']):<15} "
        f"{res_ab['valor_lanzar']:<11} "
        f"{res_ab['nodos_evaluados']:<8} "
        f"{t_ab:.3f}"
    )

    # ── Análisis de la comparativa ────────────────────────────────────
    print(f"\n  ANALISIS:")
    if res_puro["accion"] == res_ab["accion"]:
        print(f"  -> Ambos coinciden en: {res_puro['accion']}")
        print(f"     La Poda Alfa-Beta llego a la MISMA decision")
        nodos_puro = res_puro['nodos_evaluados']
        nodos_ab   = res_ab['nodos_evaluados']
        if nodos_puro > nodos_ab:
            ahorro = nodos_puro - nodos_ab
            print(f"     evaluando {ahorro} nodos MENOS ({nodos_puro} vs {nodos_ab}).")
        else:
            print(f"     con {nodos_puro} vs {nodos_ab} nodos evaluados.")
    else:
        # En teoria no deberian diferir — si pasa indica un caso borde
        print(f"  -> Difieren! Puro={res_puro['accion']} / AB={res_ab['accion']}")

    print(f"{'─'*64}")


# ─────────────────────────────────────────────
# MODO 2: TABLA COMPARATIVA DE LOS 36 PARES
# Relacionado con: Evaluación Comparativa del informe (sección IV)
# ─────────────────────────────────────────────

def modo_todos_los_pares():
    """
    Genera la tabla comparativa para los 36 pares posibles de dados.

    PROPÓSITO EN EL INFORME:
      Esta es la EVALUACIÓN COMPARATIVA principal que pide el informe:
      "comparativa de las rutas solución encontradas por cada una de las
       metodologías de búsqueda, a través de los parámetros de evaluación".

      Muestra para CADA par (d1, d2) con 1 lanzamiento ya usado:
        - Utilidad actual U(d1, d2)
        - Decisión del Minimax Puro
        - Decisión del Minimax + Poda Alfa-Beta
        - Nodos evaluados por cada uno (eficiencia)

    EL RESULTADO CLAVE:
      Ambos algoritmos deben COINCIDIR en todos los pares.
      La diferencia está en los NODOS EVALUADOS: la Poda usa menos.
      Esto demuestra que la poda es una MEJORA de eficiencia, no de calidad.
    """
    print("\n" + "="*76)
    print("  EVALUACION COMPARATIVA: Expectiminimax vs. Minimax + Poda Alfa-Beta")
    print("  (Analisis para los 36 pares posibles, con 1 lanzamiento ya usado)")
    print("="*76)
    print(f"  {'Dados':<10} {'U(actual)':<11} {'Expectiminimax':<16}"
          f" {'Poda AB':<12} {'Nodos Expc':<12} {'Nodos AB'}")
    print(f"  {'─'*72}")

    total_nodos_puro = 0
    total_nodos_ab   = 0
    diferencias      = 0

    for (d1, d2) in TODOS_LOS_RESULTADOS:
        u_act    = utilidad(d1, d2)
        res_puro = decidir_accion_expectiminimax((d1, d2), lanzamientos_usados=1)
        res_ab   = decidir_accion_minimax((d1, d2),      lanzamientos_usados=1)

        total_nodos_puro += res_puro["nodos_evaluados"]
        total_nodos_ab   += res_ab["nodos_evaluados"]

        if res_puro["accion"] != res_ab["accion"]:
            diferencias += 1
            marca = "(!)"
        else:
            marca = ""

        print(
            f"  ({d1},{d2}){'':<6} {u_act:<11} "
            f"{res_puro['accion']:<16} "
            f"{res_ab['accion']:<12} "
            f"{res_puro['nodos_evaluados']:<12} "
            f"{res_ab['nodos_evaluados']} {marca}"
        )

    # ── Resumen de la evaluación comparativa ──────────────────────────
    print(f"\n{'='*76}")
    print(f"  RESUMEN DE LA EVALUACION COMPARATIVA")
    print(f"{'─'*76}")
    print(f"  Total nodos evaluados — Expectiminimax   : {total_nodos_puro}")
    print(f"  Total nodos evaluados — Poda Alfa-Beta   : {total_nodos_ab}")
    if total_nodos_puro > 0:
        reduccion = (1 - total_nodos_ab / total_nodos_puro) * 100
        print(f"  Reduccion de nodos con Poda Alfa-Beta    : {reduccion:.1f}%")
    print(f"  Pares con decision diferente             : {diferencias}")
    print(f"")
    print(f"  CONCLUSION:")
    print(f"  La Poda Alfa-Beta llega a la MISma decision (o casi) pero evaluando")
    print(f"  una fraccion significativamente menor de nodos respecto a Expectiminimax.")
    print(f"{'='*76}\n")


# ─────────────────────────────────────────────
# MODO 3: SIMULAR UN TURNO COMPLETO
# Relacionado con: Prototipo del informe (P→A en acción)
# ─────────────────────────────────────────────

def simular_turno_completo(nombre_jugador: str = "Jugador 1") -> tuple:
    """
    Simula un turno completo de un jugador.

    PROPÓSITO EN EL INFORME:
      Demuestra el Prototipo en funcionamiento y el mapa P→A:
        Percepción (dados visibles) → Acción (LANZAR o PLANTARSE)

      En el informe el P→A del Juego 21 es:
        - Resultado contiene (2,1) → DETENERSE (PLANTARSE)
        - Resultado NO contiene (2,1) y puede mejorar → METER AL CUBILETE (LANZAR)

      El agente usa Minimax + Poda Alfa-Beta para decidir (la mejor metodología).

    Retorna:
        tuple: Par (d1, d2) final con el que el jugador termina su turno.
    """
    dados_actuales = None
    lanzamientos   = 0

    print(f"\n  {'─'*50}")
    print(f"  Turno de: {nombre_jugador}")
    print(f"  Algoritmo: Minimax con Poda Alfa-Beta")
    print(f"  {'─'*50}")

    while lanzamientos < MAX_LANZAMIENTOS:
        # ── Paso 1: Lanzar los dados ─────────────────────────────────
        dados_actuales = lanzar_dados()
        lanzamientos  += 1
        u = utilidad(*dados_actuales)

        print(f"\n  Lanzamiento {lanzamientos}/{MAX_LANZAMIENTOS}: "
              f"[ {dados_actuales[0]} - {dados_actuales[1]} ]   "
              f"Utilidad = {u}", end="")

        # Victoria inmediata: obtuvo el par (2,1)
        if u == UTILIDAD_21:
            print(f"  <- OBTUVO EL 21! Victoria inmediata.")
            break

        # ── Paso 2: El algoritmo decide ────────────────────────────
        # (P→A del informe: percepcion de dados → accion)
        decision = decidir_accion_minimax(dados_actuales, lanzamientos)

        print()
        print(f"  Percepcion: dados = {dados_actuales[0]}-{dados_actuales[1]}, "
              f"lanzamientos usados = {lanzamientos}")
        print(f"  Decision  : V(plantarse)={decision['valor_plantarse']}  "
              f"V(lanzar)={decision['valor_lanzar']}  "
              f"-> {decision['accion']}")

        # ── Paso 3: Ejecutar la acción ─────────────────────────────
        if decision["accion"] == "PLANTARSE":
            print(f"  Accion    : El jugador se PLANTA con {dados_actuales[0]}-{dados_actuales[1]}")
            break

        if lanzamientos == MAX_LANZAMIENTOS:
            print(f"  Accion    : Lanzamientos agotados. "
                  f"Resultado final: {dados_actuales[0]}-{dados_actuales[1]}")

    return dados_actuales


# ─────────────────────────────────────────────
# MODO 4: SIMULAR PARTIDA COMPLETA
# Relacionado con: Prototipo del informe (demostración completa)
# ─────────────────────────────────────────────

def simular_partida():
    """
    Simula una partida completa entre dos jugadores.

    PROPÓSITO EN EL INFORME:
      Muestra el Prototipo funcionando de principio a fin.
      Ambos jugadores usan Minimax + Poda Alfa-Beta para decidir.

      Demuestra el criterio de meta del Conjunto Problema:
        PM = "Se ha conseguido la combinación 2 y 1 con los dados?"

    Retorna:
        int: 1 si gana J1, 2 si gana J2, 0 si empate.
    """
    print("\n" + "="*54)
    print("  SIMULACION DE PARTIDA COMPLETA")
    print("  Metodologia: Minimax con Poda Alfa-Beta")
    print("="*54)

    # Turno del Jugador 1
    dados_j1 = simular_turno_completo("Jugador 1")
    # Turno del Jugador 2
    dados_j2 = simular_turno_completo("Jugador 2")

    # Comparar resultados finales
    u1 = utilidad(*dados_j1)
    u2 = utilidad(*dados_j2)

    print(f"\n  {'='*50}")
    print(f"  RESULTADO FINAL")
    print(f"  {'─'*50}")
    print(f"  Jugador 1  : {dados_j1[0]} - {dados_j1[1]}   Utilidad = {u1}")
    print(f"  Jugador 2  : {dados_j2[0]} - {dados_j2[1]}   Utilidad = {u2}")
    print(f"  {'─'*50}")

    if u1 > u2:
        print(f"  GANA el Jugador 1  ({u1} > {u2})")
        ganador = 1
    elif u2 > u1:
        print(f"  GANA el Jugador 2  ({u2} > {u1})")
        ganador = 2
    else:
        print(f"  EMPATE  ({u1} = {u2})")
        ganador = 0

    print("="*54)
    return ganador
