# MP2984 应用公式与布局疑点：联网交叉查证

查证日期：2026-11-11。范围：原文第35、37、38、39页。未改动忠实译稿；下述推断不是MPS发布的勘误。

## 来源与版本

- [MPS 当前公开 MP2984 数据手册](https://www.monolithicpower.com/en/documentview/productdocument/index/version/2/document_type/Datasheet/lang/en/sku/MP2984GR/document_id/11081/)：打开后仍为43页、Rev.1.0、2021-12-09。URL中的`version/2`不代表手册Rev.2.0。
- [MPS 当前公开 MP2980 数据手册](https://www.monolithicpower.com/en/documentview/productdocument/index/version/2/document_type/Datasheet/lang/en/sku/MP2980GR/)：45页、Rev.1.0、2023-11-09。同族资料只能交叉核对文档写法，不能替代MP2984芯片行为的直接证据。
- [TI LM5121 官方数据手册](https://www.ti.com/lit/ds/symlink/lm5121.pdf)：SNVS963C，2016-06修订；第27页表1用于独立核查电流模式Boost的小信号结构，不把该器件参数套给MP2984。
- [MPS MPQ3432GLE-AEC1 官方手册](https://www.monolithicpower.com/en/documentview/productdocument/index/version/2/document_type/Datasheet/lang/en/sku/MPQ3432GLE-AEC1/)的输出电容说明，以及[TI SLVA061](https://www.ti.com/lit/an/slva061/slva061.pdf)的Boost功率级分析，作为输出侧脉冲电流的一般拓扑依据。

## 逐项结论

| MP2984位置与疑点 | 可核实的交叉证据 | 结论及边界 |
|---|---|---|
| 第35页式（7）（8）把电感量写成`IL_BUCK/IL_BOOST` | MP2980第37页同型式（8）（9）明确使用`LBUCK/LBOOST`。 | **高可信符号笔误**。该式给出的量纲为H，不是A；建议阅读为降压/升压所需电感量。未找到针对MP2984的独立官方勘误。 |
| 第35页把`IOUT`称作不连续的输出电压 | MP2980第37页只称`IOUT`不连续；MPS MPQ3432GLE-AEC1输出电容段明确称输出电流不连续。TI SLVA061第1页说明Boost输出整流支路是脉冲电流，电容在其关断期间供给负载。 | **高可信名词笔误**，应理解为送往输出滤波端的电流脉动/不连续，不能据此说电容两端输出电压跳变中断。这里也不表示负载电流必然不连续。 |
| 第37页补偿电容`C10`与图14/式（28）的`C12`冲突 | 本手册第40页典型电路中C10是AVDD去耦，C12在COMP补偿支路；MP2980第40页同类说明使用C12。 | **高可信位号笔误：该段应指C12**。这是图、式、接法三者一致支持的文档判断，不是器件实测。 |
| 第38页称`FP3`是EA输出电阻极点，但式（29）只含`COUT·RLOAD` | MP2980第40页分别说明：补偿电容与EA输出电阻形成FP2，COUT与负载形成FP3。 | **高可信极点名称错置**。式（28）对应EA输出节点，式（29）对应输出RC节点；这只厘清名称，没有验证原稿近似环路模型的完整性。 |
| 第38页Boost直流环路增益式（31）额外乘`R13` | MP2980第40页式（32）、[MPQ4210官方手册式（32）](https://www.monolithicpower.com/en/documentview/productdocument/index/version/2/document_type/Datasheet/lang/EN/sku/MPQ4210)、[MPQ4214-AEC1 Rev.1.2第30页式（30）](https://www.monolithicpower.com/en/documentview/productdocument/index/version/2/document_type/Datasheet/lang/en/sku/MPQ4214GU-AEC1/)均重复这个因子；TI LM5121第27页Boost调制器直流增益不含外部补偿电阻。 | **按该手册所给参数定义，公式量纲不自洽；高可信公式疑点，具体正式修订仍未解决**。多个同族手册重复同式可能是共享模板传播，不能算多份独立正确性验证。候选解释见下文。 |
| 第39页第8/15条出现`R4`，图和其他文字用`RSENSE1` | 本页第8条下一句已改用RSENSE2/RSENSE1；图15标注RSENSE1；MP2980第41页Kelvin布线第9/10条对应RSENS1/RSENSE2。 | **高可信旧位号残留**。逐周期检测应针对原理图中CSP/CSN所跨的开关电流采样电阻RSENSE1；不能因字面R4另找一个无关电阻。 |

上述同族对照由MP2980第37、39–41页提供，尤其C12与输出RC极点归属写得更清楚。[MP2980官方手册](https://www.monolithicpower.com/en/documentview/productdocument/index/version/2/document_type/Datasheet/lang/en/sku/MP2980GR/)

## 式（31）：为什么不能只说“删掉R13就对了”

以下为本次独立分析，模型假设是低频、理想连续导通Boost、输入电压固定、阻性负载、忽略损耗及内电流环动态。它说明一种自洽的近似形式，不能替代MPS验证的完整传递函数。

本手册把EA电压增益定义为约300 V/V，把COMP至采样电压的增益定义为约0.2 V/V。二者均无量纲。原式其余因子`VIN·VFB/VOUT²`及`RLOAD/RSENSE1`也无量纲；因此再乘实际电阻R13（Ω），结果会带Ω，与“电压环路增益”不一致。用Ω或kΩ代入会改变1000倍，也表明不能把位号当作无单位的纯数。

从功率平衡出发：

\[
V_{IN} I_{IN}=\frac{V_{OUT}^2}{R_{LOAD}},\qquad
\frac{\partial V_{OUT}}{\partial I_{IN}}=
\frac{V_{IN}R_{LOAD}}{2V_{OUT}}.
\]

若内电流控制在该近似下满足

\[
\frac{\partial I_{IN}}{\partial V_{COMP}}\approx
\frac{G_{CS}}{R_{SENSE1}},\qquad
\beta=\frac{V_{FB}}{V_{OUT}},
\]

则环路直流增益候选式为

\[
A_{VDC}\approx
A_{EA}\frac{G_{CS}}{R_{SENSE1}}
\frac{V_{IN}R_{LOAD}}{2V_{OUT}}
\frac{V_{FB}}{V_{OUT}}.
\]

这恰是原式除去R13后的形式。在TI LM5121的独立模型中，调制器直流增益含`D'/2`和电流检测通路增益、负载/检测电阻比，也与这一结构吻合；该比较不意味着MP2984的采样、斜坡、限流及高频模型等同于LM5121。[TI LM5121，第27页表1](https://www.ti.com/lit/ds/symlink/lm5121.pdf)

还存在另一种可能的文档混淆：在Type II补偿器的中频平台，EA有效增益可近似为`g_m·R13`。若某个推导原本使用跨导`g_m`（A/V），乘R13能恢复无量纲；但这与手册明写的300 V/V电压增益、以及“直流增益”的名称不是同一个量。不能一边保留300 V/V，一边再乘R13，也不能未经厂家确认就把`A_EA`静默换成跨导。

从补偿网络本身看，直流时C12、C14为开路，R13支路不决定直流输出电阻；有限的EA输出电阻`R_o`决定EA直流增益。以本手册定义作一致性检查，`R_o≈A_EA/g_m≈300/0.00122≈246 kΩ`，于是`FP2≈1/(2πR_oC12)`，正好与式（28）结构对应。R13主要设置补偿零点和中高频增益，而不是与300 V/V再相乘构成直流增益。

因此可说明“已发表式（31）在其自身符号定义下有问题”，但不能宣布找到官方修正版。译文仍应保留原式，另加查证注释；实际设计的带宽/裕度应以经验证模型或环路测量核对。

## 论坛、开源实测和搜索边界

- 已检索MPS中英文技术论坛、EEVblog、Electrical Engineering Stack Exchange、21ic、电源网及立创开源硬件平台中MP2984/MP2980与compensation、R13、C12、R4等组合。没有找到公开帖直接发布上述六项MP2984勘误；这是本次检索结果，不代表全网不存在。
- [MPS官方论坛：MP2980 as buck/boost controller](https://forum.monolithicpower.com/t/mp2980-as-buck-boost-controller/3845)（2024-09-02至2024-09-19）有FAE审查原理图及器件选型回复，但未处理这些补偿公式问题。其末尾把采样电阻所需功率写成12V×30A，不能当作正确的采样电阻损耗计算；采样电阻自身导通损耗应按其电流与电阻计算。官方论坛回复也需与物理关系交叉核对。
- [立创：ROBOCON算力设备供电模块](https://oshwhub.com/jnu_sober/mp2980-_2026)的搜索索引可见作者给出COMP改值前后的动态波形对比，另列C12、R13、C14的选值过程。页面正文打开返回403，故本次没有独立核验原始波形和所有条件，不能用其数值证明某一增益公式正确。
- [另一作者的MP2980模块](https://oshwhub.com/roboticlib/project_tzqcxewf)公开了仪器列表及动态响应测试，并说明沿用典型补偿组合。它是MP2980单板应用经验，不是MP2984勘误，更不是芯片全工况稳定性证明。
- EEVblog定向检索遇robots访问限制，未取得MP2984相关原始讨论正文。本报告没有用无法查看的帖文作为结论依据。

公开资料未提供EV2984-R-00B单独可核验的完整评估板手册/原理图下载，本次主要利用MP2984手册自身的典型电路与布局图进行位号交叉核对；不宣称检查过未取得的板级原文件。
