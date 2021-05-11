from gopher import GopherRenderer
import mistune

f = open('./source/page/about/index.md')
html = f.read()
f.close()


markdown = mistune.create_markdown(renderer=GopherRenderer())
print(markdown(html))
