"""
juego.py — Reglas y función de utilidad del "Juego 21 con Dados"
================================================================

DESCRIPCIÓN DEL JUEGO:
  Dos jugadores compiten lanzando dos dados. El objetivo es obtener
  el par (2, 1) — equivalente al "21" en dominó. En cada turno,
  un jugador puede lanzar los dados hasta MAX_LANZAMIENTOS veces
  y decidir en qué momento plantarse.

CONTENIDO DE ESTE MÓDULO:
  - Constantes del juego (caras del dado, lanzamientos máximos, etc.)
  - Espacio de resultados: todos los 36 pares posibles (d1, d2)
  - Función de utilidad U(d1, d2) definida en el informe
  - Clase EstadoJuego que representa un instante de la partida
  - Función auxiliar para mostrar la tabla completa de utilidades

Referencia: Russell & Norvig, Cap. 5.5; Von Neumann & Morgenstern (1944)
"""

# ─────────────────────────────────────────────
# CONSTANTES DEL JUEGO
# ─────────────────────────────────────────────

# Número de caras de cada dado
CARAS_DADO = 6

# Máximo de lanzamientos que un jugador puede realizar en su turno
# (el jugador puede decidir plantarse antes de llegar a este límite)
MAX_LANZAMIENTOS = 3

# Valor de utilidad de la combinación ganadora (2,1) — el "21"
UTILIDAD_21 = 1000


# ─────────────────────────────────────────────
# ESPACIO DE RESULTADOS (36 pares posibles)
# ─────────────────────────────────────────────

# Al lanzar dos dados de 6 caras hay 6 × 6 = 36 resultados equiprobables.
# Cada resultado (d1, d2) tiene probabilidad P = 1/36 ≈ 0.0278.
TODOS_LOS_RESULTADOS = [
    (d1, d2)
    for d1 in range(1, CARAS_DADO + 1)   # d1 va de 1 a 6
    for d2 in range(1, CARAS_DADO + 1)   # d2 va de 1 a 6
]

# Probabilidad de obtener cualquier par específico (distribución uniforme)
PROBABILIDAD_POR_RESULTADO = 1 / len(TODOS_LOS_RESULTADOS)  # = 1/36


# ─────────────────────────────────────────────
# FUNCIÓN DE UTILIDAD
# ─────────────────────────────────────────────

def utilidad(d1: int, d2: int) -> int:
    """
    Función de utilidad U(d1, d2) definida en el informe del Grupo 2.

    Reglas de valoración (en orden de prioridad):
      1. Par (2,1) o (1,2) → +1000   [Victoria absoluta: el "21"]
      2. Dobles (d1 == d2) → d1 × d2 × 10   [Puntaje alto por dobles]
      3. Cualquier otro par → (d1 + d2) × 5  [Caso general]

    Ejemplos de valores:
      U(2,1) = 1000   U(1,2) = 1000   (caso 1: victoria)
      U(6,6) = 360    U(5,5) = 250    (caso 2: dobles)
      U(6,5) = 55     U(3,2) = 25     (caso 3: general)

    Parámetros:
        d1 (int): Valor del primer dado  [1 .. 6]
        d2 (int): Valor del segundo dado [1 .. 6]

    Retorna:
        int: Valor de utilidad del par (d1, d2)
    """
    # ──────────────────────────────────────────
    # Caso 1: El par (2,1) o (1,2) es el "21"
    # Máxima utilidad posible — el jugador no puede mejorar.
    # ──────────────────────────────────────────
    if (d1, d2) in ((2, 1), (1, 2)):
        return UTILIDAD_21

    # ──────────────────────────────────────────
    # Caso 2: Dobles — ambos dados muestran el mismo valor
    # La multiplicación d1 × d2 premia los dobles altos.
    # ──────────────────────────────────────────
    if d1 == d2:
        return d1 * d2 * 10

    # ──────────────────────────────────────────
    # Caso 3: Cualquier otro resultado
    # La suma de los dados determina el puntaje base.
    # ──────────────────────────────────────────
    return (d1 + d2) * 5


def valor_esperado_lanzamiento() -> float:
    """
    Calcula el valor esperado E[U] al lanzar ambos dados libremente.

    Fórmula:
        E[U] = Σ P(d1, d2) × U(d1, d2)   para los 36 pares posibles
             = (1/36) × Σ U(d1, d2)

    Este valor es útil para comparar si vale la pena lanzar vs. plantarse:
      - Si U(actual) > E[U_lanzar] → conviene PLANTARSE
      - Si U(actual) < E[U_lanzar] → conviene LANZAR

    Retorna:
        float: Valor esperado de un lanzamiento sin restricciones
    """
    # Sumamos las utilidades de todos los 36 pares posibles
    suma_utilidades = sum(utilidad(d1, d2) for d1, d2 in TODOS_LOS_RESULTADOS)

    # El valor esperado es el promedio ponderado (pesos iguales = 1/36)
    return suma_utilidades * PROBABILIDAD_POR_RESULTADO


