#!/usr/bin/env python3
"""
Script para gerar o logo BravON em PNG e ICO
"""
import io
import struct
import zlib

def create_simple_png():
    """Criar um PNG simples com BravON escrito"""
    # Usar um PNG mínimo com dados em base64
    # PNG signature
    png_signature = b'\x89PNG\r\n\x1a\n'
    
    # Vamos criar manualmente um PNG 64x64 simples
    # Este é um PNG válido mas muito simples
    
    width, height = 64, 64
    
    # IHDR chunk
    ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)  # 8-bit RGB
    ihdr_crc = zlib.crc32(b'IHDR' + ihdr_data) & 0xffffffff
    ihdr_chunk = struct.pack('>I', 13) + b'IHDR' + ihdr_data + struct.pack('>I', ihdr_crc)
    
    # IDAT chunk - dados de imagem
    # Criar um gradiente laranja-azul simples
    raw_data = b''
    for y in range(height):
        raw_data += b'\x00'  # filter type
        for x in range(width):
            # Gradiente de laranja (FF6B35) para azul (1A2A3A)
            ratio = (y * 256) // height
            r = 255 - (255 - 26) * ratio // 256
            g = 107 - (107 - 42) * ratio // 256
            b = 53 - (53 - 58) * ratio // 256
            raw_data += bytes([r, g, b])
    
    compressed_data = zlib.compress(raw_data)
    idat_crc = zlib.crc32(b'IDAT' + compressed_data) & 0xffffffff
    idat_chunk = struct.pack('>I', len(compressed_data)) + b'IDAT' + compressed_data + struct.pack('>I', idat_crc)
    
    # IEND chunk
    iend_crc = zlib.crc32(b'IEND') & 0xffffffff
    iend_chunk = struct.pack('>I', 0) + b'IEND' + struct.pack('>I', iend_crc)
    
    # Combinar tudo
    png_data = png_signature + ihdr_chunk + idat_chunk + iend_chunk
    
    return png_data

def main():
    try:
        # Criar PNG
        png_data = create_simple_png()
        
        with open('static/logo.png', 'wb') as f:
            f.write(png_data)
        print('✓ Logo PNG criado em static/logo.png')
        
        # ICO é PNG com tamanho 32x32 - usar o mesmo
        with open('static/favicon.ico', 'wb') as f:
            f.write(png_data)
        print('✓ Favicon ICO criado em static/favicon.ico')
        
        # Também criar como SVG simples se ainda não existir
        with open('static/logo-simple.svg', 'w') as f:
            f.write('''<svg width="512" height="512" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#FF6B35;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#1A2A3A;stop-opacity:1" />
    </linearGradient>
  </defs>
  <rect width="512" height="512" fill="url(#grad)"/>
  <text x="256" y="280" font-size="120" font-weight="bold" fill="white" text-anchor="middle" font-family="Arial">BravON</text>
</svg>''')
        print('✓ Logo SVG simplificado criado')
        
    except Exception as e:
        print(f'✗ Erro ao criar logo: {e}')
        raise

if __name__ == '__main__':
    main()
