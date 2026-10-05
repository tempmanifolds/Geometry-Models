# 八字形模型：共斜边、外角平分线与辅助线

署名：Hence

## 关键的八字形

△ABC 与 △DBC 有公共边 BC，连接 AD，AC 与 BD 相交于 O。

![关键的八字形：双色突出两个三角形，标出直角](assets/diagrams/model.png)

由八字形得

\[
\angle BAC+\angle ABD=\angle BDC+\angle ACD.
\]

因此，∠BAC＝∠BDC 与 ∠ABD＝∠ACD 可以相互推出。图中两个顶角为直角时，就能得到 ∠ABD＝∠ACD。

## 例 1 四个条件，知三推一

按图取定方位：A、D 在 BC 的同侧，AC 与 BD 在内部相交。延长 CD 至 X，连接 AD，DA 位于 ∠BDX 内部。有四个条件：

![例 1 的共用构型](assets/diagrams/exterior.png)

| 条件 | 内容 |
| --- | --- |
| ① | AB＝AC |
| ② | ∠BAC＝90° |
| ③ | ∠BDC＝90° |
| ④ | DA 平分 ∠BDX，即 ∠BDA＝∠ADX |

**知道其中任意三个，就能推出剩下的一个。**

### （1）$\text{①②③}\Rightarrow\text{④}$：连接直角顶点，得到外角平分线

已知 AB＝AC，∠BAC＝∠BDC＝90°，说明 DA 平分 ∠BDX。

**怎么想**

两个直角先给出 ∠ABD＝∠ACD。接下来有两个方向：从 A 向 BD、CD 作双垂，把斜边 AB、AC 配成直角三角形；或者围绕 A 补出另一个等腰直角三角形，把上一章的手拉手用起来。

由 ∠BAC＝∠BDC，利用八字形倒角，得

\[
\angle ABD=\angle ACD.
\]

**方法一：从 A 作双垂。**

过 A 作 AM⊥BD，垂足为 M；作 AN⊥CD，垂足为 N。本图中 M 在线段 BD 上，N 在 CD 经过 D 的延长线上。

![从 A 作双垂](assets/diagrams/double-perpendicular.png)

在 Rt△ABM 与 Rt△ACN 中，AB＝AC，∠ABM＝∠ACN，且两垂足处都是直角，故

\[
\triangle ABM\cong\triangle ACN\quad(\mathrm{AAS}),
\qquad AM=AN.
\]

再看 Rt△ADM 与 Rt△ADN：斜边 AD 公共，AM＝AN，所以

\[
\triangle ADM\cong\triangle ADN\quad(\mathrm{HL}).
\]

因此 ∠MDA＝∠NDA，即 ∠BDA＝∠ADX。又因为 ∠BDA＋∠ADX＝90°，所以

\[
\boxed{\angle BDA=\angle ADX=45^\circ.}
\]

**方法二：过 A 添直角，构造手拉手。**

过 A 作 AP⊥AD，交 BD 于 P。

![过 A 补等腰直角三角形](assets/diagrams/hand-lower.png)

由 AB⊥AC、AP⊥AD，按图有 ∠BAP＝∠CAD；又有 ∠ABP＝∠ACD、AB＝AC，故

\[
\triangle ABP\cong\triangle ACD\quad(\mathrm{ASA}),
\qquad AP=AD.
\]

因此 △APD 为等腰直角三角形，∠PDA＝45°。P 在 DB 上，故 ∠BDA＝45°，∠ADX＝90°－45°＝45°。

也可以先在 BD 上取 P，使 BP＝CD。由 ∠ABP＝∠ACD、AB＝AC，先以 SAS 证明同一组全等，得到 AP＝AD、∠BAP＝∠CAD，再推出 AP⊥AD。两种作法落到同一幅图上：一种先添角，另一种先添边。

**方法点睛**：共斜边先倒角，再把“等腰”转成一组全等；外角平分线由等距离或等腰直角三角形得到。

