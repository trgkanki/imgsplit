<template lang='pug'>
#app
  .canvas-container
    canvas.downscale.overlay(ref='separatorCanvas', @mousemove='updateCursor', @click='toggleSeparator')
    canvas.downscale(ref='imgCanvas')

  .button-container
    button(v-shortkey="['s']", @shortkey='splitAtCursor', disabled) Split at cursor (S)
    .hpadding
    button(v-shortkey="['ctrl', 'enter']", @shortkey='onSubmit', @click='onSubmit') OK
    button(v-shortkey="['esc']", @shortkey='onCancel', @click='onCancel') Cancel
</template>

<script lang="ts">
import { Component, Watch, Vue } from 'vue-property-decorator'
import Jimp from 'jimp'
import { imageDataFromJimp } from './utils'
import { callPyFunc } from '../../jssrc/utils/pyfunc'
import { splitImage } from './splitImage'

@Component
export default class extends Vue {
  private separatorList: number[] = []
  private image: Jimp | null = null
  private cursorY = -1

  mounted () {
    // Sleep 100ms until pycmd function is registered
    setTimeout(async () => {
      if (navigator.userAgent.indexOf('QtWebEngine') !== -1) {
        const imgb64 = (await callPyFunc('imgsplit_getCurrentImage')) as string
        const imgBuffer = Buffer.from(imgb64, 'base64')
        this.setImage(await Jimp.read(imgBuffer))
      } else {
        this.setImage(await Jimp.read('/p1.png'))
      }
    }, 100)
  }

  async onSubmit () {
    if (this.separatorList.length === 0) this.onCancel()
    if (!this.image) return

    const images = splitImage(this.image, this.separatorList)
    const ret = await Promise.all(images.map(x => x.getBase64Async('image/png')))
    await callPyFunc('imgsplit_retSplitImage', ret)
    window.close()
  }

  async onCancel () {
    await callPyFunc('imgsplit_retSplitImage', null)
    window.close()
  }

  setImage (img: Jimp) {
    this.image = img

    const imgData = imageDataFromJimp(img)
    const imgCanvas = this.$refs.imgCanvas as HTMLCanvasElement
    const separatorCanvas = this.$refs.separatorCanvas as HTMLCanvasElement

    imgCanvas.width = imgData.width
    imgCanvas.height = imgData.height
    imgCanvas.getContext('2d')!.putImageData(imgData, 0, 0)

    separatorCanvas.width = imgData.width
    separatorCanvas.height = imgData.height
    this.separatorList = []
  }

  updateCursor (e: MouseEvent) {
    this.cursorY = e.offsetY
  }

  toggleSeparator (e: { offsetY: number }) {
    const separatorList = this.separatorList
    const target = this.$refs.separatorCanvas as HTMLCanvasElement

    const clickedY = (e.offsetY / target.offsetHeight * target.height) | 0
    if (clickedY < 0 || clickedY >= target.height) return // OOB

    for (let i = 0; i < separatorList.length; i++) {
      const y = separatorList[i]
      if (Math.abs(y - clickedY) < 10) {
        separatorList.splice(i, 1)
        return
      }
    }
    separatorList.push(clickedY)
  }

  splitAtCursor () {
    this.toggleSeparator({ offsetY: this.cursorY })
  }

  @Watch('separatorList')
  onSeperatorChanged (v: number[]) {
    const canvas = this.$refs.separatorCanvas as HTMLCanvasElement
    const ctx = canvas.getContext('2d')!
    ctx.clearRect(0, 0, canvas.width, canvas.height)

    for (const y of v) {
      ctx.beginPath()
      ctx.moveTo(0, y)
      ctx.lineTo(canvas.width, y)
      ctx.stroke()
    }
  }
}
</script>

<style lang="scss">

* {
  box-sizing: border-box;
}

html, body, #app {
  margin: 0;
  padding: 0;
  height: 100%;
}

#app {
  display: flex;
  flex-direction: column;
  padding: 1em;

  .canvas-container {
    position: relative;
    flex: 1;
    border: 1px solid black;

    background: #ddd;

    .downscale {
      max-width: 95%;
    }

    .overlay {
      position: absolute;
      top: 0;
    }
  }

  .button-container {
    text-align: right;
    font-size: 2em;
  }
}

.hpadding {
  display: inline-block;
  width: 2em;
}

</style>
