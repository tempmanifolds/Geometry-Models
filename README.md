# geometry Models

初中几何模型总结与培优讲义。各专题保留模型识别、入手提示、规范证明与可迁移结论，题目区与解析区分开。

## 第一部分 夹半角

- [阅读讲义 PDF](output/pdf/geometry-Models-01-夹半角讲义.pdf)
- [编辑内容稿](chapters/01-half-angle/content.md)
- [LaTeX 主文件](chapters/01-half-angle/latex/main.tex)
- [专题说明与原稿对应表](chapters/01-half-angle/README.md)

本讲面向初二、初三培优学生，包含 10 道题、4 种识别构型和旋转、翻折、延长构造等方法。拓展部分讨论条件等价、定高、定周长、乘积关系、线段长度范围及内部/外部构型的加减变化。

原始 Word 与 PDF 只保留在本地，已从版本管理中排除。

## 文件结构

```text
chapters/
  01-half-angle/
    content.md          内容稿
    README.md           专题维护说明
    latex/
      main.tex          主文件与显示开关
      loom.cls          Loom 排版模板
      diagrams.tex      可编辑几何图
      sections/         导读、题目、解析、总结
output/pdf/             正式 PDF
scripts/
  build.py              两遍编译并导出 PDF
  check_math.py         数值及模型关系核验
```

## 编译

安装有 XeLaTeX 的 TeX Live 环境后，在项目根目录执行：

```text
python scripts/build.py
```

如果 XeLaTeX 不在环境路径中，用 `--xelatex` 指定可执行文件路径，例如：

```text
python scripts/build.py --xelatex "D:/texlive/2026/bin/windows/xelatex.exe"
```

脚本执行两遍 XeLaTeX，检查编译错误、版面溢出、缺字及未定义引用，再将 PDF 导出到 `output/pdf/`。几何图由 TikZ 绘制，随 LaTeX 源文件一起编辑，不依赖原始材料中的截图。

## 编辑与版本切换

在 `content.md` 中讨论内容；最终排版文件按板块放在 `latex/sections/`，修改内容时同步更新两者。调整几何图时编辑 `diagrams.tex` 并重新核验位置与角度。

`main.tex` 中的 `\showhintstrue` 可改成 `\showhintsfalse`，隐藏入手提示；`\teachernotestrue` 可改成 `\teachernotesfalse`，将总结部分切换为学生自主总结区。原有内容保留在开关内，方便继续修订。

Loom 模板由 Polaris（北极甜虾）提供，类文件头保留原作者与 MIT 许可说明。
