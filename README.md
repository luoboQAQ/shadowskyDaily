# shadowskyDaily

基于GitHub Actions，用于shadowsky每日签到来获得流量。

## 实现功能

- 自动签到
- 查询剩余流量
- 推送到企业微信

## 使用教程

1. fork本仓库

2. 配置Github Actions，打开仓库的`secrets`，填入以下内容。

   ```
   SHADOWSKY_ACCOUNT=账号
   SHADOWSKY_PSW=密码
   ```

3. （可选）设置企业微信推送

   在仓库的`secrets`，填入以下内容

   ```
   SEND_CODE=1
   CORPID=企业ID
   AGENTID=应用ID
   SECRET=应用secret