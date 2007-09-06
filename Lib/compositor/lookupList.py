"""
GSUB and GPOS LookupList objects (and friends).
"""


import weakref
from subTablesGSUB import *
from subTablesGPOS import *


# ------------
# Base Classes
# ------------


class BaseLookupList(object):

    __slots__ = ["LookupCount", "Lookup", "_LookupClass", "__weakref__"]
    _LookupClass = None

    def __init__(self, lookupList, table, gdef):
        self.LookupCount = lookupList.LookupCount
        self.Lookup = [self._LookupClass(lookup, self, gdef) for lookup in lookupList.Lookup]


class BaseLookup(object):

    __slots__ = ["LookupType", "LookupFlag", "SubTableCount", "SubTable",
                "_lookupList", "_gdefReference", "__weakref__"]

    def __init__(self, lookup, lookupList, gdef):
        self._lookupList = weakref.ref(lookupList)
        if gdef is not None:
            gdef = weakref.ref(gdef)
        self._gdefReference = gdef
        self.LookupType = lookup.LookupType
        self.LookupFlag = LookupFlag(lookup.LookupFlag, gdef)
        self.SubTableCount = lookup.SubTableCount
        self.SubTable = [self._loadSubTable(subtable) for subtable in lookup.SubTable]

    def _get_gdef(self):
        if self._gdefReference is not None:
            return self._gdefReference()
        return None

    _gdef = property(_get_gdef)


class LookupFlag(object):

    __slots__ = ["_gdef", "_flag", "_haveIgnore",
                "IgnoreBaseGlyphs", "IgnoreLigatures", "IgnoreMarks",
                "RightToLeft", "MarkAttachmentType"]

    def __init__(self, lookupFlag, gdef):
        self._gdef = gdef
        self._flag = lookupFlag
        self._haveIgnore = lookupFlag & 0x0E
        self.RightToLeft = lookupFlag & 0x0001
        self.IgnoreBaseGlyphs = lookupFlag & 0x0002
        self.IgnoreLigatures = lookupFlag & 0x0004
        self.IgnoreMarks = lookupFlag & 0x0008
        self.MarkAttachmentType = lookupFlag & 0xFF00

    def coversGlyph(self, glyphName):
        gdef = self._gdef
        if gdef is None:
            return False
        gdef = gdef()
        cls = gdef.GlyphClassDef[glyphName]
        if cls == 0:
            return False
        if self._haveIgnore:
            if cls == 1 and self.IgnoreBaseGlyphs: #IgnoreBaseGlyphs
                return True
            if cls == 2 and self.IgnoreLigatures: #IgnoreLigatures
                return True
            if cls == 3 and self.IgnoreMarks: #IgnoreMarks
                return True
        if self.MarkAttachmentType and cls == 3:
            if gdef.MarkAttachClassDef is None:
                return False
            markClass = gdef.MarkAttachClassDef[glyphName]
            if (self._flag & 0xff00) >> 8 != markClass:
                return True
        return False

# ----
# GSUB
# ----


class GSUBLookup(BaseLookup):

    __slots__ = []

    def _loadSubTable(self, subtable):
        lookupType = self.LookupType
        if lookupType == 1:
            cls = GSUBLookupType1Format2
        elif lookupType == 2:
            cls = GSUBLookupType2
        elif lookupType == 3:
            cls = GSUBLookupType3
        elif lookupType == 4:
            cls = GSUBLookupType4
        elif lookupType == 5:
            cls = (GSUBLookupType5Format1, GSUBLookupType5Format2, GSUBLookupType5Format3)[subtable.Format-1]
        elif lookupType == 6:
            cls = (GSUBLookupType6Format1, GSUBLookupType6Format2, GSUBLookupType6Format3)[subtable.Format-1]
        elif lookupType == 7:
            cls = GSUBLookupType7
        elif lookupType == 8:
            cls = GSUBLookupType8
        obj = cls(subtable, self)
        return obj


class GSUBLookupList(BaseLookupList):

    __slots__ = []
    _LookupClass = GSUBLookup


# ----
# GPOS
# ----


class GPOSLookup(BaseLookup):

    __slots__ = []

    def _loadSubTable(self, subtable):
        lookupType = self.LookupType
        if lookupType == 1:
            cls = (GPOSLookupType1Format1, GPOSLookupType1Format2)[subtable.Format-1]
        elif lookupType == 2:
            cls = (GPOSLookupType2Format1, GPOSLookupType2Format2)[subtable.Format-1]
        elif lookupType == 3:
            cls = GPOSLookupType3
        elif lookupType == 4:
            cls = GPOSLookupType4
        elif lookupType == 5:
            cls = GPOSLookupType5
        elif lookupType == 6:
            cls = GPOSLookupType6
        elif lookupType == 7:
            cls = (GPOSLookupType7Format1, GPOSLookupType7Format2, GPOSLookupType7Format3)[subtable.Format-1]
        elif lookupType == 8:
            cls = (GPOSLookupType8Format1, GPOSLookupType8Format2, GPOSLookupType8Format3)[subtable.Format-1]
        elif lookupType == 9:
            cls = GPOSLookupType9
        obj = cls(subtable, self)
        return obj


class GPOSLookupList(BaseLookupList):

    __slots__ = []
    _LookupClass = GPOSLookup
