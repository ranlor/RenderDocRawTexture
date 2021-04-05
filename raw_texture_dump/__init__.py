import qrenderdoc as qrd
import renderdoc as rd
from . import WindowDialog

extiface_version = ''


def windowCallback(ctx: qrd.CaptureContext, data):
    win = WindowDialog.get_window(ctx,extiface_version)

    ctx.RaiseDockWindow(win)

def register(version: str, ctx: qrd.CaptureContext):
    global extiface_version
    extiface_version = version

    print("Registering  extension for RenderDoc version {}".format(version))
    ctx.Extensions().RegisterPanelMenu(qrd.PanelMenu.TextureViewer,["Save Texture as Binary"], windowCallback)
    
def unregister():
    print("Unregistering extension")