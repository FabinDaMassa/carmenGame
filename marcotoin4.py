import math

def f(x1, x2):
    return 1/2 * ((x1 - 2) * 2) + ((x2 - 1) * 2)

def gradiente(x):
    return [(x[0] - 2), 2*(x[1] - 1)]


def norma(vetor):
    return math.sqrt(sum([i**2 for i in vetor]))

def dot_product(v1:list, v2:list):
    res = 0

    for i in range(len(v1)):
        res += v1[i] * v2[i]

    return res

def secao_aurea(x, d, a=0, b=2, toler=1e-4):
    k = 0
    
    while True:
        t1 = a + 0.38*(b-a)
        t2 = a + 0.62*(b-a)
        if f(x[0] + t1 * d[0], x[1] + t1 * d[1]) < f(x[0] + t2 * d[0], x[1] + t2 * d[1]):
            b = t2
        else:
            a = t1

        k += 1

        if b - a <= 2 * toler:
            break
    

    t = (a + b) / 2
    return t


def cauchy(X0:list, toler):
    x = X0[:]
    k = 0
    
    while True:
        dk = [-i for i in gradiente(x)]

        if norma(dk) <= toler:
            break
        
        tk = secao_aurea(x, dk)
        
        x = [x[i] + tk * dk[i] for i in range(len(x))]
        k += 1
    
    return x, k

def main():
    x = [1,0]
    toler = 1e-6

    ans, k = cauchy(x, toler)

    print(ans)
    print(k, "iteracoes")


if __name__ == "__main__":
    main()