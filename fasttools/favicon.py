import urllib
import base64
from typing import Tuple




def _is_remote_url(favicon: str) -> bool:
    return favicon.startswith('http://') or favicon.startswith('https://')


def _is_char(favicon: str) -> bool:
    return len(favicon) == 1 or '\ufe0f' in favicon


def _is_svg(favicon: str) -> bool:
    return favicon.strip().startswith('<svg')


def _is_data_url(favicon: str) -> bool:
    return favicon.startswith('data:')


def _char_to_svg(char: str) -> str:
    return f'''
        <svg viewBox="0 0 128 128" width="128" height="128" xmlns="http://www.w3.org/2000/svg" >
            <style>
                @supports (-moz-appearance:none) {{
                    text {{
                        font-size: 100px;
                        transform: translateY(0.1em);
                    }}
                }}
                text {{
                    font-family: Arial, sans-serif;
                }}
            </style>
            <text y=".9em" font-size="128" font-family="Georgia, sans-serif">{char}</text>
        </svg>
    '''


def _svg_to_data_url(svg: str) -> str:
    svg_urlencoded = urllib.parse.quote(svg)
    return f'data:image/svg+xml,{svg_urlencoded}'


def _data_url_to_bytes(data_url: str) -> Tuple[str, bytes]:
    media_type, base64_image = data_url.split(',', 1)
    media_type = media_type.split(':')[1].split(';')[0]
    return media_type, base64.b64decode(base64_image)