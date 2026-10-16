"""下载并转换四张图片，只以普通文件方式复制到 F 盘；原始卷仅只读。"""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from io import BytesIO
import hashlib
import json
import struct
import subprocess
import urllib.request

from PIL import Image, ImageOps, ImageDraw

ROOT = Path(__file__).resolve().parent
SOURCES = [
    ('001.bmp', 'photo-1500534623283-312aade485b7'),
    ('002.bmp', 'photo-1470770841072-f978cf4d019e'),
    ('003.bmp', 'photo-1441974231531-c6227db76b6e'),
    ('004.bmp', 'photo-1472396961693-142e6e269027'),
]


def download(entry):
    name, photo_id = entry
    url = f'https://images.unsplash.com/{photo_id}?w=800&h=600&fit=crop&fm=jpg'
    request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(request, timeout=35) as response:
        original = response.read()
    with Image.open(BytesIO(original)) as source:
        picture = ImageOps.fit(ImageOps.exif_transpose(source).convert('RGB'),
                               (640, 480), method=Image.Resampling.LANCZOS)
    (ROOT / (name[:-4] + '_source.jpg')).write_bytes(original)
    picture.save(ROOT / name, format='BMP')
    data = (ROOT / name).read_bytes()
    size = struct.unpack_from('<I', data, 2)[0]
    offset = struct.unpack_from('<I', data, 10)[0]
    width, height = struct.unpack_from('<ii', data, 18)
    planes, bits, compression = struct.unpack_from('<HHI', data, 26)
    assert data[:2] == b'BM'
    assert (width, height, planes, bits, compression) == (640, 480, 1, 24, 0)
    assert size == len(data) == offset + 640 * 480 * 3
    return {'file': name, 'source_url': url, 'bytes': len(data),
            'sha256': hashlib.sha256(data).hexdigest(),
            'width': width, 'height': height, 'bits': bits, 'compression': compression}


def inspect_card(records):
    # r+b/wb are deliberately never used for a raw volume.
    with open(r'\\.\F:', 'rb', buffering=0) as volume:
        boot = volume.read(512)
        bps = struct.unpack_from('<H', boot, 11)[0]
        spc = boot[13]
        reserved = struct.unpack_from('<H', boot, 14)[0]
        fats = boot[16]
        fat_size = struct.unpack_from('<I', boot, 36)[0]
        root_cluster = struct.unpack_from('<I', boot, 44)[0]
        bpb_hidden_sectors = struct.unpack_from('<I', boot, 28)[0]
        partition_offset = int(subprocess.check_output(
            ['powershell', '-NoProfile', '-Command',
             '(Get-Partition -DriveLetter F).Offset'], text=True).strip())
        assert partition_offset % 512 == 0
        partition_sector = partition_offset // 512
        extflags = struct.unpack_from('<H', boot, 40)[0]
        active_fat = (extflags & 0xF) if extflags & 0x80 else 0
        assert bps == 512 and boot[82:90] == b'FAT32   '
        data_sector = reserved + fats * fat_size
        cluster_size = bps * spc
        volume.seek((reserved + active_fat * fat_size) * bps)
        fat = volume.read(fat_size * bps)

        def chain(start):
            seen = set()
            while 2 <= start < 0x0FFFFFF8:
                if start in seen:
                    raise ValueError('FAT cluster loop')
                seen.add(start)
                yield start
                start = struct.unpack_from('<I', fat, start * 4)[0] & 0x0FFFFFFF

        def cluster_bytes(cluster):
            volume.seek((data_sector + (cluster - 2) * spc) * bps)
            return volume.read(cluster_size)

        directory = b''.join(cluster_bytes(c) for c in chain(root_cluster))
        entries = {}
        for pos in range(0, len(directory), 32):
            ent = directory[pos:pos + 32]
            if ent[0] == 0:
                break
            if ent[0] == 0xE5 or ent[11] & 0x18 or ent[11] == 0x0F:
                continue
            short_name = ent[:8].decode('ascii').strip() + '.' + ent[8:11].decode('ascii').strip()
            start = (struct.unpack_from('<H', ent, 20)[0] << 16) | struct.unpack_from('<H', ent, 26)[0]
            entries[short_name.lower()] = (start, struct.unpack_from('<I', ent, 28)[0])
        for record in records:
            start, size = entries[record['file']]
            clusters = list(chain(start))
            contiguous = all(b == a + 1 for a, b in zip(clusters, clusters[1:]))
            sector = partition_sector + data_sector + (start - 2) * spc
            last_sector = sector + (size + 511) // 512 - 1
            readback = b''.join(cluster_bytes(c) for c in clusters)[:size]
            assert hashlib.sha256(readback).hexdigest() == record['sha256']
            record.update(start_sector=sector, last_sector=last_sector,
                          contiguous=contiguous, cluster_count=len(clusters),
                          raw_readback_matches=True,
                          fits_fpga_layout=contiguous and last_sector <= 131071)
        return {'bytes_per_sector': bps, 'sectors_per_cluster': spc,
                'partition_start_sector': partition_sector,
                'bpb_hidden_sectors': bpb_hidden_sectors,
                'data_start_sector': data_sector}


def main():
    ROOT.mkdir(exist_ok=True)
    destinations = [Path('F:/') / name for name, _ in SOURCES]
    with ThreadPoolExecutor(max_workers=4) as pool:
        records = list(pool.map(download, SOURCES))
    # 下载全部成功后，依次写普通文件，便于顺序分配簇。
    for record, destination in zip(records, destinations):
        data = (ROOT / record['file']).read_bytes()
        if destination.exists():
            if destination.read_bytes() != data:
                raise FileExistsError(f'卡中已有不同内容，停止以免覆盖：{destination}')
            continue
        with destination.open('xb') as output:
            output.write(data)
            output.flush()
            import os
            os.fsync(output.fileno())
        assert destination.read_bytes() == data
    # 镜像只保存到本机工作区，不写入 TF 卡原始扇区。
    with (ROOT / 'four_images_raw.img').open('wb') as output:
        for record in records:
            data = (ROOT / record['file']).read_bytes()
            output.write(data)
            output.write(bytes((-len(data)) % 512))
    card = inspect_card(records)
    preview = Image.new('RGB', (640, 520), 'white')
    draw = ImageDraw.Draw(preview)
    for index, record in enumerate(records):
        with Image.open(ROOT / record['file']) as picture:
            thumb = picture.resize((320, 240), Image.Resampling.LANCZOS)
        x, y = (index % 2) * 320, (index // 2) * 260
        preview.paste(thumb, (x, y))
        draw.text((x + 8, y + 242), record['file'], fill='black')
    preview.save(ROOT / 'preview.jpg', quality=90)
    report = {'card': card, 'images': records,
              'all_fit_fpga_layout': all(r['fits_fpga_layout'] for r in records)}
    (ROOT / 'verification.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
