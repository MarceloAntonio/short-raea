#!/usr/bin/env python3
"""Aponta frases com cara de IA ou de tradução na narração e na legenda.

uso: lint-texto.py ARQUIVO [ARQUIVO...]     (.txt, .md ou roteiro.json)
     lint-texto.py --texto "legenda aqui"
     lint-texto.py --teste                  (roda a checagem do próprio script)

Sai com 1 se achar algo. As listas vêm de references/legenda.md ("Tom para o público brasileiro") e
references/conceitos.md ("Clichês proibidos"); quando uma delas mudar, mude aqui também.

No .md, o que está entre aspas ou crases é citação (é assim que as próprias regras listam os termos
proibidos) e não conta. No roteiro.json, entram todas as strings com espaço (falas, rótulos, CTA).
"""
import json
import re
import sys

# (padrão, motivo). Padrões sem distinção de maiúsculas.
REGRAS = [
    (r"\bdescubra\b", "cara de anúncio traduzido (legenda.md)"),
    (r"\bmergulhe\b", "tradução de 'dive into' (legenda.md)"),
    (r"\beleve (seu|sua|seus|suas|o|a)\b", "tradução de 'elevate your' (legenda.md)"),
    (r"\bdesbloqueie\b", "tradução de 'unlock' (legenda.md)"),
    (r"\bjornada\b", "palavra de IA (legenda.md)"),
    (r"\bgame[ -]?changer\b", "anglicismo de marketing (legenda.md)"),
    (r"\bno final do dia\b", "tradução de 'at the end of the day' (legenda.md)"),
    (r"\bnão é (só|apenas|somente) [^.!?\n]{1,60}?, é\b", "fórmula 'Não é só X, é Y' (conceitos.md)"),
    (r"\bo futuro é agora\b", "frase de efeito vazia (conceitos.md)"),
    (r"\boi,? tudo bem\b", "abertura clichê (conceitos.md)"),
]
TRAVESSAO_POR_CARACTERES = 400  # mais de um travessão a cada 400 caracteres é excesso
CITACAO = re.compile(r'"[^"\n]*"|“[^”\n]*”|`[^`\n]*`|```.*?```', re.S)


def apagar_citacoes(texto: str) -> str:
    """Troca o conteúdo citado por espaços, para as posições (linha:coluna) continuarem certas."""
    return CITACAO.sub(lambda m: re.sub(r"[^\n]", " ", m.group()), texto)


def checar(texto: str, nome: str) -> list[str]:
    achados = []

    def pos(i: int) -> str:
        linha = texto.count("\n", 0, i) + 1
        return f"{nome}:{linha}:{i - (texto.rfind(chr(10), 0, i) + 1) + 1}"

    for padrao, motivo in REGRAS:
        for m in re.finditer(padrao, texto, re.I):
            achados.append(f"{pos(m.start())}: \"{m.group()}\": {motivo}")
    travessoes = [m.start() for m in re.finditer("—", texto)]
    limite = max(1, len(texto) // TRAVESSAO_POR_CARACTERES)
    if len(travessoes) > limite:
        achados.append(f"{pos(travessoes[0])}: {len(travessoes)} travessões em {len(texto)} caracteres (máx {limite}): troque por vírgula, dois-pontos ou ponto (legenda.md)")
    return achados


def textos_do_json(dado, caminho="") -> list[tuple[str, str]]:
    if isinstance(dado, dict):
        return [t for k, v in dado.items() for t in textos_do_json(v, f"{caminho}.{k}")]
    if isinstance(dado, list):
        return [t for i, v in enumerate(dado) for t in textos_do_json(v, f"{caminho}[{i}]")]
    if isinstance(dado, str) and " " in dado:
        return [(caminho.lstrip("."), dado)]
    return []


def checar_arquivo(arq: str) -> list[str]:
    with open(arq, encoding="utf-8") as f:
        texto = f.read()
    if arq.endswith(".json"):
        return [a for caminho, t in textos_do_json(json.loads(texto)) for a in checar(t, f"{arq}#{caminho}")]
    if arq.endswith(".md"):
        texto = apagar_citacoes(texto)
    return checar(texto, arq)


def teste() -> None:
    assert checar("Descubra a jornada que vai elevar.", "t") and len(checar("Descubra a jornada.", "t")) == 2
    assert checar("Não é só um backup, é paz de espírito.", "t")
    assert not checar("Seu e-mail provavelmente já apareceu num vazamento.", "t")
    assert checar("a — b — c", "t"), "dois travessões num texto curto"
    assert not checar("a — b", "t"), "um travessão passa"
    assert not checar(apagar_citacoes('Evite "Descubra" e `jornada`.'), "t"), "citação no .md não conta"
    assert checar_json_teste()
    print("✓ lint-texto ok")


def checar_json_teste() -> bool:
    achados = [a for c, t in textos_do_json({"gancho": {"narracao": "Mergulhe nessa jornada"}, "id": "gancho"}) for a in checar(t, c)]
    return len(achados) == 2 and achados[0].startswith("gancho.narracao:1:1")


def main() -> int:
    args = sys.argv[1:]
    if args == ["--teste"]:
        teste()
        return 0
    if not args:
        print(__doc__)
        return 2
    if args[0] == "--texto":
        achados = checar(" ".join(args[1:]), "texto")
    else:
        achados = [a for arq in args for a in checar_arquivo(arq)]
    for a in achados:
        print(a)
    print(f"{len(achados)} trecho(s) com cara de IA ou de tradução" if achados else "✓ nenhum trecho com cara de IA ou de tradução")
    return 1 if achados else 0


if __name__ == "__main__":
    sys.exit(main())
