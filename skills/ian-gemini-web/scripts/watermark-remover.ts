/**
 * Gemini Watermark Remover - Reverse Alpha Blending Algorithm
 * Based on: https://github.com/journey-ad/gemini-watermark-remover (MIT License)
 * Formula: original = (watermarked - α × 255) / (1 - α)
 */

import { readFile } from 'node:fs/promises';
import path from 'node:path';
import * as zlib from 'node:zlib';

const ALPHA_THRESHOLD = 0.002;
const MAX_ALPHA = 0.99;
const LOGO_VALUE = 255;

interface WatermarkConfig {
  logoSize: number;
  marginRight: number;
  marginBottom: number;
}

interface WatermarkPosition {
  x: number;
  y: number;
  width: number;
  height: number;
}

interface PNGImage {
  width: number;
  height: number;
  data: Uint8Array;
  colorType: number;
  bitDepth: number;
}

const alphaMapCache: Map<number, Float32Array> = new Map();

function detectWatermarkConfig(imageWidth: number, imageHeight: number): WatermarkConfig {
  if (imageWidth > 1024 && imageHeight > 1024) {
    return { logoSize: 96, marginRight: 64, marginBottom: 64 };
  }
  return { logoSize: 48, marginRight: 32, marginBottom: 32 };
}

function calculateWatermarkPosition(
  imageWidth: number,
  imageHeight: number,
  config: WatermarkConfig,
): WatermarkPosition {
  return {
    x: imageWidth - config.marginRight - config.logoSize,
    y: imageHeight - config.marginBottom - config.logoSize,
    width: config.logoSize,
    height: config.logoSize,
  };
}

function decodePNG(buffer: Uint8Array): PNGImage {
  const view = new DataView(buffer.buffer, buffer.byteOffset, buffer.byteLength);
  
  if (view.getUint32(0) !== 0x89504e47 || view.getUint32(4) !== 0x0d0a1a0a) {
    throw new Error('Invalid PNG signature');
  }

  let offset = 8;
  let width = 0, height = 0, bitDepth = 0, colorType = 0;
  const idatChunks: Uint8Array[] = [];

  while (offset < buffer.length) {
    const length = view.getUint32(offset);
    const type = String.fromCharCode(buffer[offset+4], buffer[offset+5], buffer[offset+6], buffer[offset+7]);
    
    if (type === 'IHDR') {
      width = view.getUint32(offset + 8);
      height = view.getUint32(offset + 12);
      bitDepth = buffer[offset + 16];
      colorType = buffer[offset + 17];
    } else if (type === 'IDAT') {
      idatChunks.push(buffer.slice(offset + 8, offset + 8 + length));
    } else if (type === 'IEND') {
      break;
    }
    offset += 12 + length;
  }

  const compressed = new Uint8Array(idatChunks.reduce((sum, c) => sum + c.length, 0));
  let pos = 0;
  for (const chunk of idatChunks) {
    compressed.set(chunk, pos);
    pos += chunk.length;
  }

  const decompressed = zlib.inflateSync(Buffer.from(compressed));
  const channels = colorType === 6 ? 4 : colorType === 2 ? 3 : colorType === 4 ? 2 : 1;
  const data = new Uint8Array(width * height * 4);

  for (let y = 0; y < height; y++) {
    const filterType = decompressed[y * (width * channels + 1)];
    for (let x = 0; x < width; x++) {
      const srcIdx = y * (width * channels + 1) + 1 + x * channels;
      const dstIdx = (y * width + x) * 4;
      
      let r = 0, g = 0, b = 0, a = 255;
      if (channels === 4) {
        r = decompressed[srcIdx]; g = decompressed[srcIdx+1]; b = decompressed[srcIdx+2]; a = decompressed[srcIdx+3];
      } else if (channels === 3) {
        r = decompressed[srcIdx]; g = decompressed[srcIdx+1]; b = decompressed[srcIdx+2];
      } else if (channels === 2) {
        r = g = b = decompressed[srcIdx]; a = decompressed[srcIdx+1];
      } else {
        r = g = b = decompressed[srcIdx];
      }

      const left = x > 0 ? dstIdx - 4 : -1;
      const up = y > 0 ? dstIdx - width * 4 : -1;
      const upLeft = x > 0 && y > 0 ? dstIdx - width * 4 - 4 : -1;

      const paeth = (a: number, b: number, c: number) => {
        const p = a + b - c;
        const pa = Math.abs(p - a), pb = Math.abs(p - b), pc = Math.abs(p - c);
        return pa <= pb && pa <= pc ? a : pb <= pc ? b : c;
      };

      const unfilter = (val: number, idx: number) => {
        const l = left >= 0 ? data[left + idx] : 0;
        const u = up >= 0 ? data[up + idx] : 0;
        const ul = upLeft >= 0 ? data[upLeft + idx] : 0;
        switch (filterType) {
          case 0: return val;
          case 1: return (val + l) & 0xff;
          case 2: return (val + u) & 0xff;
          case 3: return (val + Math.floor((l + u) / 2)) & 0xff;
          case 4: return (val + paeth(l, u, ul)) & 0xff;
          default: return val;
        }
      };

      data[dstIdx] = unfilter(r, 0);
      data[dstIdx + 1] = unfilter(g, 1);
      data[dstIdx + 2] = unfilter(b, 2);
      data[dstIdx + 3] = channels === 4 || channels === 2 ? unfilter(a, 3) : 255;
    }
  }

  return { width, height, data, colorType, bitDepth };
}

