# coding : utf-8

from flask import Flask, request
import os
import re
import mistune
import urllib.parse
from rich import print as print


markdown = mistune.create_markdown()


app = Flask(__name__)
SITEHOST = "http://192.168.1.197"


@app.route("/a/<path:filename>")
def a(filename):
    filename = "a/" + urllib.parse.unquote(filename)

    if os.path.isdir(filename):
        all_dir_files = "".join(
            [
                (
                    f'<p><a href="{SITEHOST}/{filename}/{i}">{i}    文件夹</a></p>'
                    if os.path.isdir(f"./{filename}/" + i)
                    else f'<p><a href="{SITEHOST}/{filename}/{i}">{i}   文件</a></p>'
                )
                for i in os.listdir(f"./{filename}")
            ]
        )
        if len(all_dir_files) == 0:
            all_dir_files = "空"
        return all_dir_files

    if not os.path.isfile(filename):
        return "404"

    with open(filename, encoding="utf-8") as f:
        return markdown(f.read())


@app.route("/s")
def s():
    # 设置要搜索的文件夹路径和要搜索的关键词
    folder_path = "a/"
    keyword = request.args.get("k")
    search_keyword = keyword

    # 遍历文件夹下的所有文件
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            # 如果是文件，则打开文件并读取内容
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                # 使用正则表达式匹配关键词
                match = re.search(search_keyword, content)
                if match:
                    # 如果关键词匹配成功，则输出文件名和匹配位置
                    return f"Found '{search_keyword}' in <a href=\"{SITEHOST}/a/{file_name}\">{file_name}</a> at position {match.start()}"

    return "no results found"


@app.route("/")
def index():
    search = f"""<form action="{SITEHOST}/s" method="get">
		<label for="k">请输入关键字：</label>
		<input type="text" id="k" name="k">
		<input type="submit" value="搜索">
	</form>"""
    all_dir_files = "".join(
        [
            (
                f'<p><a href="{SITEHOST}/a/{i}">{i}    文件夹</a></p>'
                if os.path.isdir(f"./a/" + i)
                else f'<p><a href="{SITEHOST}/a/{i}">{i}    文件</a></p>'
            )
            for i in os.listdir("./a")
        ]
    )
    if len(all_dir_files) == 0:
        all_dir_files = "空"
    return search + all_dir_files


if __name__ == "__main__":
    app.run("127.0.0.1", port=80, debug=False)
