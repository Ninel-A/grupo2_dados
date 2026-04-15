"""
expectiminimax.py — Expectiminimax para el Juego 21 con Dados
=============================================================

DESCRIPCIÓN:
  Implementa el algoritmo Expectiminimax con TRES tipos de nodos:

  ┌───────────┬────────────────────────────────────────────────────────────┐
  │ Tipo      │ Descripción                                                │
  ├───────────┼────────────────────────────────────────────────────────────┤
  │ NODO_MAX  │ Jugador 1 elige la acción que MAXIMIZA su utilidad         │
  │ NODO_MIN  │ Jugador 2 elige la acción que MINIMIZA la utilidad de J1   │
  │ NODO_CHANCE│ Nodo de azar: E[V] = Σ P(s)·V(s) sobre los 36 resultados │
  └───────────┴────────────────────────────────────────────────────────────┘

¿POR QUÉ EXPECTIMINIMAX ES SUPERIOR A MINIMAX AQUÍ?

  Minimax puro asume que el "adversario" controla los dados.
  Expectiminimax trata el dado como lo que realmente es: una variable
  aleatoria uniforme con 36 resultados equiprobables (P = 1/36 cada uno).

  Consecuencia práctica:
    - Minimax es DEMASIADO CONSERVADOR (pesimista)
    - Expectiminimax toma decisiones más alineadas con la realidad

ÁRBOL DE DECISIÓN (flujo de nodos):

  MAX (J1 decide: plantar o lanzar)
   ├─ PLANTARSE → U(dados_actuales) ← valor terminal
   └─ LANZAR    → CHANCE (dado se lanza)
                    ├─ (1,1) P=1/36 → MAX (J1 decide de nuevo)
                    ├─ (1,2) P=1/36 → MAX
                    ├─ (2,1) P=1/36 → MAX   [utilidad=1000, se detiene]
                    │      ...
                    └─ (6,6) P=1/36 → MAX
                   E[V] = Σ P(d1,d2) × V(resultado)

Referencia: Russell & Norvig, Cap. 5.5; Von Neumann & Morgenstern (1944)
"""

try:
    from grupo2_dados.juego import (
        utilidad, TODOS_LOS_RESULTADOS, PROBABILIDAD_POR_RESULTADO,
        MAX_LANZAMIENTOS, UTILIDAD_21,
    )
except ModuleNotFoundError:
    from juego import (
        utilidad, TODOS_LOS_RESULTADOS, PROBABILIDAD_POR_RESULTADO,
        MAX_LANZAMIENTOS, UTILIDAD_21,
    )

# ─────────────────────────────────────────────
# TIPOS DE NODO (constantes de identificación)
# ─────────────────────────────────────────────
NODO_MAX    = "MAX"     # El jugador actual maximiza su utilidad
NODO_MIN    = "MIN"     # El jugador actual minimiza la utilidad del oponente
NODO_CHANCE = "CHANCE"  # Nodo de azar: pondera todos los resultados posibles


# ─────────────────────────────────────────────
# FUNCIÓN PRINCIPAL: EXPECTIMINIMAX RECURSIVO
# ─────────────────────────────────────────────

