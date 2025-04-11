---
description: Options for regaining access
last_updated: '2025-04-11'
related:
- docs: /common-tasks/os/#listing-all-users-from-the-command-line
  title: Listing all usernames via command line
- title: Reset the Yellow
  url: https://yellow.home-assistant.io/guides/factory-reset/
- title: Reset the Green
  url: https://green.home-assistant.io/guides/reset/
title: I'm locked out!
translation: true
---


以下部分介绍如何从无法登录的情况中恢复，
或需要恢复您的数据。

## Forgot username

### 症状：我是所有者，但我忘记了我的用户名

您是 Home Assistant 服务器的 **所有者**，由于忘记了用户名，因此无法登录。

#### Remedy

1. 检查是否满足以下条件：
   - 您正在使用 {% 术语 “Home Assistant Operating System” %}
   - 您可以访问 Home Assistant 服务器。
2. 打开与 Home Assistant 的终端连接：
   - 如果您使用的是 Home Assistant Green，请按照以下步骤 [访问控制台]（https://green.home-assistant.io/guides/use-terminal/）。
   - 如果您使用的是 Home Assistant Yellow，请按照以下步骤作：
     - [从 Windows 访问控制台]（https://yellow.home-assistant.io/guides/use-serial-console-windows/）
     - [从 Linux 或 macOS 访问控制台]（https://yellow.home-assistant.io/guides/use-serial-console-linux-macos/）。
   - 如果您使用的是其他系统，请连接键盘和显示器。该过程可能与用于 Green 的过程类似。
   - 如果您使用的是 Home Assistant OVA（虚拟化映像）：
     - 通过虚拟化平台的界面（例如 Proxmox、VMware、VirtualBox）打开终端来访问系统控制台。
     - 按照特定于平台的步骤与虚拟机的控制台进行交互。
3. 在终端中，输入“auth list”命令。
   - 此命令列出在您的 Home Assistant 上注册的所有用户。

## Forgot password

### 症状：我是所有者，我忘记了密码

您是 Home Assistant 的所有者或管理员，但忘记了密码。

### 补救措施：重置所有者的密码

如果您是所有者或管理员，则根据您的情况，可以使用不同的方法来重置密码：

- [在仍处于登录状态时重置密码]（#to-reset-a-password-while-still-login-in-including-supervised）
- [注销时重置所有者密码]（#to-reset-an-owners-password-via-console）
- [重置用户的密码，通过容器命令行]（#to-reset-a-users-password-via-the-container-command-line）

#### 在登录时重置密码（包括受监督）

用于重置密码的方法取决于您的用户权限：

- 如果您是没有管理员权限的普通用户，请让所有者 [给您一个新密码]（/docs/locked_out/#to-reset-a-users-password-as-an-owner-via-the-web-interface）。
- 如果您是所有者，请选择以下过程之一来重置您的密码。
  - 您无法从 Home Assistant 中恢复所有者密码。
  - 每个系统只有一个所有者。您无法添加新的所有者。
- 如果您是管理员，请添加新用户作为管理员，并为新用户提供您可以记住的密码。
  1. 然后注销，并使用此新用户登录。
  2. 通过这个新的管理员帐户重置您的密码（然后 [删除此新帐户]（/docs/locked_out/#to-delete-a-user））。
     - 您的配置将保留，您不必执行新的载入过程。

#### 通过控制台重置所有者的密码

仅当满足以下条件时，才使用此过程：

- 您知道用户名。
- 您可以访问 Home Assistant 控制台 **在设备本身上**（而不是通过附加组件的 SSH 终端）。

1. 如果您使用的是 Home Assistant Yellow 或 Green，请参阅他们的文档。
   - 如果您使用的是 Home Assistant Yellow，请参阅以下过程：
     - [在 Home Assistant Yellow 上重置所有者密码]（https://yellow.home-assistant.io/faq/#i-forgot-the-owner-password-for-home-assistant-how-can-i-reset-it）
   - 如果您使用的是 Home Assistant Green，请参阅以下过程：
     - [重置 Home Assistant Green 的所有者密码]（https://green.home-assistant.io/faq/#i-forgot-the-owner-password-for-the-home-assistant-green-how-can-i-reset-it）
2. 如果您不使用黄色或绿色：连接到 Home Assistant 服务器的控制台：
   - 如果您使用的是虚拟机，请连接到您的虚拟机控制台。
   - 如果您使用的是其他开发板，请将键盘和显示器连接到您的设备并访问终端。该程序可能与 Home Assistant Green 所描述的程序非常相似。
