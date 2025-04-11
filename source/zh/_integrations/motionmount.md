---
description: Instructions on how to integrate Vogel's MotionMount into Home Assistant.
ha_category:
- Number
- Select
- Binary sensor
- Sensor
ha_codeowners:
- '@RJPoelstra'
ha_config_flow: true
ha_domain: motionmount
ha_iot_class: Local Push
ha_platforms:
- number
- select
- binary_sensor
- sensor
ha_release: 2024.1
ha_zeroconf: true
last_updated: '2025-04-11'
title: Vogel's MotionMount
translation: true
---


'motionmount' {% term integration %} 允许您控制 Vogel's 的 [TVM 7675 Pro]（https://www.vogels.com/p/tvm-7675-pro-motorized-tv-wall-mount-black） SIGNATURE MotionMount 的位置。

此集成使用 MotionMount 的以太网 （IP） 连接。无法使用 RS-232 连接进行连接。

它提供有关安装座当前位置的信息，并允许设置新位置。

一个用例是根据是否有人正在积极观看来定位电视。MotionMount 提供 HDMI 连接来监控电视是否打开，并相应地将其移动到预设位置或最后已知位置。但是，如果您还将电视用于背景音乐，则可能不希望 MotionMount 扩展。通过使用存在传感器检查是否有人真的在电视机前，您可以确保 MotionMount 仅在电视机正在观看时伸出。

{% include integrations/config_flow.md %}

{% configuration_basic %}
主机：
  description：设备的主机名或 IP 地址，例如：'192.168.1.2'。
港口：
  description：设备的 TCP 端口。默认为 23。仅在您绝对确定它不应该为 23 时更改此字段。
针：
  description：用户级别 PIN 码（如果在设备上配置）。
{% endconfiguration_basic %}

## 删除集成

此集成遵循标准集成删除。不需要额外的步骤。

{% include integrations/remove_device_service.md %}

## Data updates

MotionMount 将新数据推送到集成中。
唯一的例外是预设。对预设的更改为 {% term polling polling %}，默认每 60 秒一次。

## Known limitations

该集成不提供配置 MotionMount 的功能。
所有设置，包括配置预设，都应通过 MotionMount 应用程序完成。

仅支持 IP 连接。不支持通过 RS-232 或低功耗蓝牙进行连接。

## Supported devices

支持以下设备：

- TVM 7675 Pro（带 Pro 延长杆的 SIGNATURE MotionMount）

## 不支持的设备

以下设备*不受*支持：

- TVM 7675 （SIGNATURE MotionMount 不带 Pro 延长杆）
- TVM 7355 （NEXT MotionMount）

## 支持的功能

### Entities

#### Sensors

-**移动**
  - 描述：表示 MotionMount 是否在移动。

- **错误状态**
  - **描述**：MotionMount 的错误状态。
    - None：没有错误。
    - 电机：与电机通信时出现问题。
    - HDMI CEC：与电视通信时出现问题。检查 HDMI 电缆。
    - 障碍物：MotionMount 检测到障碍物并停止移动。
    - TV Width Constraint：MotionMount 检测到 TV 移动得离墙壁太近，并停止移动。
    - 内部：存在内部错误。请参阅 MotionMount 应用程序以获取支持。

#### Numbers

-**外延**
  - **描述**：MotionMount 从墙上的当前延伸。

-**转**
  - **描述**：MotionMount 的当前旋转。

#### Selects

-**预设**
  - **描述**： 如果 MotionMount 位于预设位置，则会显示对应的预设。
        可以选择任何预设，以将 MotionMount 移动到此预设位置。

## Troubleshooting

### 无法连接到设备

1. 确保设备已开机。
2. 确保设备与 Home Assistant 连接到同一网络。
3. 确保 MotionMount 的 IP 地址配置正确。
    - 如有疑问，请按住重置按钮约 5 秒钟来执行网络重置。
      - **结果**： LED 指示灯将开始缓慢闪烁。这表示正在重置网络配置以使用 DHCP。
      - **重要**：不要按住重置按钮太久（约 10 秒）。按住按钮 10 秒或更长时间将开始恢复出厂设置。LED 快速闪烁表示恢复出厂设置。