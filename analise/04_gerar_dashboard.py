# Gera o dashboard offline e a pasta de downloads a partir de analise/trabalhos.json.
# Saídas: dashboard/index.html, dashboard/downloads/originais/, classificacao.csv e classificacao.json
# O visual fica em analise/dashboard_template.html; este script só preenche o marcador __DADOS__.
# Uso: python analise/04_gerar_dashboard.py   (só biblioteca padrão)
import csv, json, os, re, shutil
from urllib.parse import quote

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENTRADA = os.path.join(BASE, "analise", "trabalhos.json")
TEMPLATE_PATH = os.path.join(BASE, "analise", "dashboard_template.html")
DASH = os.path.join(BASE, "dashboard")
DOWN = os.path.join(DASH, "downloads")
ORIG = os.path.join(DOWN, "originais")

def limpa(nome, n=90):
    nome = re.sub(r'[\\/:*?"<>|]+', " ", nome)
    return re.sub(r"\s+", " ", nome).strip()[:n].rstrip(" .")

def nome_base(t):
    return f"{t['id']} - {limpa(t['titulo'])}"

def preparar_downloads(trabalhos):
    if os.path.isdir(ORIG):
        shutil.rmtree(ORIG)
    os.makedirs(ORIG)
    for t in trabalhos:
        base = nome_base(t)
        ext = os.path.splitext(t["arquivo"])[1].lower()
        t["download_original"] = f"downloads/originais/{quote(base + ext)}"
        shutil.copy(os.path.join(BASE, t["arquivo"]), os.path.join(ORIG, base + ext))

def gravar_classificacao(dados):
    trabalhos, clusters = dados["trabalhos"], dados["clusters"]
    with open(os.path.join(DOWN, "classificacao.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["ID", "Título", "Sessão", "Cluster", "Objetivo", "Técnica", "Dados", "Resultados", "Conclusões"])
        for t in trabalhos:
            w.writerow([t["id"], t["titulo"], t["sessao"], clusters[t["cluster"]]["nome"],
                        t["objetivo"], t["tecnica"], t["dados"], t["resultados"], t["conclusao"]])
    with open(os.path.join(DOWN, "classificacao.json"), "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

def html(dados):
    template = open(TEMPLATE_PATH, encoding="utf-8").read()
    # "</" escapado para o JSON não fechar a tag <script> por engano
    dados_js = json.dumps(dados, ensure_ascii=False).replace("</", "<\\/")
    return template.replace("__DADOS__", dados_js)

def main():
    dados = json.load(open(ENTRADA, encoding="utf-8"))
    preparar_downloads(dados["trabalhos"])
    gravar_classificacao(dados)
    os.makedirs(DASH, exist_ok=True)
    with open(os.path.join(DASH, "index.html"), "w", encoding="utf-8") as f:
        f.write(html(dados))
    print(f"Dashboard gerado em {os.path.join(DASH, 'index.html')}")

if __name__ == "__main__":
    main()
