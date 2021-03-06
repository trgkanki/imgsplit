import ImageView from './ImageView'
import Jimp from 'jimp/es'

export function splitImage (img: Jimp, separatorYList: number[]): Jimp[] {
  let y0 = 0
  const imgs = [] as Jimp[]
  const { width: imgW, height: imgH } = img.bitmap
  const view = new ImageView(img)

  separatorYList = separatorYList.slice()
  separatorYList.sort((a, b) => a - b)

  for (const y1 of separatorYList) {
    if (y1 !== y0) imgs.push(view.crop(0, y0, imgW, y1 - y0).autocrop().toJimpWithPad(8))
    y0 = y1
  }
  if (imgH !== y0) imgs.push(view.crop(0, y0, imgW, imgH - y0).autocrop().toJimpWithPad(8))
  return imgs
}
