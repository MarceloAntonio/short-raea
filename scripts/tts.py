"""Uma fala do edge-tts: grava o MP3 e imprime em JSON o tempo de cada palavra (segundos).

uso: tts.py TEXTO VOZ VELOCIDADE SAIDA.mp3
"""
import asyncio
import json
import sys

import edge_tts


async def main(texto: str, voz: str, velocidade: str, saida: str) -> None:
    fala = edge_tts.Communicate(texto, voz, rate=velocidade, boundary="WordBoundary")
    palavras = []
    with open(saida, "wb") as f:
        async for parte in fala.stream():
            if parte["type"] == "audio":
                f.write(parte["data"])
            elif parte["type"] == "WordBoundary":
                inicio = parte["offset"] / 1e7  # unidades de 100 ns
                palavras.append({"texto": parte["text"], "inicio": inicio, "fim": inicio + parte["duration"] / 1e7})
    if not palavras:
        sys.exit("edge-tts não devolveu tempos de palavra")
    print(json.dumps(palavras, ensure_ascii=False))


asyncio.run(main(*sys.argv[1:5]))
