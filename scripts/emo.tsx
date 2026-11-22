// Troca cada emoji de um texto por um PNG da Noto (compositions/media/emoji/CODIGO.png, de `npm pack emoji-datasource-google`, img/google/64/) e o ✓ por um traço SVG.
import { Fragment, type ReactNode } from "react";
import { Img, staticFile } from "raea";

const EMOJI = /(\p{Extended_Pictographic}️?|✓)/u;

export function emo(texto: string): ReactNode {
  if (!EMOJI.test(texto)) return texto;
  return texto.split(EMOJI).map((parte, i) => {
    if (i % 2 === 0) return parte ? <Fragment key={i}>{parte}</Fragment> : null;
    const tam = { width: "1.1em", height: "1.1em", verticalAlign: "-0.2em", display: "inline-block" } as const;
    if (parte === "✓")
      return (
        <svg key={i} viewBox="0 0 24 24" style={tam}>
          <path d="M4 12.5l5 5L20 6.5" fill="none" stroke="currentColor" strokeWidth={3.4} strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      );
    const codigo = parte.codePointAt(0)!.toString(16);
    return <Img key={i} src={staticFile(`emoji/${codigo}.png`)} style={tam} />;
  });
}
