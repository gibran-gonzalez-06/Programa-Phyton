# Importamos las librerías necesarias
import numpy as np
from scipy.optimize import linprog

# Función para solicitar los datos al usuario
def leer_datos():
    print("=== Método Simplex ===")
    tipo = input("¿El problema es de 'maximización' o 'minimización'? ").strip().lower()

    # Número de variables
    n_vars = int(input("¿Cuántas variables tiene la función objetivo? "))

    # Leemos los coeficientes de la función objetivo
    print("\nIntroduce los coeficientes de la función objetivo:")
    c = []
    for i in range(n_vars):
        coef = float(input(f"Coeficiente de x{i+1}: "))
        c.append(coef)
    
    # Si es maximización, cambiamos el signo de los coeficientes
    # porque linprog resuelve solo problemas de minimización
    if tipo == 'maximización':
        c = [-x for x in c]

    # Leemos el número de restricciones
    n_restricciones = int(input("\n¿Cuántas restricciones hay? "))

    A = []  # Matriz de coeficientes
    b = []  # Lado derecho
    signos = []  # Signos de las restricciones

    print("\nIntroduce las restricciones una por una:")
    print("Ejemplo: Para '2x1 + 3x2 <= 10', escribe los coeficientes y el signo")

    for i in range(n_restricciones):
        print(f"\nRestricción {i+1}:")
        fila = []
        for j in range(n_vars):
            coef = float(input(f"Coeficiente de x{j+1}: "))
            fila.append(coef)
        signo = input("Signo de la restricción (<=, >=, =): ").strip()
        valor = float(input("Valor del lado derecho: "))

        # Ajustamos el signo de la desigualdad
        if signo == '<=':
            A.append(fila)
            b.append(valor)
        elif signo == '>=':
            # Multiplicamos por -1 para convertir a <=
            A.append([-x for x in fila])
            b.append(-valor)
        elif signo == '=':
            # Para igualdad, agregamos tanto <= como >=
            A.append(fila)
            b.append(valor)
            A.append([-x for x in fila])
            b.append(-valor)
        else:
            print("Signo no válido. Usa <=, >= o =")
            return None, None, None, None

    return c, A, b, tipo

# Función principal
def main():
    # Leemos los datos del problema
    c, A, b, tipo = leer_datos()
    if c is None:
        return

    # Resolvemos con linprog (por defecto método simplex revisado)
    res = linprog(c, A_ub=A, b_ub=b, method='highs')

    print("\n=== RESULTADOS ===")
    if res.success:
        print("Solución óptima encontrada.")
        for i, val in enumerate(res.x):
            print(f"x{i+1} = {val:.4f}")

        # Recordar: si era de maximización, revertimos el signo
        valor_optimo = res.fun if tipo == 'minimización' else -res.fun
        print(f"\nValor óptimo de la función objetivo: {valor_optimo:.4f}")
    else:
        print("No se encontró una solución óptima. Revisa los datos.")

# Ejecutamos el programa principal
if _name_ == "_main_":
    main()