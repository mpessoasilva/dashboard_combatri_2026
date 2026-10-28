# Gera o dashboard offline e a pasta de downloads a partir de analise/trabalhos.json.
# Saídas: dashboard/index.html, dashboard/downloads/{originais,textos}/, classificacao.csv e classificacao.json
# Uso: python analise/04_gerar_dashboard.py   (só biblioteca padrão)
import csv, json, os, re, shutil
from urllib.parse import quote

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENTRADA = os.path.join(BASE, "analise", "trabalhos.json")
DASH = os.path.join(BASE, "dashboard")
DOWN = os.path.join(DASH, "downloads")
ORIG = os.path.join(DOWN, "originais")
TXT = os.path.join(DOWN, "textos")

CAMPOS_TEXTO = [("objetivo", "Objetivo"), ("tecnica", "Técnica utilizada"),
                ("dados", "Dados utilizados"), ("resultados", "Resultados"),
                ("conclusao", "Conclusões")]

def limpa(nome, n=90):
    nome = re.sub(r'[\\/:*?"<>|]+', " ", nome)
    return re.sub(r"\s+", " ", nome).strip()[:n].rstrip(" .")

def nome_base(t):
    return f"{t['id']} - {limpa(t['titulo'])}"

def preparar_downloads(trabalhos):
    for pasta in (ORIG, TXT):
        if os.path.isdir(pasta):
            shutil.rmtree(pasta)
        os.makedirs(pasta)
    for t in trabalhos:
        base = nome_base(t)
        ext = os.path.splitext(t["arquivo"])[1].lower()
        t["download_original"] = f"downloads/originais/{quote(base + ext)}"
        t["download_texto"] = f"downloads/textos/{quote(base + '.txt')}"
        shutil.copy(os.path.join(BASE, t["arquivo"]), os.path.join(ORIG, base + ext))
        shutil.copy(os.path.join(BASE, t["texto"]), os.path.join(TXT, base + ".txt"))

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
    # "</" escapado para o JSON não fechar a tag <script> por engano
    dados_js = json.dumps(dados, ensure_ascii=False).replace("</", "<\\/")
    return TEMPLATE.replace("__DADOS__", dados_js)

TEMPLATE = r"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Trabalhos CONBRATRI 2026</title>
<style>
:root {
  color-scheme: light dark;
  --fundo: #f6f7f9; --superficie: #ffffff; --texto: #1d2330; --suave: #5b6474;
  --borda: #d9dee7; --destaque: #2f6fb0; --barra: #5b8fc7; --sucesso: #2e7d4f;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --fundo: #14171d; --superficie: #1d222b; --texto: #e6e9ef; --suave: #9aa3b2;
    --borda: #323a47; --destaque: #7fb2e6; --barra: #5b8fc7; --sucesso: #6fc292;
  }
}
:root[data-theme="dark"] {
  --fundo: #14171d; --superficie: #1d222b; --texto: #e6e9ef; --suave: #9aa3b2;
  --borda: #323a47; --destaque: #7fb2e6; --barra: #5b8fc7; --sucesso: #6fc292;
}
* { box-sizing: border-box; }
body { margin: 0; background: var(--fundo); color: var(--texto);
  font: 15px/1.5 system-ui, -apple-system, "Segoe UI", Roboto, sans-serif; }
main { max-width: 1100px; margin: 0 auto; padding: 24px 16px 48px; }
h1 { font-size: 1.6rem; margin: 0 0 4px; }
h2 { font-size: 1.15rem; margin: 28px 0 12px; }
.sub { color: var(--suave); margin: 0 0 20px; }
.kpis { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 12px; }
.kpi, .painel, .cartao { background: var(--superficie); border: 1px solid var(--borda); border-radius: 10px; }
.kpi { padding: 14px 16px; }
.kpi b { display: block; font-size: 1.6rem; }
.kpi span { color: var(--suave); font-size: .9rem; }
.painel { padding: 16px; }
.barra-linha { display: grid; grid-template-columns: minmax(120px, 1fr) 3fr 40px; gap: 10px; align-items: center; margin: 6px 0; cursor: pointer; }
.barra-linha button { all: unset; cursor: pointer; display: contents; }
.barra-linha:focus-within .rotulo { text-decoration: underline; }
.rotulo { font-size: .9rem; }
.trilho { background: var(--borda); border-radius: 4px; height: 14px; overflow: hidden; }
.preench { display: block; background: var(--barra); height: 100%; border-radius: 4px; }
.valor { text-align: right; font-variant-numeric: tabular-nums; font-size: .9rem; }
.filtros { display: grid; grid-template-columns: 2fr 1fr 1fr; gap: 10px; margin: 16px 0; }
@media (max-width: 720px) { .filtros { grid-template-columns: 1fr; } .barra-linha { grid-template-columns: 1fr 2fr 36px; } }
input, select { width: 100%; padding: 9px 10px; border: 1px solid var(--borda); border-radius: 8px;
  background: var(--superficie); color: var(--texto); font: inherit; }
