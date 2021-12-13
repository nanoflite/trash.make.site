from .gopher import GopherRenderer
from .gopher_refs import plugin_gopher_refs
from TrashMakeSite.images import plugin_images
import mistune

def mdtogopher(md):
    markdown = mistune.create_markdown(renderer=GopherRenderer(), plugins=[plugin_gopher_refs, plugin_images])
    return markdown(md)