# Vídeo do LinkedIn: carreira como suíte de testes (HyperFrames)

Vídeo de 21 s em 1080×1350 (4:5, formato de feed do LinkedIn), 30 fps, sem áudio.

1. **0–11 s:** seis marcos da carreira rodam como cenários de teste (DXC, Telefônica/VIVO, Marlabs, QA Engineer, CTFL 4.0, automação com IA). O contador vai de 0 a 6 e o ano, de 2018 até hoje.
2. **12–15 s:** a barra de progresso cheia vira o card "Build aprovado · 6 de 6 cenários · 8 anos de QA".
3. **15–21 s:** o card encolhe até virar o círculo da foto, seguido de nome, cargo, tecnologias e jvcaires.github.io.

O quadro 0 já mostra o título e a suíte, então serve de miniatura no feed.

## Variáveis

| Variável | Valores |
| --- | --- |
| `lang` | `pt` (padrão) ou `en` |
| `theme` | `dark` (padrão) ou `light` |

## Renderizar com a CLI do HyperFrames

```bash
cd animations/linkedin
npx hyperframes preview
npx hyperframes render --variables '{"lang":"pt","theme":"dark"}' --output linkedin-pt-br-dark.mp4
npx hyperframes render --variables '{"lang":"en","theme":"dark"}' --output linkedin-en-dark.mp4
```

Alternativa sem a CLI: `python3 render_local.py` (Python Playwright + FFmpeg) gera as quatro versões em `renders/`.

## Créditos

Bricolage Grotesque, Instrument Sans e IBM Plex Mono (SIL OFL, licenças em `assets/fonts/`). GSAP 3.14.2.
