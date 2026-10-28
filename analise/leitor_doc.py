# Leitor mínimo de texto de arquivos Word 97-2003 (.doc), sem dependências externas.
# Lê o contêiner OLE, o FIB e a tabela de peças (PlcPcd) do stream WordDocument.
import struct, sys

def _ler_setores(dados, setor_tam, ids, fat):
    saida = bytearray()
    for sid in ids:
        if sid < 0:
            break
        inicio = (sid + 1) * setor_tam
        saida += dados[inicio:inicio + setor_tam]
    return bytes(saida)

def _cadeia(fat, inicio):
    ids, sid, vistos = [], inicio, set()
    while sid < 0xFFFFFFFA and sid not in vistos and sid < len(fat):
        vistos.add(sid)
        ids.append(sid)
        sid = fat[sid]
    return ids

def _streams_ole(dados):
    setor_tam = 1 << struct.unpack_from("<H", dados, 0x1E)[0]
    mini_corte = struct.unpack_from("<I", dados, 0x38)[0]
    difat = [v for v in struct.unpack_from("<109I", dados, 0x4C) if v < 0xFFFFFFFA]
    fat_bytes = b"".join(dados[(s + 1) * setor_tam:(s + 2) * setor_tam] for s in difat)
    fat = struct.unpack(f"<{len(fat_bytes) // 4}I", fat_bytes)
    dir_ids = _cadeia(fat, struct.unpack_from("<I", dados, 0x30)[0])
    diretorio = _ler_setores(dados, setor_tam, dir_ids, fat)
    entradas = []
    for i in range(len(diretorio) // 128):
        e = diretorio[i * 128:(i + 1) * 128]
        nome_len = struct.unpack_from("<H", e, 0x40)[0]
        nome = e[:max(nome_len - 2, 0)].decode("utf-16-le", "ignore")
        tipo = e[0x42]
        inicio, tamanho = struct.unpack_from("<II", e, 0x74)
        entradas.append((nome, tipo, inicio, tamanho))
    raiz = next(x for x in entradas if x[1] == 5)
    mini_stream = _ler_setores(dados, setor_tam, _cadeia(fat, raiz[2]), fat)
    mini_fat_ini = struct.unpack_from("<I", dados, 0x3C)[0]
    mini_fat_bytes = _ler_setores(dados, setor_tam, _cadeia(fat, mini_fat_ini), fat) if mini_fat_ini < 0xFFFFFFFA else b""
    mini_fat = struct.unpack(f"<{len(mini_fat_bytes) // 4}I", mini_fat_bytes) if mini_fat_bytes else ()

    def conteudo(entrada):
        _, _, inicio, tamanho = entrada
        if tamanho < mini_corte:
            ids = _cadeia(mini_fat, inicio)
            return b"".join(mini_stream[s * 64:(s + 1) * 64] for s in ids)[:tamanho]
        return _ler_setores(dados, setor_tam, _cadeia(fat, inicio), fat)[:tamanho]

    return {e[0]: conteudo(e) for e in entradas if e[1] == 2}

def texto_doc(caminho):
    dados = open(caminho, "rb").read()
    fluxos = _streams_ole(dados)
    word = fluxos["WordDocument"]
    flags = struct.unpack_from("<H", word, 0x0A)[0]
    tabela = fluxos["1Table" if flags & 0x0200 else "0Table"]
    fc_clx, lcb_clx = struct.unpack_from("<II", word, 0x1A2)
    ccp_texto = struct.unpack_from("<I", word, 0x4C)[0]
    clx = tabela[fc_clx:fc_clx + lcb_clx]
    pos = 0
    while clx[pos] == 0x01:  # pula prc (propriedades)
        pos += 3 + struct.unpack_from("<H", clx, pos + 1)[0]
    if clx[pos] != 0x02:
        raise ValueError("Clx sem PlcPcd")
    lcb_plc = struct.unpack_from("<I", clx, pos + 1)[0]
    plc = clx[pos + 5:pos + 5 + lcb_plc]
    n = (lcb_plc - 4) // 12
    cps = struct.unpack_from(f"<{n + 1}I", plc, 0)
    partes = []
    for i in range(n):
        fc_raw = struct.unpack_from("<I", plc, (n + 1) * 4 + i * 8 + 2)[0]
        comprimido = bool(fc_raw & 0x40000000)
        fc = fc_raw & 0x3FFFFFFF
        qtd = min(cps[i + 1], ccp_texto) - cps[i]
        if qtd <= 0:
            continue
        if comprimido:
            bruto = word[fc // 2:fc // 2 + qtd].decode("cp1252", "replace")
        else:
            bruto = word[fc:fc + 2 * qtd].decode("utf-16-le", "replace")
        partes.append(bruto)
    texto = "".join(partes)
    # marcas de controle do Word: parágrafo/célula viram quebra de linha, o resto é descartado
    texto = texto.replace("\r", "\n").replace("\x07", "\t").replace("\x0c", "\n")
    texto = "".join(ch for ch in texto if ch in "\n\t" or ord(ch) >= 32)
    return texto

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    print(texto_doc(sys.argv[1]))
