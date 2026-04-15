"""
minimax_puro.py — Minimax Puro (sin ninguna poda)
=================================================

DESCRIPCIÓN:
  Esta es la versión MÁS SIMPLE del algoritmo Minimax.
  No tiene ninguna optimización — explora TODOS los nodos del árbol.

  Es el "Algoritmo 1" de la evaluación comparativa del informe:
    ► Metodología 1: MINIMAX (este archivo)        → sin poda
    ► Metodología 2: PODA ALFA-BETA (minimax.py)   → con optimización

  ÁRBOL QUE CONSTRUYE:
    El jugador tiene dos acciones posibles en cada turno:
      A) PLANTARSE → conserva el resultado actual (valor fijo)
      B) LANZAR    → obtiene el valor esperado de un nuevo lanzamiento

    El árbol alterna entre:
      Nodo MAX: Jugador 1 elige la acción que le DA MÁS puntos
      Nodo MIN: Jugador 2 elige la acción que le DA MENOS puntos al J1

  DIFERENCIA CON PODA ALFA-BETA:
    ✗ Minimax puro  → explora TODOS los nodos del árbol (lento)
    ✓ Poda Alfa-Beta → descarta ramas que NO cambian el resultado (rápido)

    IMPORTANTE: el resultado (LANZAR o PLANTARSE) es IDÉNTICO en ambos.
    La poda no cambia la DECISIÓN, solo la hace MÁS RÁPIDA.

  POR QUÉ SE INCLUYE:
    El informe requiere comparar ambas metodologías para evidenciar
    que la Poda Alfa-Beta es más eficiente (menos nodos evaluados)
    sin sacrificar la calidad de la decisión.

Referencia: Russell & Norvig, Inteligencia Artificial (Cap. 5.2)
"""

try:
    from grupo2_dados.juego import (
        utilidad, valor_esperado_lanzamiento, MAX_LANZAMIENTOS, UTILIDAD_21,
    )
except ModuleNotFoundError:
    from juego import (  # cuando se ejecuta directamente desde grupo2_dados/
        utilidad, valor_esperado_lanzamiento, MAX_LANZAMIENTOS, UTILIDAD_21,
    )

# Valor esperado fijo del lanzamiento libre.
# Este valor reemplaza al nodo de azar en la abstracción determinista.
# (igual valor que en minimax.py para comparación justa)
VALOR_ESPERADO_DADO = valor_esperado_lanzamiento()


# ─────────────────────────────────────────────
# FUNCIÓN PRINCIPAL: MINIMAX PURO (SIN PODA)
# ─────────────────────────────────────────────

