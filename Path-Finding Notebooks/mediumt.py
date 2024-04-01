import matplotlib.pyplot as plt
from PIL import Image

image_path = r"C:\Users\2000039241\OneDrive - Fulton County Schools\Desktop\tempimg.png"

image = Image.open(image_path)
fig1 = plt.figure(num = 1)
plt.scatter(560 - 220 + 100 , 400 - 257.4 + 100, marker='o', color="red", edgecolors='black')
plt.imshow(image)
plt.show()