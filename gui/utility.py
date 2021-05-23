
# for colored glow set the color and an opacity < 1
def createPinDict(text, x, y, color='white', opacity=1, imgSrc='glow2', width=1):
    pinOffset = width / 2
    return {'text': text, 'x': x-pinOffset, 'y': y-pinOffset, 'color': color, 'opacity': opacity, 'imgSrc': imgSrc, 'width': width}

def coordsToPins(thing, text, color='white', opacity=1, imgSrc='glow2', width=1):
    pinList = []
    for zone in thing.cByZone:
        if zone == 0:
            continue
        for coord in thing.cByZone[zone]:
            pinList.append((zone, createPinDict(text, coord[0], coord[1], color, opacity, imgSrc, width)))
    return pinList
