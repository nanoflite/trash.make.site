__all__ = ['plugin_gopher_refs']

def refs_hook(md, result, state):
    refs = md.renderer.generateRefs()
    return result + refs

def plugin_gopher_refs(md):
    md.after_render_hooks.append(refs_hook)