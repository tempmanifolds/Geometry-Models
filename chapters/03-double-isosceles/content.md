# 双等腰模型（婆罗摩笈多模型）

署名：Hence

## 一线三等角：快速回顾

先看一幅熟悉的图：A、B、C 在同一直线上，B 在 A、C 之间，D、E 在直线 AC 的同侧，且

\[
\angle DAB=\angle DBE=\angle BCE=90^\circ,\qquad BD=BE.
\]

![一线三等角：直角全等型](<assets/diagrams/review.png>)

直线上的三个角满足

\[
\angle DBA+\angle DBE+\angle EBC=180^\circ,
\]

所以 ∠DBA＋∠EBC＝90°。而在 Rt△DAB 中，∠BDA＋∠DBA＝90°，故 ∠BDA＝∠EBC。

再结合 ∠DAB＝∠BCE 和 BD＝BE，得到

\[
\triangle DBA\cong\triangle BEC\quad(\mathrm{AAS}),
\]

于是 **AB＝CE，AD＝BC**。注意对应顺序：D↔B、B↔E、A↔C。

**识别顺序：一条直线 → 三个直角 → 等斜边 → 全等后交换对应直角边。** 本章只回顾这一种直角全等型，下面“作双垂”的证明会连续用到它两次。

## 题目区

### 共用构型

如图，△CBC′ 和 △DBD′ 都是以 B 为直角顶点的等腰直角三角形，即

\[
BC=BC',\quad BD=BD',\quad
\angle CBC'=\angle DBD'=90^\circ.
\]

各点方向按图取定：射线 BD、BD′、BC、BC′ 绕 B 依次排列，∠CBD′ 为锐角。因此，从 BC 到 BC′、从 BD 到 BD′ 的 90° 转动方向相同。以下三题共用这一构型，分别作辅助线。

![双等腰共用构型](<assets/diagrams/model.png>)

**题 1 等面积从哪里来**

求证：S△CBD′＝S△C′BD。

入手提示：已经有 BC＝BC′。分别以 BC、BC′ 为底，试着比较两条高。

**题 2 已知中点，证明垂直**

E 是 CD′ 的中点。连接 BE，求证：BE⊥C′D。

入手提示：中点条件能否通过倍长 BE，转化成一组八字形全等？

**题 3 已知垂直，证明中点**

过 B 作 BF⊥C′D，F 为垂足；直线 BF 与 CD′ 相交于 E。求证：CE＝ED′。

入手提示：此时还不知道 E 是中点。分别从 C、D′ 向直线 BF 作垂线，看看会出现几组一线三等角。

## 集中解析

### 题 1 解析

**怎么想**

两个三角形不一定全等，等面积也不必比较三边。先用已知的 BC＝BC′ 作等底，再把问题转成等高。

**解**

过 D′ 作 D′M⊥BC，M 为垂足；过 D 作 DN⊥BC′，N 为垂足。本图中 M 在射线 BC 上，N 在 C′B 向 B 外的延长线上。

![题 1：作高比较面积](<assets/diagrams/area.png>)

由两个公共顶角都是直角，按图有

\[
\angle CBD'=180^\circ-\angle C'BD.
\]

由于 BM 与 BC 同向、BN 与 BC′ 反向，

\[
\angle MBD'=\angle CBD',\qquad
\angle NBD=180^\circ-\angle C'BD,
\]

所以 ∠MBD′＝∠NBD。结合 ∠BMD′＝∠BND＝90°、BD′＝BD，得到

\[
\triangle BMD'\cong\triangle BND\quad(\mathrm{AAS}),
\qquad D'M=DN.
\]

从而

\[
S_{\triangle CBD'}=\frac12 BC\cdot D'M
=\frac12 BC'\cdot DN=S_{\triangle C'BD}.
\]

**方法点睛**：等面积先找等底；高不现成，就作垂线，把等高交给直角三角形全等。

### 题 2 解析

**怎么想**

E 是 CD′ 的中点，但原图中这个等长条件还不能和 BC＝BC′、BD＝BD′ 放进同一组全等。倍长 BE，把 BD′ 搬到 C 处，再比较一个大三角形。

**解**

延长 BE 到 G，使 EG＝EB，连接 CG。于是 B、E、G 共线，CE＝ED′，∠CEG＝∠D′EB。

![题 2：倍长中线](<assets/diagrams/midpoint.png>)

**第一步：用八字形全等搬运一条边。**

\[
\triangle CEG\cong\triangle D'EB\quad(\mathrm{SAS}).
\]

因此 CG＝D′B＝DB，且 ∠ECG＝∠ED′B，故 CG∥BD′。按图，射线 CG 与 BD′ 同向。

**第二步：把两组等腰条件放进同一组大三角形。**

由于 CB 与 BC 反向，CG 与 BD′ 同向，

\[
\angle GCB=180^\circ-\angle CBD'=\angle DBC'.
\]

结合 CG＝DB、CB＝BC′，得到

\[
\triangle GCB\cong\triangle DBC'\quad(\mathrm{SAS}).
\]

于是 ∠GBC＝∠DC′B。

**第三步：用对应角推出垂直。**

