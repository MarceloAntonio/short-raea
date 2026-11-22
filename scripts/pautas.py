#!/usr/bin/env python3
"""Coleta assuntos recentes de um nicho para o modo Pautas da short-raea (só biblioteca padrão).

uso: pautas.py --nicho seguranca-digital [--termos "golpe pix,vazamento"] [--janela 7d] [--regiao BR]
               [--saida PASTA] [--max-termos 3] [--tipos sugestao,sugestao-yt]
     pautas.py --teste        (checagem dos parsers, sem rede)

--janela  24h | 7d | 30d (padrão 7d)
--regiao  BR (padrão), BR-SC (estado), "cidade:Florianópolis" (BR + a cidade na busca) ou global
--tipos   só as fontes desses tipos (ex.: "sugestao,sugestao-yt" para temas que não envelhecem)

As fontes vêm de references/nichos/<nicho>.md, seção "## Fontes para o script", uma por linha:
    - tipo | nome | endereço
Tipos: rss (feed fixo), rss-busca (feed com {termo}), trends, hn, kev, sugestao, sugestao-yt, youtube.
No endereço valem {termo}, {janela}, {geo}, {hl}, {gl} e {ceid}. Em hn, sugestao, sugestao-yt e youtube, o
endereço é "{termo}" (usa os termos da rodada) ou uma lista fixa separada por vírgula.
Os termos da rodada são os de --termos ou, sem ele, os primeiros da seção "## Termos de busca".

Grava pautas/<data>-<nicho>/coleta.json (na pasta da skill, ou em --saida). Cada fonte tem timeout de 15 s
e uma nova tentativa; se falhar, a falha fica anotada em "fontes" e a coleta segue.
YouTube Data API só se existir ~/api/youtube.env com YOUTUBE_API_KEY; a chave nunca é impressa nem gravada.
"""
import argparse
import datetime as dt
import email.utils
import html
import json
import re
import sys
import time
import unicodedata
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
UA = "Mozilla/5.0 (X11; Linux x86_64) short-raea-pautas/1.0"
TIMEOUT = 15
JANELAS = {"24h": 1, "7d": 7, "30d": 30}
UTC = dt.timezone.utc


# ---------- rede ----------

def baixar(url: str) -> bytes:
    """GET com timeout de 15 s e uma nova tentativa."""
    erro = None
    for tentativa in range(2):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.5"})
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                return r.read()
        except Exception as e:  # noqa: BLE001 - qualquer falha de rede vira anotação
            erro = e
            if tentativa == 0:
                time.sleep(1)
    raise erro


# ---------- parsers ----------

def limpar(texto: str | None, n: int = 280) -> str:
    t = html.unescape(re.sub(r"<[^>]+>", " ", texto or ""))
    t = re.sub(r"\s+", " ", t).strip()
    return t[: n - 1] + "…" if len(t) > n else t


def data_de(texto: str | None) -> dt.datetime | None:
    if not texto:
        return None
    texto = texto.strip()
    try:
        d = email.utils.parsedate_to_datetime(texto)
    except (TypeError, ValueError):
        try:
            d = dt.datetime.fromisoformat(texto.replace("Z", "+00:00"))
        except ValueError:
            return None
    return d if d.tzinfo else d.replace(tzinfo=UTC)


def filho(el, *nomes):
    """Primeiro filho com um dos nomes, ignorando o namespace."""
    for c in el:
        if c.tag.split("}")[-1] in nomes:
            return c
    return None


def ler_feed(xml: bytes, fonte: str) -> list[dict]:
    """RSS 2.0 ou Atom → itens {titulo, fonte, link, data, trecho}."""
    raiz = ET.fromstring(xml)
    itens = []
    for el in raiz.iter():
        if el.tag.split("}")[-1] not in ("item", "entry"):
            continue
        t = filho(el, "title")
        l = filho(el, "link")
        link = (l.get("href") or l.text or "").strip() if l is not None else ""
        d = filho(el, "pubDate", "published", "updated", "date")
        desc = filho(el, "description", "summary", "content")
        orig = filho(el, "source")  # Google Notícias: o veículo de verdade
        itens.append({
            "titulo": limpar(t.text if t is not None else "", 200),
            "fonte": f"{fonte} / {orig.text.strip()}" if orig is not None and orig.text else fonte,
            "link": link,
            "data": d.text if d is not None else None,
            "trecho": limpar(desc.text if desc is not None else ""),
        })
    return itens


