---
description: Instructions on how to use Locative to track devices in Home Assistant.
ha_category:
- Presence detection
ha_domain: locative
ha_iot_class: Cloud Push
ha_release: 0.86
last_updated: '2025-04-11'
title: Locative
translation: true
---


此平台允许您使用 [Locative]（https://www.locative.app/） 来检测存在。Locative 是一款适用于 [iOS]（https://apps.apple.com/us/app/locative/id725198453?ign-mpt=uo%3D4） 的开源应用程序，允许用户在进入或退出地理围栏时设置“GET”或“POST”请求。这可以通过 Home Assistant 进行配置以更新您的位置。

在您的智能手机上安装：

- [iOS]（https://apps.apple.com/us/app/locative/id725198453?ign-mpt=uo%3D4）

要配置 Locative，您必须通过配置屏幕中的集成面板进行设置。您必须将应用程序设置为在设置期间通过集成提供的 webhook URL 向您的 Home Assistant 实例发送 POST 请求。当您进入或退出地理围栏时，Locative 将向该 URL 发送相应的请求，并更新 Home Assistant。您无法在 Locative 中指定设备名称。相反，你需要在你的 'dev-state' 菜单中查找 Locative 将在其第一个 'GET' 中创建的新设备。如果您曾经或正在使用 Owntracks，则需要使用 Locative 生成的名称更新 Owntracks 设置中使用的设备名称。

<p class='img'>
  <img src='/images/screenshots/locative.png'/>
</p>

当您输入地理围栏时，您在 Home Assistant 中的位置名称将设置为 Locate 中的地理围栏名称。当您退出地理围栏时，您在 Home Assistant 中的位置名称将设置为 “not home”。