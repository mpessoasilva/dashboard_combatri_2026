# Classificação e extração manual (objetivo, técnica, dados, resultados, conclusão) de cada trabalho.
# Base: resumos e conclusões lidos em analise/textos/<id>.txt.
# Uso: python analise/03_classificacao.py  -> grava analise/trabalhos.json
import json, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOGO = os.path.join(BASE, "analise", "catalogo.json")
SAIDA = os.path.join(BASE, "analise", "trabalhos.json")

CLUSTERS = {
    "C1": {"nome": "IA na elaboração e revisão de itens",
           "descricao": "Uso de IA generativa para produzir, revisar e corrigir itens, com validação humana."},
    "C2": {"nome": "Predição e pré-testagem com IA",
           "descricao": "Estimar dificuldade de itens, comparar itens por LLMs e usar respondentes sintéticos ou redes neurais no lugar da pré-testagem."},
    "C3": {"nome": "IA na análise e gestão de dados educacionais",
           "descricao": "Plataformas, dashboards, diagnósticos e formação de equipes para uso de dados e IA."},
    "C4": {"nome": "Modelos TRI e estimação de proficiência",
           "descricao": "Comparação de modelos (Rasch, 1PL, 2PL, 3PL), estimadores de proficiência e softwares."},
    "C5": {"nome": "Equalização, escalas e interpretação",
           "descricao": "Comparabilidade entre escalas e edições, e o sentido pedagógico dos níveis de proficiência."},
    "C6": {"nome": "Padrões de desempenho e standard setting",
           "descricao": "Pontos de corte, descrição de níveis e métodos como Angoff Modificado."},
    "C7": {"nome": "Fidedignidade, qualidade de instrumentos e correção",
           "descricao": "Confiabilidade, discriminação, validade de questionários e monitoramento da correção."},
    "C8": {"nome": "Funcionamento de itens, equidade e uso de resultados",
           "descricao": "DIF, efeito de posição, anomalias em itens e o uso de resultados em políticas e pesquisa."},
}

ATRIBUICAO = {
    "C1": ["T01", "T02", "T33", "T39", "T44"],
    "C2": ["T03", "T04", "T18", "T19", "T20", "T21", "T36", "T42"],
    "C3": ["T05", "T06", "T07", "T16", "T22", "T29", "T30"],
    "C4": ["T25", "T31", "T32", "T34", "T40"],
    "C5": ["T08", "T28", "T38"],
    "C6": ["T12", "T13", "T41"],
    "C7": ["T09", "T10", "T11", "T15", "T26", "T35", "T37"],
    "C8": ["T14", "T17", "T23", "T24", "T27", "T43"],
}

