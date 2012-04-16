
from ctypes import *

FT_Pos = c_long
FT_UInt = c_uint
FT_Int = c_int
FT_Short = c_short
FT_UShort = c_ushort
FT_Library = c_voidp
FT_Fixed = c_long
FT_Glyph_Format = c_uint
FT_SubGlyph = c_voidp
FT_Slot_Internal = c_voidp

class RStructure(Structure):
	def __repr__(self):
		return Structure.__repr__(self) + ": %r" % [(n, getattr(self, n)) for (n, t) in self._fields_]
	def _dump(self, indent = 0):
		itab = "   " * indent
		print itab + Structure.__repr__(self)
		for n, t in self._fields_:
			print itab + "  %s:" % n,
			v = getattr(self, n)
			if isinstance(v, RStructure) and n != "next":
				v._dump(indent + 1)
			else:
				print repr(v)


class FT_Vector(Structure):
	_fields_ = [("x", FT_Pos), ("y", FT_Pos)]
	def __repr__(self):
		return "<Vector(%d, %d)>" % (self.x, self.y)

class FT_Glyph_Metrics(RStructure):
	_fields_ = [(name, FT_Pos) for name in ("width", "height", "horiBearingX", "horiBearingY", "horiAdvance", "vertBearingX", "vertBearingY", "vertAdvance")]

class FT_BBox(RStructure):
	_fields_ = [(name, FT_Pos) for name in ("xMin", "yMin", "xMax", "yMax")]


class FT_Generic(RStructure):
	_fields_ = [("data", c_voidp), ("finalizer", c_voidp)]

class FT_Outline(Structure):
	_fields_ = [("n_contours", c_short), ("n_points", c_short), ("points", POINTER(FT_Vector)), ("tags", POINTER(c_byte)), ("contours", POINTER(c_short)), ("flags", c_int)]


class FT_FaceRec(RStructure):
	pass

class FT_GlyphSlotRec(RStructure):
	pass

class FT_Bitmap(RStructure):
	_fields_ = [
		("rows",        c_int32),
		("width",       c_int32),
		("pitch",       c_int32),
		("buffer",      POINTER(c_ubyte)),
		("num_grays",   c_short),
		("pixel_mode",  c_byte),
		("palette_mode",  c_byte),
		("palette",  c_voidp),
	]

FT_Face = POINTER(FT_FaceRec)
FT_GlyphSlot = POINTER(FT_GlyphSlotRec)

FT_GlyphSlotRec._fields_ = [
	("library", FT_Library),
	("face", FT_Face),
	("next", FT_GlyphSlot),
	("reserved", FT_UInt),
	("generic", FT_Generic),
	("metrics", FT_Glyph_Metrics),
	("linearHoriAdvance", FT_Fixed),
	("linearVertAdvance", FT_Fixed),
	("advance", FT_Vector),
	("format", FT_Glyph_Format),
	("bitmap", FT_Bitmap),
	("bitmap_left", FT_Int),
	("bitmap_top", FT_Int),
	("outline", FT_Outline),
	("num_subglyphs", FT_UInt),
	("subglyphs", FT_SubGlyph),
	("control_data", c_voidp),
	("control_len", c_long),
	("lsb_delta", FT_Pos),
	("rsb_delta", FT_Pos),
	("other", c_voidp),
	("internal", FT_Slot_Internal)
]


FT_FaceRec._fields_ = [
	("num_faces",   c_long),
	("face_index",  c_long),
	("face_flags",  c_long),
	("style_flags",   c_long),
	("num_glyphs",   c_long),
	("family_name",     c_char_p),
	("style_name",      c_char_p),
	("num_fixed_sizes",  c_int),
	("available_sizes",  c_voidp),
	("num_charmaps",  c_int),
	("charmaps",  c_voidp),
	("generic",  FT_Generic),
	("bbox",  FT_BBox),
	("units_per_EM", FT_UShort),
	("ascender", FT_Short),
	("descender", FT_Short),
	("height", FT_Short),
	("max_advance_width", FT_Short),
	("max_advance_height", FT_Short),
	("underline_position", FT_Short),
	("underline_thickness", FT_Short),
	("glyph", FT_GlyphSlot),
	("size", c_voidp),
	("charmap", c_voidp),
	# ("driver", FT_Driver),
	# ("memory", FT_Memory),
	# ("stream", FT_Stream),
	# ("sizes_list", FT_ListRec),
	# ("autohint", FT_Generic),
	# ("extensions", c_voidp),
	# ("internal", FT_Face_Internal),
]

FT = cdll.freetype6

