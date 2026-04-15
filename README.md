
# Guía del Programa: Juego 21 con Dados

## Universidad Mayor de San Simón

**Facultad de Ciencias y Tecnología** **Departamento de Informática y Sistemas**

  * **Materia:** Inteligencia Artificial
  * **Grupo:** 2
  * **Metodologías:** Expectiminimax vs. Poda Alfa-Beta
  * **Lenguaje:** Python 3
  * **Fecha:** Abril 2026

-----

### Integrantes

  * Alcocer Zabala Ninel Daniela
  * Alvarado Mamani Jhonatan
  * Anave Zenteno Alejandro Robert
  * Aranibar Mamani Madahi Angeles
  * Montaño Frias Andres
  * Perez Brañez Israel Emanuel
  * Rodriguez Peña Jose Miguel

**Cochabamba — Bolivia**

-----

## Índice

1.  [Descripción del Programa]()
2.  [Cómo Ejecutar el Programa]()
3.  [Opción 1 — Tabla de Combinaciones]()
4.  [Opción 2 — Analizar un Par de Dados]()
5.  [Opción 3 — Evaluación Comparativa]()
6.  [Opción 4 — Simular Turno (P → A)]()
7.  [Opción 5 — Simular Partida Completa]()
8.  [Los Dos Algoritmos]()
9.  [Estructura de Archivos]()
10. [Secuencia para la Presentación]()
11. [Referencias]()

-----

## 1\. Descripción del Programa

El programa simula el **Juego 21 con Dados** aplicando dos algoritmos de búsqueda adversarial estudiados en el libro de Russell & Norvig:

  * **Expectiminimax:** Manejo completo del azar (archivo `expectiminimax.py`).
  * **Minimax con Poda Alfa-Beta:** Optimización de búsqueda (archivo `minimax.py`).

### Reglas del Juego

Dos jugadores compiten lanzando dos dados de 6 caras. El objetivo es obtener el par **(2, 1)** — el "21" del dominó. Cada jugador tiene hasta **3 lanzamientos** por turno y debe decidir si se planta o arriesga.

-----

## 2\. Cómo Ejecutar el Programa

### 2.1. Desde la terminal

Navega a la carpeta del proyecto y ejecuta:

```bash
cd grupo2_dados
python main.py
```

### 2.2. Requisitos

  * Python 3.8 o superior.
  * Si la terminal muestra caracteres extraños (problemas de codificación), usa:
    ```bash
    python -X utf8 main.py
    ```

-----

## 3\. Opción 1 — Tabla de Combinaciones

Esta opción muestra el **Espacio de Estados (EE)** y la **Función de Utilidad $U(d_1, d_2)$**:

$$U(d_1, d_2) = \begin{cases} 1000 & \text{si } (d_1, d_2) \in \{(2,1), (1,2)\} \\ (d_1 \times d_2 \times 10) & \text{si } d_1 = d_2 \\ (d_1 + d_2) \times 5 & \text{en cualquier otro caso} \end{cases}$$

| Par de Dados | Utilidad | Tipo |
| :--- | :--- | :--- |
| (2, 1) o (1, 2) | 1000 | Victoria absoluta |
| (6, 6) | 360 | Dobles |
| (1, 1) | 10 | Dobles (mínimo) |
| (6, 5) | 55 | General |

> **Nota:** El valor esperado $E[U] \approx 109.17$ es el umbral de decisión.

-----

## 4\. Opción 2 — Analizar un Par de Dados

Permite ingresar manualmente los dados y ver la decisión de la IA.

**Ejemplo de salida para (3, 2):**

```text
Dados actuales: 3 y 2 | Utilidad: 25 | Lanzamientos usados: 0/3
-----------------------------------------------------------------------
Metodología       Acción    V(plantar)  V(lanzar)   Nodos
Expectiminimax    LANZAR    25.0        109.17      71
Poda Alfa-Beta    LANZAR    25.0        109.17      3
-----------------------------------------------------------------------
ANÁLISIS: Ambos coinciden en LANZAR.
```

-----

## 5\. Opción 3 — Evaluación Comparativa

Analiza los 36 pares posibles simultáneamente con ambos algoritmos para comparar eficiencia.

| Parámetro | Expectiminimax | Poda Alfa-Beta |
| :--- | :--- | :--- |
| **Decisiones** | 36/36 correctas | 36/36 correctas |
| **Eficiencia** | Menor (recorre todo) | **Mayor (poda ramas)** |
| **Complejidad** | $O(b^m n^m)$ | $O(b^{m/2})$ |

-----

## 6\. Opción 4 — Simular Turno (P → A)

Demuestra el mapa **Percepción → Acción** en tiempo real.

  * **Percepción:** El agente ve los dados y los tiros restantes.
  * **Acción:** Si $V(lanzar) > V(plantar)$, elige LANZAR.

-----

## 7\. Opción 5 — Simular Partida Completa

Muestra un enfrentamiento **Jugador 1 vs Jugador 2**. El programa determina el ganador basándose en quién se acercó más a la utilidad máxima o si alguien obtuvo el "21".

-----

## 8\. Los Dos Algoritmos

### 8.1. Expectiminimax

Modela la incertidumbre mediante nodos **CHANCE**.

```python
# Pseudocódigo simplificado
SI tipo_nodo es CHANCE:
    suma_esperada = 0
    PARA CADA resultado r:
        suma_esperada += Prob(r) * EXPECTIMINIMAX(r, SIGUIENTE_TURNO)
    RETORNAR suma_esperada
```

### 8.2. Minimax con Poda Alfa-Beta

Optimiza el tiempo de respuesta descartando opciones que no mejoran el resultado ya encontrado.

```python
# Pseudocódigo de Poda
SI esMax:
    mejor = -infinito
    PARA CADA accion:
        mejor = max(mejor, MINIMAX_AB(accion, alfa, beta))
        alfa = max(alfa, mejor)
        SI beta <= alfa: ROMPER  # Poda
```

-----

## 9\. Estructura de Archivos (CD)

| Archivo | Contenido |
| :--- | :--- |
| `main.py` | Punto de entrada (menú interactivo). |
| `juego.py` | Reglas, utilidad $U(d_1, d_2)$ y estados. |
| `expectiminimax.py` | Implementación del algoritmo probabilístico. |
| `minimax.py` | Implementación con Poda Alfa-Beta. |
| `simulacion.py` | Funciones de apoyo para las demostraciones. |

-----

## 10\. Secuencia para la Presentación

1.  **Mostrar Tabla (Opción 1):** Explicar el Espacio de Estados.
2.  **Caso Perdedor (Opción 2 con 1-1):** Mostrar que la IA decide arriesgar.
3.  **Caso Ganador (Opción 2 con 2-1):** Mostrar que la IA se planta de inmediato.
4.  **Comparativa (Opción 3):** Demostrar que Alfa-Beta es más rápido pero igual de efectivo.
5.  **Simulación (Opción 5):** Ejecutar una partida completa.

-----

## 11\. Referencias

1.  Russell & Norvig (2004). *IA: Un Enfoque Moderno*. Cap 5.
2.  Nilsson, N. J. (2001). *Inteligencia Artificial: Una Nueva Síntesis*.
3.  GeeksforGeeks (2026). *Alpha-Beta Pruning in Adversarial Search*.
