import cairocffi as cairo
from cairoPen import CairoPen
from compositor import Font


# a simple function that implements path caching
def getCachedPath(glyph, font, ctx):
    if not hasattr(glyph, "pathOperationList"):
        ctx.new_path()
        pen = CairoPen(font, ctx)
        glyph.draw(pen)
        glyph.pathOperationList = ctx.copy_path()
    return glyph.pathOperationList

# a path to a font
fontPath = aPathToYourFont

# a path to save the image to
imagePath = "demo.png"

# setup the layout engine
font = Font(fontPath)

# turn the aalt feature on so that we get any alternates
font.setFeatureState("aalt", True)

# process some text
glyphRecords = font.process(u"HERE IS SOME TEXT!")

# calculate the image size
pointSize = 50.0
offset = 20
scale = pointSize / font.info.unitsPerEm
imageWidth = sum([font[record.glyphName].width + record.xAdvance for record in glyphRecords]) * scale
imageWidth = int(round(imageWidth))
imageWidth += offset * 2
imageHeight = pointSize + (offset * 2)

# setup the image
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, int(imageWidth), int(imageHeight))
ctx = cairo.Context(surface)

# fill it with white
ctx.set_source_rgb(1.0, 1.0, 1.0)
ctx.paint()

# Transform to normal cartesian coordinate system
matrix = cairo.Matrix(yy=-1, y0=imageHeight)
ctx.transform(matrix)

# offset and set the scale
ctx.translate(offset, offset)
ctx.scale(scale, scale)
ctx.translate(0, abs(font.info.descender))

# iterate over the glyph records
for record in glyphRecords:
    glyph = font[record.glyphName]

    # shift for x and y placement
    ctx.translate(record.xPlacement, record.yPlacement)

    # if alternates are present, switch the color
    if record.alternates:
        ctx.set_source_rgb(1.0, 0.0, 0.0)
    # otherwise, set the color to black
    else:
        ctx.set_source_rgb(0.0, 0.0, 0.0)

    # get a PathOperation list for the glyph and fill it
    path = getCachedPath(glyph, font, ctx)
    ctx.append_path(path)
    ctx.fill()

    # shift for the next glyph
    ctx.translate(record.xAdvance + glyph.width, -record.yPlacement)

# write the image to disk
surface.write_to_png(imagePath)
