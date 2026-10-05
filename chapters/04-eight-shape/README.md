# 八字形模型 · 独立 LaTeX 核对工程

本章已根据审阅后的 Markdown 建立独立 Loom 工程，保留“例题后直接展开解法”的结构，已登记为 `integrated` 并作为第四章并入全书。

- [内容稿](content.md)：标准方位、八字倒角、四条件互推、45°/135°变式、图片例题一题四解。
- [LaTeX 主入口](latex/main.tex)：封面、目录、排版宏与分节导入。
- [单文件编辑稿](review.tex)：内嵌公共类文件和全部正文、TikZ 图，可在 Codex 内置编辑器打开。
- [独立核对 PDF](../../output/pdf/geometry-Models-04-八字形模型-核对稿.pdf)。
- [来源与整理说明](source-notes.md)：资料位置、视频时间、字幕校正和图片处理。
- `assets/diagrams/`：14 幅重绘图，每幅提供 PNG 与 SVG；对应 TikZ 宏位于 `latex/diagrams.tex`。
- `make_diagrams.py`：使用同一套坐标生成 PNG、SVG、TikZ，核对所有直角标记。
- `sync_latex.py`：将内容稿同步到四个分节正文，统一数学记号。
- `build.py`：先检查 Markdown/TeX 是否一致，再两遍编译，生成单文件编辑稿和 PDF；不会重写正文或图形。
- `check_math.py`：本章作者侧数学核验。

内容按 2 个例题展开，解法紧跟例题。例 1 将四条件互推的四种情况放在一起，并接上 45°、135° 两个单角变式；例 2 保留图片原题及四种解法。章首“关键的八字形”用蓝色、橙色突出 △ABO、△DCO，只标直角，正文用完整点名表示角。四种互推的标题统一使用数学符号 `\Rightarrow`，圈码用 TikZ 绘制，避免标题字体缺字。

公共 Loom 类文件从 `chapters/01-half-angle/latex/loom.cls` 转引；保留作者与 MIT 许可，不修改字体适配区。`review.tex` 从同一类文件和分节正文展开。内容迭代需要保持 Markdown、分节正文与单文件编辑稿一致。

用户已确认并入全书。全书入口为 `latex/sections/04-eight-shape.tex`，保留本章例题就地解答及例 2 前的分页；登记为 0 道正式练习、2 个例题。

从项目根目录运行：

```powershell
python scripts/build.py --target eight-shape --check
python scripts/build.py --target eight-shape --math
python scripts/build.py --target eight-shape --xelatex "D:/texlive/2026/bin/windows/xelatex.exe"
```

公共 `--check` 只检查源文件与例题编号，`--math` 执行数学核验。独立构建先检查 Markdown/TeX 一致性、生成编辑稿、核对两例结构与四种互推，再执行数学核验与两遍编译。数学核验使用精确分数与根式，检查 69 组标准构型、各组全等的对应顺序、K 型长度搬运、图片例题四种解法和同侧方位反例。本章已进入公共编译登记表，默认构建会包含本章和全书。

编译两遍后检查零错误、零溢出、零缺字、无未定义引用和非空目录；最终 PDF 另作逐页视觉检查。`teachernotes` 开关控制辅助线总结的显示，原有内容保留在源文件中。

本轮内置编译器返回平台标准目录不可用；编辑稿予以保留，本机 XeLaTeX 用于编译与验证，无需安装新编译器。

视频关键帧位于被忽略的 `work/video-frames/`。原始资料继续保留在主仓库的“八字变式”文件夹，本轮未搬移或纳入版本管理。

直接修改 TeX 后，先将内容改动回填到 `content.md`；若二者不一致，本章编译会停止并保留手改文件。`sync_latex.py` 只在已确认要从 Markdown 更新正文时手动运行；`make_diagrams.py` 只在确认要按坐标重绘时运行，避免覆盖手改图形。
