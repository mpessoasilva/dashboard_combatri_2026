# Baixa os arquivos listados em lista_trabalhos_e_links.csv para as pastas de cada sessão.
# Uso: python baixar_trabalhos.py   (use a pasta Apresentacao_de_trabalhos_CONBRATRI_2026 como diretório atual)
import csv, glob, os, re, sys, urllib.request, urllib.error

BASE = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE, "lista_trabalhos_e_links.csv")
UA = {"User-Agent": "Mozilla/5.0"}

def limpa(nome, n=90):
    nome = re.sub(r'[\\/:*?"<>|]+', " ", nome)
    nome = re.sub(r"\s+", " ", nome).strip()
    return nome[:n].rstrip(" .")

def main():
    with open(CSV_PATH, encoding="utf-8-sig", newline="") as f:
        linhas = list(csv.DictReader(f, delimiter=";"))
    ok, pulados, falhas = 0, 0, []
    for i, row in enumerate(linhas, 1):
        link = row["Link do arquivo"].strip()
        pasta_pref = row["Pasta sugerida"].split(" (")[0].strip()
        achados = glob.glob(os.path.join(BASE, pasta_pref + "*"))
        if not achados:
            falhas.append((i, "pasta não encontrada: " + pasta_pref)); continue
        pasta = achados[0]
        ext = os.path.splitext(link)[1].lower() or ".pdf"
        destino = os.path.join(pasta, f"{i:02d} - {limpa(row['Titulo'])}{ext}")
        if os.path.exists(destino) or glob.glob(os.path.join(pasta, f"{i:02d} - *")):
            pulados += 1; continue
        try:
            req = urllib.request.Request(link, headers=UA)
            with urllib.request.urlopen(req, timeout=60) as r, open(destino, "wb") as out:
                out.write(r.read())
            ok += 1
            print(f"[ok] {os.path.basename(pasta)}/{os.path.basename(destino)}")
        except (urllib.error.URLError, OSError) as e:
            falhas.append((i, f"{link} -> {e}"))
            print(f"[falha] {i}: {e}", file=sys.stderr)
    print(f"\nBaixados: {ok} | já existiam: {pulados} | falhas: {len(falhas)}")
    for i, msg in falhas:
        print(f"  linha {i}: {msg}")

if __name__ == "__main__":
    main()
