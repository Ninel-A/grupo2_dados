"""
main.py — Punto de entrada del Juego 21 con Dados (version CD)
===============================================================

Este archivo esta dentro de grupo2_dados/ para que el CD
se pueda ejecutar directamente desde esa carpeta:

  cd grupo2_dados
  python main.py

Las 5 opciones cubren los requisitos del informe:
  1. Tabla combinaciones  → EE del Conjunto Problema
  2. Analizar par         → Prototipo (screenshots)
  3. Evaluacion comp.     → Expectiminimax vs Poda Alfa-Beta
  4. Simular turno        → Prototipo P->A en accion
  5. Simular partida      → Prototipo completo J1 vs J2
"""

import sys
import io

# Configurar UTF-8 en Windows
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# Imports planos (funciona directamente desde grupo2_dados/)
from juego      import mostrar_tabla_utilidades, utilidad
from simulacion import (
    mostrar_decision,
    modo_todos_los_pares,
    simular_turno_completo,
    simular_partida,
)

# ─────────────────────────────────────────────
# MENÚ PRINCIPAL
# ─────────────────────────────────────────────

MENU = """
+----------------------------------------------------------+
|        JUEGO 21 CON DADOS  -  Practica IA                |
|   Metodologias: Expectiminimax  vs  Poda Alfa-Beta        |
+----------------------------------------------------------+
|                                                          |
| 1. Ver tabla de combinaciones posibles   [Conj. Problema]|
| 2. Analizar un par de dados              [Prototipo]     |
| 3. Comparar Expectiminimax vs Alfa-Beta  [Evaluacion]    |
| 4. Simular turno de un jugador           [Prototipo P->A]|
| 5. Simular partida completa  J1 vs J2    [Prototipo]     |
|                                                          |
| 0. Salir                                                 |
+----------------------------------------------------------+"""


def pedir_dados() -> tuple:
    """Solicita un par de dados valido (ambos entre 1 y 6)."""
    while True:
        try:
            entrada = input("  Ingresa los dados separados por espacio (ej: 3 5): ").strip()
            partes = entrada.split()
            if len(partes) != 2:
                raise ValueError
            d1, d2 = int(partes[0]), int(partes[1])
            if not (1 <= d1 <= 6 and 1 <= d2 <= 6):
                raise ValueError
            return (d1, d2)
        except (ValueError, IndexError):
            print("  Entrada invalida. Ingresa dos numeros entre 1 y 6. Ej: 2 5")


def pedir_lanzamientos() -> int:
    """Solicita cuantos lanzamientos ya uso el jugador (0, 1 o 2)."""
    while True:
        try:
            n = int(input("  Cuantos lanzamientos ya uso? [0, 1 o 2]: ").strip())
            if 0 <= n <= 2:
                return n
            raise ValueError
        except ValueError:
            print("  Ingresa 0, 1 o 2.")


def main():
    print("\n" + "="*58)
    print("  Bienvenido al Simulador del Juego 21 con Dados")
    print("  Practica 1er Parcial - Inteligencia Artificial")
    print("  Grupo 2: Juego 21 con dos dados")
    print("="*58)

    while True:
        print(MENU)
        opcion = input("  Selecciona una opcion [0-5]: ").strip()

        # Opcion 1 — Tabla combinaciones (EE del Conjunto Problema)
        if opcion == "1":
            mostrar_tabla_utilidades()
            input("\n  Presiona ENTER para continuar...")

        # Opcion 2 — Analizar par concreto (Prototipo / screenshot)
        elif opcion == "2":
            print()
            dados = pedir_dados()
            lanz  = pedir_lanzamientos()
            mostrar_decision(dados, lanz)
            input("\n  Presiona ENTER para continuar...")

        # Opcion 3 — Evaluacion comparativa Expectiminimax vs Alfa-Beta
        elif opcion == "3":
            modo_todos_los_pares()
            input("\n  Presiona ENTER para continuar...")

        # Opcion 4 — Simular turno (P->A en accion)
        elif opcion == "4":
            dados_final = simular_turno_completo("Jugador (Agente IA)")
            u = utilidad(*dados_final)
            print(f"\n  Resultado del turno: {dados_final[0]}-{dados_final[1]}"
                  f"  (Utilidad = {u})")
            input("\n  Presiona ENTER para continuar...")

        # Opcion 5 — Simular partida completa
        elif opcion == "5":
            simular_partida()
            input("\n  Presiona ENTER para continuar...")

        # Opcion 0 — Salir
        elif opcion == "0":
            print("\n  Programa terminado.\n")
            sys.exit(0)

        else:
            print("  Opcion no valida. Escribe un numero entre 0 y 5.")


if __name__ == "__main__":
    main()
