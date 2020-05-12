import Jimp from 'jimp'

export function imageDataFromJimp (img: Jimp) {
  return new ImageData(
    new Uint8ClampedArray(img.bitmap.data),
    img.bitmap.width, img.bitmap.height
  )
}