def minimax_puro(
    dados_actuales: tuple,
    lanzamientos_usados: int,
    es_maximizador: bool,
    profundidad: int,
    _contador: list,
) -> float:
    """
    Minimax básico sin ninguna optimización.

    Explora TODOS los nodos del árbol posible, sin descartar ninguna rama.
    Esto garantiza encontrar el resultado óptimo, pero a un costo mayor
    que la versión con Poda Alfa-Beta.

    Parámetros:
        dados_actuales     (tuple | None):
            El par (d1, d2) visible del jugador. None si no ha lanzado.

        lanzamientos_usados (int):
            Cuántos lanzamientos ya realizó en este turno [0, 1, 2].

        es_maximizador (bool):
            True  → nodo MAX: el jugador quiere el mayor valor posible.
            False → nodo MIN: el jugador quiere el menor valor para el oponente.

        profundidad (int):
            Profundidad máxima de búsqueda. En 0 se evalúa directamente.

        _contador (list):
            Lista [n] para contar cuántos nodos se evalúan en total.
            Se pasa por referencia para acumular en recursión.

    Retorna:
        float: El mejor valor encontrado desde este nodo.
    """
    # Contamos este nodo (para comparar con la versión con poda)
    _contador[0] += 1

    # ══ CASOS BASE ════════════════════════════════════════════════════

    # Caso 1 — Profundidad máxima: evaluar lo que hay en la mano
    if profundidad == 0:
        if dados_actuales is None:
            return VALOR_ESPERADO_DADO   # Sin dados → valor promedio
        return float(utilidad(*dados_actuales))

    # Caso 2 — Sin lanzamientos restantes: el jugador debe plantarse
    if lanzamientos_usados >= MAX_LANZAMIENTOS and dados_actuales is not None:
        return float(utilidad(*dados_actuales))

    # Caso 3 — Victoria con el "21": no se puede mejorar
    if dados_actuales is not None and utilidad(*dados_actuales) == UTILIDAD_21:
        return float(UTILIDAD_21)

    # ══ ACCIONES DISPONIBLES ══════════════════════════════════════════

    # Acción A — PLANTARSE: conservar el resultado actual (si tiene dados)
    if dados_actuales is not None:
        valor_plantarse = float(utilidad(*dados_actuales))
    else:
        valor_plantarse = None  # No puede plantarse sin haber lanzado

    # Acción B — LANZAR: se obtiene el valor esperado del siguiente lanzamiento
    # (abstracción: en lugar de modelar los 36 dados, usamos E[U] fijo)
    valor_lanzar = minimax_puro(
        dados_actuales=None,                          # El resultado cambiará
        lanzamientos_usados=lanzamientos_usados + 1,  # Se consume un lanzamiento
        es_maximizador=es_maximizador,
        profundidad=profundidad - 1,
        _contador=_contador,
    )

    # ══ NODO MAX — Jugador 1: elige la acción de MAYOR valor ══════════
    if es_maximizador:
        mejor = -float("inf")
        if valor_plantarse is not None:
            mejor = max(mejor, valor_plantarse)   # Evalúa PLANTARSE
        mejor = max(mejor, valor_lanzar)          # Evalúa LANZAR
        return mejor
        # NOTAR: no hay poda aquí — se evalúan TODAS las opciones siempre

    # ══ NODO MIN — Jugador 2: elige la acción de MENOR valor ══════════
    else:
        peor = float("inf")
        if valor_plantarse is not None:
            peor = min(peor, valor_plantarse)     # Evalúa PLANTARSE
        peor = min(peor, valor_lanzar)            # Evalúa LANZAR
        return peor
        # NOTAR: tampoco hay poda — se evalúan TODAS las opciones siempre


# ─────────────────────────────────────────────
# INTERFAZ PÚBLICA: DECIDIR ACCIÓN
# ─────────────────────────────────────────────

def decidir_accion_minimax_puro(
    dados_actuales: tuple,
    lanzamientos_usados: int,
    es_maximizador: bool = True,
) -> dict:
    """
    Recomienda LANZAR o PLANTARSE usando Minimax Puro (sin poda).

    Parámetros:
        dados_actuales     (tuple | None): Par (d1,d2) actual. None si no tiene.
        lanzamientos_usados (int): Lanzamientos ya realizados [0..2].
        es_maximizador     (bool): True = Jugador 1, False = Jugador 2.

    Retorna:
        dict con claves:
          'accion'          → "PLANTARSE" o "LANZAR"
          'valor_plantarse' → Utilidad actual (None si sin dados)
          'valor_lanzar'    → Valor minimax de lanzar
          'nodos_evaluados' → Nodos explorados (SIN poda = más que la versión con poda)
    """
    contador = [0]
    profundidad_restante = MAX_LANZAMIENTOS - lanzamientos_usados

    # Calcular el valor de LANZAR con el árbol Minimax Puro
    valor_lanzar = minimax_puro(
        dados_actuales=None,
        lanzamientos_usados=lanzamientos_usados + 1,
        es_maximizador=es_maximizador,
        profundidad=profundidad_restante,
        _contador=contador,
    )

    # Valor de PLANTARSE (si tiene dados en mano)
    if dados_actuales is not None:
        valor_plantarse = float(utilidad(*dados_actuales))
    else:
        valor_plantarse = None

    # Decisión final: la acción con mayor valor
    if valor_plantarse is None:
        accion = "LANZAR"
    elif valor_plantarse >= valor_lanzar:
        accion = "PLANTARSE"
    else:
        accion = "LANZAR"

    return {
        "accion":          accion,
        "valor_plantarse": valor_plantarse,
        "valor_lanzar":    round(valor_lanzar, 2),
        "nodos_evaluados": contador[0],
    }
