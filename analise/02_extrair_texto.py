# Converte cada trabalho de catalogo.json para analise/textos/<id>.txt
# PDF -> pdftotext; DOCX -> XML do pacote; DOC -> leitor_doc.py (LibreOffice não abre estes arquivos aqui).
# Uso: python analise/02_extrair_texto.py
import json, os, re, subprocess, sys, zipfile
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from leitor_doc import texto_doc

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOGO = os.path.join(BASE, "analise", "catalogo.json")
SAIDA = os.path.join(BASE, "analise", "textos")
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

def pdf_para_texto(caminho):
    return subprocess.run(["pdftotext", "-layout", caminho, "-"],
                          check=True, capture_output=True, text=True).stdout

def docx_para_texto(caminho):
    with zipfile.ZipFile(caminho) as z:
        raiz = ET.fromstring(z.read("word/document.xml"))
    paragrafos = []
    for p in raiz.iter(W + "p"):
        trechos = []
        for no in p.iter():
            if no.tag == W + "t" and no.text:
                trechos.append(no.text)
            elif no.tag == W + "tab":
                trechos.append("\t")
            elif no.tag in (W + "br", W + "cr"):
                trechos.append("\n")
        paragrafos.append("".join(trechos))
    return "\n".join(paragrafos)

def extrair(caminho):
    ext = os.path.splitext(caminho)[1].lower()
    if ext == ".pdf":
        return pdf_para_texto(caminho)
    if ext == ".docx":
        return docx_para_texto(caminho)
    return texto_doc(caminho)

def main():
    catalogo = json.load(open(CATALOGO, encoding="utf-8"))
    os.makedirs(SAIDA, exist_ok=True)
    curtos = []
    for o in catalogo:
        texto = extrair(os.path.join(BASE, o["arquivo"]))
        texto = re.sub(r"\n{3,}", "\n\n", texto).strip() + "\n"
        with open(os.path.join(SAIDA, f"{o['id']}.txt"), "w", encoding="utf-8") as f:
            f.write(texto)
        if len(texto) < 2000:
            curtos.append(o["id"])
    print(f"Textos gerados: {len(catalogo)} | possivelmente incompletos: {curtos}")

if __name__ == "__main__":
    main()
