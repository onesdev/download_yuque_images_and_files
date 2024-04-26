import os
import re
import pathlib
import requests
import sys

# 遍历当前目录，打印出所有.md文件的路径
def process_md_files(directory_path):
    # print("处理目录:", directory_path)
    
    # 遍历当前目录，如果是目录，就递归调用process_md_files函数，如果是.md文件，就调用yuque_files_download函数
    for file_path in directory_path.glob("**/*"):
        if file_path.is_dir():
            process_md_files(file_path)
        elif file_path.suffix == '.md':
            # 下载.md文件中的图片或附件
            yuque_files_download(file_path)
        else:
            continue


def yuque_files_download(file_path):
    print('处理文件:{}...'.format(file_path))

    # 判断file_path指向的是否是markdown文件
    if re.search(r'\.md$', str(file_path)) is None:
        print('Error: 请输入markdown文件（.md）')
        return None

    # 获取文件附件的路径
    assets_path = file_path.parent / 'assets'
    
    # 读取文件内容
    with open(file_path, encoding='utf-8') as md_file:
        content = md_file.read()

        if content is not None:

            # 查找图片链接: image_link = ![...](image_url)
            pattern_image_link = r'\!\[.*?\]\(.*?\)'
            image_links = re.findall(pattern_image_link, content)
            for image_link in image_links:
                # 判断是否是语雀的图片链接
                if "https://cdn.nlark.com/yuque" in image_link:
                    pattern_image_url = r'\((.*?)\)'
                    image_urls = re.findall(pattern_image_url, image_link)
                    for image_url in image_urls:
                        if "https://cdn.nlark.com/yuque" in image_url:
                            # 下载图片
                            local_image_path = download_file(image_url, assets_path)
                            # 替换链接
                            if local_image_path is not None:
                                new_image_link = image_link.replace(image_url, local_image_path)
                                content = content.replace(image_link, new_image_link)
                                
            # 查找文件链接: file_link = [...](file_url)
            pattern_file_link = r'\[.*?\]\(.*?\)'
            file_links = re.findall(pattern_file_link, content)
            for file_link in file_links:
                # 判断是否是语雀的附件链接
                if "https://www.yuque.com/attachments/yuque" in file_link:
                    pattern_file_url = r'\((.*?)\)'
                    file_urls = re.findall(pattern_file_url, file_link)
                    for file_url in file_urls:
                        if "https://www.yuque.com/attachments/yuque" in file_url:
                            # 下载文件
                            local_file_path = download_file(file_url, assets_path)
                            # 替换链接
                            if local_file_path is not None:
                                new_file_link = file_link.replace(file_url, local_file_path)
                                content = content.replace(file_link, new_file_link)
            
            # 处理下换行符，语雀导出的md文件缺少换行，vuepress渲染出来的无换行
            # content = format_newline(content)

            # 写入文件
            with open(file_path, 'w', encoding='utf-8') as md_file:
                md_file.write(content)
                print('写入文件成功')


def download_file(file_url, assets_path):
    """
    给定文件（含图片）链接，将附件下载到本地，返回本地的图片链接字符串
    :param
        file_url: 语雀文件下载链接
        assets_path: 本地资源目录
    :return:
        local_file_path: 本地资源路径（相对路径字符串）
        or None: 下载失败
    """

    # 初始化本地附件链接字符串，如果下载图片失败直接返回None
    local_file_link = None

    # 获取附件的文件名
    if "mermaid" in file_url:
        pattern_name = r'__mermaid_v3\/(.*?\.svg)'
    elif 'latex' in file_url:
        pattern_name = r'__latex\/(.*?\.svg)'
    elif "?" in file_url:
        # 如果包含"?", 则匹配"?"之前和第一个"/"之后的内容作为file_name
        pattern_name = r'\/(\d+\-.*?\-.*?\-.*?\-.*?\-.*?\..*?)\?'
    elif "#" in file_url:
        pattern_name = r'\/(\d+\-.*?\-.*?\-.*?\-.*?\-.*?\..*?)#'
    else:
        # 如果不包含"?"或"#", 则匹配字符串结尾之前和最后一个"/"之后的内容作为file_name
        pattern_name = r'\/(\d+\-.*?\-.*?\-.*?\-.*?\-.*?\..*?)$'
    file_name = re.findall(pattern_name, file_url)[0]

    file_path = assets_path / file_name

    # 下载文件到本地资源库
    # 如果assets目录不存在，则创建目录
    if not assets_path.exists():
        assets_path.mkdir(parents=True)
    # 如果文件不存在，则下载文件
    if not file_path.exists():
        try:
            get_file = requests.get(file_url)
            file_path.write_bytes(get_file.content)
            print('{} 下载成功'.format(file_url))
            local_file_link = 'assets/' + file_name
        except:
            print('{} 下载错误: {}'.format(file_url, sys.exc_info()[0]))
    else:
        print('{} 图片已下载'.format(file_url))
        local_file_link = 'assets/' + file_name
    
    return local_file_link



def format_newline(content):
    """
    对语雀导出的markdown文本处理换行符：添加\n和<br/>，但是要注意避开代码块
    :param content: 读取到内存的语雀md文档内容
    :return: True or Flase
    """

    # 先对所有的内容都添加换行
    content = content.replace('\n', '\n\n')
    content = content.replace('\n\n\n\n', '\n\n<br/>\n\n')

    # 然后用正则表达式匹配找出代码块，将代码块再换回来
    code_blocks = re.findall('```[^`]*```', content, re.S)
    for code_block in code_blocks:
        code_block_new = code_block.replace('\n\n', '\n')
        code_block_new = code_block_new.replace('\n<br/>\n', '\n\n')
        content = content.replace(code_block, code_block_new)
       
    # 处理标题，将标题降一级，即一级变二级，二级变三级，因为vuepress中一级标题被用作文章标题
    content = re.sub('# ', '## ', content)

    return content



if __name__ == '__main__':
    # 获取当前目录
    current_directory = pathlib.Path.cwd()

    process_md_files(current_directory)