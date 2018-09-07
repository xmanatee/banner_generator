# -*- coding: utf-8 -*-

import subprocess
import os
import tempfile
import logging
import re

# from css2video.renderers.image import render_image as render

# https://github.com/bpsagar/css2video/blob/master/css2video/renderers/image/cutycapt.py

MOUNTED_VOLUME = "/mnt/target"
# PNG_STORAGE_PATH = os.path.join(MOUNTED_VOLUME, "pngs")
PNG_STORAGE_PATH = "/mnt/pngs"

TIMEOUT_SECONDS = 60
XDISPLAY = ":89"


def prepare_str_for_css(s):
    s = s.encode("ascii", 'backslashreplace').replace(b"\\u", b"\\").decode()
    s = re.sub(r'(\\[0-9a-fA-F]{4} )', r'\1 ', s)
    s = s.replace("'", "\\'").replace('"', '\\"')
    return s


class CutycaptRenderer:
    def __init__(self):
        self.tempdir = tempfile.mkdtemp()
        self.xvfb = subprocess.Popen([
            'Xvfb',
            XDISPLAY,
            '-screen',
            '0',
            '1080x1920x24',
            '-fbdir',
            self.tempdir
        ])
        os.environ["DISPLAY"] = XDISPLAY

    def html_to_png(self, html_path, png_path, min_width=1080, min_height=1920):

        args = [
            "cutycapt",
            "--url={url}".format(url=html_path),
            "--plugins=on",
            "--min-width={min_width}".format(min_width=min_width),
            "--min-height={min_height}".format(min_height=min_height),
            "--out={png_path}".format(png_path=png_path)
        ]
        logging.info("starting png generation")
        process = subprocess.call(args, timeout=TIMEOUT_SECONDS)
        logging.info("...done!")

        return process

    def png_for_title_and_category(self, png_path, title, category, template):
        # title = re.escape(title)
        # category = re.escape(category)

        title = prepare_str_for_css(title)
        category = prepare_str_for_css(category)

        styles_str = ".text:after {{ content: '{title}'; }}\n #paper:after {{ content: '#{category}'; }}".format(
            title=title,
            category=category,
        )

        return self.png_for_extra_styles(
            png_path=png_path,
            styles_str=styles_str,
            template=template,
        )

    def png_for_extra_styles(self, png_path, styles_str="", template="vk", dump_styles=False):

        if template == "vk":
            url = "/mnt/templates/empty_vk/index.html"
            min_width = 1080
            min_height = 480
        elif template == "insta":
            url = "/mnt/templates/empty_insta/index.html"
            min_width = 1080 // 2
            min_height = 1920 // 2
        else:
            raise ValueError

        args = [
            "cutycapt",
            "--url={url}".format(url=url),
            "--plugins=on",
            "--min-width={min_width}".format(min_width=min_width),
            "--min-height={min_height}".format(min_height=min_height),
            "--out={png_path}".format(png_path=png_path)
        ]
        if dump_styles:
            styles_path = png_path + ".css"
            with open(styles_path, "w", encoding="utf8") as f:
                f.write(styles_str)

            args.append(
                "--user-style-path={styles_path}".format(styles_path=styles_path),
            )

            # with open(styles_str, "r") as f:
            #     print(f.readlines())
        else:
            args.append(
                "--user-style-string={styles_str}".format(styles_str=styles_str),
            )
        logging.info("starting png generation")
        process = subprocess.call(args, timeout=TIMEOUT_SECONDS)
        logging.info("...done!")

        return process


# if __name__ == "__main__":
#     google_path = "https://google.com"
#     github_path = "https://github.com"
#     vk_post_path = "/mnt/templates/vk_post_1/index.html"
#     ig_stories_path = "/mnt/templates/ig_stories_1/index.html"
#
#     google_png_path = os.path.join(PNG_STORAGE_PATH, "google_from_docker_2.png")
#     github_png_path = os.path.join(PNG_STORAGE_PATH, "github_from_docker_2.png")
#     vk_post_png_path = os.path.join(PNG_STORAGE_PATH, "vk_post_from_docker_2.png")
#     ig_stories_png_path = os.path.join(PNG_STORAGE_PATH, "ig_stories_from_docker_2.png")
#
#     start()
#
#     html_to_png(google_path, google_png_path)
#     html_to_png(github_path, github_png_path)
#     html_to_png(vk_post_path, vk_post_png_path, 1080, 480)
#     html_to_png(ig_stories_path, ig_stories_png_path)
#
#     logging.info("DONE")
#
# .text:after {
#     content: '"When I get sad I stop being sad and be LALAKA instead. @Barney Stinson"';
# }
#
# #paper:after {
#     content: "#paper";
# }
#
# .bg {
#     height: 10%;
#     background: url('img/image-1.png');
# }