### （2）$\text{①②④}\Rightarrow\text{③}$：已知外角平分线，反推 D 处直角

已知 AB＝AC，∠BAC＝90°，DA 平分 ∠BDX，说明 ∠BDC＝90°。

**怎么想**

这次不能先用两个直角倒角，因为 D 处的直角正是待证结论。∠BDA＝∠ADX 能先制造对称：作双垂得到 AM＝AN，或截取等长边制造 SAS 全等。把对称带来的等长再接上 AB＝AC，便能推出 ∠ABD＝∠ACD。

**方法一：作双垂，先用角平分线。**

沿用例 1（1）的 AM、AN。由 ∠BDA＝∠ADX、公共边 AD 和两个直角，得

\[
\triangle ADM\cong\triangle ADN\quad(\mathrm{AAS}),
\qquad AM=AN.
\]

再结合 AB＝AC，以 HL 得 Rt△ABM≅Rt△ACN，所以 ∠ABD＝∠ACD。由八字形倒角，

\[
\angle BDC=\angle BAC=90^\circ.
\]

**方法二：向上延长 CD，截取 DE＝DB。**

延长 CD 至 E，使 DE＝DB，连接 AE。

![向上延长 CD 构造对称全等](assets/diagrams/extend-cd.png)

由 ∠BDA＝∠ADE、公共边 AD、DB＝DE，得

\[
\triangle ADB\cong\triangle ADE\quad(\mathrm{SAS}).
\]

所以 AB＝AE，∠ABD＝∠AED。又因为 AB＝AC，所以 AE＝AC，即 ∠AEC＝∠ACE。因此 ∠AEC＝∠ACE＝∠ABD。

最后八字形得 ∠BDC＝90°。

**方法三：向右延长 BD，截取 DF＝DC。**

延长 BD 至 F，使 DF＝DC，连接 AF。

![向右延长 BD 构造对称全等](assets/diagrams/extend-bd.png)

\[
\angle ADF=180^\circ-\angle BDA,
\qquad \angle ADC=180^\circ-\angle ADX.
\]

等角的补角相等，所以 ∠ADF＝∠ADC。结合 AD 公共、DF＝DC，得

\[
\triangle ADF\cong\triangle ADC\quad(\mathrm{SAS}),
\qquad AF=AC,
\quad \angle AFD=\angle ACD.
\]

故 AB＝AC＝AF，从而 ∠ABD＝∠AFD＝∠ACD。最后八字形得 ∠BDC＝90°。

**方法点睛**：已知角平分线，可以先围绕它制造全等或者等腰。

### （3）$\text{②③④}\Rightarrow\text{①}$：保留两个直角，反推等腰

已知 ∠BAC＝∠BDC＝90°，DA 平分 ∠BDX，说明 AB＝AC。

**怎么想**

两个直角给 ∠ABD＝∠ACD；外角平分线给 AM＝AN。这一次 AB＝AC 是待证结论，全等不能再用 HL。已有两个角和一条直角边，可以改用 AAS。

由 ∠BAC＝∠BDC＝90°，八字形倒角得 ∠ABD＝∠ACD。

从 A 向 BD、CD 作双垂，记垂足为 M、N。由 ∠BDA＝∠ADX，得 Rt△ADM≅Rt△ADN，从而 AM＝AN。

再由 ∠ABM＝∠ACN、两个直角、AM＝AN，得

\[
\triangle ABM\cong\triangle ACN\quad(\mathrm{AAS}),
\qquad AB=AC.
\]

**另外两种对称全等的写法。**

- 按（2）方法二作 E，得到 AB＝AE、∠ABD＝∠AED。由 ∠ABD＝∠ACD，得 ∠AEC＝∠ACE，所以 AE＝AC，进而 AB＝AC。
- 按（2）方法三作 F，得到 AF＝AC、∠AFD＝∠ACD。由 ∠ABD＝∠ACD，得 ∠AFB＝∠ABF，所以 AB＝AF，进而 AB＝AC。

