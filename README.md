<div align="center">
  <img src="https://foruda.gitee.com/images/1795179430570073327/66396482_17054380.png" width="120" alt="MingChart Logo">
  <h1>📊 MingChart - 数据图表生成器</h1>
  <p><strong>让数据可视化，优雅且简单。</strong></p>
  
  <p>
    <a href="#-中文文档">中文</a> | 
    <a href="#-english-documentation">English</a>
  </p>
  
  <p>
    <a href="https://github.com/wm1524/MingChart"><img src="https://img.shields.io/badge/GitHub-Repository-black?logo=github" alt="GitHub"></a>
    <a href="https://gitee.com/wm1524/MingChart"><img src="https://img.shields.io/badge/Gitee-Repository-C71D23?logo=gitee" alt="Gitee"></a>
    <a href="https://chart.152427.xyz"><img src="https://img.shields.io/badge/Web-Online-brightgreen.svg" alt="Web"></a>
    <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License"></a>
    <a href="https://www.python.org/"><img src="https://img.shields.io/badge/python-3.8+-green.svg" alt="Python"></a>
  </p>
</div>

---

## 🇨🇳 中文文档

### ✨ 简介

**MingChart** 是一款轻量、高效且界面优雅的数据可视化工具。由独立开发者 **万铭** 倾力打造。

它不仅拥有纯本地运行的桌面客户端，还拥有全设备适配的网页体验端。摒弃了繁琐的配置和庞大的商业软件，MingChart 提供了一种所见即所得的操作体验：无需编写代码，只需输入数据或直接用鼠标/手指拖拽图形，即可一键生成专业级别的饼图、柱状图和折线图。

🌐 **官方网站**：[https://chart.152427.xyz](https://chart.152427.xyz)  
🖥️ **网页体验端**：[https://chart.152427.xyz/mobile.html](https://chart.152427.xyz/mobile.html)  
📦 **开源镜像**：[GitHub](https://github.com/wm1524/MingChart) | [Gitee](https://gitee.com/wm1524/MingChart)

### 🚀 核心特性

- 🎨 **极简现代界面**：采用卡片式 UI 设计，操作直观，全中文界面无缝衔接。
- 📊 **多图表支持**：完美支持饼图、柱状图和折线图。
- 🖱 **网页级悬停交互**：鼠标悬停在图表元素上时，**柱状图会高亮变色**，**饼图扇区会灵动弹出（Explode 效果）**，并展示具体数值。
- ✋ **颠覆式“绘制拖拽”模式**：打破传统输入框限制，按住鼠标/手指拖动柱状图高度或折线节点，即可实时修改数值，带有弹性的阻尼手感，且数据会自动同步回左侧输入框。
- 🔗 **多 API 接口接入**：支持输入多个 JSON 接口地址，自动抓取数据并生成对比图表。
- 📦 **全平台覆盖**：提供 Windows 桌面客户端（一键安装）与全设备适配的网页体验端。
- 🔒 **纯本地运行**：客户端无需网络连接，保护您的数据隐私。

### 📥 下载与安装

请前往我们的官方网站或开源仓库 Releases 下载最新版本：
👉 **[MingChart 官网](https://chart.152427.xyz)**
👉 **[GitHub Releases](https://github.com/wm1524/MingChart/releases)**
👉 **[Gitee 发行版](https://gitee.com/wm1524/MingChart/releases)**

系统要求：Windows 10 / 11 (64-bit)

### 🛠️ 本地开发指南

如果你想基于此项目进行二次开发或贡献代码：

**1. 克隆仓库**
打开终端，运行：
`git clone https://github.com/wm1524/MingChart.git`
`cd MingChart`

**2. 安装依赖**
`python -m pip install -r requirements.txt`

**3. 运行程序**
`python main.py`

**4. 打包编译**
打包为独立 exe：
`python -m PyInstaller MingChart.spec --noconfirm`

编译安装包 (需要安装 Inno Setup)：
`"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss`

### 🤝 关于作者与联系

- **作者**：万铭
- **QQ**：3807559825
- **邮箱**：ttsd1524@qq.com
*(注：由于日常较忙，消息回复可能会有延迟，感谢您的理解与支持。)*

### 📄 开源协议

本项目采用 [MIT License](LICENSE) 协议开源。您可以自由使用、修改，甚至用于商业用途，但请保留原作者版权声明。

---

## 🇬🇧 English Documentation

### ✨ Introduction

**MingChart** is a lightweight, highly efficient, and elegantly designed data visualization tool. Crafted by independent developer **WanMing**.

It offers both a fully offline desktop client and a responsive web experience. Eliminating the need for complex configurations or bulky commercial software, MingChart provides a WYSIWYG experience: no coding required—just input your data or drag the shapes directly with your mouse/finger to generate professional pie charts, bar charts, and line charts.

🌐 **Official Website**: [https://chart.152427.xyz](https://chart.152427.xyz)  
🖥️ **Web Experience**: [https://chart.152427.xyz/mobile.html](https://chart.152427.xyz/mobile.html)  
📦 **Mirrors**: [GitHub](https://github.com/wm1524/MingChart) | [Gitee](https://gitee.com/wm1524/MingChart)

### 🚀 Core Features

- 🎨 **Minimalist Modern UI**: Card-based design with an intuitive, seamless full-Chinese interface.
- 📊 **Multi-Chart Support**: Fully supports Pie charts, Bar charts, and Line charts.
- 🖱 **Web-level Hover Interaction**: Hovering over chart elements causes **Bar charts to highlight** and **Pie slices to dynamically explode outward**, while displaying the exact values.
- ✋ **Revolutionary "Drag-to-Draw" Mode**: Break free from input boxes. Hold and drag the bars or line nodes with your mouse/finger to modify values in real-time. Features a smooth damping effect, and data automatically syncs back to the input fields.
- 🔗 **Multi-API Integration**: Connect to multiple JSON API endpoints to automatically fetch and compare data.
- 📦 **Cross-Platform**: Includes a Windows desktop client (one-click install) and a responsive web experience version.
- 🔒 **100% Offline**: The desktop client requires no internet connection, ensuring data privacy.

### 📥 Download & Installation

Please visit our official website or repository Releases to download the latest version:
👉 **[MingChart Official Website](https://chart.152427.xyz)**
👉 **[GitHub Releases](https://github.com/wm1524/MingChart/releases)**
👉 **[Gitee Releases](https://gitee.com/wm1524/MingChart/releases)**

System Requirements: Windows 10 / 11 (64-bit)

### 🛠️ Local Development Guide

If you want to contribute or build upon this project:

**1. Clone the repository**
Run in your terminal:
`git clone https://github.com/wm1524/MingChart.git`
`cd MingChart`

**2. Install dependencies**
`python -m pip install -r requirements.txt`

**3. Run the app**
`python main.py`

**4. Build the executable**
Build standalone exe:
`python -m PyInstaller MingChart.spec --noconfirm`

Compile installer (Requires Inno Setup):
`"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss`

### 🤝 About & Contact

- **Developer**: WanMing
- **QQ**: 3807559825
- **邮箱/Email**: ttsd1524@qq.com
*(Note: Responses may be delayed due to a busy schedule. Thank you for your understanding!)*

### 📄 License

This project is open-sourced under the [MIT License](LICENSE). You are free to use, modify, and distribute it, even for commercial purposes, as long as the original copyright notice is retained.

---
<div align="center">
  <i>If you find this project helpful, please consider giving it a ⭐️!</i>
</div>