# ─────────────────────────────────────────────
# CLASE ESTADO DE JUEGO
# ─────────────────────────────────────────────

class EstadoJuego:
    """
    Representa el estado completo de la partida en un instante dado.

    Un "estado" en el árbol de búsqueda contiene toda la información
    necesaria para tomar una decisión: los dados de cada jugador,
    cuántos lanzamientos han usado, y si ya se plantaron.

    Atributos:
        dados_jugador1  (tuple | None): Par (d1,d2) del Jugador 1.
                                        None si aún no ha lanzado.
        dados_jugador2  (tuple | None): Par (d1,d2) del Jugador 2.
                                        None si aún no ha lanzado.
        turno_actual    (int):   1 = turno del Jugador 1,
                                 2 = turno del Jugador 2.
        lanzamientos_j1 (int):  Número de lanzamientos usados por J1.
        lanzamientos_j2 (int):  Número de lanzamientos usados por J2.
        plantado_j1     (bool): True si el Jugador 1 ya se plantó.
        plantado_j2     (bool): True si el Jugador 2 ya se plantó.
    """

    def __init__(self):
        self.dados_jugador1   = None   # Todavía no ha lanzado
        self.dados_jugador2   = None
        self.turno_actual     = 1      # Empieza el Jugador 1
        self.lanzamientos_j1  = 0
        self.lanzamientos_j2  = 0
        self.plantado_j1      = False
        self.plantado_j2      = False

    def es_terminal(self) -> bool:
        """
        La partida termina cuando AMBOS jugadores se han plantado.
        En ese momento se comparan las utilidades para determinar el ganador.
        """
        return self.plantado_j1 and self.plantado_j2

    def ganador(self) -> int:
        """
        Determina el ganador al final de la partida comparando utilidades.

        Retorna:
            1  → Gana el Jugador 1
            2  → Gana el Jugador 2
            0  → Empate
            None → La partida no ha terminado aún
        """
        if not self.es_terminal():
            return None  # La partida sigue en curso

        # Calcular la utilidad final de cada jugador
        u1 = utilidad(*self.dados_jugador1) if self.dados_jugador1 else 0
        u2 = utilidad(*self.dados_jugador2) if self.dados_jugador2 else 0

        if u1 > u2:
            return 1   # Gana Jugador 1
        elif u2 > u1:
            return 2   # Gana Jugador 2
        else:
            return 0   # Empate

    def __repr__(self):
        """Representación legible del estado para depuración."""
        return (
            f"EstadoJuego("
            f"J1={self.dados_jugador1}[lanz={self.lanzamientos_j1}, "
            f"plantado={self.plantado_j1}], "
            f"J2={self.dados_jugador2}[lanz={self.lanzamientos_j2}, "
            f"plantado={self.plantado_j2}], "
            f"turno={self.turno_actual})"
        )


# ─────────────────────────────────────────────
# FUNCIÓN AUXILIAR: TABLA DE UTILIDADES
# ─────────────────────────────────────────────

def mostrar_tabla_utilidades():
    """
    Imprime la tabla completa U(d1, d2) para los 36 pares posibles.

    Formato: filas = d1 (dado 1), columnas = d2 (dado 2).
    Útil para entender y verificar la función de utilidad del informe.
    """
    linea = "═" * 58
    print(f"\n{linea}")
    print("   TABLA DE UTILIDADES  U(d1, d2) — Juego 21 con Dados")
    print(linea)

    # Encabezado de columnas (d2 = 1..6)
    print(f"  {'':>6}", end="")
    for d2 in range(1, 7):
        print(f"  d2={d2}", end="")
    print()
    print("  " + "─" * 53)

    # Filas (d1 = 1..6)
    for d1 in range(1, 7):
        print(f"  d1={d1} ", end="")
        for d2 in range(1, 7):
            u = utilidad(d1, d2)
            # Resaltar el "21" con un marcador visual
            marca = "*" if u == UTILIDAD_21 else " "
            print(f" {u:>5}{marca}", end="")
        print()

    # Valor esperado del lanzamiento libre
    e = valor_esperado_lanzamiento()
    print("─" * 58)
    print(f"  (* = par ganador '21')   E[U al lanzar] = {e:.2f}")
    print(f"{linea}\n")