3. 打开 Home Assistant 命令行后，输入以下命令：
   - 注意：“existing_user”是一个占位符。将其替换为您的用户名。
   - 注意：“new_password”是一个占位符。将其替换为您的新密码。
   - **命令**： 'auth reset --username 'existing_user' --password 'new_password''
     ![显示如何输入 ha auth reset 命令的截屏视频]（/images/docs/troubleshooting/home-assistant-cli.webp）
   - **故障排除**：如果您看到消息“zsh： command not found： auth”，您可能没有在连接到设备本身的串行控制台中输入命令，而是在 Home Assistant 的终端中输入命令。
4. 您现在可以使用此新密码登录 Home Assistant。

#### 重置用户的密码，通过容器命令行

如果您在容器中运行 Home Assistant，您可以使用容器中的命令行和“hass”命令来更改您的密码。以下步骤引用 Docker 中名为 “homeassistant” 的 Home Assistant 容器。请注意，在容器中工作时，命令将需要一些时间来执行。

1. 'docker exec -it homeassistant bash' 打开容器命令行
2. 'hass' 创建默认用户（如果这是您第一次使用该工具）
3. 'hass --script auth --config /config change_password existing_user new_password' 更改密码
4. 'exit' 退出容器命令行
5. 'docker restart homeassistant' 重启容器。

#### 以所有者身份通过 Web 界面重置用户的密码

只有所有者可以更改其他用户的密码。

1. 在左下角，选择您的用户以转到 {% my profile title=“**Profile**” %} 页面，并确保 **高级模式** 已激活。
2. 转到 {% my people title=“**Settings** > **People**” %}，然后选择要更改密码的人员。
3. 在对话框底部，选择 **更改密码**。
   - 注意：这是所有者而非管理员可用的。
4. 输入新密码，然后选择 **确定**。
5. 再次输入新密码以确认新密码，然后再次选择 **确定**。
6. 将显示一个确认框，其中包含 **密码已成功更改** 文本。

## 准备系统以启动新的载入流程

如果您丢失了与所有者账户关联的密码，并且上述步骤无法重置密码，则解决此问题的唯一方法是启动新的载入过程。

- 如果您有一个外部备份，其管理员帐户仍然知道该帐户的登录凭据，则可以还原该备份。
- 如果您没有备份，重置设备将擦除所有数据。

- 如果您有 Home Assistant Green，请 [重置绿色]（https://green.home-assistant.io/guides/reset/）。
- 如果您有 Home Assistant Yellow，[重置黄色]（https://yellow.home-assistant.io/guides/factory-reset/）。

## 恢复 Home Assistant 的数据（包括受监督的）

除非您的 SD 卡/数据已损坏，否则您仍然可以访问您的文件或进一步排除故障。
有几条路线：

- 将 USB 键盘和 HDMI 显示器直接连接到 Raspberry Pi。
- 移除 SD 并从另一台计算机（最好是运行 Linux 的计算机）访问文件。

## Connect directly

如果您使用的是 Raspberry Pi，则可能必须拔掉电源才能在启动时识别您的显示器。拉力有损坏 SD 的风险，但您可能别无选择。大多数标准 USB 键盘应该很容易识别。

连接后，您将看到一个正在运行的 dmesg 日志。按 Enter 键中断日志。
以 “root” 身份登录。没有密码。

然后，您将进入 Home Assistant CLI，您可以在其中运行自定义命令。这些与使用 SSH 附加组件运行相同，但不在其前面使用 'ha'。例如：

- Home Assistant 的 'core logs' 核心日志
- “supervisor logs” 用于 supervisor logs
- “host reboot”以重新启动主机
- 用于检查 DNS 的 'DNS logs'
- 等（键入 'help' 将显示更多）

## 从 SD/HDD 访问文件

### 删除 SD 并从另一台计算机访问文件

这些文件位于 EXT4 分区 （'hassos-data'） 上，路径为 '/mnt/data/supervisor'。
可以使用另一台支持 EXT 的 Linux 计算机轻松访问这些内容。

对于 Windows 或 macOS，您将需要第三方软件。以下是一些选项。

- Windows：<https://www.diskinternals.com/linux-reader/>（对 SD 的只读访问权限）
- macOS：<https://osxfuse.github.io/>

## Deleting a user

您需要是所有者或具有管理员权限才能删除用户。

1. 转到 {% my people title=“**Settings** > **People**” %}，然后选择要删除的人员。
   - 注意：您无法删除所有者。
2. 在对话框底部，选择 **删除**。
   - 将显示一个确认对话框。
3. 要确认，请选择 **确定**。