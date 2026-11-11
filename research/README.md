# MP2984 原文疑点联网查证

日期：2026-11-11。核查对象为用户提供的MP2984 Rev.1.0（2021-12-09）43页手册。

**译文与查证分开：本轮不修改LaTeX正文、公式或PDF。原文的错误、矛盾和不规范写法仍按原文翻译。以下解释仅供对照阅读，不是MPS发布的勘误，也不替代该型号的正式规格。**

## 先说明两点

1. 目前从MPS产品页进入的公开手册仍为Rev.1.0（2021-12-09）。网址中的`version/2`不是手册Rev.2，也不能将搜索结果的抓取时间当修订日期。[MP2984官方手册][m4]
2. 先前将“VREF+0.6V”直接判为误译、将固定0.6V当成确定解释，证据不足，现撤回这一复核定论。MP2984原句有歧义，MP2980同族手册明确写参考电压之上0.6V；后者是旁证，不能直接移成MP2984规格。忠实译稿不据此改写。[软启动查证](soft-start-findings.md)，[MP2980官方手册][m0]

## 逐项结果

“高可信笔误”表示同册其他位置、量纲或电路关系有一致支持，不表示收到厂商针对该句的正式确认。“未定”表示仍缺MP2984本型号直接澄清或实测。

| 原文页 | 疑点 | 查证结果与边界 | 详细证据 |
|---|---|---|---|
| 5 | ILIM“两种电平”后列四档 | 高可信文字笔误；同页已列四档，同族说明也列四档。 | [前部第1项](front-findings.md) |
| 7 | VREF典型值与误差共用单位栏 | 主要是表格混合表达问题：典型栏为电压，最小/最大栏为相对误差；不能把典型值按百分比读。 | [前部第2项](front-findings.md) |
| 8 | 同一条件列有IAVGN=5V、20V | 可能表示两个共模测试点，证据不足以指定哪一个变量写错；不擅改为IAVGP。 | [前部第3项](front-findings.md) |
| 9 | 注8启动电压“6”缺单位 | 可由同册推荐工作条件及官方产品页确认指6V。 | [前部第4项](front-findings.md) |
| 24 | SWB导通后电感电流“上升” | 在图示正向降压续流阶段，电感电压约为−VOUT，电流斜率为负；高可信方向词笔误。 | [前部第5项](front-findings.md) |
| 25 | SS钳位写成0.6V>VREF | 有歧义；同族资料较支持VREF+0.6V，不能证明MP2984保证值。此前固定0.6V定论撤回。 | [软启动](soft-start-findings.md) |
| 25 | PFM被展开为pulse-width modulation | 缩写与展开不符，较新同族资料使用pulse-frequency modulation。 | [前部第6项](front-findings.md) |
| 26 | 随负载变化的输入电流记作ILIMIT | 高可信符号误用，但无法唯一确定应改成IIN还是IL。 | [前部第7项](front-findings.md) |
| 27 | OVP将VOUT与127%VREF直接比较 | 同册比较节点为FB，需考虑反馈分压；变量名高度可信有误。 | [寄存器R1](register-findings.md) |
| 28 | IMON增益单位18.8mV/V | 同册参数表、式（4）和曲线支持18.8V/V；高可信单位笔误。 | [前部第8项](front-findings.md) |
| 28 | ILIM/FS启动锁存说明例外句自相重复 | 启动后电平变化不改变已锁存默认值这一原则清楚；重新采样所需的具体复位边界仍不宜猜定。 | [寄存器R9](register-findings.md) |
| 28、31 | GO_BIT及20ms放电先后不一致 | “GO_BIT清零后继续20ms放电”有较强同族旁证；MP2984仍未获针对性澄清。不能把20ms无条件当整个斜坡时长。 | [寄存器R2](register-findings.md) |
| 31 | VREF_L重复、DISCHRG拼写 | 可由同册寄存器映射判定文字错误；应涉及高低两组参考值，正式位名为DISCHG。 | [寄存器R3](register-findings.md) |
| 32 | FSW频率档称为slew rate | kHz档位是开关频率；与控制电压变化率的SR位不同，属术语笔误。 | [寄存器R4](register-findings.md) |
| 26、32 | OCP_MODE=10自动恢复还是锁断 | 高可信推定对应锁断；MP2984具体哪些操作能清除锁断仍未定。 | [寄存器R5](register-findings.md) |
| 33 | OVP状态说明混入限流条件 | 尾句高度疑似复制编辑错误；不能由此推导电流参与OVP判定的新逻辑。 | [寄存器R6](register-findings.md) |
| 34 | PNG正常范围写成固定0.5–28V | 混淆可设输出范围和相对设定值的PG窗口；同册电气特性给出相对阈值和迟滞。 | [寄存器R7](register-findings.md) |
| 34 | INT被称作input | 同册明确INT为开漏输出，方向术语可判为笔误。 | [寄存器R8](register-findings.md) |
| 35 | 电感量使用IL_BUCK/IL_BOOST | 公式量纲为H，同族写LBUCK/LBOOST；高可信符号问题。 | [应用与公式](model-findings.md) |
| 35 | IOUT被称为不连续输出电压 | 高可信名词笔误；Boost送往输出滤波端的电流不连续，不代表电容两端电压中断。 | [应用与公式](model-findings.md) |
| 37–38 | C10/C12及极点归属文字冲突 | 图、典型电路、式及同族说明支持C12；FP3由COUT与负载形成，原说明名称有误。 | [应用与公式](model-findings.md) |
| 38 | 式（31）额外乘R13 | 按手册所定义的EA电压增益，量纲不自洽。独立推导和TI模型支持不含该因子的候选形式；仍非官方修正版。 | [推导与其他可能解释](model-findings.md) |
| 39 | R4与RSENSE1混用 | 图与上下文支持旧位号残留，逐周期检测电阻实际标作RSENSE1。 | [应用与公式](model-findings.md) |

