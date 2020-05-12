import { callPyFunc } from './utils/pyfunc'

window.addEventListener('click', function (evt) {
  if (evt.detail === 3) {
    const el = evt.target as HTMLElement
    if (el.nodeName === 'IMG') {
      const src = (el as HTMLImageElement).src
      callPyFunc('imgsplit_onTripleClick', src)
    }
  }
})
