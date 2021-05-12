from TrashMakeSite.gopher import mdtogopher
from pyfiglet import Figlet

figlet = Figlet(font='small', width=75)
print(figlet.renderText("About."))
print(figlet.renderText("Flappy bird running on my home build BASIC computer."))

fns = ['./source/page/about/index.md', './source/post/2021-03-02-a-new-site/index.md', './source/post/2017-03-08-flappy-bird-running-home-build-basic-computer/index.md']
for fn in fns:
    f = open(fn)
    html = f.read()
    f.close()
    print(mdtogopher(html))