def ler_trends(xml: bytes, fonte: str) -> list[dict]:
    """Google Trends RSS: o termo, o tráfego aproximado e a primeira notícia ligada a ele."""
    itens = []
    for el in ET.fromstring(xml).iter("item"):
        t = filho(el, "title")
        trafego = filho(el, "approx_traffic")
        noticia = filho(el, "news_item")
        link = trecho = ""
        if noticia is not None:
            nl, nt = filho(noticia, "news_item_url"), filho(noticia, "news_item_title")
            link = nl.text if nl is not None else ""
            trecho = limpar(nt.text if nt is not None else "")
        d = filho(el, "pubDate")
        itens.append({
            "titulo": limpar(t.text if t is not None else "", 200) + (f" ({trafego.text} buscas)" if trafego is not None else ""),
            "fonte": fonte, "link": link, "data": d.text if d is not None else None, "trecho": trecho,
        })
    return itens


# ---------- coleta por tipo ----------

def coletar(tipo, nome, endereco, termos, ctx, desde):
    """Devolve (itens, perguntas). perguntas = {termo: [sugestões do autocompletar]}."""
    sub = lambda s, termo="": s.format(termo=urllib.parse.quote_plus(termo), **ctx)  # noqa: E731
    lista = termos if endereco.strip() == "{termo}" else [t.strip() for t in endereco.split(",") if t.strip()]
    itens, perguntas = [], {}
    if tipo == "rss":
        itens = ler_feed(baixar(sub(endereco)), nome)
    elif tipo == "rss-busca":
        for termo in termos:
            itens += ler_feed(baixar(sub(endereco, termo)), nome)
    elif tipo == "trends":
        itens = ler_trends(baixar(sub(endereco)), nome)
    elif tipo == "hn":
        ts = int(desde.timestamp())
        for termo in lista:
            q = urllib.parse.urlencode({"query": termo, "tags": "story", "numericFilters": f"created_at_i>{ts},points>20", "hitsPerPage": 15})
            for h in json.loads(baixar(f"https://hn.algolia.com/api/v1/search?{q}"))["hits"]:
                itens.append({"titulo": h.get("title") or "", "fonte": f"{nome} ({h.get('points', 0)} pontos)",
                              "link": h.get("url") or f"https://news.ycombinator.com/item?id={h['objectID']}",
                              "data": h.get("created_at"), "trecho": f"{h.get('num_comments', 0)} comentários no HN"})
    elif tipo == "kev":
        for v in json.loads(baixar(endereco))["vulnerabilities"]:
            d = data_de(v.get("dateAdded"))
            if d and d >= desde:
                itens.append({"titulo": f"{v['cveID']} {v['vendorProject']} {v['product']}: {v['vulnerabilityName']}",
                              "fonte": nome, "link": f"https://nvd.nist.gov/vuln/detail/{v['cveID']}",
                              "data": v["dateAdded"], "trecho": limpar(v.get("shortDescription"))})
    elif tipo in ("sugestao", "sugestao-yt"):
        for termo in lista:
            q = {"client": "firefox", "hl": ctx["hl"], "q": termo}
            if tipo == "sugestao-yt":
                q["ds"] = "yt"
            perguntas[termo] = json.loads(baixar("https://suggestqueries.google.com/complete/search?" + urllib.parse.urlencode(q)).decode("utf-8", "replace"))[1]
    elif tipo == "youtube":
        chave = chave_youtube()
        if not chave:
            raise PularFonte("sem ~/api/youtube.env (opcional)")
        for termo in lista:
            q = urllib.parse.urlencode({"part": "snippet", "q": termo, "type": "video", "order": "viewCount", "maxResults": 10,
                                        "publishedAfter": desde.strftime("%Y-%m-%dT%H:%M:%SZ"), "regionCode": ctx["gl"],
                                        "relevanceLanguage": ctx["hl"][:2], "key": chave})
            try:
                dados = json.loads(baixar(f"https://www.googleapis.com/youtube/v3/search?{q}"))
            except Exception as e:  # noqa: BLE001
                raise RuntimeError(str(e).replace(chave, "***")) from None  # a chave nunca vai para o JSON
            for v in dados.get("items", []):
                s = v["snippet"]
                itens.append({"titulo": html.unescape(s["title"]), "fonte": f"{nome} / {s['channelTitle']}",
                              "link": f"https://www.youtube.com/watch?v={v['id']['videoId']}", "data": s["publishedAt"],
                              "trecho": limpar(s.get("description"))})
    else:
        raise PularFonte(f"tipo desconhecido: {tipo}")
    return itens, perguntas


