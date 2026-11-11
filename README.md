# MP2984 数据手册中文翻译

依据用户提供的 MPS MP2984 Rev. 1.0（2021-12-09）英文数据手册翻译，共43页，逐页对应原文。正文、表格说明、图题、图中说明和脚注译为中文；数值、单位、公式编号、引脚名、寄存器名与位定义保留原稿。

- 成品：`output/pdf/mp2984-zh.pdf`
- LaTeX入口：`main.tex`
- 逐页中文与TikZ排版：`pages/p01.tex` 至 `pages/p43.tex`
- 对照原稿：`assets/original.pdf`
- 复核说明：`REVIEW.md`
- 原文疑点联网查证（独立于忠实译稿）：[`research/README.md`](research/README.md)
- 编译：`./build.ps1`

## 排版与图形

保留原稿Letter纸张、43页分页、双栏位置、表格框线、电路、机械尺寸及实测曲线。中文为LaTeX原生文字，用TikZ定位和蒙版叠排；公式、电路及实测图形使用原PDF内容，不以估算数据重新绘图。原图中的变量、器件位号、寄存器名和示波器通道标记保持不变。原稿文本仍可能存在于PDF底层；复制文字时请注意叠排的原文与译文。

## 构建环境

Windows、Tectonic（或支持XeLaTeX的TeX发行版），以及Arial、SimSun、SimHei字体。Tectonic首次构建可能需要联网下载宏包与数学字体；`build.ps1 -CacheDir <缓存路径>` 可指定缓存。也可运行 `xelatex main.tex` 两次。

## 来源和版权

本项目是非官方中文翻译。原文来源为用户提供的 `DEF63F1ECCF452016DB393E7230F7AC6.pdf`，版权属于Monolithic Power Systems, Inc.。原文保留“MPS专有信息、受专利保护、未经授权禁止复印与复制”的声明。本仓库不对原文及其图表另行授予许可。原文中的内部矛盾单独列在复核说明中，未擅自修改其技术结论。

