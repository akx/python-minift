# -- encoding: utf-8 --
from minift import *

def get_glyph_data(text, faceptr):
	glyphs = []

	for ch in text:
		gi = FT.FT_Get_Char_Index(faceptr, ord(ch))
		assert gi
		assert not FT.FT_Load_Glyph(faceptr, gi, 0)
		assert not FT.FT_Render_Glyph(faceptr.contents.glyph, 2) # 2 = Mono mode
		g = faceptr.contents.glyph.contents
		assert addressof(g.bitmap) - addressof(g) == 76

		bmp = g.bitmap

		glyphs.append({
			"width":	bmp.width,
			"height":	bmp.rows,
			"pitch":	bmp.pitch,
			"left":		g.bitmap_left,
			"top":		g.bitmap_top,
			"data":		tuple(bmp.buffer[:(bmp.rows * bmp.pitch)]),
			"advance":	(g.advance.x >> 6)
		})
	return glyphs

def render_pil_glyphs(glyphs):

	w = sum(g["advance"] + g["left"] for g in glyphs)
	h = max(g["height"] + g["top"] for g in glyphs)

	import Image

	img = Image.new("RGB", (1024, 768))

	bx = 0
	by = 50

	def yield_bits(bytes):
		for byte in bytes:
			for offset in range(8)[::-1]:
				yield ((byte >> offset) & 1)

	idata = img.load()

	for g in glyphs:
		#print g
		for y in xrange(g["height"]):
			bits = yield_bits(g["data"][y * g["pitch"]:(y+1) * g["pitch"]])
			for x in xrange(g["width"]):
				bit = bits.next()
				if bit:
					px = bx + x + g["left"]
					py = by + y - g["top"]
					if 0 < px < img.size[0] and 0 < py < img.size[1]:
						idata[px, py] = (255, 255, 255)
		bx += g["advance"] # May not be correct

	return img


def main():
	libptr = c_voidp()
	res = FT.FT_Init_FreeType(byref(libptr))
	faceptr = FT_Face()
	res = FT.FT_New_Face(libptr, r"c:/windows/fonts/simhei.ttf", 0, byref(faceptr))
	fc = faceptr.contents
	assert (addressof(fc.glyph) - addressof(fc) == 84)

	font_size = 70

	res = FT.FT_Set_Pixel_Sizes(faceptr, 0, font_size)
	glyphs = get_glyph_data(u"测试中文文本。 Hello, world", faceptr)

	img = render_pil_glyphs(glyphs)

	img.save("test.png")



if __name__ == '__main__':
	main()