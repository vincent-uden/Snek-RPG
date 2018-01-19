from PIL import Image, ImageDraw

grid_base = Image.new("RGBA", (1320, 1160))

draw = ImageDraw.Draw(grid_base)

for x in range(1320):
    if x % 40 == 0:
        draw.line((x, 0, x, 1160), fill=(100,100,100))
for y in range(1160):
    if y % 40 == 0:
        draw.line((0, y, 1320, y), fill=(100,100,100))

grid_base.save("grid.png")