延长 EB 过 B，与 C′D 相交于 H。按图，BH、BG 是反向射线，∠CBC′＝90°，所以

\[
\angle C'BH+\angle GBC=90^\circ.
\]

又因 H 在 C′D 上，∠BC′H＝∠DC′B＝∠GBC。在 △BC′H 中，B、C′ 两个角之和为 90°，故 ∠BHC′＝90°，即 BE⊥C′D。

**顺手得到的长度关系。**

第二次全等还给出 GB＝DC′。因为 GB＝2BE，故

\[
\boxed{2BE=C'D}.
\]

**方法点睛**：倍长中线先搬运等长边，再用大三角形全等同时取得角度与长度关系。

### 题 3 解析

**怎么想**

这一题和题 2 的已知、结论交换了位置。现在 CE＝ED′ 还是待证，不能把它放进倍长后的全等条件。题目给出了垂直，便从 C、D′ 向 BF 作双垂，连续用两次章首模型。

**解**

过 C 作 CM⊥BF，过 D′ 作 D′N⊥BF，M、N 为垂足。本题的 M、N 与题 1 的垂足不同。

![题 3：作双垂，连续两次一线三等角](<assets/diagrams/converse.png>)

**第一步：用 BC＝BC′，得到 CM＝BF。**

M、B、F 共线，∠CMB＝∠CBC′＝∠BFC′＝90°。由直线上的角和，

\[
\angle CBM+\angle C'BF=90^\circ.
\]

而在 Rt△C′BF 中，∠BC′F＋∠C′BF＝90°，故 ∠CBM＝∠BC′F。再结合 BC＝BC′，得到

\[
\triangle BCM\cong\triangle C'BF\quad(\mathrm{AAS}),
\qquad CM=BF.
\]

这正是章首的一线三等角：等斜边推出对应直角边相等。

**第二步：用 BD′＝BD，得到 D′N＝BF。**

N、B、F 共线，∠D′NB＝∠D′BD＝∠BFD＝90°。同样，

\[
\angle D'BN+\angle DBF=90^\circ,
\qquad \angle BDF+\angle DBF=90^\circ,
\]

所以 ∠D′BN＝∠BDF。结合 BD′＝BD，得到

\[
\triangle BD'N\cong\triangle DBF\quad(\mathrm{AAS}),
\qquad D'N=BF.
\]

于是 CM＝D′N。

**第三步：接上八字形全等，得到中点。**

按图，C、E、D′ 共线，M、E、N 共线，∠CME＝∠D′NE＝90°，∠CEM＝∠D′EN。结合 CM＝D′N，得到

\[
\triangle CME\cong\triangle D'NE\quad(\mathrm{AAS}),
\qquad CE=ED'.
\]

所以 E 是 CD′ 的中点。若 M、N 恰好都与 E 重合，则 CM＝D′N 直接给出 CE＝ED′，不再使用退化三角形的全等。

**方法点睛**：要从垂直证明中点，先用双垂把同一条 BF 搬到两侧，再用八字形全等收尾。

## 模型总结与迁移

### 三个条件，三条路线

| 已知／目标 | 辅助线 | 真正起作用的关系 |
| --- | --- | --- |
| 两等腰直角，证明等面积 | 以等长边作底，分别作高 | 等底＋直角三角形全等得到等高 |
| E 是 CD′ 的中点，证明 BE⊥C′D | 倍长 BE | 八字形全等搬运边，再比较大三角形 |
| BE⊥C′D，证明 E 是 CD′ 的中点 | 从 C、D′ 向 BE 作双垂 | 两次一线三等角，再接八字形全等 |

在本章构型下，可以把题 2、题 3 合起来记：

\[
E\in CD':\qquad CE=ED'\ \Longleftrightarrow\ BE\perp C'D.
\]

题 2 还告诉我们：当 E 是 CD′ 的中点时，**BE 既垂直于 C′D，又等于 C′D 的一半**。

### 再看一次等面积

题 3 的两组全等给出 CM＝D′N＝BF。以 BE 为底，△CBE 和 △D′BE 的高都是 BF，所以

\[
S_{\triangle CBD'}=S_{\triangle CBE}+S_{\triangle D'BE}
=BE\cdot BF.
\]

而题 2 已经得到 2BE＝C′D，故

\[
S_{\triangle CBD'}=\frac12 C'D\cdot BF=S_{\triangle C'BD}.
\]

这给出等面积的另一种看法：倍长中线得到的长度关系，和双垂得到的高度关系，最终在面积公式里相遇。

### 易错提醒

1. 两个等腰直角三角形的方向要按图取定。只记两组等长和两个直角，不看方位，不能直接套用本章结论。
2. 高是到**直线**的距离，垂足可能在边的延长线上；题 1 的 N 就在 BC′ 的延长线上。
3. 题 3 中的中点是结论，不能预先使用 CE＝ED′ 来证明全等。
4. “两块面积始终相等”不表示“每块面积是一个固定值”；构型变化时，两块面积可以一起变化。
5. 三题分别作图。题 1、题 3 的 M、N 含义不同；题 2 的 G 是倍长点，H 是交点。