**方法点睛**：条件与结论交换后，要重新选择全等判定；等边待证时，用等角和等距离搭桥。

### （4）$\text{①③④}\Rightarrow\text{②}$：保留等边，反推 A 处直角

已知 AB＝AC，∠BDC＝90°，DA 平分 ∠BDX，说明 ∠BAC＝90°。

从 A 向 BD、CD 作双垂，垂足分别为 M、N。由 ∠BDA＝∠ADX、AD 公共和两个直角，得 Rt△ADM≅Rt△ADN，所以 AM＝AN。

又 AB＝AC，故

\[
\triangle ABM\cong\triangle ACN\quad(\mathrm{HL}),
\qquad \angle ABD=\angle ACD.
\]

由八字形倒角，得

\[
\angle BAC=\angle BDC=90^\circ.
\]

也可以照例 1（2）的两种延长作法：先由对称全等和 AB＝AC 得到 ∠ABD＝∠ACD，再把已知的 ∠BDC＝90° 换回 ∠BAC＝90°。

**方法点睛**：先清点已知条件；通过等距离与等斜边得到等角，再把直角搬回另一顶点。

### 单角变式：把④换成 45° 或 135°

#### 变式一：只给 ∠BDA＝45°

已知 AB＝AC，∠BAC＝90°，∠BDA＝45°，说明 ∠BDC＝90°。

**怎么想**

只给 ∠BDA＝45°，还没有给 ∠ADX。此时“到角两边距离相等”不能直接用。应让这个 45° 和新作的直角出现在同一个三角形里，先得到等腰直角三角形，再用手拉手；另一条路是把 B、C 向 AD 作双垂，用 K 型全等搬运两条直角边。

**方法一：过 A 作 AP⊥AD，交 BD 于 P。**

![过 A 作 AP⊥AD，交 BD 于 P](assets/diagrams/hand-lower.png)

由于 ∠ADP＝45°、∠PAD＝90°，△APD 是等腰直角三角形，故 AP＝AD。

由 AB＝AC、AP＝AD、∠BAP＝∠CAD，得

\[
\triangle ABP\cong\triangle ACD\quad(\mathrm{SAS}).
\]

所以 ∠ABP＝∠ACD，即 ∠ABD＝∠ACD。由八字形倒角，∠BDC＝∠BAC＝90°。

与例 1（1）对照：那里先全等，再证明 AP＝AD；这里先由 45° 得 AP＝AD，再全等。辅助线相同，证明顺序由已知条件决定。

**方法二：从 B、C 向 AD 作双垂。**

过 B 作 BM⊥AD，过 C 作 CN⊥AD，垂足分别为 M、N。构造一线三等角。

![从 B、C 向 AD 作双垂：K 型全等](assets/diagrams/k-perpendicular.png)

在 Rt△ABM 与 Rt△CAN 中，∠BAM＝∠ACN，AB＝CA，所以

\[
\triangle ABM\cong\triangle CAN\quad(\mathrm{AAS}),
\qquad BM=AN,\quad AM=CN.
\]

由于 ∠BDM＝45°，Rt△BMD 为等腰直角三角形，所以 BM＝DM。于是

\[
AN=DM=AM+AD,
\qquad DN=AN-AD=AM=CN.
\]

故 Rt△CDN 也是等腰直角三角形，∠CDN＝45°。又 ∠BDA＝45°，故 ∠BDC＝180°－45°－45°＝90°。

**方法点睛**：只给单个 45° 时，先补等腰直角三角形；用一线三等角时，等长常藏在“加减公共部分”中。

#### 变式二：换成 ∠ADC＝135°

已知 AB＝AC，∠BAC＝90°，∠ADC＝135°，说明 ∠BDC＝90°。

**怎么想**

∠ADC＝135° 等价于 ∠ADX＝45°。与变式一对照，现在方便补出的是 AD 与 CD 延长线之间的等腰直角三角形。K 型全等也仍可用，只是先得到等腰直角的变成了 △CDN。

