import numpy as np
import random
import sys
from collections import Counter

def check_isomorphism(adj1, adj2):
    if adj1.shape != adj2.shape or np.sum(adj1) != np.sum(adj2):
        return False
    if Counter(np.sum(adj1, axis=1)) != Counter(np.sum(adj2, axis=1)):
        return False
    for k in range(1, adj1.shape[0] + 1):
        if not np.allclose(sorted(np.linalg.matrix_power(adj1, k).flatten()),
                           sorted(np.linalg.matrix_power(adj2, k).flatten())):
            return False
    return True

def generate_random_graph(n):
    return (np.random.rand(n, n) < 0.5).astype(int)

def generate_isomorphic_graph(adj):
    perm = np.random.permutation(adj.shape[0])
    return adj[perm][:, perm]

def input_graph():
    try:
        n = int(input("Número de vértices: "))
        print("Digite a matriz de adjacência (linha por linha):")
        matrix = np.array([list(map(int, input().split())) for _ in range(n)])
        return np.maximum(matrix, matrix.T) * (1 - np.eye(n, dtype=int))
    except Exception as e:
        print(f"Erro: {e}")
        return None

def print_matrix_with_paths(matrix, label="Matriz"):
    print(f"\n{label}:")
    print(matrix)
    for k in range(1, matrix.shape[0] + 1):
        paths = np.linalg.matrix_power(matrix, k)
        print(f"A^{k}:")
        print(paths)

def main_menu():
    while True:
        print("\n1. Inserir grafos manualmente\n2. Gerar grafos aleatórios\n3. Gerar grafo e isomorfo\n4. Sair")
        choice = input("Escolha: ")
        if choice == '1':
            g1, g2 = input_graph(), input_graph()
            if g1 is not None and g2 is not None:
                print(f"Resultado: {'Isomorfos' if check_isomorphism(g1, g2) else 'Não isomorfos'}")
        elif choice == '2':
            n1 = int(input("Quantidade de Vértices G1: "))
            n2 = int(input("Quantidade Vértices G2: "))
            if n1 != n2:
                print("Os grafos não têm o mesmo número de vértices, logo não são isomorfos.")
                break
            g1, g2 = generate_random_graph(n1), generate_random_graph(n2)
            print_matrix_with_paths(g1, "Matriz de adjacência do Grafo 1")
            print_matrix_with_paths(g2, "Matriz de adjacência do Grafo 2")
            print(f"Resultado: {'Isomorfos' if check_isomorphism(g1, g2) else 'Não isomorfos'}")
        elif choice == '3':
            n = int(input("Vértices: "))
            g1 = generate_random_graph(n)
            g2 = generate_isomorphic_graph(g1)
            print_matrix_with_paths(g1, "Matriz de adjacência do Grafo 1 (original)")
            print_matrix_with_paths(g2, "Matriz de adjacência do Grafo 2 (isomorfo)")
            print(f"Resultado: {'Isomorfos' if check_isomorphism(g1, g2) else 'Erro no algoritmo'}")
        elif choice == '4':
            sys.exit(0)
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    random.seed()
    main_menu()
