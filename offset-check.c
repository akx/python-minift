#include <ft2build.h>
#include <freetype/freetype.h>

int main() {
	printf("offsetof glyph in face: %d\n", offsetof(FT_FaceRec, glyph));
	printf("offsetof bitmap in glyph: %d\n", offsetof(FT_GlyphSlotRec, bitmap));
}