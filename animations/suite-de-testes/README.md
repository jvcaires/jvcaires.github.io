# Animação: suíte de testes (HyperFrames)

Composição [HyperFrames](https://github.com/heygen-com/hyperframes) do painel animado que aparece no topo do portfólio: uma suíte de regressão rodando, 37 cenários passando e 1 defeito barrado antes do deploy. São 10 s a 30 fps, 1280×960, em loop sem corte (o último quadro é igual ao primeiro).

A composição tem duas variáveis:

| Variável | Valores |
| --- | --- |
| `lang` | `pt` (padrão) ou `en` |
| `theme` | `light` (padrão) ou `dark` |

## Editar e renderizar com a CLI do HyperFrames

Requer Node.js 22+ e FFmpeg.

```bash
cd animations/suite-de-testes
npx hyperframes preview                                   # pré-visualização com recarga automática
npx hyperframes render --variables '{"lang":"pt","theme":"light"}' --output suite-pt-br-light.mp4
npx hyperframes render --variables '{"lang":"pt","theme":"dark"}'  --output suite-pt-br-dark.mp4
npx hyperframes render --variables '{"lang":"en","theme":"light"}' --output suite-en-light.mp4
npx hyperframes render --variables '{"lang":"en","theme":"dark"}'  --output suite-en-dark.mp4
```

Depois copie os MP4 para `assets/video/` na raiz do site. Para gerar as versões WebM e os pôsteres:

```bash
ffmpeg -i suite-pt-br-light.mp4 -c:v libvpx-vp9 -b:v 0 -crf 36 -an suite-pt-br-light.webm
ffmpeg -ss 8 -i suite-pt-br-light.mp4 -frames:v 1 suite-pt-br-light.webp
```

## Renderizador local alternativo

`render_local.py` faz o mesmo processo da CLI (seek da timeline GSAP quadro a quadro no Chromium + FFmpeg) usando Python Playwright. Foi o que gerou os vídeos atuais, porque a CLI não pôde ser instalada no ambiente onde a animação foi criada.

```bash
python3 render_local.py            # as quatro versões em renders/
python3 render_local.py en dark    # só uma
```

## Créditos

- IBM Plex Mono, licença SIL OFL (`assets/fonts/IBMPlexMono-OFL.txt`)
- GSAP 3.14.2
