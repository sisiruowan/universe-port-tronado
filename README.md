# tornado 接口框架

## 文件说明：
```text
/bin:源码文件-获取用户名demo
    conf.py:配置文件
    log.py:日志模块
    user_server_webmain.py:web服务主文件示例，主要是和web外层服务相关的操作
    user_server_core.py:web服务api文件示例，主要是得到接口参数后调用后台函数的操作
    user_info.py:后台操作类示例，后台逻辑操作，与web框架完全解耦合
/conf:配置文件（需要的话）
/data:数据文件（需要的话）
/test:测试post接口示例代码
```

## 使用方法：
1. 启动服务方法(端口号自定义,启动路径为项目根目录)：
```bash
# 前台启动，主要用于调试
python bin/user_server_webmain.py 1111
# 后台启动
nohup bin/user_server_webmain.py 1111 &
tail -f log/user_server.log # 查看并刷新日志

# 杀死后台进程方法
ps -ef | grep user_server_webmain
kill [对应的pid号]
```

2. 接口调用方法
```bash
# get格式调用，浏览器直接访问（需要安装json_view插件）
http://localhost:1111/in/userinfo/userid?userid=3
# post格式调用，使用python requests类post对应的参数到接口，示例test/post_test.py;或者使用postman软件
```

## 配置&注意事项
1. 配置`user_server_webmain`:
    - 配置log文件路径：`log_path = './log/user_server.log'`
    - 配置url并绑定到`Handler`:
    ```python
    app_inst = web.Application([
            (r'/in/userinfo/userlist', UserListHandler),
            (r'/in/userinfo/userid', UserIdHandler),
        ], compress_response = True)
    ```

2. 配置文件路径一般都是相对路径，注意启动目录的位置，否则容易报错

3. 建议在重要函数入口出口处分别打印日志，并记录耗时，方便日后分析统计
