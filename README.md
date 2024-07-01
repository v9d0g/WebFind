# WebFind

```sh
0  ___           _ __ __                
x  \==\    _    /===__ _/      WEB FIND V1.0.2
7   \==\  /=\  /==/_ __        	批量web存活探测
7    \==\/ _ \/==_ _ _/        	[*] 支持socks代理
1     \===/ \/==/              	[*] 自定义指纹识别
5      \_/  /__/               	[*] by. (https://github.com/v9d0g/WebFind)
```

通过多协程的方式对大量url目标进行扫描，目前支持socks代理以及自定义模板进行指纹识别，其余功能待开发。

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

number用于指定爬取socks代理时的测试数量。

## 用法

查询指令帮助。

```sh
python webfind.py -H
```

常规存活探测，将需要探测的url保存于url.txt文件中。

```sh
python webfind.py -u url.txt
```

### 参数详解

- 与指纹模板进行匹配，并显示目标web的标题与响应码。

  ```sh
  python webfind.py -u url.txt -D
  ```

- 保存结果到output.xlsx文件。

  ```sh
  python webfind.py -u url.txt -S
  ```

- **使用socks5代理。**

  使用`-P`通过fofa获取未授权socks代理保存在proxies.txt文件中，建议从获取的proxies.txt文件中，手动输入`-p`指定代理。

  ```sh
  # Self
  python webfind.py -u url.txt -p ip:port
  
  # Auto
  python webfind.py -u url.txt -P
  ```

## 指纹编写

使用python正则判断与或。

```yaml
img:
  src:
    and:
      regular:
        -
    or:
      regular:
        - "^/images/hcm/themes/default/login"
        - "^/hcm/themes/default/login"
```

只要满足其中一项

```html
<img src="xxx/images/hcm/themes/default/login">
<img src="xxx/hcm/themes/default/login">
```

就会被认定为该模板所指指纹

------


```yaml
img:
  src:
    and:
      regular:
        - "^/images/hcm/themes/default/login"
        - "^/hcm/themes/default/login"
    or:
      regular:
```

必须满足全部

```html
<img src="xxx/images/hcm/themes/default/login">
<img src="xxx/hcm/themes/default/login">
```

才会被认定为该模板所指指纹
