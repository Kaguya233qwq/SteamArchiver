# SteamArchiver

一个快速、轻量的命令行工具，用于迅速导出你的 Steam 游戏清单及密钥。

[English](README.md) | [简体中文](README_zh.md)

# 📖 关于项目

SteamArchiver 是一款为 Steam 用户设计的简单而强大的工具。它提供了一种快速、一键式的方式来直接导出你的游戏清单和密钥。其设计理念是极简、快速且易于使用，非常适合用于归档你的游戏库或与朋友分享游戏列表。

# ✨ 功能特性

-   ⚡ **快速轻量**：无沉重依赖，确保快速执行。
-   🔑 **密钥导出**：轻松获取并导出你的游戏的清单及对应的秘钥。
-   🔒 **安全可靠**：你的凭据仅用于与 SteamDB 通信，并且本项目不会损坏你设备上的任何文件。
-   ⚙️ **配置简单**：仅需几条命令即可完成设置并运行。

# 🚀 开始使用

请按照以下说明在你的本地计算机上配置并运行此项目。

## 先决条件

在开始之前，请确保你已安装以下环境：

1. 确保你的操作系统是**Windows**
2.  已安装**Python 3.12** 或更高版本
3.  **uv**: 一个快速的 Python 包安装器和解析器。你可以通过 pip 安装它：
    ```bash
    pip install uv
    ```

## 安装与使用

1.  **克隆仓库**
    ```bash
    git clone https://github.com/your-username/SteamArchiver.git
    cd SteamArchiver
    ```

2.  **同步依赖**
    ```bash
    uv sync
    ```

3.  **首次运行（配置）**

    首次运行此应用以生成配置文件。
    ```bash
    uv run python main.py
    ```

    程序会检测到这是首次运行，并在项目目录中创建一个 `.env` 文件。现在，你需要用你的身份验证信息填充此文件。

    **如何获取你的 `User-Agent` 和 `Cookie`：**

    a. 打开你的浏览器，访问 [steamdb.info/sub/](https://steamdb.info/sub/) 并确保你已登录。

    b. 打开浏览器的 **开发者工具**（通常按 `F12` 或 `Ctrl+Shift+I`）。

    c. 切换到 **网络 (Network)** 标签页。

    d. 刷新页面（按 `F5`）。

    e. 在网络请求列表中，找到并点击一个向 `steamdb.info` 发出的请求。

    f. 在 **标头 (Headers)** 部分（有时也叫“请求标头”），找到并完整复制 `User-Agent` 和 `Cookie` 的字符串值。

    现在，打开 `.env` 文件并像下面这样粘贴你的值：
    ```
    USER_AGENT=Your User-Agent string here
    COOKIE=Your complete cookie string here
    ```

4.  **导出你的游戏清单和密钥**
    配置好 `.env` 文件后，再次运行程序。
    ```bash
    uv run python main.py
    ```
    程序会提示你输入想要导出详情的游戏 `app_id`。提供 ID 后，它将获取数据并输出一个包含数据的文件夹。

# 📄 免责声明

## 重要声明

-   本项目 **不** 提供任何修改原始游戏文件或数据的方式或数据。
-   本项目的唯一目的是为玩家提供一个方便的途径来归档和分享他们的个人游戏清单。
-   SteamArchiver 是完全 **开源且免费** 的。不鼓励任何商业用途。

# 🤝 参与贡献

欢迎参与贡献代码！如果你有任何建议或想要改进此工具，请随时提交 Issue 或 Pull Request。

# 📜 许可证

本项目采用 MIT 许可证。详情请参阅 `LICENSE` 文件。