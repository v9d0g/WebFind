# WebFind

```sh
0  ___           _ __ __                
x  \==\    _    /===__ _/      WEB FIND V1.1.0
7   \==\  /=\  /==/_ __         批量web存活探测
7    \==\/ _ \/==_ _ _/         [*] 支持socks代理
1     \===/ \/==/               [*] by. (https://github.com/v9d0g/WebFind)
5      \_/  /__/               
```

在挖洞以及渗透测试中，时常出现要对大量资产进行测试，该项目用于实现对大量目标资产的快速存活探测。

经测试，1w左右资产约耗时16分钟：



资源占用情况：



## 配置

仅在使用自动代理`-P`时，需要根据fofa-api配置HTTP-proxy中的email、key。

```yaml
proxy:
    email: ""
    key: ""
    q: 'protocol=="socks5" && "Version:5 Method:No Authentication(0x00)" && country="CN"'
```

自定义存活探测的响应时间以及允许的响应码、协程的并发数。

```yaml
SETTINGS:
  connect: 5
  write: 5
  read: 5
  pool: 5
  allow:
    - 200
    - 301
    - 302
  thread: 100
  number: 50
```

`number`用于指定爬取socks代理时的测试数量。

## 用法

查询指令帮助。

```sh
python webfind.py -H
```

常规存活探测，将需要探测的url保存于url.txt文件中。显示目标web的状态码、title。

```sh
python webfind.py -u url.txt
```

### 参数详解

- 存活保存结果到result.xlsx文件，忽略的状态码以及错误情况保存至error.xlsx文件。

  ```sh
  python webfind.py -u url.txt -S
  ```

- **使用socks5代理。**

  使用`-P`通过fofa获取未授权socks代理保存在proxies.txt文件中，建议从获取的proxies.txt文件中，手动输入`-p`指定代理。

  也可以自己添加可使用的socks代理至proxies.txt中，每次探测将使用该文件中的随机ip。

  ```sh
  # Self
  python webfind.py -u url.txt -p ip:port
  
  # Auto
  python webfind.py -u url.txt -P
  ```

### TODO

1. 对于yaml模板匹配的算法以及优化

   

2. 对于由于负载或者其他情况引起的非状态码显示的404

   

