#!/usr/bin/env python3
"""Conta as ênfases (zoom, pop, tremida, pulso) do roteiro.json contra o orçamento e lista as animações de escala
no código. Reprova (sai com 1) se passar do orçamento. Regra em references/movimento.md, seção 2.

uso: scripts/contar-enfases.py roteiro.json [pasta-components]
     scripts/contar-enfases.py --teste        (autoteste)

Orçamento por vídeo de 30 a 40 s:
  zoom    ≤ 2, só nos passos "gancho" e "virada"
  pop     ≤ 3 (entrada em escala de 0 para 1, só nos momentos-chave)
  tremida ≤ 1
  pulso   = 0 (nada que já está na tela pulsa, respira ou cresce)

No roteiro, cada ênfase é um objeto com "enfase": true e "tipo", em qualquer lugar do passo (o normal é
passo.movimento.enfases). Cada passo precisa do campo "movimento".

No código (components/**/*.tsx), a busca é heurística: lista as linhas que animam escala, zoom ou fov e as que
usam pulso()/soco() ou cameraPorPasso() com força. Pulso no código reprova; mais linhas de escala animada do que
o orçamento total (2 + 3 + 1 = 6) também. Confira a lista: uma linha pode ser falso positivo.
"""
import json
import os
import re
import sys
import tempfile

ORCAMENTO = {"zoom": 2, "pop": 3, "tremida": 1, "pulso": 0}
ZOOM_SO_EM = {"gancho", "virada"}
LIMITE_CODIGO = ORCAMENTO["zoom"] + ORCAMENTO["pop"] + ORCAMENTO["tremida"]

# escala com valor calculado (não literal): scale(${e}), withScale([e, e, e]), scale: e, scale={e}; fov ou zoom animado
ESCALA = re.compile(r"scale\(\$\{(?!\s*[\d.]+\s*\})|withScale\(\[(?![\d.,\s]+\])|\bscale\s*[:=]\s*\{?(?![\d.\s]*[,}\"'])"
                    r"|\b(fov|zoom)\b.*(interpolate|spring|entra\(|\bf\b|frame)", re.I)
PULSO_USO = re.compile(r"\b(pulso|soco)\(")
DEFINICAO = re.compile(r"^\s*(export\s+)?(const|function)\s+(pulso|soco|cameraPorPasso)\b")
CAMERA_FORCA = re.compile(r"cameraPorPasso\(([^;]*)\)")


def enfases(o, acc):
    if isinstance(o, dict):
        if o.get("enfase") is True:
            acc.append(o)
        for v in o.values():
            enfases(v, acc)
    elif isinstance(o, list):
        for v in o:
            enfases(v, acc)
    return acc


def contar_roteiro(r):
    """Devolve (contagem por tipo, lista de problemas)."""
    passos = [p for p in [r.get("gancho"), *r.get("passos", [])] if p]
    conta = {t: 0 for t in ORCAMENTO}
    problemas = []
    for p in passos:
        pid = p.get("id", "?")
        if "movimento" not in p:
            problemas.append(f'passo "{pid}" sem o campo "movimento"')
        for e in enfases(p, []):
            tipo = str(e.get("tipo", "")).lower()
            if tipo not in conta:
                problemas.append(f'passo "{pid}": ênfase de tipo desconhecido "{tipo}" (use zoom, pop, tremida ou pulso)')
                continue
            conta[tipo] += 1
            if tipo == "zoom" and pid not in ZOOM_SO_EM:
                problemas.append(f'passo "{pid}": zoom fora do gancho e da virada')
    for tipo, n in conta.items():
        if n > ORCAMENTO[tipo]:
            problemas.append(f"{tipo}: {n} (máx {ORCAMENTO[tipo]})")
    return conta, problemas


def varrer_codigo(pasta):
    """Devolve (linhas de escala animada, linhas de pulso/soco) como 'arquivo:linha: trecho'."""
    escala, pulso = [], []
    if not pasta or not os.path.isdir(pasta):
        return escala, pulso
    for raiz, _, arqs in os.walk(pasta):
        if "node_modules" in raiz:
            continue
        for a in sorted(arqs):
            if not a.endswith(".tsx"):
                continue
            cam = os.path.join(raiz, a)
            rel = os.path.relpath(cam, os.path.dirname(pasta.rstrip("/")) or ".")
            with open(cam, encoding="utf-8") as fh:
                for i, linha in enumerate(fh, 1):
                    s = linha.strip()
                    if s.startswith("//") or DEFINICAO.search(linha) or "forca *" in linha:
                        continue
                    onde = f"{rel}:{i}: {s[:110]}"
                    m = CAMERA_FORCA.search(linha)
                    if m and not re.search(r",\s*0(\.0+)?\s*\)?\s*$", m.group(1)):
                        pulso.append(onde + "   ← cameraPorPasso com força: soco de câmera em cada efeito")
                    elif PULSO_USO.search(linha):
                        pulso.append(onde)
                    elif ESCALA.search(linha):
                        escala.append(onde)
    return escala, pulso


