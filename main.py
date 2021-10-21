
import os
import shutil
from pathlib import Path
from pdf2image import convert_from_path
import glob
import cv2
import pyocr
from PIL import Image


IMAGE_DIR = "./images"
TMP_DIR = "./tmp"
DIST_DIR = "./dist"

poppler_dir = Path(__file__).parent.absolute() / "poppler/bin"
os.environ["PATH"] += os.pathsep + str(poppler_dir)

# PDFファイルのパス
pdf_path = Path("./Kadai02.pdf")

# PDF -> Image に変換（150dpi）
pages = convert_from_path(str(pdf_path), 150)

# 画像ファイルを１ページずつ保存
image_dir = Path(IMAGE_DIR)
tmp_dir = Path(TMP_DIR)

if not tmp_dir.exists():
    tmp_dir.mkdir()

shutil.rmtree(tmp_dir)
tmp_dir.mkdir()


images = image_dir.glob("*.jpeg")
images = sorted(images)

engines = pyocr.get_available_tools()
engine = engines[0]

for source_img_name in images:
    source_img = cv2.imread(str(source_img_name))
    rows, cols = source_img.shape[:2]

    source_img = cv2.fastNlMeansDenoisingColored(src=source_img, h=10)

    for i in range(rows):
        for j in range(cols):
            s = source_img[i][j]

            if (j < 90 and i > 50):
                s = [255, 255, 255]
                source_img[i][j] = s

            if (j > cols-250 and i < 50):
                s = [255, 255, 255]
                source_img[i][j] = s

            if (i > rows-100):
                s = [255, 255, 255]
                source_img[i][j] = s

    cv2.imwrite(str(tmp_dir / source_img_name.name), source_img)

tmp_images = tmp_dir.glob("*.jpeg")
tmp_images = sorted(tmp_images)


for tmp_images_name in tmp_images:
    txt = engine.image_to_string(Image.open(
        str(tmp_images_name)), lang="eng")
    txt = txt.replace("datal", "data1")
    txt = txt.replace("“", '"')
    txt = txt.replace("”", '"')
    txt = txt.replace("’", "'")
    txt = txt.replace("‘", "'")

    filename = txt[:15]
    txt = txt[15:].split("\n")
    txt.remove("")

    new_txt = []
    for t in txt:
        if len(t) > 0:
            new_txt.append(t)

    txt = new_txt

    php = ""
    for t in txt:
        if t.count("//") > 0:
            i = t.index("//")
            t = t[:i]

        if len(t) == 0:
            continue

        php += t

        if t[len(t) - 1] == ";" or t[len(t) - 1] == ">" or t.count("<") > 0:
            php += "\n"

    print(php)
