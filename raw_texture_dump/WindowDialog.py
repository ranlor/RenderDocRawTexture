import qrenderdoc as qrd
import renderdoc as rd
from typing import Optional

mqt: qrd.MiniQtHelper

class WindowDialog(qrd.CaptureViewer):
    def __init__(self, ctx: qrd.CaptureContext, version: str):
        super().__init__()

        self.mFilepath = ""
        self.ctx = ctx
        self.version = version
        self.topWindow = mqt.CreateToplevelWidget("Texture as binary", lambda c, w, d: closed())

        vert = mqt.CreateVerticalContainer()
        mqt.AddWidget(self.topWindow, vert)

        self.saveCloseButton = mqt.CreateButton(lambda c, w, d:self.actionSaveImage(ctx))
        self.saveToButton = mqt.CreateButton(lambda c, w, d:self.setFilePath(ctx))
        self.filePathTextbox = mqt.CreateTextBox(True, lambda c,w,d:self.updatePath(d))

        mqt.SetWidgetText(self.saveToButton, "...")
        mqt.SetWidgetText(self.saveCloseButton, "save")

        # Add inside a horizontal container to left align it
        horiz = mqt.CreateHorizontalContainer()
        mqt.AddWidget(horiz, self.filePathTextbox)
        mqt.AddWidget(horiz, self.saveToButton)
        mqt.AddWidget(horiz, self.saveCloseButton)
        mqt.AddWidget(vert, horiz)

        okay = mqt.ShowWidgetAsDialog(self.topWindow)
        if okay:
            print("closed ivoking replay call")
            # after the dialog is closed, invoke the replay call
            # replay async calls can't be called from inside a button event lambda 
            ctx.Replay().AsyncInvoke("somesaveimage__", self.saveImage)

    def updatePath(self, newFilePath):
        self.mFilepath = newFilePath
        print(self.mFilepath)


    def setFilePath(self, ctx: qrd.CaptureContext):
        self.updatePath( ctx.Extensions().SaveFileName("Save Binary Texture As...","","*.bin") )
        mqt.SetWidgetText(self.filePathTextbox, self.mFilepath)

    def actionSaveImage(self, ctx: qrd.CaptureContext):
        currentTexId = ctx.GetTextureViewer().GetCurrentResource()
        tex = ctx.GetTexture(currentTexId)

        self.mResourceId = tex.resourceId
        self.mMips = tex.mips
        self.mSample = tex.msSamp

        # when the dialog is closed (with true value) the replay call will be invoked
        mqt.CloseCurrentDialog(True)


    def saveImage(self, rc : rd.ReplayController):

        sub = rd.Subresource()
        sub.mips = self.mMips
        sub.sample = self.mSample
        sub.slice = 1

        print(sub.mips, self.mResourceId, sub.sample)
        texBytes = rc.GetTextureData(self.mResourceId, sub)

        if (len(texBytes) == 0 ):
            self.ctx.Extensions().MessageDialog("failed to read texture byte data from {} ".format(self.mResourceId),"texture bytes")
            return

        try:
            print("save to {}".format(self.mFilepath))
            with open(self.mFilepath,"wb") as fileHandle:
                fileHandle.write(texBytes)
                #fileHandle.close()
        except IOError as err:
            self.ctx.Extensions().MessageDialog("failed write texture byte data to {} ".format(self.mFilepath),"texture bytes")
            print("Failed to write to file {}, error {}".format(self.mFilepath, err) )

    

cur_window: Optional[WindowDialog] = None


def closed():
    global cur_window
    if cur_window is not None:
        cur_window.ctx.RemoveCaptureViewer(cur_window)
    cur_window = None


def get_window(ctx, version):
    global cur_window, mqt

    mqt = ctx.Extensions().GetMiniQtHelper()

    if cur_window is None:
        cur_window = WindowDialog(ctx, version)

    return cur_window.topWindow