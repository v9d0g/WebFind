# WebFind

```sh
0 ___           _ __ __
x \  \    _    /   __ _/      
7  \  \  / \  /  /_ __       WEB FIND beta_v1.0
7   \  \/ _ \/  _ _ _/       \t批量web存活探测
1    \   / \/  /             \t[*] 自动化代理
5     \_/  /__/              \t[*] 自定义指纹识别
```

**通过多协程的方式对大量url目标进行扫描，可支持socks代理以及自定义模板进行指纹识别。**

Scanning a large number of URL targets through multiple coroutines can support socks agents and custom templates for fingerprint recognition.

## 配置

**在使用自动代理时，需要根据fofa-api配置HTTP-proxy中的email、key。**

When using automatic proxies, it is necessary to configure email and key in HTTP proxy based on fofa API.

```yaml
HTTP:
  headers:
    User-Agent: "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
  cookies: ""
  proxy:
    email: ""
    key: ""
    q: 'protocol=="socks5" && "Version:5 Method:No Authentication(0x00)" && country="CN"'
    url:
```

**自定义存活探测的响应时间以及允许的响应码、协程的并发数。**

Customize the response time and allowed response codes for survival detection.

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
  code: false
  detail: false
  save: false
  proxy: false
```

## 用法

**常规存活探测，将需要探测的url保存于url.txt文件中。**

Conventional alive detection, save the URL that needs to be detected in the url.txt file.

```sh
python webfind.py -u url.txt
```

### 参数详解

- **显示目标web的响应状态码。**

  Display the response status code of the target web.

  ```sh
  python webfind.py -u url.txt -C
  ```

- **与指纹模板进行匹配，并显示目标web的title。**
  Match with fingerprint template and display the title of the target web

  ```sh
  python webfind.py -u url.txt -D
  ```

- **保存结果到output.xlsx文件。**

  Save the results to the output.xlsx file

  ```sh
  python webfind.py -u url.txt -S
  ```

- **使用socks5代理。**

  Use socks5 proxy.

  使用`-P`获取未授权socks代理，建议从获取的proxies.txt文件中，手动输入`-p`指定代理。
  
  ```sh
  # Self
  python webfind.py -u url.txt -p ip:port
  
  # Auto
  python webfind.py -u url.txt -P
  ```

## 指纹

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