class PularFonte(Exception):
    pass


def chave_youtube() -> str | None:
    arq = Path.home() / "api/youtube.env"
    if not arq.exists():
        return None
    m = re.search(r"^YOUTUBE_API_KEY=(.+)$", arq.read_text(encoding="utf-8"), re.M)
    return m.group(1).strip() if m else None


# ---------- nicho, filtro e duplicados ----------

def secao(md: str, titulo: str) -> list[str]:
    m = re.search(rf"^## {re.escape(titulo)}\s*$(.*?)(?=^## |\Z)", md, re.M | re.S)
    if not m:
        return []
    return [l[2:].strip() for l in m.group(1).splitlines() if l.startswith("- ")]


def ler_nicho(nicho: str) -> tuple[list[tuple[str, str, str]], list[str]]:
    arq = SKILL / "references/nichos" / f"{nicho}.md"
    if not arq.exists():
        sys.exit(f"nicho sem arquivo: {arq} (copie references/nichos/_modelo.md)")
    md = arq.read_text(encoding="utf-8")
    fontes = []
    for linha in secao(md, "Fontes para o script"):
        partes = [p.strip() for p in linha.split("|")]
        if len(partes) == 3:
            fontes.append(tuple(partes))
    return fontes, [t.strip("`\"") for t in secao(md, "Termos de busca")]


def chave_titulo(t: str) -> str:
    t = unicodedata.normalize("NFKD", t.lower()).encode("ascii", "ignore").decode()
    t = re.sub(r"\s+-\s+[^-]+$", "", t)  # Google Notícias põe " - Veículo" no fim
    return re.sub(r"[^a-z0-9]+", " ", t).strip()[:80]


def chave_link(l: str) -> str:
    p = urllib.parse.urlsplit(l)
    q = urllib.parse.urlencode([(k, v) for k, v in urllib.parse.parse_qsl(p.query) if not k.startswith("utm_")])
    return urllib.parse.urlunsplit((p.scheme, p.netloc.lower(), p.path.rstrip("/"), q, ""))


def filtrar(itens: list[dict], desde: dt.datetime) -> list[dict]:
    """Tira o que é mais velho que a janela e os duplicados (mesmo link ou mesmo título)."""
    vistos, saida = set(), []
    for it in itens:
        d = data_de(it["data"])
        if d and d < desde:
            continue
        it["data"] = d.isoformat() if d else None
        chaves = {chave_link(it["link"]) if it["link"] else None, chave_titulo(it["titulo"]) or None} - {None}
        if not chaves or chaves & vistos:
            continue
        vistos |= chaves
        saida.append(it)
    return sorted(saida, key=lambda i: i["data"] or "", reverse=True)


def contexto(regiao: str, janela: str) -> tuple[dict, str]:
    """Placeholders das URLs e um termo extra de cidade (ou "")."""
    dias = f"{JANELAS[janela]}d"
    if regiao == "global":
        return {"geo": "US", "hl": "en-US", "gl": "US", "ceid": "US:en", "janela": dias}, ""
    cidade = regiao.split(":", 1)[1].strip() if regiao.startswith("cidade:") else ""
    geo = regiao if re.fullmatch(r"BR(-[A-Z]{2})?", regiao) else "BR"
    return {"geo": geo, "hl": "pt-BR", "gl": "BR", "ceid": "BR:pt-419", "janela": dias}, cidade


