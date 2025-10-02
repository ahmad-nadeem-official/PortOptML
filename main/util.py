from PIL import Image

img = Image.open("Tradmincer.png")
bigger = img.resize((1000, 1000), Image.LANCZOS)  # upscale to 1000x1000
bigger.save("Tradmincer_big.png")
