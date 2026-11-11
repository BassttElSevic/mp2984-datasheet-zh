# 软启动钳位电压：对先前复核判断的再核查

检索日期：2026-11-11。对象是MP2984，MP2980仅作为同族旁证。

## 结论

MP2984第25页的 `0.6 V > VREF` 不能可靠解释成一个适用于整个VREF范围的固定0.6V钳位值。先前复核将“VREF+0.6V”直接判成误译、再将固定0.6V写成确定结论，判断过早，应撤回。

现有旁证更支持 `VSS ≈ VREF + 0.6 V`；但未找到MPS针对MP2984该句的公开勘误、明确工程师答复或本芯片实测，因此不能把MP2980的规格直接移植成MP2984的保证值。

## 证据与推理

1. [MP2984官方手册](https://www.monolithicpower.com/en/documentview/productdocument/index/version/2/document_type/Datasheet/lang/en/sku/MP2984GR/document_id/11081/)第25页写法含糊；同页又要求软启动电压越过参考电压才进入正常闭环。第1页允许参考电压达到2.047V。由此作一致性检验：如果SS永远被固定钳在0.6V，参考电压设为0.8V或更高时便无法满足同页所述越过参考电压的条件。这是对固定0.6V解释的反证，不是测得了实际钳位电路。
2. [MP2980官方手册](https://www.monolithicpower.com/en/documentview/productdocument/index/version/2/document_type/Datasheet/lang/en/sku/MP2980GR/document_id/11523/)Rev.1.0（2023-11-09）第25页明确给出：稳态SS电压钳位在参考电压之上0.6V。这是厂家对MP2980的直接描述，对MP2984仅构成较强同族旁证。
3. [MP2980/MP2984无I2C应用论坛帖](https://forum.monolithicpower.com/t/mp28167-and-mp2980-mp2984-solution-without-i2c-bus/3815)主要讨论默认配置与独立工作，未回答软启动钳位。不能将该帖当作对此歧义的确认。
4. MPS产品页提供[MPSmart模型入口](https://www.monolithicpower.com/en/documentview/productdocument/index/version/2/document_type/MPSmart%20Model/lang/en/sku/MP2984GR/document_id/12661/)。此次网页工具未取得模型，本地下载也连接超时；没有读取模型内部电路，更没有运行仿真，不以模型作证。

## 译文处理

不改动忠实译稿，原文直译继续保留。固定0.6V或VREF+0.6V的物理解释均不在正文中作为新增规格；查证判断仅放在本独立说明。此报告提供较可信的工程解释；实际SS钳位值及其随VREF变化的关系仍需MPS确认或在不同VREF设置下实测。