# ---------- principal ----------

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--nicho")
    ap.add_argument("--termos", default="")
    ap.add_argument("--janela", default="7d", choices=JANELAS)
    ap.add_argument("--regiao", default="BR")
    ap.add_argument("--saida")
    ap.add_argument("--max-termos", type=int, default=3)
    ap.add_argument("--tipos", default="")
    ap.add_argument("--teste", action="store_true")
    a = ap.parse_args()
    if a.teste:
        teste()
        return 0
    if not a.nicho:
        ap.error("--nicho é obrigatório")

    fontes, termos_nicho = ler_nicho(a.nicho)
    if a.tipos:
        fontes = [f for f in fontes if f[0] in a.tipos.split(",")]
    termos = [t.strip() for t in a.termos.split(",") if t.strip()] or termos_nicho[: a.max_termos]
    ctx, cidade = contexto(a.regiao, a.janela)
    termos_busca = [f"{t} {cidade}" for t in termos] if cidade else termos
    agora = dt.datetime.now(UTC)
    desde = agora - dt.timedelta(days=JANELAS[a.janela])

    brutos, perguntas, relatorio = [], {}, []
    for tipo, nome, endereco in fontes:
        try:
            itens, pergs = coletar(tipo, nome, endereco, termos_busca, ctx, desde)
            brutos += itens
            for termo, lista in pergs.items():
                perguntas.setdefault(f"{nome}: {termo}", lista)
            relatorio.append({"nome": nome, "tipo": tipo, "status": "ok", "itens": len(itens) or sum(len(l) for l in pergs.values())})
        except PularFonte as e:
            relatorio.append({"nome": nome, "tipo": tipo, "status": "pulada", "itens": 0, "erro": str(e)})
        except Exception as e:  # noqa: BLE001 - uma fonte nunca derruba a coleta
            relatorio.append({"nome": nome, "tipo": tipo, "status": "falhou", "itens": 0, "erro": f"{type(e).__name__}: {e}"[:300]})

    itens = filtrar(brutos, desde)
    pasta = Path(a.saida) if a.saida else SKILL / "pautas" / f"{agora.astimezone():%Y-%m-%d}-{a.nicho}"
    pasta.mkdir(parents=True, exist_ok=True)
    saida = {"nicho": a.nicho, "termos": termos_busca, "janela": a.janela, "regiao": a.regiao,
             "gerado_em": agora.astimezone().isoformat(timespec="seconds"), "fontes": relatorio,
             "itens": itens, "perguntas": perguntas}
    (pasta / "coleta.json").write_text(json.dumps(saida, ensure_ascii=False, indent=2), encoding="utf-8")

    for f in relatorio:
        print(f"{f['status']:7} {f['itens']:4}  {f['nome']}" + (f"  ({f['erro']})" if f.get("erro") else ""))
    print(f"{len(itens)} itens depois da janela e dos duplicados (de {len(brutos)}), "
          f"{sum(len(v) for v in perguntas.values())} perguntas do autocompletar → {pasta / 'coleta.json'}")
    return 0


def teste() -> None:
    rss = b"""<rss><channel><item><title>Golpe do Pix cresce - G1</title><link>https://g1.com/a?utm_source=x</link>
      <pubDate>Fri, 20 Nov 2026 10:00:00 GMT</pubDate><description>&lt;b&gt;Novo&lt;/b&gt; golpe</description>
      <source url="https://g1.com">G1</source></item></channel></rss>"""
    atom = b"""<feed xmlns="http://www.w3.org/2005/Atom"><entry><title>Golpe do Pix cresce</title>
      <link href="https://outro.com/b"/><updated>2026-11-19T08:00:00Z</updated></entry>
      <entry><title>Velha</title><link href="https://x.com/v"/><updated>2026-10-01T08:00:00Z</updated></entry></feed>"""
    itens = ler_feed(rss, "Google Notícias") + ler_feed(atom, "Blog")
    assert itens[0]["fonte"] == "Google Notícias / G1" and itens[0]["trecho"] == "Novo golpe", itens[0]
    desde = dt.datetime(2026, 11, 14, tzinfo=UTC)
    f = filtrar(itens, desde)
    assert [i["titulo"] for i in f] == ["Golpe do Pix cresce - G1"], "tira a velha e o mesmo título de outro veículo"
    assert chave_link("https://g1.com/a/?utm_source=x") == chave_link("https://g1.com/a")
    md = "## Fontes para o script\n- rss | A | https://a\n- linha ruim\n\n## Termos de busca\n- `golpe pix`\n"
    assert secao(md, "Fontes para o script") == ["rss | A | https://a", "linha ruim"]
    assert secao(md, "Termos de busca") == ["`golpe pix`"]
    assert contexto("cidade:Florianópolis", "7d") == ({"geo": "BR", "hl": "pt-BR", "gl": "BR", "ceid": "BR:pt-419", "janela": "7d"}, "Florianópolis")
    assert contexto("BR-SC", "24h")[0]["geo"] == "BR-SC"
    print("✓ pautas ok")


if __name__ == "__main__":
    sys.exit(main())