**方法一：向上补等腰直角三角形。**

过 A 作 AQ⊥AD，交 CD 经过 D 的延长线于 Q。

![过 A 向上补等腰直角三角形](assets/diagrams/hand-upper.png)

由 ∠ADQ＝180°－135°＝45°，得 AQ＝AD。又 AB＝AC，且由两对垂直关系，按图有 ∠BAD＝∠CAQ，故

\[
\triangle ABD\cong\triangle ACQ\quad(\mathrm{SAS}).
\]

所以 ∠ABD＝∠ACQ＝∠ACD。再倒角得 ∠BDC＝90°。

**方法二：从 B、C 向 AD 作双垂。**

沿用变式一的 K 型图，由 Rt△ABM≅Rt△CAN，有 BM＝AN、AM＝CN。

因为 ∠CDN＝180°－∠CDA＝45°，所以 Rt△CDN 为等腰直角三角形，CN＝DN。于是

\[
AM=DN,
\qquad DM=AM+AD=DN+AD=AN=BM.
\]

故 Rt△BMD 为等腰直角三角形，∠BDA＝45°。已知 ∠ADX＝45°，所以 ∠BDC＝90°。

**方法点睛**：135° 先看邻补角；与 45° 变式比较，交换的是先出现的等腰直角三角形。

## 例 2 角平分线上的二倍关系

如图，在 △ABC 中，∠A＝90°，AB＝AC。BD 平分 ∠ABC，交 AC 于 D。过 C 作 CE⊥BD，交 BD 的延长线于 E。求证：BD＝2CE。

![例 2 原题重绘](assets/diagrams/example.png)

**怎么想**

∠ABC＝∠ACB＝45°，而 BD 平分 ∠ABC，所以 ∠ABD＝∠DBC＝22.5°。目标 BD＝2CE 可以分别拆成四条路线：

1. 延长相交：把 BD 换成一条整段 CF，再用 E 是 CF 的中点。
2. 平行补形：找到 BD 的中点 G，证明 DG＝CE。
3. 手拉手补形：找到 BD 的中点 F，证明 BF＝CE。
4. 补短：先把 CE 补成整段 CF，再证明 CF＝BD。

下面各方法中的 F、G 都独立作出。

**方法一：延长 BA，与 CE 的延长线相交。**

延长 BA、CE，交于 F。

![例 2 方法一：延长相交](assets/diagrams/example-extend.png)

由于 AB⊥AC、BD⊥CF，按图有 ∠ABD＝∠ACF。又 ∠BAD＝∠CAF＝90°、AB＝AC，故

\[
\triangle ABD\cong\triangle ACF\quad(\mathrm{ASA}),
\qquad BD=CF.
\]

在 △BFC 中，∠FBC＝45°，∠FCB＝90°－22.5°＝67.5°，所以 ∠BFC＝67.5°，从而 BF＝BC。

因为 BE⊥FC，在等腰三角形 BFC 中，底边上的高也是中线，故 FE＝EC，CF＝2CE。因此 BD＝2CE。

**方法二：过 D 作平行线，把二倍关系拆成两半。**

过 D 作 DF∥AB，交 BC 于 F；过 F 作 FG⊥BD，垂足为 G。

![例 2 方法二：平行线与垂线](assets/diagrams/example-parallel.png)

由 DF∥AB、BD 平分 ∠ABC，得 ∠DBF＝∠BDF＝22.5°，所以 BF＝DF。

又 DF⊥DC，∠DCF＝∠ACB＝45°，故 △DCF 是等腰直角三角形，DF＝DC。

在 Rt△BFG 与 Rt△DFG 中，BF＝DF，FG 公共，故两三角形全等，BG＝DG。因此 BD＝2DG。

由于 DF⊥DC、DG⊥CE，按图有 ∠FDG＝∠DCE。结合两个直角、DF＝DC，得