同族手册和多个MPS手册可能共享文本模板，重复同一公式或句子不算多份独立正确性证明。式（31）的量纲检查还对照了[TI LM5121第27页表1](https://www.ti.com/lit/ds/symlink/lm5121.pdf)，并明确列出了理想CCM、低频等推导假设。

## 论坛查了哪些，能说明什么

- [MPS中文论坛：MP2984电源开关频率异常、空载功耗高的问题](https://forum.monolithicpower.cn/t/topic/7412)：读取了6帖公开讨论。存在用户实测与排查建议，但没有针对本报告这些条目的正式勘误或明确结案，不能将某种故障原因当成已经确认。
- [MPS英文论坛：MP2980 Demo board Question](https://forum.monolithicpower.com/t/mp2980-demo-board-question/3637)：有用户Arduino代码和GUI使用回复。程序同时改变多个控制位，作者未隔离各位作用，不能用于证明GO_BIT时序。
- [MPS英文论坛：MP28167 and MP2980/MP2984 solution without I2C bus](https://forum.monolithicpower.com/t/mp28167-and-mp2980-mp2984-solution-without-i2c-bus/3815)：后续主要回答MP28167A问题，没有解决MP2984这些保护逻辑歧义。
- [MPS英文论坛：MP2980 as buck/boost controller](https://forum.monolithicpower.com/t/mp2980-as-buck-boost-controller/3845)：有选型与原理图审查，但未给出补偿公式勘误；其中个别说法还需按电路物理关系核对。
- 还定向检索了21ic、电子发烧友、电源网、EEVblog、Electrical Engineering Stack Exchange与立创开源硬件平台。没有取得能直接解决这些MP2984疑点的第三方逐项勘误。部分页面受robots或403限制；未查看的正文没有被当作证据。检索无结果不等于全网不存在。

## 处理方式

本轮仅增加独立查证记录，并纠正先前复核说明中过早下定论的部分；忠实译稿的TeX、公式和PDF均不变。原文所述内容与外部较可信解释应分别阅读。未发布论坛提问、未联系厂商、未进行硬件测试或仿真。

[m4]: https://www.monolithicpower.com/en/documentview/productdocument/index/version/2/document_type/Datasheet/lang/en/sku/MP2984GR/document_id/11081/
[m0]: https://www.monolithicpower.com/en/documentview/productdocument/index/version/2/document_type/Datasheet/lang/en/sku/MP2980GR/

