"""
minimax.py — Minimax con Poda Alfa-Beta para el Juego 21 con Dados
==================================================================

DESCRIPCIÓN:
  Implementa el algoritmo Minimax clásico ADAPTADO a un juego con azar.

LIMITACIÓN FUNDAMENTAL DE MINIMAX EN JUEGOS ESTOCÁSTICOS:
  Minimax NO puede modelar el azar de los dados directamente porque:

    1. Asume que el "dado" actúa como un ADVERSARIO que elige el
       resultado más desfavorable para el jugador actual.
    2. Esto es IRREAL — los dados son aleatorios, no adversariales.
    3. Consecuencia: el agente resultante es EXCESIVAMENTE CONSERVADOR
       (pesimista), y tiende a plantarse cuando en realidad convendría lanzar.

SOLUCIÓN ADOPTADA (Abstracción Determinista):
  Para hacer funcionar Minimax en este juego, se usa el "valor esperado"
  del lanzamiento como si fuera un resultado fijo y conocido:

    E[U al lanzar] = (1/36) × Σ U(d1, d2) ≈ un valor constante

  Esto convierte el árbol estocástico en un árbol determinístico plano,
  sacrificando precisión a cambio de simplicidad.

  → Compare las decisiones de este módulo con expectiminimax.py
    para observar las diferencias en los casos límite.

ÁRBOL DE DECISIÓN (simplificado):
  Turno J1 (MAX):
    ├─ PLANTARSE → U(dados_actuales)
    └─ LANZAR    → E[U] (valor esperado fijo, nodo determinístico)
  Turno J2 (MIN):
    ├─ PLANTARSE → -U(dados_actuales)
    └─ LANZAR    → -E[U]

PODA ALFA-BETA:
  Reduce la complejidad de O(b^d) a O(b^(d/2)) en el mejor caso.
  En este árbol pequeño el ahorro es menor, pero el principio es válido.

Referencia: Russell & Norvig, Cap. 5.2–5.3
"""

try:
    from grupo2_dados.juego import (
        utilidad, valor_esperado_lanzamiento, MAX_LANZAMIENTOS, UTILIDAD_21,
    )
except ModuleNotFoundError:
    from juego import (
        utilidad, valor_esperado_lanzamiento, MAX_LANZAMIENTOS, UTILIDAD_21,
    )


# Valor esperado fijo del lanzamiento (calculado una sola vez al importar).
# Este valor reemplaza a los nodos CHANCE en la abstracción determinista.
VALOR_ESPERADO_DADO = valor_esperado_lanzamiento()


# ─────────────────────────────────────────────
# FUNCIÓN PRINCIPAL: MINIMAX CON ALFA-BETA
# ─────────────────────────────────────────────

def minimax_ab(
    dados_actuales: tuple,
    lanzamientos_usados: int,
    es_maximizador: bool,
    alfa: float,
    beta: float,
    profundidad: int,
    _contador: list,
) -> float:
    """
    Algoritmo Minimax con Poda Alfa-Beta (adaptado para juego con dados).

    Parámetros:
        dados_actuales     (tuple | None):
            Par (d1, d2) visible del jugador en turno.
            None si todavía no ha lanzado en este turno.

        lanzamientos_usados (int):
            Cuántos lanzamientos ya realizó el jugador en este turno.
            Cuando llega a MAX_LANZAMIENTOS, debe plantarse.

        es_maximizador (bool):
            True  → el nodo es MAX (Jugador 1 quiere maximizar).
            False → el nodo es MIN (Jugador 2 quiere minimizar la utilidad de J1).

        alfa (float):
            El mejor valor garantizado para MAX hasta ahora.
            Inicializar con -infinito en la llamada raíz.

        beta (float):
            El mejor valor garantizado para MIN hasta ahora.
            Inicializar con +infinito en la llamada raíz.

        profundidad (int):
            Límite de profundidad del árbol de búsqueda.
            Cuando llega a 0 se evalúa la utilidad directamente.

        _contador (list):
            Lista de UN elemento [n] para contar nodos evaluados.
            Se pasa por referencia para acumular conteos en recursión.

    Retorna:
        float: Valor minimax del nodo actual.
    """
    # ── Contamos este nodo para las estadísticas de rendimiento ─────────
    _contador[0] += 1

    # ═══════════════════════════════════════════════════════════════════
    # CASOS BASE: condiciones donde la recursión se detiene
    # ═══════════════════════════════════════════════════════════════════

    # Caso base 1: Profundidad máxima alcanzada
    # → Se evalúa directamente la situación actual.
    if profundidad == 0:
        if dados_actuales is None:
            # Sin resultado aún, se devuelve el valor esperado (promedio)
            return VALOR_ESPERADO_DADO
        return float(utilidad(*dados_actuales))

    # Caso base 2: El jugador agotó todos sus lanzamientos
    # → Debe plantarse con los dados que tiene.
    if lanzamientos_usados >= MAX_LANZAMIENTOS and dados_actuales is not None:
        return float(utilidad(*dados_actuales))

    # Caso base 3: El jugador obtuvo el "21"
    # → Es la utilidad máxima, no tiene sentido seguir analizando.
    if dados_actuales is not None and utilidad(*dados_actuales) == UTILIDAD_21:
        return float(UTILIDAD_21)

    # ═══════════════════════════════════════════════════════════════════
    # ACCIONES DISPONIBLES: PLANTARSE o LANZAR
    # ═══════════════════════════════════════════════════════════════════

    # Acción A — PLANTARSE: conservar los dados actuales.
    # Solo disponible si el jugador ya tiene un resultado.
    if dados_actuales is not None:
        valor_plantarse = float(utilidad(*dados_actuales))
    else:
        valor_plantarse = None  # No puede plantarse sin haber lanzado

    # Acción B — LANZAR: en Minimax usamos el valor esperado fijo
    # (abstracción determinista — no modelamos los 36 resultados).
    # El siguiente nivel del árbol analiza qué hacer con ese valor esperado.
    valor_lanzar = minimax_ab(
        dados_actuales=None,          # El resultado cambiará (simulado con E[U])
        lanzamientos_usados=lanzamientos_usados + 1,
        es_maximizador=es_maximizador,
        alfa=alfa,
        beta=beta,
        profundidad=profundidad - 1,
        _contador=_contador,
    )

    # ═══════════════════════════════════════════════════════════════════
    # NODO MAXIMIZADOR (Jugador 1): elegir la acción de mayor valor
    # ═══════════════════════════════════════════════════════════════════
    if es_maximizador:
        mejor_valor = -float("inf")

        # Evaluar PLANTARSE (si tiene dados disponibles)
        if valor_plantarse is not None:
            mejor_valor = max(mejor_valor, valor_plantarse)
            alfa = max(alfa, mejor_valor)

        # Evaluar LANZAR
        mejor_valor = max(mejor_valor, valor_lanzar)
        alfa = max(alfa, mejor_valor)

        # ── Poda Beta ─────────────────────────────────────────────────
        # Si alfa ≥ beta, el nodo MIN padre ya tiene una opción mejor.
        # No tiene sentido explorar más ramas de este nodo.
        if beta <= alfa:
            return mejor_valor  # ✂️ Poda Beta — se corta la rama

        return mejor_valor

    # ═══════════════════════════════════════════════════════════════════
    # NODO MINIMIZADOR (Jugador 2): elegir la acción de menor valor
    # (en juego de suma cero, minimizar la utilidad de J1 = maximizar la de J2)
    # ═══════════════════════════════════════════════════════════════════
    else:
        peor_valor = float("inf")

        # Evaluar PLANTARSE
        if valor_plantarse is not None:
            peor_valor = min(peor_valor, valor_plantarse)
            beta = min(beta, peor_valor)

        # Evaluar LANZAR
        peor_valor = min(peor_valor, valor_lanzar)
        beta = min(beta, peor_valor)

        # ── Poda Alfa ─────────────────────────────────────────────────
        # Si beta ≤ alfa, el nodo MAX padre ya tiene una opción mejor.
        if beta <= alfa:
            return peor_valor  # ✂️ Poda Alfa — se corta la rama

        return peor_valor


