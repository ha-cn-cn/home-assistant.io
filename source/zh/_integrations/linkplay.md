---
description: Connect and control your LinkPlay media players using the LinkPlay integration
ha_category:
- Media player
ha_codeowners:
- '@Velleman'
ha_config_flow: true
ha_domain: linkplay
ha_integration_type: integration
ha_iot_class: Local Polling
ha_platforms:
- media_player
- button
ha_release: 2024.8
ha_zeroconf: true
last_updated: '2025-04-11'
title: LinkPlay
translation: true
---


Home Assistant 的 LinkPlay {% term integrations %} 允许您根据 LinkPlay 协议控制各种媒体播放器。该集成支持通过 [Zeroconf]（/integrations/zeroconf） 在本地网络上进行自动发现。

{% include integrations/config_flow.md %}

## Features

### Media Player 

媒体播放器实体提供来自媒体播放器集成的强大控件和播放功能，并提供：

- **预设播放**：使用作“linkplay.play_preset”播放在设备上配置的 LinkPlay 预设。
- **多房间**：将多个 LinkPlay 设备组合到一个多房间中。使用作 'media_player.join' 和 'media_player.unjoin'。

### Buttons

按钮实体提供设备上可用的一些其他 LinkPlay 功能：

- **时间同步**：将设备的内部时钟与 Home Assistant 中的当前时间同步。
- **重启设备**：重启设备，方便排查和维护。

## Actions

除了 [标准媒体播放器作]（/integrations/media_player/#actions） 之外，LinkPlay 集成还提供各种自定义作。

###作 'linkplay.play_preset'

在 LinkPlay 媒体播放器上播放预设。

{% 注意 %}
配套应用程序，例如 4stream，允许保存音乐预设（例如，Spotify 播放列表）。此作可用于开始播放这些预设。
{% 尾注 %}

|数据属性 |可选 |描述 |
|---------------------- |-------- |----------- |
|'entity_id' |否 |要定位的扬声器。要定位所有 LinkPlay 设备，请使用 'all'。
|'preset_number' |否 |要播放的预设的编号。