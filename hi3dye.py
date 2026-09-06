"""HI3 dye model: predict the resulting hex from a recipe."""
import math

# ingredient -> (hue_degrees, saturation_per_unit, darkening_per_unit)
ING = {
 'Acorn':(0,0,2), 'Aridberry':(270,10,5), 'Basil':(111,10,5), 'Beet':(348,10,5),
 'Bird of Paradise':(336,5,0), 'Black Nightshade Flower':(0,0,5), 'Blackberry':(0,0,10),
 'Blueberry':(240,10,0), 'Bluebonnet Flower':(230,5,0), 'Carrot':(27,10,5),
 'Cineraria Flower':(210,5,0), 'Cloudberry':(30,10,5), 'Coal':(0,0,20), 'Cranberry':(7,10,5),
 'Crystal Flower':(190,10,0), 'Dandelion':(55,5,0), 'Desert Rose':(25,5,0),
 'Dragonblood Sap':(2,50,10), 'Fire Flower':(345,10,0), 'Frangipanis Flower':(310,2,0),
 'Gerbera Daisy':(43,5,0), 'Grape Bundle':(335,10,5), 'Hellebore Flower':(100,5,0),
 'Iceberry':(180,10,5), 'Kelp':(106,10,5), 'Lemon':(60,10,5), 'Liatris Flower':(280,5,0),
 'Lime':(80,10,5), 'Lotus Flower':(63,7,0), 'Mango':(57,10,5), 'Mint':(122,10,5),
 'Morel Mushroom':(41,3,2), 'Mulberry':(290,7,7), 'Mullein Flower':(47,5,0),
 'Olive':(72,2,2), 'Oozeberry':(130,10,5), 'Orange':(33,10,5), 'Pansy':(165,5,0),
 'Pimpernel Flower':(15,5,0), 'Pineapple':(52,10,5), 'Pink Zinnia':(320,5,0),
 'Plum':(285,10,5), 'Poppy':(38,5,0), 'Raspberry':(0,10,0), 'Red Rose':(355,5,0), 'Saffron':(32,5,0),
 'Seaberry':(65,10,5), 'Spiderwort Flower':(263,5,0), 'Spinach':(115,10,10),
 'Star Flower':(200,5,0), 'Strawberry':(5,10,5), 'Sulfur':(51,5,0), 'Water Iris':(300,5,0),
}
ALIAS = {'Spiderwort':'Spiderwort Flower'}

def mix_hsv(counts):
    """counts: {ingredient: units} -> (H deg, S 0-100, V 0-100)"""
    x = y = 0.0; total = 0.0; dark = 0.0
    for name, n in counts.items():
        h, s, d = ING[ALIAS.get(name, name)]
        w = s * n
        total += w
        dark += d * n
        x += w * math.cos(math.radians(h))
        y += w * math.sin(math.radians(h))
    mag = math.hypot(x, y)
    S = min(100.0, mag)
    H = math.degrees(math.atan2(y, x)) % 360
    # 99 only when nothing in the pot has a hue. Confirmed both ways: colourless
    # mixes start at 99, while coloured ingredients that cancel exactly start at 100.
    base = 100.0 if total > 0 else 99.0
    V = max(0.0, min(100.0, base - (total - mag) - dark))
    return H, S, V

def _hsv2rgb(H, S, V):
    H %= 360; i = int(H // 60); f = H / 60 - i
    p = V * (1 - S); q = V * (1 - S * f); t = V * (1 - S * (1 - f))
    return [(V,t,p),(q,V,p),(p,V,t),(p,q,V),(t,p,V),(V,p,q)][i]

def mix_hex(counts):
    H, S, V = mix_hsv(counts)
    rgb = [math.floor(c * 255 + 0.5 + 1e-9) for c in _hsv2rgb(H, S/100, V/100)]
    return '%02x%02x%02x' % tuple(rgb)
