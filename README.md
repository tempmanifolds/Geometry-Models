# geometry Models

Hence 的初中几何模型总结与培优讲义。面向初二、初三培优学生，先做原题，再阅读提示和完整解析，最后归纳可迁移的模型结论。

## 阅读与编辑

- [完整讲义 PDF](output/pdf/geometry-Models-讲义.pdf)：夹半角、手拉手与双等腰合编，共用封面和目录，各章保留自己的题号。
- [全书 Markdown](content.md)：由各章内容稿汇总。
- [全书 LaTeX 主文件](latex/main.tex)：可编辑正文、显示开关与编译入口。
- [夹半角单章 PDF](output/pdf/geometry-Models-01-夹半角讲义.pdf)：保留单章使用方式。
- [双等腰独立核对稿](output/pdf/geometry-Models-03-双等腰模型-核对稿.pdf)：与主书第三章共用正文和重绘图。

## 章节

| 章节 | 状态 | 内容 | 内容稿 | 维护说明 |
| --- | --- | --- | --- | --- |
| 第一章 夹半角 | 已并入全书 | 10 道题、4 种识别构型；旋转、翻折、延长、矩形迁移及和差变化 | [Markdown](chapters/01-half-angle/content.md) | [专题说明](chapters/01-half-angle/README.md) |
| 第二章 手拉手模型 | 已并入全书 | 2 道原题，每题两种解法；手拉脚、脚拉脚、倍长及中点搬运 | [Markdown](chapters/02-hand-in-hand/content.md) | [专题说明](chapters/02-hand-in-hand/README.md) |
| 第三章 双等腰模型（婆罗摩笈多模型） | 已并入全书 | 1 页一线三等角回顾、3 项结论及完整证明；等面积、中点与垂直、伴随长度关系 | [Markdown](chapters/03-double-isosceles/content.md) | [专题说明](chapters/03-double-isosceles/README.md) |

章节登记表为 [chapters.json](chapters.json)，多对话分工与新增章节流程见[项目维护说明](docs/project-workflow.md)，对话开始时遵循 [AGENTS.md](AGENTS.md)。

原始 Word、PDF、视频、字幕及提取截图只保留在本地，均从版本管理和交付项目包中排除。GitHub 保存整理后的讲义、可编辑源文件和重绘图。

## 编译

安装有 XeLaTeX 的 TeX Live 环境后，在项目根目录执行：

    python scripts/build.py

脚本读取章节登记表，默认各编译两遍，生成完整讲义、夹半角单章与双等腰独立核对稿 PDF，同时更新全书 Markdown。核对稿需要显式指定，不自动进入全书。单独编译全书可增加参数：

    python scripts/build.py --target book

如果 XeLaTeX 不在环境路径中，用参数指定位置：

    python scripts/build.py --xelatex "D:/texlive/2026/bin/windows/xelatex.exe"

编译前递归检查输入文件、题目与解析配对；编译后检查错误、版面溢出、缺字、未定义引用及目录。正式输出位于 output/pdf/。

查看目标和状态、只检查源文件或只同步全书入口时，无需 XeLaTeX：

    python scripts/build.py --list
    python scripts/build.py --check
    python scripts/build.py --sync

独立编译双等腰核对稿，不更新全书：

    python scripts/build.py --target double-isosceles --xelatex "D:/texlive/2026/bin/windows/xelatex.exe"

## 维护方式

各章内容稿位于 chapters/ 下的 content.md，排版正文按导入、题目、解析、总结保存在各章的 latex/sections/ 中。内容修改时同步更新这两种格式；根目录 content.md 是自动汇总稿，下一次编译会重新生成。

全书主文件引入 latex/sections/ 中的章节入口。以后增加章节时，保持各章独立，在登记表记录状态、入口和本章题数；全书导入顺序与题数由登记表决定，无需在 Python 脚本里逐处增加章节。`latex/main.tex` 标注为 GENERATED 的两处导入区由脚本维护，其余封面和显示开关仍在主文件中编辑。全书和夹半角单章共用第一章目录中的 Loom 类文件。

并行章节对话各用独立工作树，只修改本章；一个整合对话维护公共文件和全书输出。单章编译不会改动根目录汇总稿。原始素材放在各章 `assets/source/`，工作文件放在 `work/`，均被 Git 忽略。

几何图由 TikZ 绘制，可在各章的 diagrams.tex 中修改。图中保留点名、角度、等长记号及必要的变量；数值长度写在题干或推导中。

解析采用“怎么想、规范解答、方法点睛”，取消独立“检验”板块及其中的文字；数学核验继续在作者侧脚本中进行。

全书现有等长标记的小短线统一加长 50%，TikZ 参数从总长 4pt 调到 6pt，配套 PNG、SVG 同步更新。重绘命令：

    python scripts/make_hand_in_hand_diagrams.py
    python scripts/make_double_isosceles_diagrams.py

主文件中的显示开关可以隐藏入手提示，或将模型总结切换为学生自主总结区。原有讲解内容保留在开关内。

## 数学核验

    python scripts/build.py --math
    python scripts/build.py --target double-isosceles --math

默认核验全书三个章节：夹半角数值题和拓展公式、手拉手两题的旋转与搬运关系、双等腰的等面积与中点垂直关系。双等腰检查 288 组精确构型，包含垂足重合情形及镜像反例。第二条命令只核验双等腰。原有各章脚本仍可直接运行。最终 PDF 还需逐页检查。

编译管理脚本修改后运行回归测试：

    python -m unittest discover -s tests -v

Loom 模板由 Polaris（北极甜虾）提供，类文件头保留原作者与 MIT 许可说明。
