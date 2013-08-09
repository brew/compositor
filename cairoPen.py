from fontTools.pens.basePen import BasePen


__all__ = ["CairoPen"]


class CairoPen(BasePen):

    def __init__(self, glyphSet, ctx):
        BasePen.__init__(self, glyphSet)
        self.ctx = ctx

    def _moveTo(self, (x, y)):
        self.ctx.move_to(x, y)

    def _lineTo(self, (x, y)):
        self.ctx.line_to(x, y)

    def _curveToOne(self, (x1, y1), (x2, y2), (x3, y3)):
        self.ctx.curve_to(x1, y1, x2, y2, x3, y3)

    def _closePath(self):
        self.ctx.close_path()
