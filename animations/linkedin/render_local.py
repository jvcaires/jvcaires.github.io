"""Renderizador local no mesmo modelo do HyperFrames (seek quadro a quadro + FFmpeg).

Com a CLI do HyperFrames disponível, o equivalente é:
    npx hyperframes render --variables '{"lang":"pt","theme":"dark"}' --output linkedin-pt-br-dark.mp4
"""
import json, subprocess, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
FPS = 30
W, H = 1080, 1350
CLIP = {"x": 0, "y": 0, "width": W, "height": H}


def open_page(p, lang, theme):
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
    page.add_init_script("window.__hyperframes = { getVariables: () => (%s) };" % json.dumps({"lang": lang, "theme": theme}))
    page.goto((ROOT / "index.html").as_uri())
    page.wait_for_function("() => !!(window.__timelines && window.__timelines.main)")
    page.evaluate("document.fonts.ready")
    return browser, page


def seek(page, t):
    page.evaluate("t => { window.__timelines.main.seek(t, false); }", t)


def render(lang, theme, out_dir):
    name = f"linkedin-{'pt-br' if lang == 'pt' else 'en'}-{theme}"
    with sync_playwright() as p:
        browser, page = open_page(p, lang, theme)
        dur = page.evaluate("parseFloat(document.querySelector('[data-composition-id=main]').dataset.duration)")
        ff = subprocess.Popen(
            ["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS), "-i", "-",
             "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p",
             "-movflags", "+faststart", "-an", str(out_dir / f"{name}.mp4")],
            stdin=subprocess.PIPE)
        for f in range(round(dur * FPS)):
            seek(page, f / FPS)
            ff.stdin.write(page.screenshot(type="png", clip=CLIP))
        ff.stdin.close(); ff.wait()
        seek(page, 0)  # capa: o quadro 0 já mostra o título e a suíte
        page.screenshot(path=str(out_dir / f"{name}-capa.png"), type="png", clip=CLIP)
        browser.close()
    print("ok", name)


def stills(lang, theme, times, out_dir):
    with sync_playwright() as p:
        browser, page = open_page(p, lang, theme)
        for t in times:
            seek(page, t)
            page.screenshot(path=str(out_dir / f"still-{lang}-{theme}-{t:05.2f}.png"), type="png", clip=CLIP)
        browser.close()


if __name__ == "__main__":
    out = ROOT / "renders"; out.mkdir(exist_ok=True)
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        stills(sys.argv[2], sys.argv[3], [float(x) for x in sys.argv[4].split(",")], out)
    else:
        combos = [(l, t) for t in ("dark", "light") for l in ("pt", "en")]
        if len(sys.argv) == 3:
            combos = [(sys.argv[1], sys.argv[2])]
        for l, t in combos:
            render(l, t, out)
