# -*- coding: utf-8 -*-
#
# addon_template v20.5.4i8
#
# Copyright: trgk (phu54321@naver.com)
# License: GNU AGPL, version 3 or later;
# See http://www.gnu.org/licenses/agpl.html

from aqt.editor import Editor
from anki.hooks import wrap
from aqt import mw
from aqt.qt import QMimeData
from aqt.utils import askUser
from urllib.parse import unquote

from .utils.MiniBrowser import MiniBrowser
from .utils.JSCallable import JSCallable
from .utils.JSEval import execJSFile

import os
import base64
import json

currentSplitImagePath = ''

@JSCallable
def imgsplit_retSplitImage(ret):
    if ret is None:
        return  # nothing to do

    htmlFragments = []
    for imgDataUri in ret:
        htmlFragments.append('<div><img src="%s"></div>' % imgDataUri)

    clip = mw.app.clipboard()
    mime = QMimeData()
    html = mime.html()
    mime.setHtml(''.join(htmlFragments))
    clip.setMimeData(mime)



@JSCallable
def imgsplit_getCurrentImage():
    mediafolder = os.path.join(mw.pm.profileFolder(), "collection.media")
    fullPath = os.path.join(mediafolder, currentSplitImagePath)
    with open(fullPath, 'rb') as f:
        return base64.b64encode(f.read()).decode('ascii')

@JSCallable
def imgsplit_onTripleClick(imgSrc):
    global currentSplitImagePath
    serverUrl = mw.serverURL()
    if imgSrc.startswith(serverUrl):
        imgSrc = imgSrc[len(serverUrl):]
        currentSplitImagePath = unquote(imgSrc)
        MiniBrowser(None, 'dlg1/index.html', 'maximized')

    return 1


def onLoadNote(self, focusTo=None):
    execJSFile(self.web, "js/main.min.js")


Editor.loadNote = wrap(Editor.loadNote, onLoadNote, "after")