def expectiminimax(
    tipo_nodo: str,
    dados_actuales: tuple,
    lanzamientos_usados: int,
    profundidad: int,
    _contador: list,
) -> float:
    """
    Algoritmo Expectiminimax con nodos MAX, MIN y CHANCE.

    La recursión sigue este patrón:
      MAX → decide si LANZAR o PLANTARSE
        └─ si LANZA → CHANCE (pondera los 36 resultados del dado)
                         └─ cada resultado → MAX (decide de nuevo)

    Parámetros:
        tipo_nodo (str):
            Tipo del nodo actual: NODO_MAX, NODO_MIN o NODO_CHANCE.

        dados_actuales (tuple | None):
            Par (d1, d2) visible del jugador en turno.
            None si todavía no ha lanzado en esta rama del árbol.

        lanzamientos_usados (int):
            Cuántos lanzamientos ya realizó el jugador en este turno.
            Cuando llega a MAX_LANZAMIENTOS el jugador debe plantarse.

        profundidad (int):
            Límite de profundidad del árbol.
            Cuando llega a 0 se evalúa la utilidad directamente.

        _contador (list):
            Lista de UN elemento [n] para contar nodos explorados.
            Se comparte entre todas las llamadas recursivas.

    Retorna:
        float: Valor de utilidad esperado del nodo actual.
    """
    # ── Contamos este nodo para las estadísticas ─────────────────────
    _contador[0] += 1

    # ═══════════════════════════════════════════════════════════════════
    # CASOS BASE: condiciones donde la recursión se detiene
    # ═══════════════════════════════════════════════════════════════════

    # Caso base 1: Profundidad máxima alcanzada
    # → Evaluamos la situación actual sin seguir explorando.
    if profundidad == 0:
        if dados_actuales is None:
            return 0.0  # Sin resultado: valor neutro
        return float(utilidad(*dados_actuales))

    # Caso base 2: El jugador agotó sus lanzamientos con dados disponibles
    # → No puede lanzar más, debe aceptar el resultado actual.
    if lanzamientos_usados >= MAX_LANZAMIENTOS and dados_actuales is not None:
        return float(utilidad(*dados_actuales))

    # Caso base 3: El jugador obtuvo el "21" — victoria absoluta
    # → Es la utilidad máxima posible (1000). No tiene sentido seguir.
    if dados_actuales is not None and utilidad(*dados_actuales) == UTILIDAD_21:
        return float(UTILIDAD_21)

    # ═══════════════════════════════════════════════════════════════════
    # NODO CHANCE: el dado se lanza, calculamos el valor esperado real
    # ═══════════════════════════════════════════════════════════════════
    if tipo_nodo == NODO_CHANCE:
        #
        # Fórmula del valor esperado:
        #   E[V] = Σ P(d1,d2) × V(siguente_nodo(d1,d2))
        #        = (1/36) × Σ V(d1,d2)   para todos los 36 pares
        #
        # Cada par (d1,d2) es igualmente probable → P = 1/36
        #
        valor_esperado = 0.0

        for (d1, d2) in TODOS_LOS_RESULTADOS:
            # El jugador recibe el resultado (d1,d2) y decide qué hacer
            # → pasa a un nodo MAX (o MIN según el turno)
            valor_resultado = expectiminimax(
                tipo_nodo=NODO_MAX,           # El jugador ahora decide con el nuevo par
                dados_actuales=(d1, d2),      # El resultado visible del lanzamiento
                lanzamientos_usados=lanzamientos_usados,
                profundidad=profundidad - 1,
                _contador=_contador,
            )
            # Acumulamos: P(d1,d2) × V(d1,d2) = 1/36 × V(d1,d2)
            valor_esperado += PROBABILIDAD_POR_RESULTADO * valor_resultado

        return valor_esperado  # E[V] = Σ P(s) × V(s)

    # ═══════════════════════════════════════════════════════════════════
    # NODO MAX: el Jugador 1 elige la acción que maximiza su utilidad
    # ═══════════════════════════════════════════════════════════════════
    if tipo_nodo == NODO_MAX:
        #
        # Acciones disponibles:
        #   A) PLANTARSE → valor fijo: U(dados_actuales)
        #   B) LANZAR    → pasa a NODO_CHANCE (ponderación de 36 resultados)
        #
        # MAX elige la acción con MAYOR valor esperado.
        #

        # Acción A — PLANTARSE (solo si tiene dados en mano)
        if dados_actuales is not None:
            valor_si_se_planta = float(utilidad(*dados_actuales))
        else:
            # Sin dados: no puede plantarse → valor -∞ para descartar esta opción
            valor_si_se_planta = -float("inf")

        # Acción B — LANZAR (solo si le quedan lanzamientos disponibles)
        if lanzamientos_usados < MAX_LANZAMIENTOS:
            # Al lanzar → el resultado es incierto → NODO_CHANCE
            valor_si_lanza = expectiminimax(
                tipo_nodo=NODO_CHANCE,
                dados_actuales=dados_actuales,   # Los dados previos (antes del lanzamiento)
                lanzamientos_usados=lanzamientos_usados + 1,  # Consumimos un lanzamiento
                profundidad=profundidad - 1,
                _contador=_contador,
            )
        else:
            # Sin lanzamientos restantes → no puede lanzar → valor -∞
            valor_si_lanza = -float("inf")

        # MAX elige la acción con MAYOR valor (PLANTARSE o LANZAR)
        return max(valor_si_se_planta, valor_si_lanza)

    # ═══════════════════════════════════════════════════════════════════
    # NODO MIN: el Jugador 2 elige la acción que minimiza la utilidad de J1
    # (En juego de suma cero: minimizar U(J1) = maximizar U(J2))
    # ═══════════════════════════════════════════════════════════════════
    if tipo_nodo == NODO_MIN:
        #
        # Misma lógica que NODO_MAX pero invirtiendo la elección:
        # MIN elige la acción con MENOR valor (desde la perspectiva de J1).
        #

        # Acción A — PLANTARSE
        if dados_actuales is not None:
            valor_si_se_planta = float(utilidad(*dados_actuales))
        else:
            # Sin dados → MIN preferiría plantarse, pero no puede → +∞ para ignorar
            valor_si_se_planta = float("inf")

        # Acción B — LANZAR
        if lanzamientos_usados < MAX_LANZAMIENTOS:
            valor_si_lanza = expectiminimax(
                tipo_nodo=NODO_CHANCE,
                dados_actuales=dados_actuales,
                lanzamientos_usados=lanzamientos_usados + 1,
                profundidad=profundidad - 1,
                _contador=_contador,
            )
        else:
            valor_si_lanza = float("inf")

        # MIN elige la acción con MENOR valor (la más desfavorable para J1)
        return min(valor_si_se_planta, valor_si_lanza)

    # Si el tipo de nodo no es ninguno de los tres válidos → error
    raise ValueError(
        f"Tipo de nodo desconocido: '{tipo_nodo}'. "
        f"Usa NODO_MAX, NODO_MIN o NODO_CHANCE."
    )