function encodePNG(img: PNGImage): Uint8Array {
  const { width, height, data } = img;
  const raw = new Uint8Array(height * (1 + width * 4));
  
  for (let y = 0; y < height; y++) {
    raw[y * (width * 4 + 1)] = 0;
    for (let x = 0; x < width; x++) {
      const src = (y * width + x) * 4;
      const dst = y * (width * 4 + 1) + 1 + x * 4;
      raw[dst] = data[src]; raw[dst+1] = data[src+1]; raw[dst+2] = data[src+2]; raw[dst+3] = data[src+3];
    }
  }

  const compressed = zlib.deflateSync(Buffer.from(raw), { level: 9 });
  
  const crcTable = new Uint32Array(256);
  for (let n = 0; n < 256; n++) {
    let c = n;
    for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
    crcTable[n] = c;
  }
  const crc32 = (buf: Uint8Array) => {
    let crc = 0xffffffff;
    for (let i = 0; i < buf.length; i++) crc = crcTable[(crc ^ buf[i]) & 0xff] ^ (crc >>> 8);
    return (crc ^ 0xffffffff) >>> 0;
  };

  const chunks: Uint8Array[] = [];
  chunks.push(new Uint8Array([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]));

  const ihdr = new Uint8Array(25);
  const ihdrView = new DataView(ihdr.buffer);
  ihdrView.setUint32(0, 13);
  ihdr.set([0x49, 0x48, 0x44, 0x52], 4);
  ihdrView.setUint32(8, width);
  ihdrView.setUint32(12, height);
  ihdr[16] = 8; ihdr[17] = 6; ihdr[18] = 0; ihdr[19] = 0; ihdr[20] = 0;
  ihdrView.setUint32(21, crc32(ihdr.slice(4, 21)));
  chunks.push(ihdr);

  const idat = new Uint8Array(12 + compressed.length);
  const idatView = new DataView(idat.buffer);
  idatView.setUint32(0, compressed.length);
  idat.set([0x49, 0x44, 0x41, 0x54], 4);
  idat.set(compressed, 8);
  idatView.setUint32(8 + compressed.length, crc32(idat.slice(4, 8 + compressed.length)));
  chunks.push(idat);

  const iend = new Uint8Array(12);
  new DataView(iend.buffer).setUint32(0, 0);
  iend.set([0x49, 0x45, 0x4e, 0x44], 4);
  new DataView(iend.buffer).setUint32(8, crc32(iend.slice(4, 8)));
  chunks.push(iend);

  const total = chunks.reduce((s, c) => s + c.length, 0);
  const result = new Uint8Array(total);
  let off = 0;
  for (const c of chunks) { result.set(c, off); off += c.length; }
  return result;
}

function calculateAlphaMap(data: Uint8Array, width: number, height: number): Float32Array {
  const alphaMap = new Float32Array(width * height);
  for (let i = 0; i < alphaMap.length; i++) {
    const idx = i * 4;
    alphaMap[i] = Math.max(data[idx], data[idx + 1], data[idx + 2]) / 255.0;
  }
  return alphaMap;
}

async function getAlphaMap(size: 48 | 96): Promise<Float32Array> {
  const cached = alphaMapCache.get(size);
  if (cached) return cached;

  const assetPath = path.join(import.meta.dir, 'assets', `bg_${size}.png`);
  const fileData = await readFile(assetPath);
  const png = decodePNG(new Uint8Array(fileData));
  const alphaMap = calculateAlphaMap(png.data, png.width, png.height);

  alphaMapCache.set(size, alphaMap);
  return alphaMap;
}

function applyReverseAlphaBlending(
  data: Uint8Array,
  imageWidth: number,
  alphaMap: Float32Array,
  position: WatermarkPosition,
): void {
  const { x, y, width, height } = position;

  for (let row = 0; row < height; row++) {
    for (let col = 0; col < width; col++) {
      const imgIdx = ((y + row) * imageWidth + (x + col)) * 4;
      let alpha = alphaMap[row * width + col];

      if (alpha < ALPHA_THRESHOLD) continue;
      alpha = Math.min(alpha, MAX_ALPHA);

      for (let c = 0; c < 3; c++) {
        const original = (data[imgIdx + c] - alpha * LOGO_VALUE) / (1.0 - alpha);
        data[imgIdx + c] = Math.max(0, Math.min(255, Math.round(original)));
      }
    }
  }
}

export async function removeWatermark(imageBuffer: Uint8Array): Promise<Uint8Array> {
  const png = decodePNG(imageBuffer);
  const config = detectWatermarkConfig(png.width, png.height);
  const position = calculateWatermarkPosition(png.width, png.height, config);
  const alphaMap = await getAlphaMap(config.logoSize as 48 | 96);

  applyReverseAlphaBlending(png.data, png.width, alphaMap, position);

  return encodePNG(png);
}

export function hasWatermarkArea(width: number, height: number): boolean {
  const config = detectWatermarkConfig(width, height);
  return width >= config.logoSize + config.marginRight && height >= config.logoSize + config.marginBottom;
}
