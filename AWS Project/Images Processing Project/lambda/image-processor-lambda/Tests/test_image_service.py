from image_processor.image_service import create_thumbnail
from PIL import Image
import os


def test_create_thumbnail():

    input_path = "tests/test_input.jpg"
    output_path = "tests/test_output.jpg"

    # 创建测试图片（500x500）
    img = Image.new("RGB", (500, 500), color="red")
    img.save(input_path)

    # 调用函数
    create_thumbnail(input_path, output_path)

    # 验证输出文件存在
    assert os.path.exists(output_path)

    # 验证尺寸
    thumb = Image.open(output_path)

    assert thumb.width <= 300
    assert thumb.height <= 300

    # 清理
    os.remove(input_path)
    os.remove(output_path)