from .gopher import GopherRenderer
from .gopher_refs import plugin_gopher_refs
import mistune

def mdtogopher(md):
    markdown = mistune.create_markdown(renderer=GopherRenderer(), plugins=[plugin_gopher_refs])
    return markdown(md)