# ─────────────────────────────────────────────
# INTERFAZ PÚBLICA: DECIDIR ACCIÓN
# ─────────────────────────────────────────────

def decidir_accion_expectiminimax(
    dados_actuales: tuple,
    lanzamientos_usados: int,
    es_maximizador: bool = True,
) -> dict:
    """
    Interfaz principal del Expectiminimax: recomienda LANZAR o PLANTARSE.

    A diferencia de decidir_accion_minimax(), esta función evalúa
    TODOS los 36 resultados posibles del dado, ponderados por
    su probabilidad real (1/36 cada uno).

    La decisión final surge de comparar:
      V(PLANTARSE) = U(dados_actuales)              [valor fijo, sin incertidumbre]
      V(LANZAR)    = E[V] = Σ (1/36) × V(d1,d2)   [valor esperado real del árbol]

    Parámetros:
        dados_actuales     (tuple | None): Par (d1,d2) actual. None si sin dados.
        lanzamientos_usados (int): Lanzamientos ya realizados en este turno [0..2].
        es_maximizador     (bool): True = Jugador 1, False = Jugador 2.

    Retorna:
        dict con las siguientes claves:
          'accion'          → "PLANTARSE" o "LANZAR"
          'valor_plantarse' → Utilidad del par actual (None si sin dados)
          'valor_lanzar'    → Valor esperado real del lanzamiento (Expectiminimax)
          'nodos_evaluados' → Total de nodos explorados en el árbol
    """
    contador = [0]  # Lista mutable compartida entre todas las llamadas recursivas

    # El jugador lanza → pasa primero por un NODO_CHANCE
    # (el dado determina el resultado antes de que el jugador decida de nuevo)
    valor_lanzar = expectiminimax(
        tipo_nodo=NODO_CHANCE,          # El dado se lanza primero
        dados_actuales=dados_actuales,  # Dados previos al lanzamiento
        lanzamientos_usados=lanzamientos_usados + 1,  # Se consume un lanzamiento
        profundidad=MAX_LANZAMIENTOS * 2 + 2,         # Profundidad generosa
        _contador=contador,
    )

    # Valor de PLANTARSE: directo, sin incertidumbre
    if dados_actuales is not None:
        valor_plantarse = float(utilidad(*dados_actuales))
    else:
        valor_plantarse = None  # Sin dados: no puede plantarse

    # ── Decisión final ────────────────────────────────────────────────
    if valor_plantarse is None:
        accion = "LANZAR"                            # Sin dados → obligatorio lanzar
    elif valor_plantarse >= valor_lanzar:
        accion = "PLANTARSE"                         # Quedarse es mejor o igual
    else:
        accion = "LANZAR"                            # Lanzar tiene mayor valor esperado

    return {
        "accion":           accion,
        "valor_plantarse":  valor_plantarse,
        "valor_lanzar":     round(valor_lanzar, 2),
        "nodos_evaluados":  contador[0],
    }
