"""Génère les images de partage à partir de modèles HTML, rendus par Chrome sans fenêtre.

- tools/og-image.html → assets/img/partage.jpg (1200x630, aperçu des liens partagés)
- tools/icone.html    → assets/img/apple-touch-icon.png (180x180, icône iPhone/iPad)

Il faut Google Chrome, Chromium ou Microsoft Edge (sinon : variable CHROME=chemin)
et Pillow pour l'enregistrement en JPEG. Usage :

    uv run --with pillow tools/og_image.py     # ou : pip install pillow && python3 tools/og_image.py
"""
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

from PIL import Image

RACINE = Path(__file__).resolve().parent.parent
OUTILS = RACINE / "tools"
IMG = RACINE / "assets" / "img"
POIDS_MAX = 300_000  # WhatsApp ignore les images d'aperçu trop lourdes

CANDIDATS = [
    "google-chrome", "chromium", "chromium-browser", "chrome", "msedge",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
]


def trouver_chrome():
    for nom in [os.environ.get("CHROME")] + CANDIDATS:
        if nom and (shutil.which(nom) or Path(nom).is_file()):
            return shutil.which(nom) or nom
    raise SystemExit("Chrome introuvable : indiquer son chemin dans la variable CHROME.")


def capturer(chrome, modele, largeur, hauteur, sortie):
    subprocess.run(
        [
            chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars",
            "--force-device-scale-factor=1", f"--window-size={largeur},{hauteur}",
            "--virtual-time-budget=3000",  # laisse le temps aux polices de se charger
            f"--screenshot={sortie}", modele.as_uri(),
        ],
        check=True, capture_output=True,
    )
    with Image.open(sortie) as image:
        assert image.size == (largeur, hauteur), image.size
        return image.convert("RGB")


def main():
    chrome = trouver_chrome()
    with tempfile.TemporaryDirectory() as tmp:
        apercu = capturer(chrome, OUTILS / "og-image.html", 1200, 630, Path(tmp) / "apercu.png")
        icone = capturer(chrome, OUTILS / "icone.html", 180, 180, Path(tmp) / "icone.png")

    partage = IMG / "partage.jpg"
    apercu.save(partage, "JPEG", quality=90, optimize=True)
    assert partage.stat().st_size < POIDS_MAX, partage.stat().st_size
    print(f"{partage} ({partage.stat().st_size} octets)")

    touch = IMG / "apple-touch-icon.png"
    icone.save(touch, "PNG", optimize=True)
    print(f"{touch} ({touch.stat().st_size} octets)")


if __name__ == "__main__":
    main()
