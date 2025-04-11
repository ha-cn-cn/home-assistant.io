---
description: Monitor nearby water levels and be prepared for flooding with the UK
  Environment Agency API integration.
ha_category:
- Sensor
ha_codeowners:
- '@Jc2k'
ha_config_flow: true
ha_iot_class: Cloud Polling
ha_release: 0.115
last_updated: '2025-04-11'
title: UK Environment Agency Flood Monitoring
translation: true
---


“eafm”集成提供与 [英国环境署洪水监测]（https://environment.data.gov.uk/flood-monitoring/doc/reference） API 的集成，以提供附近水位的传感器。结合 Home Assistant 通知，如果附近的河流可能会淹没您当地的自行车道或离开您村庄的唯一道路，您可以向自己发出警告。

{% important %}

英国环境署洪水监测仅提供英格兰的数据 - 北爱尔兰、苏格兰和威尔士有自己的洪水机构。

{% endimportant %}

## Configuration

Home Assistant通过**设置** -> **设备和服务** -> **环境机构洪水测量仪**提供洪水监测集成。

系统将提示您选择监控站。您可以在洪水信息服务 [website]（https://check-for-flooding.service.gov.uk/river-and-sea-levels） 上找到附近监测站的名称。

然后，该监控站的传感器应显示在您的 Home Assistant 实例中。