"""Render the social card source with Pillow; run on a machine with Arial installed."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
svg = ET.parse(ROOT/'social-card.svg').getroot()
image = Image.new('RGB', (1200, 630), '#101212')
draw = ImageDraw.Draw(image)
for item in svg:
    tag = item.tag.rsplit('}',1)[-1]
    a = item.attrib
    if tag == 'rect':
        x,y,w,h = [float(a.get(key,0)) for key in ('x','y','width','height')]
        draw.rounded_rectangle((x,y,x+w,y+h),radius=float(a.get('rx',0)),fill=None if a.get('fill')=='none' else a.get('fill'),outline=a.get('stroke'),width=int(a.get('stroke-width',1)))
    elif tag == 'polyline':
        points = [tuple(map(float,pair.split(','))) for pair in a['points'].split()]
        draw.line(points,fill=a['stroke'],width=4)
    elif tag == 'line':
        draw.line([(float(a['x1']),float(a['y1'])),(float(a['x2']),float(a['y2']))],fill=a['stroke'],width=int(a.get('stroke-width',1)))
    elif tag == 'text':
        fontfile = 'Arial Bold.ttf' if a.get('font-weight')=='bold' else 'Arial.ttf'
        font = ImageFont.truetype('/System/Library/Fonts/Supplemental/'+fontfile,int(a['font-size']))
        x,y = float(a['x']),float(a['y'])
        spacing=float(a.get('letter-spacing',0))
        for char in item.text:
            draw.text((x,y),char,fill=a['fill'],font=font,anchor='ls')
            x+=draw.textlength(char,font=font)+spacing
image.save(ROOT/'social-card.png',optimize=True)
