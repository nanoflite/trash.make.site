from .gemini import GeminiRenderer
from .gemini_refs import plugin_gemini_refs
from TrashMakeSite.images import plugin_images
import mistune

def mdtogemini(md):
    markdown = mistune.create_markdown(renderer=GeminiRenderer(), plugins=[plugin_gemini_refs, plugin_images])
    return markdown(md)
