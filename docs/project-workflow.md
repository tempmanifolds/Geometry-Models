# 章节维护与工作树协作

本项目使用一个 Git 仓库。章节目录用于组织内容，分支记录一项任务的修改，工作树为并行对话提供独立文件。每个工作树包含整个仓库，仍需限定各对话的修改范围。

## 当前状态

| ID | 目录 | 状态 | 题数 | 编译方式 |
| --- | --- | --- | --- | --- |
| `half-angle` | `chapters/01-half-angle` | 已并入全书 | 9 | 单章与全书 |
| `hand-in-hand` | `chapters/02-hand-in-hand` | 已并入全书 | 2 | 全书；可独立检查和数学核验 |
| `double-isosceles` | `chapters/03-double-isosceles` | 已并入全书 | 3 | 单章与全书 |

这张表用于阅读，运行时以根目录 `chapters.json` 为准。手拉手目前没有独立的 `latex/main.tex`，本轮保留现有编译能力。

## 日常分工

保留一个整合对话处理全书与公共文件。并行推进章节时，各章节对话从需要的基准提交创建独立工作树；例如 `codex/03-double-isosceles` 或 `codex/02-hand-in-hand-revision`。同一工作树不要给两个写文件的对话同时使用。

给章节对话的任务应写清楚：

> 本次只修改 chapters/03-double-isosceles、该章 PDF 和 check_double_isosceles.py。先读 AGENTS.md 与本章 README；保持当前登记状态，有内容疑问先问我。

章节通过核验后，以一个清楚的提交或 PR 交给整合任务。整合任务先合并章节源文件，再更新书目状态和公共入口，最后构建全书。合并后的工作树可归档；需要继续时从最新的整合版本另起任务，不给所有历史章节永久保留工作树。

工作树间通过 Git 提交与合并同步。一个工作树的未提交文件不会实时同步到另一个工作树；本地被忽略的原始素材也要单独安排访问。

## 登记章节

`chapters.json` 数组顺序决定全书顺序。各字段含义：

| 字段 | 用途 |
| --- | --- |
| `id` | 稳定的命令行 ID，不能重复，不能使用 `all` / `book` |
| `path` | 仓库内的章节目录，如 `chapters/03-double-isosceles` |
| `title` / `book_title` | 章节名称与全书 Markdown 的显示标题 |
| `status` | `draft`、`review` 或 `integrated`；仅后者进入全书 |
| `problem_count` | 本章正式题数，题目与解析均须从 1 连续编号 |
| `book_entry` | 全书章节入口的仓库相对路径；未并入时可为 `null` |
| `standalone` | 单章主文件和 PDF 文件名；没有独立入口时为 `null` |
| `standalone.builder` | 可选的专用脚本，保留本章特殊导出；双等腰用它更新 `review.tex` |
| `math_checks` | 本章数学核验脚本列表 |
| `markdown_remove_heading` | 可选，去掉旧稿重复的章标题；第一章保留该兼容设置 |

新增章节的顺序：

1. 在 `chapters/` 建立独立目录，准备 `content.md`、`README.md`、`latex/sections/`、`latex/diagrams.tex` 与来源说明。
2. 原始素材放在本章 `assets/source/`，临时工作放在 `work/`，整理后的重绘图放在 `assets/diagrams/`。
3. 内容和题图核对后，由整合任务登记为 `draft` 或 `review`，填入真实题数和已有入口。不要为尚无源文件的空目录登记可编译目标。
4. 需要单章 PDF 时提供独立主文件；保留公共宏与模板的引用关系，不到处复制修改模板。
5. 用户要求并入全书后，准备 `book_entry`，核对章节标题和超链接命名空间，将状态改成 `integrated`，再同步和编译。

全书章节入口目前位于 `latex/sections/`，负责章标题、分节导入和超链接命名空间。登记表负责选择与排序；入口里的标题应与登记表核对。全书封面和 PDF 元数据仍在 `latex/main.tex` 的手工维护区。

## 统一命令

以下命令从项目根目录运行，需要 Python 3.9 或更新版本。

```powershell
# 查看章节状态、题数和已有编译能力
python scripts/build.py --list

# 检查现有全书和默认单章，不编译、不改文件，不需要 XeLaTeX
python scripts/build.py --check

# 单独检查双等腰；同样适用于其他章节 ID
python scripts/build.py --target double-isosceles --check

# 只同步全书 LaTeX 导入区和根目录 content.md
python scripts/build.py --sync

# 核验已并入全书的章节；核对稿需要显式指定 ID
python scripts/build.py --math
python scripts/build.py --target double-isosceles --math

# 默认编译全书及已并入全书且有独立入口的单章，各编译两遍
python scripts/build.py --xelatex "D:/texlive/2026/bin/windows/xelatex.exe"

# 只编译全书
python scripts/build.py --target book --xelatex "D:/texlive/2026/bin/windows/xelatex.exe"

# 只编译双等腰核对稿，不更新全书源文件和全书 PDF
python scripts/build.py --target double-isosceles --xelatex "D:/texlive/2026/bin/windows/xelatex.exe"

# 编译脚本的回归测试
python -m unittest discover -s tests -v
```

若 XeLaTeX 已在 PATH 中，可省略 `--xelatex`。`--check`、`--sync`、`--math` 和 `--list` 均不依赖 XeLaTeX。

单章命令不会更新根目录 `content.md` 或全书入口。`all` 的含义是全书及已并入全书的可独立编译章节，不自动包含核对稿。默认数学核验同样只针对已并入全书的章节。

题数检查逐章进行，避免相同局部题号掩盖跨章遗漏。编译检查输入是否存在、正文是否意外结束、目录及日志中的错误、溢出、缺字和未定义引用；正式交付还需查看 PDF 版面。

## 素材与提交

原始视频、字幕、Word/PDF、截图与提取帧只保留本地。现有根目录素材位置继续保留，不在本轮搬移。新工作树若需要素材，先确认其本地位置；不要为方便访问而把全部视频提交进 Git。

Git 保存章节源文件、来源说明、核验脚本、重绘图和交付 PDF。提交前查看差异，明确区分已有稿件与本次修改；全书汇总与全书 PDF 由整合任务生成后一起提交。

本轮先建立上述管理基础。公共排版宏的进一步抽取、手拉手单章入口、自动 CI 和正式版本标签，可在实际需要时逐项处理。
