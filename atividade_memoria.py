import random
import copy

# =========================
# GERAR PARTIÇÕES E PROCESSOS
# =========================

particoes = [random.randint(50, 500) for _ in range(10)]
processos = [random.randint(10, 300) for _ in range(4)]

# =========================
# MOSTRAR DADOS
# =========================

print("\nPARTIÇÕES GERADAS")
for i, p in enumerate(particoes):
    print(f"Partição {i + 1} -> {p} KB")

print("\nPROCESSOS GERADOS")
for i, p in enumerate(processos):
    print(f"Processo P{i + 1} -> {p} KB")

# =========================
# FIRST FIT
# =========================

def first_fit(particoes, processos):
    part = copy.deepcopy(particoes)
    resultado = []
    total_fragmentacao = 0

    for i, processo in enumerate(processos):
        alocado = False

        for j, tamanho in enumerate(part):
            if tamanho >= processo:
                fragmentacao = tamanho - processo

                resultado.append({
                    "processo": f"P{i+1}",
                    "memoria": processo,
                    "particao": j + 1,
                    "tam_particao": tamanho,
                    "fragmentacao": fragmentacao
                })

                total_fragmentacao += fragmentacao
                part[j] = -1
                alocado = True
                break

        if not alocado:
            resultado.append({
                "processo": f"P{i+1}",
                "memoria": processo,
                "particao": "Não alocado",
                "tam_particao": "-",
                "fragmentacao": "-"
            })

    return resultado, total_fragmentacao

# =========================
# BEST FIT
# =========================

def best_fit(particoes, processos):
    part = copy.deepcopy(particoes)
    resultado = []
    total_fragmentacao = 0

    for i, processo in enumerate(processos):
        melhor = -1

        for j, tamanho in enumerate(part):
            if tamanho >= processo:
                if melhor == -1 or tamanho < part[melhor]:
                    melhor = j

        if melhor != -1:
            fragmentacao = part[melhor] - processo

            resultado.append({
                "processo": f"P{i+1}",
                "memoria": processo,
                "particao": melhor + 1,
                "tam_particao": part[melhor],
                "fragmentacao": fragmentacao
            })

            total_fragmentacao += fragmentacao
            part[melhor] = -1

        else:
            resultado.append({
                "processo": f"P{i+1}",
                "memoria": processo,
                "particao": "Não alocado",
                "tam_particao": "-",
                "fragmentacao": "-"
            })

    return resultado, total_fragmentacao

# =========================
# NEXT FIT
# =========================

def next_fit(particoes, processos):
    part = copy.deepcopy(particoes)
    resultado = []
    total_fragmentacao = 0
    posicao = 0

    for i, processo in enumerate(processos):
        alocado = False
        contador = 0

        while contador < len(part):
            if part[posicao] >= processo:
                fragmentacao = part[posicao] - processo

                resultado.append({
                    "processo": f"P{i+1}",
                    "memoria": processo,
                    "particao": posicao + 1,
                    "tam_particao": part[posicao],
                    "fragmentacao": fragmentacao
                })

                total_fragmentacao += fragmentacao
                part[posicao] = -1
                alocado = True

                posicao = (posicao + 1) % len(part)
                break

            posicao = (posicao + 1) % len(part)
            contador += 1

        if not alocado:
            resultado.append({
                "processo": f"P{i+1}",
                "memoria": processo,
                "particao": "Não alocado",
                "tam_particao": "-",
                "fragmentacao": "-"
            })

    return resultado, total_fragmentacao

# =========================
# MOSTRAR RESULTADOS
# =========================

def mostrar(nome, resultado, fragmentacao_total):
    print(f"\n{'='*50}")
    print(f"RESULTADO: {nome}")
    print(f"{'='*50}")

    print(f"{'Processo':<10} {'Memória':<10} {'Partição':<12} {'Tam.Part':<12} {'Fragmentação'}")

    for r in resultado:
        print(f"{r['processo']:<10} "
              f"{str(r['memoria']) + ' KB':<10} "
              f"{str(r['particao']):<12} "
              f"{str(r['tam_particao']) + ' KB':<12} "
              f"{str(r['fragmentacao']) + ' KB'}")

    print(f"\nFragmentação Total: {fragmentacao_total} KB")

# =========================
# EXECUÇÃO
# =========================

resultado_ff, frag_ff = first_fit(particoes, processos)
resultado_bf, frag_bf = best_fit(particoes, processos)
resultado_nf, frag_nf = next_fit(particoes, processos)

mostrar("FIRST FIT", resultado_ff, frag_ff)
mostrar("BEST FIT", resultado_bf, frag_bf)
mostrar("NEXT FIT", resultado_nf, frag_nf)