"""Génère index.html (version installable, GitHub Pages) à partir de src/game.html.

src/game.html est la source unique du jeu (c'est aussi elle qui est publiée en aperçu Claude).
Après chaque modification du jeu : python3 build.py, puis commit des deux fichiers.
"""
import hashlib, pathlib, re

here = pathlib.Path(__file__).parent
game = (here / 'src' / 'game.html').read_text(encoding='utf-8')
manifest = (here / 'manifest.webmanifest').read_bytes()
version = hashlib.sha1(game.encode() + manifest).hexdigest()[:10]  # change si le jeu ou le manifeste change

head = """<!doctype html>
<html lang="en" translate="no">
<head>
<meta charset="utf-8">
<meta name="google" content="notranslate">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover, user-scalable=no">
<meta name="theme-color" content="#07070b">
<meta name="description" content="Find the way out of a dark maze with a 60° lamp, without getting caught by the hunters.">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Glimmer Maze">
<link rel="manifest" href="manifest.webmanifest">
<script src="/firebase-config.js"></script>
<script src="/studiom-fb.js"></script>
<link rel="icon" type="image/png" sizes="192x192" href="icons/icon-192.png">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}</style>
"""
# Le <title> et les <link>/<style> du jeu passent dans le <head>, le reste dans le <body>.
cut = game.index('</style>') + len('</style>')
body = game[cut:]
sw = """
<script>
if ('serviceWorker' in navigator) addEventListener('load', () => navigator.serviceWorker.register('sw.js?v=%s').catch(() => {}));
</script>
""" % version
out = head + game[:cut] + "\n</head>\n<body>" + body + sw + "</body>\n</html>\n"
(here / 'index.html').write_text(out, encoding='utf-8')

swsrc = (here / 'sw.template.js').read_text(encoding='utf-8').replace('__VERSION__', version)
(here / 'sw.js').write_text(swsrc, encoding='utf-8')
print('index.html et sw.js générés, version', version)
