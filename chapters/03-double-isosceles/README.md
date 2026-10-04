# 双等腰模型（婆罗摩笈多模型）· 独立核对稿

本章已作为第三章收入主书，同时保留独立核对稿。面向初二、初三培优学生，沿用现有 Loom 版式和“题目／集中解析／模型总结”的体例。

- 章首约 1 页：一线三等角的直角全等型，只回顾本章需要的识别条件与 AAS 推导。
- 主体 3 题：等面积、中点推出垂直、垂直推出中点，完整补齐视频中的辅助线和对应角。
- 补充：由第二次全等直接得到 `2BE＝C′D`，再把长度与高度关系用于另一种面积证明。
- 5 幅图同时保留 TikZ、SVG、PNG；题目区共用无辅助线图，解析区分别作图。
- 保留显示开关：`showhints` 控制提示，`teachernotes` 控制总结。

## 阅读与编辑

- [独立核对 PDF](../../output/pdf/geometry-Models-03-双等腰模型-核对稿.pdf)
- [完整讲义 PDF](../../output/pdf/geometry-Models-讲义.pdf)
- [内容稿](content.md)
- [LaTeX 主入口](latex/main.tex)
- [自包含编辑稿](review.tex)：同一正文及模板的单文件展开版，可在 Codex 内置编辑器中打开。
- [来源与校正说明](source-notes.md)

主要内容在 `latex/sections/`，图形在 `latex/diagrams.tex`；`latex/loom.cls` 保留模板作者与 MIT 许可。`review.tex` 从上述源文件展开生成；内容修改后重新编译会同步更新这个编辑稿。

本章等长标记的小短线总长由 4pt 加长到 6pt；单线、双线和三线标记的条数及位置保持原样。需要重新生成配套的 TikZ、SVG、PNG 时，从项目根目录执行：

    python scripts/make_double_isosceles_diagrams.py

## 单章编译

从项目根目录执行，不运行主书的编译脚本：

    python chapters/03-double-isosceles/build.py --xelatex "D:/texlive/2026/bin/windows/xelatex.exe"

脚本仅编译本章两遍，核对 3 道题与解析配对、目录、错误、版面溢出、缺字和未定义引用，输出独立 PDF。根目录的 `content.md`、`latex/main.tex` 和已有主书 PDF 均不更新。

数学核验：

    python scripts/check_double_isosceles.py

使用精确分数检查 288 组同方位构型，包含 10 组双垂足重合的特殊情况，并验证镜像方位不能直接套用中点与垂直结论。
