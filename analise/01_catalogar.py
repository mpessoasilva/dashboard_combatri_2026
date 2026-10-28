# Casa cada linha do CSV a um arquivo baixado, deduplica por conteúdo e grava catalogo.json.
# Uso: python analise/01_catalogar.py
import csv, glob, hashlib, json, os, re, unicodedata

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE, "lista_trabalhos_e_links.csv")
SAIDA = os.path.join(BASE, "analise", "catalogo.json")

def norm(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]", "", s.lower())

def md5(path):
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

def main():
    with open(CSV_PATH, encoding="utf-8-sig", newline="") as f:
        linhas = list(csv.DictReader(f, delimiter=";"))
    arquivos = [p for p in glob.glob(os.path.join(BASE, "0*", "*"), recursive=False)]
    arquivos += glob.glob(os.path.join(BASE, "0*", "*", "*"))
    arquivos = [p for p in arquivos if os.path.isfile(p)]
    # arquivos sem prefixo numérico também contam (ex.: Sessão 3 na raiz da pasta)
    arquivos = sorted(set(arquivos))

    def nome_sem_prefixo(p):
        # "NN - Titulo.ext" -> "Titulo" (os arquivos têm o título truncado em 90 caracteres)
        base = os.path.splitext(os.path.basename(p))[0]
        return norm(re.sub(r"^\d+ - ", "", base))

    obras = {}  # título normalizado completo -> dados
    for i, row in enumerate(linhas, 1):
        titulo = row["Titulo"].strip()
        chave = norm(titulo)
        sessao = row["Sessao"].strip()
        # o arquivo guarda um prefixo truncado do título normalizado
        candidatos = [p for p in arquivos
                      if nome_sem_prefixo(p) and chave.startswith(nome_sem_prefixo(p))]
        if not candidatos:
            print(f"[sem arquivo] linha {i}: {titulo[:60]}")
            continue
        obra = obras.setdefault(chave, {"titulo": titulo, "sessao": sessao, "linha_csv": i,
                                        "arquivos": [], "hashes": {}})
        for p in candidatos:
            h = md5(p)
            rel = os.path.relpath(p, BASE)
            if h in obra["hashes"]:
                continue
            obra["hashes"][h] = rel
            obra["arquivos"].append(rel)

    catalogo = []
    for n, (chave, obra) in enumerate(obras.items(), 1):
        principal = obra["arquivos"][0]
        catalogo.append({
            "id": f"T{n:02d}",
            "titulo": obra["titulo"],
            "sessao": obra["sessao"],
            "linha_csv": obra["linha_csv"],
            "arquivo": principal,
            "outras_versoes_identicas_ou_distintas": obra["arquivos"][1:],
        })

    os.makedirs(os.path.dirname(SAIDA), exist_ok=True)
    with open(SAIDA, "w", encoding="utf-8") as f:
        json.dump(catalogo, f, ensure_ascii=False, indent=2)
    print(f"Trabalhos únicos: {len(catalogo)} | gravado em {SAIDA}")
    for c in catalogo:
        extra = len(c["outras_versoes_identicas_ou_distintas"])
        if extra:
            print(f"  {c['id']} ({c['sessao']}) tem {extra} outra(s) versão(ões) de arquivo: {c['titulo'][:50]}")

if __name__ == "__main__":
    main()