\[
\triangle DFG\cong\triangle CDE\quad(\mathrm{AAS}),
\qquad DG=CE.
\]

故 BD＝2DG＝2CE。

**方法三：在 A 处添直角，补出手拉手。**

过 A 作 AF⊥AE，交 BD 于 F。

![例 2 方法三：共顶点补形](assets/diagrams/example-hand.png)

由 AB⊥AC、AF⊥AE，按图有 ∠BAF＝∠CAE。又 ∠ABF＝22.5°，由 AC⊥AB、CE⊥BD，得 ∠ACE＝22.5°。结合 AB＝AC，有

\[
\triangle ABF\cong\triangle ACE\quad(\mathrm{ASA}),
\qquad AF=AE,\quad BF=CE.
\]

所以 △AFE 是等腰直角三角形，∠AFE＝45°。同时 ∠BAF＝∠CAE＝22.5°，因此在 △ABF 中，AF＝BF。

F、D、E 依次共线，所以 ∠AFD＝45°；又 ∠FAD＝90°－22.5°＝67.5°，故 ∠ADF＝67.5°，从而 FD＝AF。

因此 BF＝AF＝FD，F 是 BD 的中点。于是 BD＝2BF＝2CE。

**方法四：先补短，把 CE 倍长。**

延长 CE 至 F，使 EF＝EC，连接 BF。

![例 2 方法四：补短与对称](assets/diagrams/example-reflect.png)

因为 BE⊥CF、CE＝EF、BE 公共，

\[
\triangle BEC\cong\triangle BEF\quad(\mathrm{SAS}).
\]

所以 ∠EBF＝∠EBC＝22.5°。F、C 在 BE 的两侧，故 ∠CBF＝45°＝∠CBA，即 B、A、F 共线，且 F 在 BA 经过 A 的延长线上。

再由 AB＝AC、∠BAD＝∠CAF＝90°、∠ABD＝∠ACF，得 △ABD≅△ACF（ASA），所以 BD＝CF。

又 CF＝CE＋EF＝2CE，故 BD＝2CE。

方法一和方法四最终落到同一个辅助点 F：方法一先通过相交找到它，再证明 CE＝EF；方法四先由 CE＝EF 作出它，再证明 B、A、F 共线。作图顺序不同，关键构型相同。

**方法点睛**：看到“二倍”，先决定是倍长短段，还是平分长段；再用全等把整段或半段换到目标线段上。

## 辅助线总结

| 看见的条件或目标 | 可以先作的线 | 希望得到什么 |
| --- | --- | --- |
| 已知外角平分线 | 从 A 向 BD、CD 作双垂 | 到角两边的距离相等 |
| 外角相等，想造对称全等 | 延长 CD，取 DE＝DB；或延长 BD，取 DF＝DC | SAS 全等，再借等腰换角 |
| 单个 45° 或 135° | 过 A 作 AD 的垂线，交相应边或延长线 | 等腰直角三角形，接手拉手 |
| 等腰直角 ABC，需搬运长度 | 从 B、C 向 AD 作双垂 | K 型全等，直角边交叉对应 |
| 目标为二倍关系 | 倍长短段，或给长段找中点 | 将二倍关系转为整段相等或半段相等 |
| 例 2 的角平分线 | 平行线补等腰；垂线取中点 | 把角平分线条件转成中点与等长 |

两种“双垂”要分清：**A 向 BD、CD 作双垂，是利用角平分线的等距离；B、C 向 AD 作双垂，是利用等腰直角 ABC 的 K 型全等。** 它们的出发点和全等对应顺序都不同。

### 使用时注意

1. DA 平分的是 ∠BDX，参与比较的两个角是 ∠BDA 与 ∠ADX。
2. 条件与结论交换后，重新检查全等判定。等边待证时不能用它作 HL 条件；直角待证时不能提前用手拉手。
3. K 型全等推出的是 BM＝AN、AM＝CN。写完对应边后，再按点的顺序加减公共部分，不能把同一条垂线上的两段凭图认成相等。