.contagem { color: var(--suave); font-size: .9rem; margin: 4px 0 10px; }
.cartao { margin-bottom: 10px; }
.cartao summary { list-style: none; cursor: pointer; padding: 14px 16px; }
.cartao summary::-webkit-details-marker { display: none; }
.cartao summary::before { content: "▸"; color: var(--suave); margin-right: 8px; display: inline-block; transition: transform .15s; }
.cartao[open] summary::before { transform: rotate(90deg); }
.cabeca { display: flex; flex-wrap: wrap; gap: 6px 10px; align-items: baseline; }
.tit { font-weight: 600; }
.etiqueta { font-size: .8rem; border: 1px solid var(--borda); border-radius: 999px; padding: 1px 8px; color: var(--suave); }
.corpo { padding: 0 16px 16px; border-top: 1px solid var(--borda); }
.corpo dt { font-weight: 600; margin-top: 12px; color: var(--destaque); }
.corpo dd { margin: 2px 0 0; }
.downloads { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 14px; }
.downloads a { color: var(--destaque); text-decoration: none; border: 1px solid var(--destaque);
  border-radius: 8px; padding: 6px 12px; font-size: .9rem; }
.downloads a:hover, .downloads a:focus-visible { background: var(--destaque); color: var(--superficie); }
.acoes { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 14px; }
.acoes a { font-size: .9rem; }
.vazio { color: var(--suave); padding: 24px; text-align: center; }
.rodape { color: var(--suave); font-size: .85rem; margin-top: 32px; }
</style>
</head>
<body>
<main>
  <h1>Trabalhos do CONBRATRI 2026</h1>
  <p class="sub">Organização dos trabalhos por cluster temático, com objetivo, técnica, dados, resultados e conclusões.</p>

  <section class="kpis" aria-label="Resumo">
    <div class="kpi"><b id="kpi-total"></b><span>trabalhos</span></div>
    <div class="kpi"><b id="kpi-clusters"></b><span>clusters temáticos</span></div>
    <div class="kpi"><b id="kpi-sessoes"></b><span>sessões e pôster</span></div>
    <div class="kpi"><b id="kpi-downloads"></b><span>arquivos originais disponíveis</span></div>
  </section>

  <h2>Trabalhos por cluster</h2>
  <section class="painel" id="grafico" aria-label="Quantidade de trabalhos por cluster"></section>

  <h2>Explorar</h2>
  <div class="filtros">
    <input id="busca" type="search" placeholder="Buscar em título, objetivo, técnica, dados ou resultados" aria-label="Buscar">
    <select id="filtro-cluster" aria-label="Filtrar por cluster"></select>
    <select id="filtro-sessao" aria-label="Filtrar por sessão"></select>
  </div>
  <p class="contagem" id="contagem" aria-live="polite"></p>
  <section id="lista" aria-label="Lista de trabalhos"></section>

  <p class="rodape">Os textos de análise foram extraídos dos arquivos originais publicados no encontro. Os downloads trazem o arquivo original e o texto extraído (.txt); a classificação completa está em <a href="downloads/classificacao.csv">classificacao.csv</a> e <a href="downloads/classificacao.json">classificacao.json</a>.</p>
</main>

