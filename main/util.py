import cv2

image = cv2.imread("Tradmincer_big.png")
resized_image = cv2.resize(image, (2024, 2024), interpolation=cv2.INTER_LANCZOS4)
cv2.imwrite("main/Tradmincer_big2.png", resized_image)
print("Image resized and saved as main/Tradmincer_big2.png")
# cv2.INTER_LANCZOS4 is a good interpolation method for enlarging images.
