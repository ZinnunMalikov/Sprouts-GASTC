from PIL import Image
graph_thumb = Image.open(r"C:\Users\2000039241\OneDrive - Fulton County Schools\Desktop\meep3.png").convert('RGBA')
graph_cover = Image.open(r"C:\Users\2000039241\OneDrive - Fulton County Schools\Desktop\Sprouts-main\Resources\Sprouts Cover.png").convert('RGBA')
graph_icon = Image.open(r"C:\Users\2000039241\OneDrive - Fulton County Schools\Desktop\Sprouts-main\Resources\Gallery Icon.png").convert('RGBA')


result = Image.alpha_composite(graph_thumb, graph_cover)
result.save(r"C:\Users\2000039241\OneDrive - Fulton County Schools\Desktop\meep4.png")