def avaliar(roteiro_path, pasta):
    with open(roteiro_path, encoding="utf-8") as fh:
        r = json.load(fh)
    conta, problemas = contar_roteiro(r)
    escala, pulso = varrer_codigo(pasta)
    if pulso:
        problemas.append(f"código: {len(pulso)} uso(s) de pulso/soco (orçamento 0)")
    if len(escala) > LIMITE_CODIGO:
        problemas.append(f"código: {len(escala)} linhas de escala/zoom animada (máx {LIMITE_CODIGO})")
    return conta, problemas, escala, pulso


def main(argv):
    if argv[1:] == ["--teste"]:
        return autoteste()
    if len(argv) < 2:
        print(__doc__.strip().splitlines()[2], file=sys.stderr)
        return 2
    roteiro = argv[1]
    pasta = argv[2] if len(argv) > 2 else os.path.join(os.path.dirname(os.path.abspath(roteiro)), "components")
    conta, problemas, escala, pulso = avaliar(roteiro, pasta)
    print("roteiro: " + ", ".join(f"{t} {n}/{ORCAMENTO[t]}" for t, n in conta.items()))
    if escala:
        print(f"código, escala/zoom animada ({len(escala)}):")
        print("\n".join("  " + x for x in escala))
    if pulso:
        print(f"código, pulso/soco ({len(pulso)}):")
        print("\n".join("  " + x for x in pulso))
    if problemas:
        print("REPROVADO: " + "; ".join(problemas))
        print("Troque o excesso por informação nova: um elemento que entra, uma ação, a cena que muda (references/movimento.md).")
        return 1
    print("OK: dentro do orçamento de ênfase")
    return 0


def autoteste():
    mov = lambda *e: {"entra": "x", "como": "desliza", "camera": "travelling", "enfases": list(e)}
    z = {"tipo": "zoom", "enfase": True}
    p = {"tipo": "pop", "enfase": True}
    bom = {"passos": [{"id": "gancho", "movimento": mov(z, p)}, {"id": "meio", "movimento": mov()},
                      {"id": "virada", "movimento": mov(z, p)}, {"id": "cta", "movimento": mov(p)}]}
    conta, probs = contar_roteiro(bom)
    assert conta == {"zoom": 2, "pop": 3, "tremida": 0, "pulso": 0} and not probs, (conta, probs)
    ruim = {"passos": [{"id": f"p{k}", "movimento": mov(z, p)} for k in range(6)] + [{"id": "virada", "movimento": mov(z)}]}
    conta, probs = contar_roteiro(ruim)
    assert conta["zoom"] == 7 and conta["pop"] == 6, conta
    assert any(x.startswith("zoom: 7") for x in probs) and any(x.startswith("pop: 6") for x in probs), probs
    assert any("fora do gancho" in x for x in probs), probs
    assert any("sem o campo" in x for x in contar_roteiro({"passos": [{"id": "a"}]})[1])
    with tempfile.TemporaryDirectory() as d:
        os.makedirs(os.path.join(d, "components"))
        with open(os.path.join(d, "components", "Video.tsx"), "w") as fh:
            fh.write("export const pulso = (l, f) => 1;\n"
                     "const z = 1 + 0.04 * pulso(l, f);\n"
                     "const { pos } = cameraPorPasso(l, f, fn, 0.08);\n"
                     "const ok = cameraPorPasso(l, f, fn, 0);\n"
                     "<g transform={`scale(${interpolate(f, [0, 10], [0, 1])})`} />\n"
                     "<g transform={`translate(1 2) scale(${e})`} />\n"
                     "<Camera3d projection={{ Perspective: { fov: (32 * Math.PI) / 180 } }} />\n"
                     "<g transform={`scale(${1.5})`} />\n"
                     "const fov = interpolate(f, [0, 20], [40, 30]);\n")
        escala, pulso = varrer_codigo(os.path.join(d, "components"))
        assert len(pulso) == 2 and len(escala) == 3, (escala, pulso)
    print("autoteste ok")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
