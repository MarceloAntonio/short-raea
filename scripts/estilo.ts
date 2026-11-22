// Medidas comuns dos overlays: a área segura do 9:16 e o texto com contorno.
// Fonte e cor vêm da marca (marcas/<marca>.md → roteiro.json), nunca fixas aqui.
import type { CSSProperties } from "react";

export const W = 1080;
export const H = 1920;
// zonas seguras: 10% topo, 20% base, 15% direita. O conteúdo fica centralizado em x=540 com
// largura máxima de 740 px, o que mantém tudo à esquerda de 918 px (85%).
export const SEGURO = { topo: H * 0.1, base: H * 0.8, direita: W * 0.85, esquerda: 48 };
export const LARGURA_MAX = 740;

export const contorno = (px = 10, cor = "#000"): CSSProperties => ({
  // o raea não tem -webkit-text-stroke: o contorno é um anel de 16 sombras
  textShadow: Array.from({ length: 16 }, (_, i) => `${(px * 0.6 * Math.cos((i * Math.PI) / 8)).toFixed(1)}px ${(px * 0.6 * Math.sin((i * Math.PI) / 8)).toFixed(1)}px 0 ${cor}`)
    .concat("0 6px 18px rgba(0,0,0,.55)").join(", "),
});

export const titulo = (tamanho: number, fonte: string, cor = "#fff"): CSSProperties => ({
  fontFamily: fonte,
  fontWeight: 700,
  fontSize: tamanho,
  lineHeight: 1.05,
  color: cor,
  letterSpacing: -0.5,
  ...contorno(Math.round(tamanho / 7)),
});

/** Prende x dentro da área segura, dada a largura do elemento. */
export const prenderX = (x: number, largura: number) =>
  Math.min(SEGURO.direita - largura / 2, Math.max(SEGURO.esquerda + largura / 2, x));
export const prenderY = (y: number, altura: number) =>
  Math.min(SEGURO.base - altura / 2 - 300, Math.max(SEGURO.topo + altura / 2, y));
