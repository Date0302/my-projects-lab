from PIL import Image

def create_thumbnail(input_path, output_path, size=(300, 300)):

    with Image.open(input_path) as img:

        img.thumbnail(size)

        img.save(output_path)

    return output_path