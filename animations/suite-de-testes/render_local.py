"""Renderizador local no mesmo modelo do HyperFrames (seek quadro a quadro + FFmpeg).

Usado porque a CLI `npx hyperframes` não pôde ser instalada neste ambiente.
Com a CLI disponível, o equivalente é:
    npx hyperframes render --variables '{"lang":"en","theme":"dark"}'
"""
import json, subprocess, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
FPS = 30
CLIP = {"x": 0, "y": 0, "width": 1280, "height": 960}


def render(lang: str, theme: str, out_dir: Path) -> None:
    variables = {"lang": lang, "theme": theme}
    name = f"suite-{'pt-br' if lang == 'pt' else 'en'}-{theme}"
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 960}, device_scale_factor=1)
        page.add_init_script(
            "window.__hyperframes = { getVariables: () => (%s) };" % json.dumps(variables)
        )
        page.goto((ROOT / "index.html").as_uri())
        page.wait_for_function("() => !!(window.__timelines && window.__timelines.main)")
        page.evaluate("document.fonts.ready")
        info = page.evaluate(
            "(() => { const r = document.querySelector('[data-composition-id=main]');"
            " return { d: parseFloat(r.dataset.duration) }; })()"
        )
        frames = round(info["d"] * FPS)

        ff = subprocess.Popen(
            ["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS),
             "-i", "-", "-c:v", "libx264", "-preset", "slow", "-crf", "23",
             "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-an",
             str(out_dir / f"{name}.mp4")],
            stdin=subprocess.PIPE,
        )
        for f in range(frames):
            page.evaluate("t => { window.__timelines.main.seek(t, false); }", f / FPS)
            ff.stdin.write(page.screenshot(type="png", clip=CLIP))
        ff.stdin.close()
        ff.wait()

        # Pôster: o estado completo em repouso (usado sem animação e antes do vídeo carregar)
        page.evaluate("t => { window.__timelines.main.seek(t, false); }", 8.0)
        page.screenshot(path=str(out_dir / f"{name}.png"), type="png", clip=CLIP)
        browser.close()
    print("ok", name, frames, "frames")


if __name__ == "__main__":
    out = ROOT / "renders"
    out.mkdir(exist_ok=True)
    combos = [(l, t) for l in ("pt", "en") for t in ("light", "dark")]
    if len(sys.argv) == 3:
        combos = [(sys.argv[1], sys.argv[2])]
    for l, t in combos:
        render(l, t, out)
