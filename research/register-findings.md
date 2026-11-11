# MP2984 寄存器与保护逻辑疑点：联网查证

查证日期：2026-11-11。对象为用户提供的 MP2984 Rev. 1.0（2021-12-09）；以下结论是资料交叉分析，不是制造商勘误，也不等同于本芯片实测。

## 来源与证据边界

- **M4：MP2984 官方数据手册**，Rev. 1.0，2021-12-09，43页。[官方PDF](https://www.monolithicpower.com/en/documentview/productdocument/index/version/2/document_type/Datasheet/lang/en/sku/MP2984GR/document_id/11081/)。本轮在线打开仍显示这一版本，相关疑点仍在；未找到公开的较新修订或专门勘误。搜索引擎所列“数月前发布”不是手册修订日期。
- **M0：MP2980 官方数据手册**，Rev. 1.0，2023-11-09，45页。[官方PDF](https://www.monolithicpower.com/en/documentview/productdocument/index/version/2/document_type/Datasheet/lang/en/sku/MP2980GR/)。这是另一型号，只用于同族设计及措辞的旁证；不能把其所有默认值、引脚或功能直接移给 MP2984。
- **F1：MPS 英文官方论坛，MP2980 Demo board Question**，用户代码发表于2024-06-23，MPSNow_Yu回复发表于2024-07-02。[原帖](https://forum.monolithicpower.com/t/mp2980-demo-board-question/3637)。官方回复只确认可使用 Virtual Bench Pro 4.0；代码来自用户，作者自承未确定 CONTROL1 中哪些位必需，不能当作官方寄存器勘误。
- **F2：MPS 英文官方论坛，MP28167 and MP2980/MP2984 solution without I2C bus**，问题发表于2024-08-21，工程师回复发表于2024-08-22、08-29。[原帖](https://forum.monolithicpower.com/t/mp28167-and-mp2980-mp2984-solution-without-i2c-bus/3815)。后续回答实际转向 MP28167A，未确认本轮 MP2984 保护/时序疑点。
- **P4：MP2984 官方产品页**。[产品页](https://www.monolithicpower.com/en/products/mp2984.html)。同时列出独立的开关频率和输出电压变化率功能，并链接 GUI，但未在公开页面提供上述疑点的澄清。

所有链接访问日期均为2026-11-11。官方中英文站指向同一手册的不同入口不计作独立器件验证。

## 逐项结论

### R1：第27页 OVP_MODE=10 写 VOUT 达到127% VREF

**分类：本手册交叉可确定，变量名高度可信笔误。**

M4第27页前文先定义通过 FB 电压比较实现 OVP；第9页电气表的 OVP 阈值相对于 VREF，第33页寄存器说明也在相同保护功能中使用 VFB。因此，技术上相符的比较量是 **VFB 与1.27×VREF**。输出端的等效阈值应通过反馈分压比换算，而不是把输出端电压直接与参考电压比较。[M4，第9、27、33页](https://www.monolithicpower.com/en/documentview/productdocument/index/version/2/document_type/Datasheet/lang/en/sku/MP2984GR/document_id/11081/)

M0第34页对同名保护模式也采用反馈比较并把10定义为锁断，为这一判断提供同族旁证，但并未构成MPS针对MP2984的更正。127%为典型阈值，不能抹掉电气表给出的范围。

### R2：第28页与第31页 GO_BIT、20ms放电时序矛盾

**分类：高可信推定，MP2984具体时序仍未获得官方直接确认。**

M4第31页 GO_BIT 段将过程写为：参考电压到达目标后，GO_BIT自动清零，放电再持续20ms；同页DISCHG段和第28页的简写却混淆了GO_BIT清零与放电结束的时间。不能把这些句子视为彼此一致。[M4，第28、31页](https://www.monolithicpower.com/en/documentview/productdocument/index/version/2/document_type/Datasheet/lang/en/sku/MP2984GR/document_id/11081/)

**量纲/时序交叉分析：**VREF允许在0.3–2.047V间变化，最慢标称变化率为38mV/ms；跨全量程的标称斜坡约为 `(2.047−0.3)/0.038 ≈ 46ms`。因此“所有变化都在发出GO_BIT后固定20ms完成”不可能与同一本手册的斜坡定义同时成立。这个计算支持把20ms理解为附加放电时间，而不是整个参考变化过程的固定时长。

M0第28页条目、第32页DISCHG和第33页GO_BIT三处都更明确地把附加20ms放在GO_BIT清零之后，支持上述解释。不过M0第28页概述也保留了过度简化的措辞，因此仍不能宣称这一争议已被官方针对MP2984澄清。[M0，第28、32、33页](https://www.monolithicpower.com/en/documentview/productdocument/index/version/2/document_type/Datasheet/lang/en/sku/MP2980GR/)

### R3：第31页重复 VREF_L，以及 DISCHRG 拼写

**分类：本手册交叉可确定的文字错误。**

M4第30页将11位参考值分为0x00的低3位VREF_L与0x01的高8位VREF_H。因而设置完整参考值需写这两组位，再触发GO_BIT；把两个寄存器都称为VREF_L不成立。DISCHRG在寄存器图中不存在，而0x02位5的正式名称为DISCHG。[M4，第30–31页](https://www.monolithicpower.com/en/documentview/productdocument/index/version/2/document_type/Datasheet/lang/en/sku/MP2984GR/document_id/11081/)

M0第33页明确指出先写00h和01h，再触发GO_BIT。F1用户示例也确实分别写REF_LSB和REF_MSB，但其代码包含多处不严谨注释，仅能作为低权重使用实例，不能给高于官方手册的权重。[M0，第33页](https://www.monolithicpower.com/en/documentview/productdocument/index/version/2/document_type/Datasheet/lang/en/sku/MP2980GR/)，[F1](https://forum.monolithicpower.com/t/mp2980-demo-board-question/3637)

### R4：第32页 FSW 四档被称为 slew rate

**分类：本手册交叉可确定的术语笔误。**

200/300/400/600kHz是频率，不是变化率；FSW控制开关频率，SR控制参考电压斜率，两者在M4第27、30、32页及P4产品页中清楚分开。这里应理解为“开关频率四档”。M0第34页的同名FSW栏也只写频率，没有变化率措辞。[M4](https://www.monolithicpower.com/en/documentview/productdocument/index/version/2/document_type/Datasheet/lang/en/sku/MP2984GR/document_id/11081/)，[P4](https://www.monolithicpower.com/en/products/mp2984.html)，[M0，第34页](https://www.monolithicpower.com/en/documentview/productdocument/index/version/2/document_type/Datasheet/lang/en/sku/MP2980GR/)

### R5：第32页 OCP_MODE=10 写触发后软启动恢复，第26页却说锁断

**分类：高可信推定为锁断模式；MP2984实际复位条件仍需确认。**

M4第26页列出逐周期限流、打嗝、锁断三种行为，并说明锁断需要下一次上电才恢复；第32页00、01已分别对应仅逐周期限流和打嗝，剩余10很可能对应锁断。第32页的“软启动恢复”没有说明触发软启动之前必须重新使能/重新上电的条件，不能据此假定它能自动恢复。[M4，第26、32页](https://www.monolithicpower.com/en/documentview/productdocument/index/version/2/document_type/Datasheet/lang/en/sku/MP2984GR/document_id/11081/)

M0第34页对10明确写锁断并要求重新启动，增强这一推断。**仍缺少MP2984针对EN切换、ENPWR切换或输入断电哪种操作能清除此锁断的直接实测/官方澄清，不能把它们当作等价复位方法。**[M0，第34页](https://www.monolithicpower.com/en/documentview/productdocument/index/version/2/document_type/Datasheet/lang/en/sku/MP2980GR/)

### R6：第33页 OVP状态位解释混入 IOUT_LIMIT 和 ILIMIT

**分类：尾句高可信为复制编辑错误；不能据此重建完整芯片状态机。**

M4第27页和第33页该行首句都把此位定义为OVP事件指示；平均电流限值和输出下降属于CC/限流语境，出现在此行尾部没有形成一致的OVP判据。可确定的含义是“OVP位表示发生过输出过压事件”，其锁存/清除按同一表格的复位条件处理；应把混入的限流句列为原文错误，而不是再推导一个电流参与OVP判断的新逻辑。[M4，第27、33页](https://www.monolithicpower.com/en/documentview/productdocument/index/version/2/document_type/Datasheet/lang/en/sku/MP2984GR/document_id/11081/)

M0第35页这一栏没有M4的限流尾句，但自身又出现状态值重复和OTP名称误用，故不能把M0这页当作已经全面修正的标准答案。[M0，第35页](https://www.monolithicpower.com/en/documentview/productdocument/index/version/2/document_type/Datasheet/lang/en/sku/MP2980GR/)

### R7：第34页 PNG 把正常范围写成固定0.5–28V

**分类：本手册交叉可确定地混淆“输出设定范围”与“电源良好窗口”。**

M4第1页的0.5–28V是器件允许设定的输出范围。第9页PG电气特性却把失效/恢复阈值定义成相对于VREF的百分比，存在迟滞。因此，不能把所有落在0.5–28V之间的输出都认为电源良好。举例：输出设定为5V时，6V虽处于0.5–28V范围内，却已超过典型117%上限（5.85V）。[M4，第1、9、34页](https://www.monolithicpower.com/en/documentview/productdocument/index/version/2/document_type/Datasheet/lang/en/sku/MP2984GR/document_id/11081/)

第34页PNG=1后又写输出处于该范围时指示，与本行前句相反，应列为笔误。M0第35页改用上下阈值的概念，支持窗口解释；它不替代MP2984第9页的具体参数。[M0，第35页](https://www.monolithicpower.com/en/documentview/productdocument/index/version/2/document_type/Datasheet/lang/en/sku/MP2980GR/)

### R8：第34页称仅屏蔽 INT input

**分类：本手册交叉可确定的方向术语笔误。**

M4第5页明确INT是开漏输出，第9页给出灌电流下的低电平规格；它不是芯片接收外部中断的输入。屏蔽位控制的是INT输出报警，不应把input当作引脚方向定义。M0第36页明确采用INT输出措辞。[M4，第5、9、34页](https://www.monolithicpower.com/en/documentview/productdocument/index/version/2/document_type/Datasheet/lang/en/sku/MP2984GR/document_id/11081/)，[M0，第36页](https://www.monolithicpower.com/en/documentview/productdocument/index/version/2/document_type/Datasheet/lang/en/sku/MP2980GR/)

### R9：第28页 ILIM/FS 启动锁存说明自相重复

**分类：本手册交叉可确定启动锁存原则，例外从句高度可信写坏。**

M4第5页两个引脚说明明确：启动后改变电平不改变默认位，后续通过串行接口修改。第28页例外从句不能推翻这个清楚的定义。M0第28页把例外明确写为“调整引脚设定并重新启动”，与启动采样/锁存的机制一致。对MP2984可采用“重新启动时重新采样”的解释，但应继续区分EN关闭、ENPWR关闭和完整电源复位，不能凭文字猜定其所有复位边界。[M4，第5、28页](https://www.monolithicpower.com/en/documentview/productdocument/index/version/2/document_type/Datasheet/lang/en/sku/MP2984GR/document_id/11081/)，[M0，第28页](https://www.monolithicpower.com/en/documentview/productdocument/index/version/2/document_type/Datasheet/lang/en/sku/MP2980GR/)

## 论坛与软件检索结果

本轮检索覆盖MPS中英文论坛、GO_BIT/OCP_MODE/PNG关键词及公开网络；F1/F2是直接相关帖子，但没有针对上述争议的工程师勘误回复。对EEVblog的访问受到robots限制，不能声称已阅读全文；中文检索未找到能直接解决这些寄存器争议的实测帖子。未把商城PDF镜像、搜索引擎重复索引或其他型号问答算作额外独立证据。

未找到可公开检查的MP2984官方GUI源码或寄存器映射文件。官方产品页以及F1工程师回复证实GUI支持关系，不能由此推断GUI已经验证了全部寄存器行为。F1用户程序还把多个CONTROL1位同时置位，不能隔离GO_BIT、DISCHG和其他位的作用，也不能用它确认20ms时序。

## 对译文的处理建议

“忠实翻译”版保留原句，并在独立查证说明中给出上述解释；如果制作带校注版，简单拼写、变量和量纲错误可标注“原文如此，按同页/同册交叉判断应为……”。GO_BIT时序、锁断复位条件应保持“高可信推断/待器件级确认”的标签，不宜无说明地改成确定的器件规范。

