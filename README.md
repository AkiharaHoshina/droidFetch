# droidFetch (dfetch) 📱

[English Ver.](https://github.com/AkiharaHoshina/droidFetch/blob/c36f04d5a234743fb6d762bc2eee06df3b41609d/README_en.md).

一款专为 Android 环境深度定制的系统信息命令行展示工具。在终端中优雅地展示你的设备软硬件信息。

## ✨ 核心特性

* **深度 ROM/发行版识别:** 通过读取系统属性（`getprop`），精准识别主流 Android 定制系统及第三方 ROM。
* **精美的 ASCII 图标:** 内置超过 15 种 Android 系统的 ASCII 艺术徽标*与主题配色。事实上，这些徽标并不精美，不少系统还找不到合适的徽标，这是我手搓的。
* **平板/横屏模式:** 支持横向排版，专为平板电脑、折叠屏或宽屏终端优化。
* **高度可定制:** 支持通过配置文件强制指定系统徽标、覆盖主题颜色，甚至导入自定义的 ASCII 字符画。
* **轻量级:** 纯 Python 3 编写，无臃肿的第三方依赖库。

## 🚀 支持的系统/发行版

`droidFetch` 目前可自动识别并展示以下系统的专属徽标：
* 小米澎湃 OS (HyperOS) / MIUI
* 华为 EMUI / HarmonyOS / 荣耀 MagicOS
* 绿厂 ColorOS / OxygenOS / 蓝厂 OriginOS / FuntouchOS
* 三星 One UI
* 魅族 Flyme OS
* Nothing OS
* Pixel UI / Pixel Experience
* LineageOS / Evolution X / crDroid / Paranoid Android (AOSPA) / GrapheneOS

## 🛠️ 安装指南

由于 `droidFetch` 依赖 Android 的底层系统命令（如 `getprop`），该工具需要在 Android 设备的终端环境中运行（推荐使用 [Termux](https://termux.dev/)）。

1. 克隆本仓库:
   git clone https://github.com/AkiharaHoshina/droidFetch.git
   
   cd droidFetch

3. 赋予执行权限:
   chmod +x dfetch-unstable-0.2.py

4. 运行测试:
   python3 dfetch-unstable-0.2.py

*(可选)* 你可以将脚本重命名为 `dfetch` 并移动到全局环境变量目录中（例如 Termux 的 `PREFIX/bin/`），以便随时调用。

## 📖 使用方法

直接运行即可展示标准竖排布局：
python3 dfetch-unstable-0.2.py

### 命令行选项

| 选项 | 说明 |
| :--- | :--- |
| `-h`, `--help` | 显示帮助信息并退出。 |
| `-v`, `--version` | 显示当前版本信息并退出。 |
| `-T`, `--tablet` | 启用横屏排版模式（适合平板或宽屏终端）。 |
| `-D`, `--custom-distro <ID>` | **调试模式:** 强制指定并显示特定的系统徽标（如 `MIUI`, `LINEAGE`）。 |
| `-C`, `--custom-color <COLOR>` | **调试模式:** 强制覆盖主题颜色。支持 ANSI 转义码，或特定预设（`GOOGLE_RAINBOW`, `PRIDE`, `TRANS_PRIDE`）。 |
| `--gen-config` | 在 `~/.config/dfetch` 目录下生成默认配置文件，并退出。 |
| `--gen-config-samedir` | 在程序同目录的 `dfetch` 文件夹下生成默认配置文件（适用于便携测试版）。 |

## ⚙️ 配置文件

如果你希望持久化你的自定义设置，可以生成一个配置文件：

python3 dfetch-unstable-0.2.py --gen-config

这将在 `~/.config/dfetch/dfetch.conf` 生成文件。使用文本编辑器打开它，即可修改默认行为：

# dfetch 配置文件
distro=default        # 强制指定发行版徽标（例如改为 CRDROID）

color=default         # 强制修改颜色（例如改为 \033[1;31m）

custom_ascii=default  # 指向包含自定义 ASCII 图案的 txt 文件路径

tablet_mode=default   # 修改为 'true' 以默认开启横屏模式