EXTRACAO = {
    "T01": {
        "objetivo": "Propor um protocolo human-in-the-loop que integra geração de itens assistida por IA, desenho centrado em evidências, acessibilidade e calibração pela TRI.",
        "tecnica": "Estudo teórico-metodológico, com base em Evidence-Centered Design e revisão de estudos sobre geração automática de itens e LLMs.",
        "dados": "Não se aplica: não há coleta empírica.",
        "resultados": "Protocolo em etapas (geração, desenho, revisão de acessibilidade e calibração), com foco em itens revisáveis e calibráveis.",
        "conclusao": "A IA deve acelerar operações de linguagem sem substituir a definição do construto, o julgamento de qualidade e a calibração empírica."},
    "T02": {
        "objetivo": "Analisar a elaboração de itens de Matemática com IA generativa, usando a matriz de referência do SAEB e critérios técnicos como orientadores.",
        "tecnica": "Abordagem qualitativa, exploratória e analítica, com análise de registros de elaboração e revisão feitos com intervenção especializada.",
        "dados": "Registros de elaboração e revisão de itens; dois casos representativos (raiz quadrada e pontos notáveis de triângulos).",
        "resultados": "Correção matemática e estrutura formal não garantem sozinhas a adequação do item; é preciso preservar a relação entre objeto de conhecimento, operação cognitiva e evidência.",
        "conclusao": "A matriz do SAEB pode servir como prompt técnico estruturante; a qualidade depende de critérios técnicos e julgamento especializado (coelaboração humano-IA)."},
    "T03": {
        "objetivo": "Prever automaticamente o parâmetro de dificuldade (b) da TRI a partir do texto e de metadados de itens de leitura.",
        "tecnica": "Representações BoW, TF-IDF, Word2Vec e embeddings BERT, com atributos linguísticos e metadados; vários regressores (melhor: BoW com XGBoost); validação cruzada e busca em grade; divisão 70/15/15; calibração por 1PL.",
        "dados": "5.410 itens de avaliações formativas brasileiras, aplicados entre 2021 e 2024, do 4º ano do EF ao 3º ano do EM.",
        "resultados": "Teste: MAE 0,4686; RMSE 0,6033; R² 0,5611; Pearson 0,7493. Na validação aplicada, concordância com a TRI de 100%, 60% e 78% nos padrões defasagem, intermediário e avançado.",
        "conclusao": "Modelos relativamente simples podem apoiar a triagem de itens e o planejamento da pré-testagem, mas não substituem a calibração empírica."},
    "T04": {
        "objetivo": "Avaliar a capacidade de um modelo de IA de estimar a dificuldade de 22 itens de Matemática da Prova Paraná 2025.",
        "tecnica": "Modelo de IA desenvolvido com itens do Enem, considerando características cognitivas; estimativas comparadas à TCT (percentual de acertos) e à TRI.",
        "dados": "22 itens de Matemática da 1ª edição da Prova Paraná 2025, aplicada à 3ª série do EM.",
        "resultados": "Houve correspondências e divergências entre as três abordagens.",
        "conclusao": "A IA oferece informações complementares na elaboração e revisão, sem substituir especialistas, a aplicação aos estudantes ou as análises psicométricas."},
    "T05": {
        "objetivo": "Apresentar o AlfabetizIA, portal de inteligência territorial sobre o Indicador Criança Alfabetizada.",
        "tecnica": "Plataforma web com análise comparativa, acompanhamento longitudinal e benchmarking municipal (abordagem descritiva e exploratória).",
        "dados": "Resultados de proficiência, metas e contextos socioeconômicos municipais, integrados em uma base com milhares de dados.",
        "resultados": "Apresentação da ferramenta; o trabalho não traz resultados empíricos.",
        "conclusao": "Serve de ponto de partida para formular hipóteses e para análises causais; ajuda gestores a priorizar intervenções."},
    "T06": {
        "objetivo": "Apresentar o ADEF, aplicação web com IA generativa para análises comparativas de municípios e unidades federativas.",
        "tecnica": "Pesquisa aplicada, descritivo-exploratória, com desenvolvimento iterativo por prompts, testes e validações; análises de similaridade, benchmarking e trajetória.",
        "dados": "Séries históricas de desempenho educacional, variáveis socioeconômicas e financeiras.",
        "resultados": "Ferramenta funcional com recursos de similaridade, benchmarking e trajetória; experiência de uso em formações com equipes de Secretarias de Educação.",
        "conclusao": "A IA generativa reduz barreiras ao desenvolvimento de ferramentas analíticas, desde que associada a validação e interpretação contextual."},
    "T07": {
        "objetivo": "Avaliar os impactos do uso de IA por estudantes do Ensino Fundamental.",
        "tecnica": "Pesquisa exploratória e transversal, com Questionário de Uso de IA e provas de proficiência em língua portuguesa e matemática.",
        "dados": "4.298 estudantes dos anos finais do EF; questionário de uso de IA e provas de proficiência.",
        "resultados": "Diferenças de desempenho conforme a frequência de uso: 19 pontos em língua portuguesa e 29 em matemática.",
        "conclusao": "O uso inadequado da IA está associado a prejuízos no desempenho dos estudantes nas duas disciplinas."},
    "T08": {
        "objetivo": "Investigar a relação entre as escalas do Enem e do Saeb em Matemática e Língua Portuguesa.",
        "tecnica": "Análise de dimensionalidade, calibração TRI (3PL), procedimentos de equalização e estudos de estabilidade dos parâmetros.",
        "dados": "Provas experimentais de 30 itens de cada avaliação, aplicadas à mesma amostra de estudantes.",
        "resultados": "Os itens das duas avaliações podem ser representados por uma única dimensão latente; forte relação linear entre as dificuldades; maior alinhamento em Língua Portuguesa.",
        "conclusao": "As escalas são estrutural e metricamente compatíveis, permitindo relações de equivalência entre seus resultados, respeitadas as diferenças pedagógicas."},
    "T09": {
        "objetivo": "Recordar três estimativas clássicas do coeficiente de confiabilidade e apresentar a confiabilidade empírica estimada pela TRI.",
        "tecnica": "Revisão das estimativas da TCT e aplicação da confiabilidade empírica pela TRI.",
        "dados": "Dados públicos do Saeb 2023.",
        "resultados": "As estimativas clássicas exigem correlação entre todos os itens; a abordagem pela TRI não tem essa limitação. O resumo não traz valores numéricos.",
        "conclusao": "A confiabilidade empírica da TRI é alternativa às estimativas clássicas, que dependem do planejamento do teste."},
    "T10": {
        "objetivo": "Analisar o comportamento dos corretores da Avaliação Formativa do Ceará 2025.",
        "tecnica": "Modelagem Rasch multifacetada.",
        "dados": "9.188 estudantes, 64 corretores e 7 aspectos de correção.",
        "resultados": "Elevada concordância entre corretores; ajuste adequado para a maioria dos avaliadores e aspectos; poucos casos de desajuste de leniência/severidade.",
        "conclusao": "O Rasch multifacetado é ferramenta eficaz para monitorar a qualidade da correção e pode subsidiar a validação de correção automatizada por IA."},
    "T11": {
        "objetivo": "Apresentar o desenvolvimento e as evidências de validade do Questionário de Turma, baseado no Visible Learning de Hattie.",
        "tecnica": "Análise Fatorial Exploratória e consistência interna; Modelo de Resposta Gradual de Samejima para construir índices sintéticos.",
        "dados": "114.391 observações de turmas do Ensino Fundamental em 12 estados.",
        "resultados": "Alfa de Cronbach entre 0,814 e 0,890; KMO > 0,82; associação positiva dos índices com as proficiências em Língua Portuguesa e Matemática.",
        "conclusao": "O instrumento produz medidas consistentes sobre o cotidiano das salas de aula e enriquece as avaliações em larga escala."},
    "T12": {
        "objetivo": "Descrever a metodologia para estabelecer os pontos de corte do Enem com o Método de Angoff Modificado.",
        "tecnica": "Angoff Modificado com painel de juízes; transposição dos resultados para a escala do Enem pelo TS-Score.",
        "dados": "Painel de 11 a 15 especialistas por área, das cinco regiões do país, nas quatro áreas do Enem.",
        "resultados": "Os resultados foram transpostos para a escala de proficiência do Enem e evidenciam a confiabilidade do método.",
        "conclusao": "O método oferece subsídios para aplicação em contextos semelhantes."},
    "T13": {
        "objetivo": "Apresentar as etapas de elaboração e validação das Descrições dos Padrões de Desempenho do Ensino Médio.",
        "tecnica": "Análise da BNCC do Ensino Médio e elaboração por grupos de especialistas (docentes de todo o país), como etapa prévia ao Angoff Modificado.",
        "dados": "BNCC do Ensino Médio e contribuições dos grupos de especialistas.",
        "resultados": "Documento com descrições pedagógicas dos níveis Abaixo do Básico, Básico, Adequado e Avançado.",
        "conclusao": "As descrições permitem que gestores, docentes e estudantes entendam o significado de cada nível na escala do Enem."},
    "T14": {
        "objetivo": "Decompor a variação do Ideb entre 2005 e 2025 em contribuições de desempenho e de fluxo.",
        "tecnica": "Decomposição pelo valor de Shapley, que reparte o termo de interação em partes iguais; decomposição da variância entre as UFs.",
        "dados": "Séries do Ideb e do Saeb de 2005 a 2025, por rede e unidade da federação.",
        "resultados": "Entre 2019 e 2025, o fluxo responde por 94% do crescimento nos anos finais da rede pública e por 96% no EM estadual. A redução da dispersão entre estados é de aprovação, não de proficiência.",
        "conclusao": "A convergência do Ideb é convergência de aprovação, não de aprendizagem; atribuições alternativas deslocam a resposta em até 12 pontos percentuais sem mudar a conclusão."},
    "T15": {
        "objetivo": "Apresentar o desenvolvimento e a implementação da avaliação das condições de oferta da EPT na rede estadual de Minas Gerais.",
        "tecnica": "Construção e validação de instrumentos (pré-teste e ajustes); triangulação de evidências documentais, entrevistas e observação in loco; aplicação em plataforma digital.",
        "dados": "Documentos, entrevistas e observação in loco de cursos com egressos ofertados em 2026 (Trilhas de Futuro).",
        "resultados": "O resumo descreve a metodologia de consolidação de medidas e indicadores; não traz resultados numéricos.",
        "conclusao": "As escolhas metodológicas seguem o SINAEPT e fornecem uma base para consolidar medidas e indicadores da EPT."},
    "T16": {
        "objetivo": "Analisar o uso da IA como apoio à avaliação diagnóstica de estudantes do Ensino Médio.",
        "tecnica": "Correção pelo gabarito e matriz de desempenho; a IA identificou competências, habilidades e componentes disciplinares de cada questão, com base na Matriz do Enem; análise pedagógica por percentuais.",
        "dados": "Simulado de 45 questões de Ciências da Natureza do Enem, com 150 estudantes em quatro turmas.",
        "resultados": "Aproveitamento médio de 39,2%; Biologia 43,4%, Química 39,3%, Física 35,3%; C5 com maior desempenho (49,07%); C7 (34,37%) e C6 (35,38%) com os menores.",
        "conclusao": "A IA apoia o diagnóstico pedagógico por competência e habilidade. (Conclusão formal não verificada no resumo.)"},
    "T17": {
        "objetivo": "Investigar a presença de DIF no componente de Matemática da Prova Curitiba, em relação ao nível socioeconômico e à autodeclaração étnico-racial.",
        "tecnica": "Regressão logística fundamentada na TRI, com critério de magnitude de 0,15 para detectar DIF.",
        "dados": "Respostas de 11.426 estudantes do 4º ano do EF, na aplicação de maio de 2026; 18 itens.",
        "resultados": "Nenhum dos 18 itens apresentou DIF igual ou superior ao limite.",
        "conclusao": "O instrumento demonstra robustez e equidade na mensuração da aprendizagem entre os grupos investigados."},
    "T18": {
        "objetivo": "Propor um procedimento para usar LLMs no posicionamento de itens-alvo em uma escala já existente, com itens de Matemática do Enem.",
        "tecnica": "Comparações pareadas feitas por IAs executadas localmente (o item-alvo é mais difícil que o âncora?); estimativa dos parâmetros; validação por correlação, viés, MAE, RMSE e acurácia de ordenação.",
        "dados": "45 itens de 2023 com parâmetros TRI conhecidos (âncoras) e 45 itens de 2024 (alvos); 2.025 comparações por IA.",
        "resultados": "Estimativas promissoras quando comparadas aos parâmetros oficiais de 2024.",
        "conclusao": "O procedimento é promissor para apoiar a pré-testagem, reduzindo custo e exposição de itens."},
    "T19": {
        "objetivo": "Investigar o uso de IA executada localmente para analisar a dificuldade de itens de Matemática do Saeb.",
        "tecnica": "Comparações pareadas por modelos de linguagem; matriz de julgamentos; ordenação relativa comparada às informações oficiais de dificuldade.",
        "dados": "30 itens da edição de 2007 e 30 itens da edição de 2009 do Saeb, da 4ª série do EF.",
        "resultados": "O resumo indica a comparação da ordenação com os parâmetros oficiais, sem valores numéricos.",
        "conclusao": "A IA pode contribuir para a análise preliminar da dificuldade, sem substituir os procedimentos psicométricos tradicionais."},
    "T20": {
        "objetivo": "Propor um protocolo reprodutível para pré-calibrar e estimar preliminarmente a dificuldade de 10 itens de Matemática do PISA 2022 com IA.",
        "tecnica": "Cinco LLMs executados localmente (Ollama/VSCode) em quatro etapas: descrição dos itens, rankings com justificativas, comparações dicotômicas par a par e calibração TRI.",
        "dados": "10 itens de Matemática do PISA 2022 e os parâmetros e estatísticas oficiais.",
        "resultados": "O método captura a ordenação empírica de dificuldade (resultados preliminares).",
        "conclusao": "Caminho promissor para otimizar a pré-testagem automatizada e proteger o sigilo das provas; não substitui a calibração com estudantes."},
    "T21": {
        "objetivo": "Comparar a hierarquia de complexidade gerada por LLM com a ordenação empírica de dificuldade (TRI) em itens de Formação Geral Docente da PND 2025.",
        "tecnica": "Modelo Qwen2.5-coder:14b executado localmente, com comparação dicotômica.",
        "dados": "30 itens da PND 2025.",
        "resultados": "Ainda não apresentados: o resumo indica expectativa de resultados promissores.",
        "conclusao": "Proposta em andamento; a validação do modelo é etapa futura."},
    "T22": {
        "objetivo": "Propor uma metodologia de avaliação pós-teste que combina métodos quantitativos e IA para identificar lacunas de aprendizagem no 3º ano do EM.",
        "tecnica": "Análise estatística de acertos e de distratores; IA para gerar dashboards por aluno e para a turma.",
        "dados": "Simulado padrão Enem aplicado a uma turma de 3º ano.",
        "resultados": "Resultados parciais: a visualização das defasagens por habilidade permite identificar lacunas específicas.",
        "conclusao": "Os dashboards permitem que os docentes ajustem as rotas pedagógicas de forma ágil e baseada em evidências."},
    "T23": {
        "objetivo": "Estimar a associação entre a participação em iniciação científica e a chance de egressos de Psicologia atingirem o quartil superior do ENADE.",
        "tecnica": "Propensity Score Matching, com pareamento 1:3 e balanceamento das covariáveis.",
        "dados": "Microdados do ENADE de 2018 e 2022 vinculados ao Censo da Educação Superior (SEDAP/INEP); 46.681 estudantes antes do pareamento; 2.717 com IC pareados a 8.151 sem IC.",
        "resultados": "Diferença positiva e significativa (p < 0,001): +5,48 p.p. no Componente Específico e +5,28 p.p. na Formação Geral.",
        "conclusao": "A iniciação científica fortalece competências disciplinares e transversais avaliadas pelo exame."},
    "T24": {
        "objetivo": "Investigar as características psicométricas do Enem em relação ao uso concomitante para seleção, certificação e monitoramento.",
        "tecnica": "Comparação da dificuldade dos itens com as notas da população; análise de informação e erro-padrão; Optimal Test Design.",
        "dados": "Itens e notas do Enem da população de candidatos.",
        "resultados": "Itens difíceis demais para a maioria dos candidatos; para notas entre 400 e 500 o exame fornece pouca informação; essas notas são quase indistinguíveis de padrões aleatórios.",
        "conclusao": "As características dos itens do Enem terão de mudar substancialmente para atender a todas as finalidades do exame."},
    "T25": {
        "objetivo": "Investigar o impacto da ordem de resolução dos itens na estimação da proficiência quando há fadiga.",
        "tecnica": "Simulação com TRI 3PL; três estratégias (ordem original, do mais fácil ao mais difícil e o inverso); fadiga modelada como redução linear da proficiência.",
        "dados": "Dados simulados; não há dados empíricos.",
        "resultados": "Não há estratégia uniformemente superior: respondentes de menor proficiência são menos prejudicados começando pelos itens fáceis, e os de maior proficiência se saem melhor começando pelos difíceis.",
        "conclusao": "A ordem dos itens importa e o efeito depende do nível de proficiência do respondente."},
    "T26": {
        "objetivo": "Analisar o comportamento das correlações ponto-bisserial e bisserial como indicadores de discriminação na TCT.",
        "tecnica": "Simulação Monte Carlo com o modelo 3PL; testes de 25, 50 e 100 itens; amostras de 10 mil, 50 mil e 100 mil respondentes; 15 réplicas por condição.",
        "dados": "Dados simulados: a ~ U(0,5; 3), b ~ U(-3; 3), c ~ U(0; 0,4), θ ~ N(0,1).",
        "resultados": "A ponto-bisserial corrigida tem forte associação negativa com |b|; a bisserial reduz essa associação e se relaciona melhor com a discriminação verdadeira. O padrão se mantém nas nove condições.",
        "conclusao": "Pontos de corte uniformes não devem, sozinhos, determinar a eliminação de itens; dificuldade e conteúdo também devem ser considerados."},
    "T27": {
        "objetivo": "Investigar o efeito da posição dos itens na prova de Ciências Humanas do Enem 2025.",
        "tecnica": "Testes de proporções e razões de chances entre as posições mais precoce e mais tardia, nos quatro cadernos; ajuste para múltiplas comparações.",
        "dados": "Microdados da aplicação regular; 30 itens com acerto médio entre 30% e 70%.",
        "resultados": "Todos os itens tiveram menor acerto na posição tardia (diferenças de 0,11 a 7,14 p.p.); em 29 dos 30 itens a diferença é significativa.",
        "conclusao": "Há associação entre posição e desempenho, o que levanta questões sobre a invariância dos itens entre cadernos."},
    "T28": {
        "objetivo": "Adaptar o método simplified pairs (Benton, 2021) para equalizar avaliações por julgamento comparativo da dificuldade dos itens.",
        "tecnica": "Juízes comparam pares de itens de provas diferentes; análise por regressão logística; estudo de simulação com modelo de Rasch.",
        "dados": "Julgamentos simulados, em condições sem itens comuns nem população equivalente.",
        "resultados": "Acurácia e precisão do deslocamento estimado avaliadas por simulação (valores não detalhados no resumo).",
        "conclusao": "O método é uma alternativa viável quando não há sobreposição de itens ou de população."},
    "T29": {
        "objetivo": "Revisar os trabalhos sobre IA publicados nos anais do CONBRATRI entre 2018 e 2024.",
        "tecnica": "Revisão dos anais do congresso.",
        "dados": "Anais do CONBRATRI de 2018 a 2024.",
        "resultados": "Foram encontrados apenas 12 trabalhos no evento de 2024.",
        "conclusao": "A IA generativa é um campo em consolidação; deve ser instrumento de triagem calibrada, não substituto da validação empírica, com atenção a viés, autoria e regulação."},
    "T30": {
        "objetivo": "Sistematizar oito edições de formação com IA para equipes de dados e pedagógicas de secretarias, entre setembro de 2025 e abril de 2026.",
        "tecnica": "Relato descritivo e retrospectivo com base em registros institucionais, produções e formulários de avaliação.",
        "dados": "200 inscrições e 174 conclusões; formulários de avaliação dos participantes.",
        "resultados": "Os respondentes destacaram a aplicabilidade, a didática e a utilidade das ferramentas, e pediram mais aprofundamento e continuidade.",
        "conclusao": "Vale articular conhecimento técnico e pedagógico e tratar a IA como apoio, com validação humana e proteção de dados; os achados não permitem inferir mudanças institucionais."},
    "T31": {
        "objetivo": "Comparar análises psicométricas de uma implementação própria em Python (com apoio do ChatGPT) e do pacote mirt do R.",
        "tecnica": "Modelo 2PL e alfa de Cronbach; comparação dos parâmetros de discriminação e dificuldade.",
        "dados": "Respostas de 971 candidatos a 20 itens de Matemática para ingresso no 6º ano do EF.",
        "resultados": "Correlação de 0,9998 na discriminação e 0,9963 na dificuldade; alfa de 0,767012 nos dois procedimentos; maior divergência por limite imposto na implementação em Python.",
        "conclusao": "Há alta concordância, mas são necessárias supervisão especializada, inspeção de código e reprodução em software reconhecido."},
    "T32": {
        "objetivo": "Apresentar o percurso metodológico e psicométrico da medida de proficiência das Habilidades Gerais e Específicas no piloto da EPT de 2025.",
        "tecnica": "Cadernos com blocos incompletos; validação híbrida com exclusão de itens; índice D clássico (todo-resto); modelos 1PL, 2PL e 3PL; Análise Fatorial de Informação Completa.",
        "dados": "16.278 estudantes de dez cursos técnicos.",
        "resultados": "A premissa de discriminação constante do 1PL foi rejeitada; o mesmo escore bruto leva a proficiências diferentes nos modelos 2PL e 3PL; o 3PL capta o efeito do acerto casual.",
        "conclusao": "O modelo 3PL torna a avaliação da EPT mais fidedigna."},
    "T33": {
        "objetivo": "Construir uma metodologia para avaliar competências diferenciais de nível superior, no contexto do PROVEI do SENAI-SP.",
        "tecnica": "Pesquisa de desenvolvimento; avaliação autêntica; matrizes ancoradas em quadros de qualificação; estudos de caso (framework PACADI); correção por IA assistida por especialistas.",
        "dados": "Não há dados empíricos no resumo; a proposta é conceitual e metodológica.",
        "resultados": "Proposta de um modelo replicável de aferição de competências em larga escala.",
        "conclusao": "A metodologia pode contribuir para a avaliação da educação superior, desde que testada em escala."},
    "T34": {
        "objetivo": "Comparar os estimadores de proficiência MAP, EAP, ML, EAPsum e WLE.",
        "tecnica": "Simulação Monte Carlo no mirt; modelos Rasch, 2PL e 3PL; testes de 25, 50 e 100 itens; estudo condicional em 13 níveis de θ; viés, RMSE e MAE.",
        "dados": "50.000 respondentes simulados, com θ ~ N(0,1).",
        "resultados": "Nenhum estimador é universalmente superior; MAP e EAP têm mais frequentemente o menor RMSE, a depender do modelo, do comprimento e do nível de proficiência.",
        "conclusao": "A escolha do estimador deve considerar o modelo, o comprimento do teste e a faixa de proficiência."},
    "T35": {
        "objetivo": "Medir a percepção de estudantes sobre Ciência, Tecnologia e Letramento Digital e verificar se a extensão do instrumento altera as estimativas.",
        "tecnica": "TRI pelo Modelo de Resposta Gradual para estimar escores; teste de Kruskal-Wallis para comparar as distribuições.",
        "dados": "Estudantes do 8º e 9º anos do EF da rede pública estadual de São Paulo; quatro versões de um instrumento derivado de uma matriz de 223 itens (B1 com 72, B2 com 76, B3 com 75 e Enquete com 197).",
        "resultados": "Não houve diferenças estatisticamente significativas entre os grupos.",
        "conclusao": "As versões reduzidas produzem estimativas comparáveis às do instrumento mais extenso, nas condições investigadas."},
    "T36": {
        "objetivo": "Apresentar a Rede de Estimação Cruzada (CEN), que estima simultaneamente parâmetros de pessoas e de itens no modelo 2PL com redes neurais.",
        "tecnica": "Duas sub-redes (Pessoa e Item), com treino e teste.",
        "dados": "Dados simulados com 500 respondentes e 60 itens.",
        "resultados": "Boa recuperação no treino (MSE: z = 0,0971; a = 0,0383; b = 0,0480) e generalização para dados novos sem novo treinamento.",
        "conclusao": "A CEN é uma ponte promissora entre IA e psicometria, superando limitações computacionais dos métodos clássicos."},
    "T37": {
        "objetivo": "Investigar como o tamanho do teste e o da amostra influenciam as estimativas de Alfa e Ômega.",
        "tecnica": "Simulação Monte Carlo com o modelo 2PL; aplicação da fórmula de Spearman-Brown para correção do comprimento.",
        "dados": "Dados simulados, com testes de 25, 50 e 100 itens.",
        "resultados": "Os dois coeficientes crescem de forma não linear com o número de itens, com ganhos decrescentes; a diferença entre Alfa e Ômega torna-se praticamente nula a partir de 100 itens.",
        "conclusao": "Alfa e Ômega não devem ser usados sozinhos como critério de eliminação de itens em testes curtos; a correção por Spearman-Brown deve ser usada com cuidado."},
    "T38": {
        "objetivo": "Discutir como o Sinaept transforma o número medido em descrição do que o estudante aprendeu.",
        "tecnica": "Análise documental dos documentos públicos que fundamentam o sistema; referencial de validade de Messick e Kane. Pesquisa em andamento.",
        "dados": "Documentos públicos do Sinaept, sistema nacional de avaliação da EPT criado em 2025.",
        "resultados": "Ainda não concluídos (pesquisa em andamento).",
        "conclusao": "Automatizar a produção de itens torna ainda mais necessária a interpretação pedagógica dos níveis da escala."},
    "T39": {
        "objetivo": "Desenvolver um gerador automatizado de itens com IA generativa para a Plataforma de Estudos Personalizados (PEP) do SESI-SP.",
        "tecnica": "Pesquisa exploratória e aplicada; ciclos de geração, revisão especializada e calibração das instruções do sistema (prompts e regras).",
        "dados": "Descritores curriculares, critérios pedagógicos e parâmetros técnicos de elaboração de itens; ciclos de geração e revisão.",
        "resultados": "Preliminares: comandos genéricos favorecem a adequação temática, mas não garantem o alinhamento à habilidade cognitiva; o refinamento de prompts e a validação humana aumentaram a coerência dos itens.",
        "conclusao": "O gerador tem potencial para apoiar a produção em larga escala, desde que sob critérios técnicos rigorosos, supervisão especializada e aprimoramento contínuo."},
    "T40": {
        "objetivo": "Verificar as consequências das diferenças de parametrização entre Rasch e 1PL no mirt quando os dados são gerados por um modelo 3PL heterogêneo.",
        "tecnica": "Simulação comparando recuperação da dificuldade e da proficiência, ajuste e erro condicional em 13 pontos de θ.",
        "dados": "Dados simulados: 25, 50 e 100 itens; 10 mil, 50 mil e 100 mil respondentes; a ∈ [0,5; 3], b ∈ [-3; 3], c ∈ [0; 0,4].",
        "resultados": "Não apresentados: o trabalho é uma proposta de investigação.",
        "conclusao": "Pretende esclarecer quando as diferenças de parametrização se tornam diferenças práticas sob má especificação do modelo."},
    "T41": {
        "objetivo": "Apresentar um sistema web para aplicar digitalmente o Método Angoff Modificado em sessões de standard setting.",
        "tecnica": "Estudo tecnológico, descritivo-analítico, em fase de validação; desenvolvimento de um artefato computacional para coletar dados das plenárias.",
        "dados": "Dados das plenárias de discussão entre os juízes (sem coleta empírica detalhada no resumo).",
        "resultados": "O sistema permite rodadas de plenária com fluxo contínuo de informação, métricas de priorização de discussão com identificação do Juiz-Chave e contribui para evidências de validade procedimental.",
        "conclusao": "É uma ferramenta inédita no contexto nacional, ainda em fase de validação."},
    "T42": {
        "objetivo": "Desenvolver e validar respondentes sintéticos baseados em IA como complemento à pré-testagem convencional.",
        "tecnica": "Agentes de LLM configurados com níveis de proficiência e perfis de resposta; comparação com respostas reais por viés, MAE, RMSE, correlações e concordância; equalização com itens de ligação.",
        "dados": "Provas previamente calibradas, com respostas sintéticas e reais.",
        "resultados": "Proposta metodológica em andamento; resultados não apresentados.",
        "conclusao": "Modelo híbrido: agentes sintéticos apoiam a triagem e a priorização; respondentes reais continuam como referência para a calibração definitiva."},
    "T43": {
        "objetivo": "Analisar o funcionamento psicométrico do item 97593 da prova de Matemática do Enem 2025, que foi abandonado por problema de convergência.",
        "tecnica": "Indicadores da TCT; ajustes exploratórios pelo modelo 3PL; comparação das proficiências de participantes com padrões idênticos nos demais itens.",
        "dados": "Respostas da aplicação regular, com cadernos reorganizados pela identidade dos itens.",
        "resultados": "A alternativa A, correta, tem associação negativa com o desempenho; o distrator D é mais atrativo entre os de maior desempenho; diferença de 12,6 pontos de proficiência conforme a alternativa marcada.",
        "conclusao": "Há funcionamento psicométrico anômalo do item, o que suscita discussão sobre validação, calibração e tratamento de itens atípicos."},
    "T44": {
        "objetivo": "Analisar e revisar a avaliação de Matemática do SISEDU, usada para preparar estudantes do 3º ano do EM para o SPAECE.",
        "tecnica": "Indicadores de desempenho e TRI (parâmetros a e b); análise dos itens potencialmente problemáticos com apoio de IA e análise pedagógica.",
        "dados": "26 itens aplicados a 150 estudantes da EEEP Juarez Távora.",
        "resultados": "O percentual de acertos variou de 12,3% a 84,9%; os itens problemáticos foram revisados com sugestões da IA submetidas à análise pedagógica.",
        "conclusao": "Revisão conjunta entre IA e análise pedagógica para melhorar a clareza, a coerência e o alinhamento das questões. (Conclusão completa não verificada, pois o resumo está truncado.)"},
}

def main():
    catalogo = json.load(open(CATALOGO, encoding="utf-8"))
    cluster_de = {t: c for c, ids in ATRIBUICAO.items() for t in ids}
    trabalhos = []
    for obra in catalogo:
        tid = obra["id"]
        if tid not in cluster_de:
            raise SystemExit(f"{tid} sem cluster")
        if tid not in EXTRACAO:
            raise SystemExit(f"{tid} sem extração")
        trabalhos.append({
            "id": tid,
            "titulo": obra["titulo"],
            "sessao": obra["sessao"],
            "cluster": cluster_de[tid],
            "arquivo": obra["arquivo"],
            "texto": f"analise/textos/{tid}.txt",
            **EXTRACAO[tid],
        })
    with open(SAIDA, "w", encoding="utf-8") as f:
        json.dump({"clusters": CLUSTERS, "trabalhos": trabalhos}, f, ensure_ascii=False, indent=2)
    print(f"{len(trabalhos)} trabalhos classificados em {len(CLUSTERS)} clusters -> {SAIDA}")

if __name__ == "__main__":
    main()
