"""Baut die eigenständige iPhone-App (index.html im Hauptordner) aus dashboard/index.html.

Nach jeder Änderung an dashboard/index.html:  python3 build.py
"""
from pathlib import Path

root = Path(__file__).parent
src = (root / "dashboard" / "index.html").read_text(encoding="utf-8")

# Leer starten statt mit Beispiel-Einträgen
src = src.replace(
    'load("todos",[{t:"Beispiel: Zahnarzt anrufen",d:false},{t:"Beispiel: Wocheneinkauf",d:true}])',
    'load("todos",[])',
).replace(
    'load("events",{[today]:[{h:"18:30",t:"Beispiel: Abendessen mit Freunden"}]})',
    'load("events",{})',
)
assert "Beispiel:" not in src, "Beispiel-Einträge nicht ersetzt"

head = """<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Mein Tag">
<meta name="theme-color" content="#f8f7f3" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#171614" media="(prefers-color-scheme: dark)">
<link rel="apple-touch-icon" href="icon-180.png">
<link rel="icon" href="icon-180.png">
<link rel="manifest" href="manifest.webmanifest">
<style>
/* Sofort Papierfarbe statt weißem Aufblitzen */
html{background:#f8f7f3}
@media (prefers-color-scheme: dark){html{background:#171614}}
body{margin:0}
[hidden]{display:none!important}
</style>
</head>
<body>
"""

tail = """
<style>
/* Eigenständige App: Notch / Dynamic Island und Home-Leiste freihalten */
html,body{overscroll-behavior:none;-webkit-text-size-adjust:100%}
body{-webkit-tap-highlight-color:transparent;
  padding-top:calc(26px + env(safe-area-inset-top,0px))!important;
  padding-bottom:calc(30px + max(6px,env(safe-area-inset-bottom,0px) - 20px))!important}
/* Sichern / Hell ganz unten in den Ecken, neben der Home-Leiste */
body>footer.app-foot{position:fixed;left:0;right:0;bottom:0;margin:0;z-index:5;display:flex;justify-content:space-between;
  padding:0 max(22px,env(safe-area-inset-right,0px)) max(6px,calc(env(safe-area-inset-bottom,0px) - 20px)) max(22px,env(safe-area-inset-left,0px))}
html.short body>footer.app-foot{padding-bottom:2px}
html.short body{padding-bottom:24px!important}
</style>
<script>
(function(){var f=document.querySelector(".page>footer");if(!f)return;f.classList.add("app-foot");document.body.appendChild(f);
  /* iOS 26: Die Home-Bildschirm-App endet unten ca. 59 Punkte über dem Rand und kann dort nichts zeichnen.
     Dann die Fußzeile so tief wie möglich an den unteren Rand dieses Bereichs setzen. */
  function low(){var g=(screen.height||0)-window.innerHeight;document.documentElement.classList.toggle("short",!!navigator.standalone&&window.innerHeight>window.innerWidth&&g>=20&&g<160)}
  low();window.addEventListener("resize",low);window.addEventListener("orientationchange",function(){setTimeout(low,300)})})();
if("serviceWorker" in navigator){navigator.serviceWorker.register("sw.js").catch(function(){})}
</script>
</body>
</html>
"""

(root / "index.html").write_text(head + src + tail, encoding="utf-8")
print("index.html gebaut")
