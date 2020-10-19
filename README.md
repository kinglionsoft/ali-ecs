# 定时更新阿里云安全组

## 场景
安全组中开放了的敏感端口（如：3306）仅允许指定的办公网宽带IP访问。宽带IP不是固定的，需要再其更新后，修改安全组的原地址。

## 用法

* 通过在规则的**描述**中设置指定的前缀标识需要更新的规则

* Python
``` python
group = SecruityGroup('<accessKeyId>', '<accessSecret>', 'cn-hangzhou')
group.changeSourceCidr('<Security Group ID>', '<Prifex of rule description')
```

* Linux 通过**cron**定时更新

* Windows 通过**计划任务**定时更新