// news-image-20261127 entrypoint (Node 22, standard library only).
//
// The entry is the PNG this repository holds: draw_entry.py drew it from the
// day's news, and this program copies it to the output directory. Nothing is
// fetched and nothing is drawn at run time, so both runs write the same bytes.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync, statSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, 'entry.png');
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const target = join(outDir, 'entry.png');

// Gate: the file must be a whole PNG within the competition's limits
// (at most 1 MiB, at most 1024 by 1024 pixels) before it is copied.
const bytes = readFileSync(source);
const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!bytes.subarray(0, 8).equals(PNG_MAGIC)) {
  throw new Error('entry.png is not a PNG file');
}
// The first chunk after the magic must be IHDR, so the width and height
// below are read from the header the PNG itself declares.
if (bytes.subarray(12, 16).toString('ascii') !== 'IHDR') {
  throw new Error('entry.png has no IHDR chunk where one is expected');
}
if (bytes.length > 1048576) {
  throw new Error(`entry.png is ${bytes.length} bytes, over the 1 MiB limit`);
}
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width > 1024 || height > 1024) {
  throw new Error(`entry.png is ${width}x${height}, over the 1024x1024 limit`);
}

mkdirSync(outDir, { recursive: true });
copyFileSync(source, target);
console.log(`copied entry.png (${bytes.length} bytes, ${width}x${height}) to ${target}`);