# ─────────────────────────────────────────────
# INTERFAZ PÚBLICA: DECIDIR ACCIÓN
# ─────────────────────────────────────────────

def decidir_accion_minimax(
    dados_actuales: tuple,
    lanzamientos_usados: int,
    es_maximizador: bool = True,
) -> dict:
    """
    Interfaz principal del Minimax: recomienda LANZAR o PLANTARSE.

    Evalúa el árbol Minimax desde el nodo actual y compara:
      - La utilidad de PLANTARSE (directa, si hay dados disponibles)
      - El valor Minimax de LANZAR (calculado recursivamente)

    Luego recomienda la acción con mayor valor para el maximizador.

    Parámetros:
        dados_actuales     (tuple | None): Par (d1,d2) actual o None.
        lanzamientos_usados (int): Lanzamientos ya realizados [0..2].
        es_maximizador     (bool): True = Jugador 1, False = Jugador 2.

    Retorna:
        dict con las siguientes claves:
          'accion'          → "PLANTARSE" o "LANZAR"
          'valor_plantarse' → Utilidad si se planta (None si sin dados)
          'valor_lanzar'    → Valor Minimax de lanzar (abstracción det.)
          'nodos_evaluados' → Total de nodos explorados en el árbol
    """
    contador = [0]  # Lista mutable para acumular el conteo en recursión

    # Profundidad de búsqueda: lanzamientos restantes disponibles
    profundidad_restante = MAX_LANZAMIENTOS - lanzamientos_usados

    # Evaluar el árbol Minimax para la acción LANZAR
    valor_lanzar = minimax_ab(
        dados_actuales=None,              # Valor post-lanzamiento (desconocido → E[U])
        lanzamientos_usados=lanzamientos_usados + 1,
        es_maximizador=es_maximizador,
        alfa=-float("inf"),              # α inicial = -∞
        beta=float("inf"),               # β inicial = +∞
        profundidad=profundidad_restante,
        _contador=contador,
    )

    # Valor de PLANTARSE: utilidad directa del par actual
    if dados_actuales is not None:
        valor_plantarse = float(utilidad(*dados_actuales))
    else:
        valor_plantarse = None  # Sin dados, no puede plantarse

    # ── Decisión: comparar ambas opciones ─────────────────────────────
    if valor_plantarse is None:
        # No hay dados → obligatorio lanzar
        accion = "LANZAR"
    elif valor_plantarse >= valor_lanzar:
        # Plantarse da igual o más valor que lanzar → PLANTARSE
        accion = "PLANTARSE"
    else:
        # Lanzar tiene mayor valor esperado → LANZAR
        accion = "LANZAR"

    return {
        "accion":           accion,
        "valor_plantarse":  valor_plantarse,
        "valor_lanzar":     round(valor_lanzar, 2),
        "nodos_evaluados":  contador[0],
    }