<script id="dados" type="application/json">__DADOS__</script>
<script>
(function () {
  var DADOS = JSON.parse(document.getElementById("dados").textContent);
  var CLUSTERS = DADOS.clusters;
  var TRABALHOS = DADOS.trabalhos;
  var CAMPOS = [["objetivo", "Objetivo"], ["tecnica", "Técnica utilizada"], ["dados", "Dados utilizados"],
                ["resultados", "Resultados"], ["conclusao", "Conclusões"]];

  function el(tag, attrs, texto) {
    var e = document.createElement(tag);
    Object.keys(attrs || {}).forEach(function (k) { e.setAttribute(k, attrs[k]); });
    if (texto !== undefined) e.textContent = texto;
    return e;
  }

  function sessaoRotulo(s) { return s === "Poster" ? "Sessão de pôster" : s; }

  // KPIs
  var sessoes = {};
  TRABALHOS.forEach(function (t) { sessoes[t.sessao] = true; });
  document.getElementById("kpi-total").textContent = TRABALHOS.length;
  document.getElementById("kpi-clusters").textContent = Object.keys(CLUSTERS).length;
  document.getElementById("kpi-sessoes").textContent = Object.keys(sessoes).length;
  document.getElementById("kpi-downloads").textContent = TRABALHOS.length;

  // Gráfico de barras por cluster
  var contagem = {};
  TRABALHOS.forEach(function (t) { contagem[t.cluster] = (contagem[t.cluster] || 0) + 1; });
  var maximo = Math.max.apply(null, Object.values(contagem));
  var grafico = document.getElementById("grafico");
  Object.keys(CLUSTERS).sort(function (a, b) { return contagem[b] - contagem[a]; }).forEach(function (c) {
    var linha = el("div", { class: "barra-linha" });
    var botao = el("button", { type: "button", "aria-label": "Filtrar por " + CLUSTERS[c].nome });
    botao.appendChild(el("span", { class: "rotulo" }, CLUSTERS[c].nome));
    var trilho = el("span", { class: "trilho" });
    trilho.appendChild(el("span", { class: "preench" }));
    trilho.firstChild.style.width = (100 * contagem[c] / maximo).toFixed(1) + "%";
    botao.appendChild(trilho);
    botao.appendChild(el("span", { class: "valor" }, String(contagem[c])));
    botao.addEventListener("click", function () {
      filtroCluster.value = c; desenhar();
      document.getElementById("lista").scrollIntoView({ behavior: "smooth" });
    });
    linha.appendChild(botao);
    grafico.appendChild(linha);
  });

  // Filtros
  var filtroCluster = document.getElementById("filtro-cluster");
  var filtroSessao = document.getElementById("filtro-sessao");
  filtroCluster.appendChild(el("option", { value: "" }, "Todos os clusters"));
  Object.keys(CLUSTERS).forEach(function (c) {
    filtroCluster.appendChild(el("option", { value: c }, CLUSTERS[c].nome));
  });
  filtroSessao.appendChild(el("option", { value: "" }, "Todas as sessões"));
  Object.keys(sessoes).sort().forEach(function (s) {
    filtroSessao.appendChild(el("option", { value: s }, sessaoRotulo(s)));
  });

  var busca = document.getElementById("busca");
  var lista = document.getElementById("lista");
  var contagemTxt = document.getElementById("contagem");

  function textoBusca(t) {
    return [t.titulo, t.objetivo, t.tecnica, t.dados, t.resultados, t.conclusao].join(" ").toLowerCase();
  }

  function cartao(t) {
    var det = el("details", { class: "cartao" });
    var resumo = el("summary");
    var cabeca = el("div", { class: "cabeca" });
    cabeca.appendChild(el("span", { class: "tit" }, t.titulo));
    cabeca.appendChild(el("span", { class: "etiqueta" }, t.id));
    cabeca.appendChild(el("span", { class: "etiqueta" }, CLUSTERS[t.cluster].nome));
    cabeca.appendChild(el("span", { class: "etiqueta" }, sessaoRotulo(t.sessao)));
    resumo.appendChild(cabeca);
    det.appendChild(resumo);

    var corpo = el("div", { class: "corpo" });
    var dl = el("dl");
    CAMPOS.forEach(function (c) {
      dl.appendChild(el("dt", {}, c[1]));
      dl.appendChild(el("dd", {}, t[c[0]]));
    });
    corpo.appendChild(dl);

    var downloads = el("div", { class: "downloads" });
    downloads.appendChild(el("a", { href: t.download_original, download: "" }, "Baixar original"));
    downloads.appendChild(el("a", { href: t.download_texto, download: "" }, "Baixar texto extraído (.txt)"));
    corpo.appendChild(downloads);
    det.appendChild(corpo);
    return det;
  }

  function desenhar() {
    var termo = busca.value.trim().toLowerCase();
    var cl = filtroCluster.value, ss = filtroSessao.value;
    var filtrados = TRABALHOS.filter(function (t) {
      return (!cl || t.cluster === cl) && (!ss || t.sessao === ss) && (!termo || textoBusca(t).indexOf(termo) !== -1);
    });
    lista.textContent = "";
    if (!filtrados.length) {
      lista.appendChild(el("div", { class: "vazio" }, "Nenhum trabalho encontrado com esses filtros."));
    }
    filtrados.forEach(function (t) { lista.appendChild(cartao(t)); });
    contagemTxt.textContent = filtrados.length + " de " + TRABALHOS.length + " trabalhos";
  }

  busca.addEventListener("input", desenhar);
  filtroCluster.addEventListener("change", desenhar);
  filtroSessao.addEventListener("change", desenhar);
  desenhar();
})();
</script>
</body>
</html>
"""

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
