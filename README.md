# 项目说明

本项目旨在配合[vannvan/yuque-tools: 🧰 玩转语雀-朴实无华的语雀工具集合，语雀知识库+团队资源批量导出/备份工具(无需Token)｜浏览器插件助手 (github.com)](https://github.com/vannvan/yuque-tools)项目实现语雀知识库批量导出到本地。



yeque-tools这个工具很好用，我们从官方仓库下载release包解压后，可以看到ytool.exe文件（这里我使用windows电脑），我们只需要使用`./ytool.exe pull` 命令进入交互模式，按照提示输入我们的语雀用户名和密码，就可以看到我们名下的知识库，选择要导出的知识库，就可以导出到本地markdown文档。

但是此时，导出的markdown文档中，所有图片或者附件，甚至mermaid图和latex公式（都是导出为svg图片），都是在线模式的，就是图片或者附件仍放在语雀的在线服务器上，并没有完全本地化。

我从我的知识库中，找到了以下几类典型的link模式：

```
![](https://cdn.nlark.com/yuque/0/2024/jpeg/793259/1711863000450-096431b9-c73c-4da2-bbb0-66d4c7e31983.jpeg?x-oss-process=image%2Fformat%2Cwebp#averageHue=%2323a7e9&from=url&id=FWZSv&originHeight=1115&originWidth=1982&originalType=binary&ratio=1&rotation=0&showTitle=false&status=done&style=none&title=)

[【周报】多空博弈？国家队救市？【20240121】音频（阿乐）.mp3](https://www.yuque.com/attachments/yuque/0/2024/mp3/793259/1705814652947-91d1dd42-3cd8-46d4-9c12-ab47481f4912.mp3)

[20240330-【周报】盘整仍在继续，重量级产品预发布【20240331】.pptx](https://www.yuque.com/attachments/yuque/0/2024/pptx/793259/1711871660204-f5250585-c460-43b6-8a9e-f1b7d0fccf00.pptx)

![](https://cdn.nlark.com/yuque/0/2023/jpeg/793259/1704034552269-0d12044b-878b-4857-b61e-51e12128161c.jpeg#averageHue=%23956b91&clientId=u4abc433a-0166-4&from=paste&id=u7ab70210&originHeight=641&originWidth=480&originalType=url&ratio=1&rotation=0&showTitle=false&status=done&style=none&taskId=uce3be8d7-4183-42ae-8704-4132f7962fa&title=)

[20240330-【周报】盘整仍在继续，重量级产品预发布【20240331】.pptx](https://www.yuque.com/attachments/yuque/0/2024/pptx/793259/1711871660204-f5250585-c460-43b6-8a9e-f1b7d0fccf00.pptx)

![](https://cdn.nlark.com/yuque/__mermaid_v3/1a96d0a682d75b14a43f63b985878288.svg#lake_card_v2=eyJ0eXBlIjoibWVybWFpZCIsImNvZGUiOiJncmFwaCBMUlxuQVvnn6Xor4bovpPlhaXlkozmgJ3ogINdIC0tPiBCe-ezu-e7n-i_mOaYr-mbtuaVo31cbkIgLS0-fOezu-e7n-efpeivhnwgQ1vkuJPkuJrnrJTorrBdXG5CIC0tPnzpm7bmlaPnn6Xor4Z8IERb5pel6K6wXVxuRCAtLT5857O757uf5pW055CG5ZCOfCBDIiwidXJsIjoiaHR0cHM6Ly9jZG4ubmxhcmsuY29tL3l1cXVlL19fbWVybWFpZF92My8xYTk2ZDBhNjgyZDc1YjE0YTQzZjYzYjk4NTg3ODI4OC5zdmciLCJpZCI6ImY1dmtOIiwibWFyZ2luIjp7InRvcCI6dHJ1ZSwiYm90dG9tIjp0cnVlfSwiY2FyZCI6ImRpYWdyYW0ifQ==)

![](https://cdn.nlark.com/yuque/__latex/bb569c50e036033c1bc2d290524320e2.svg#card=math&code=%EF%BC%88pageid1%2C%20pageid2%2C%20...%20%2C%20pageidi%EF%BC%89%5Ccdot%20%28age1%2C%20age2%2C%20...%20%2C%20agej%29%0A%3D%5Csum_%7B%5Csubstack%7Bi%2C%20j%7D%7D%20pageidi%20%5Ccdot%20agej&height=37&width=496)

![clipboard(1).png](https://cdn.nlark.com/yuque/0/2021/png/793259/1612972371533-71b00c7c-8215-4a95-9ed6-15a840f1b6e8.png#align=left&display=inline&height=377&originHeight=403&originWidth=690&size=281418&status=done&style=none&width=646)
```

因此，我们还需要把这些图片和附件都下载到本地才行。

这个项目就是解决这个问题的。

# 原理

1. 遍历当前目录，处理所有.md文件。
2. 对于每一个.md文件：
   1. 读取文件内容到内存。
   2. 查找所有语雀的图片链接，下载图片，替换链接。
   3. 查找所有语雀的附件链接，下载附件，替换链接。
   4. 将处理好的文件内容重新写入到文件。

# 用法

将`download_yuque_images_and_files.py` 文件复制到下载好的知识库根目录，命令行下运行：

```bash
python download_yuque_images_and_files.py
```

如果缺少依赖，自己打开源码，看看依赖，自行安装。



# 报错

如果报错，大家可以根据程序执行输出，看到是哪一个文件的哪一个图片导出出错，十有八九是相关URL没有被正确识别。这里我故意没有做错误的忽略处理，而是让它中断，就是为了方便提示哪里有问题。

大家可以自己修改源码解决。

修改好源代码后，重新运行即可，程序不会重复下载已经下载过的图片或附件，很快就会重新回到出错的位置继续下载。

