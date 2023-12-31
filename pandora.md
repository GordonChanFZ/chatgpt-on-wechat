## 安装指南
接入Pandora只需要使用pandora反代的baseurl和pk或者fk
baseurl格式是:https://域名/prefix/v1
使用该项目接入pandora，遇到的问题：
1.使用文件助手询问报错，定位到WechatMessage,self.my_msg需要做适当的处理，报错如下：
logger.warn("[WX]get other_user_id failed: " + str(e))
修改self.my_msg
```python
# 增加文件助手
            self.my_msg = itchat_msg["ToUserName"] != "filehelper" and \
                          itchat_msg["ToUserName"] == itchat_msg["User"]["UserName"] and \
                          itchat_msg["ToUserName"] != itchat_msg["FromUserName"]
```
2.机器人返回前缀报错为error，定位ChatGPTBot，
```python
                if reply_content["completion_tokens"] == 0 and len(reply_content["content"]) > 0:
                    reply = Reply(ReplyType.ERROR, reply_content["content"])
                elif reply_content["completion_tokens"] > 0:
                    self.sessions.session_reply(reply_content["content"], session_id, reply_content["total_tokens"])
                    reply = Reply(ReplyType.TEXT, reply_content["content"])
                else:
                    reply = Reply(ReplyType.ERROR, reply_content["content"])
                    logger.debug("[CHATGPT] reply {} used 0 tokens.".format(reply_content))
```
pandora reply_content["completion_tokens"] == 0 故返回ReplyType.ERROR,修改为
```python
#pandora reply_content["completion_tokens"] == 0 故返回ReplyType.ERROR
            if reply_content["pandora"] is None:
                #之前的模型返回处理
                if reply_content["completion_tokens"] == 0 and len(reply_content["content"]) > 0:
                    reply = Reply(ReplyType.ERROR, reply_content["content"])
                elif reply_content["completion_tokens"] > 0:
                    self.sessions.session_reply(reply_content["content"], session_id, reply_content["total_tokens"])
                    reply = Reply(ReplyType.TEXT, reply_content["content"])
                else:
                    reply = Reply(ReplyType.ERROR, reply_content["content"])
                    logger.debug("[CHATGPT] reply {} used 0 tokens.".format(reply_content))
            else:#Pandora返回处理
                self.sessions.session_reply(reply_content["content"], session_id, reply_content["total_tokens"])
                reply = Reply(ReplyType.TEXT, reply_content["content"])
```
reply_content["pandora"]在reply_text函数中进行判断传值
```python
return {
                "total_tokens": response["usage"]["total_tokens"],
                "completion_tokens": response["usage"]["completion_tokens"],
                "content": response.choices[0]["message"]["content"],
                "pandora": "pandora" if str(conf().get('open_ai_api_key')).startswith("fk-") or str(conf().get('open_ai_api_key')).startswith("pk-") else None
            }
```
## 微信机器人使用指南

### 1.认证和帮助

如果没有设置命令，在命令行日志中会打印出本次的临时口令，请注意观察，打印格式如下。

```
[INFO][2023-04-06 23:53:47][godcmd.py:165] - [Godcmd] 因未设置口令，本次的临时口令为0971。
```

在私聊中可使用`#auth`指令，输入口令进行管理员认证。更多详细指令请输入`#help`查看帮助文档：

`#auth <口令>` - 管理员认证，仅可在私聊时认证。
`#help` - 输出帮助文档，**是否是管理员**和是否是在群聊中会影响帮助文档的输出内容。

### 2.切换gemini模型
-config.json 中增加 gemini_api_key 配置，从官网获取 
```
#机器人端重新加载，不需要重启应用
#reconf  
#model gemini  
```
gemini体验对话，问今天是几号，回答不是今天的日期，而且每次回答的都不一样
```shell
[INFO][2023-12-18 08:55:22][google_gemini_bot.py:33] - [Gemini] query=今天是几号
[INFO][2023-12-18 08:55:25][google_gemini_bot.py:42] - [Gemini] reply=今天是 **2023年3月8日，星期三**。

[INFO][2023-12-18 08:56:35][google_gemini_bot.py:33] - [Gemini] query=今天是几号？
[INFO][2023-12-18 08:56:38][google_gemini_bot.py:42] - [Gemini] reply=今天是 **2023年4月20日，星期四**。

[INFO][2023-12-18 08:56:58][google_gemini_bot.py:33] - [Gemini] query=鲁迅和周树人是同一个人吗
[INFO][2023-12-18 08:57:02][google_gemini_bot.py:42] - [Gemini] reply=是的，鲁迅和周树人是同一个人。

鲁迅是周树人的笔名，他于1881年9月25日出生于浙江绍兴。他是一位著名的作家、思想家和革命家，也是现代文学的奠基人之一。

鲁迅一生创作了大量的小说、散文、杂文和诗歌，他的作品以深刻的思想性和犀利的批判性著称。代表作有小说集《呐喊》和《彷徨》，散文集《朝花夕拾》，杂文集《坟》和《热风》，以及长篇小说《阿Q正传》等。

周树人这个名字主要用于鲁迅的学术研究和官方文件。鲁迅这个笔名则主要用于他的文学创作和社会活动。

因此，鲁迅和周树人是同一个人，只不过鲁迅是他的笔名，而周树人是他的本名。
[INFO][2023-12-18 08:57:03][wechat_channel.py:191] - [WX] sendMsg=Reply(type=TEXT, content=@萧萧下
是的，鲁迅和周树人是同一个人。

鲁迅是周树人的笔名，他于1881年9月25日出生于浙江绍兴。他是一位著名的作家、思想家和革命家，也是现代文学的奠基人之一。

鲁迅一生创作了大量的小说、散文、杂文和诗歌，他的作品以深刻的思想性和犀利的批判性著称。代表作有小说集《呐喊》和《彷徨》，散文集《朝花夕拾》，杂文集《坟》和《热风》，以及长篇小说《阿Q正传》等。

周树人这个名字主要用于鲁迅的学术研究和官方文件。鲁迅这个笔名则主要用于他的文学创作和社会活动。

因此，鲁迅和周树人是同一个人，只不过鲁迅是他的笔名，而周树人是他的本名。

```
附指令集
```python
# 定义指令集
COMMANDS = {
    "help": {
        "alias": ["help", "帮助"],
        "desc": "回复此帮助",
    },
    "helpp": {
        "alias": ["help", "帮助"],  # 与help指令共用别名，根据参数数量区分
        "args": ["插件名"],
        "desc": "回复指定插件的详细帮助",
    },
    "auth": {
        "alias": ["auth", "认证"],
        "args": ["口令"],
        "desc": "管理员认证",
    },
    "model": {
        "alias": ["model", "模型"],
        "desc": "查看和设置全局模型",
    },
    "set_openai_api_key": {
        "alias": ["set_openai_api_key"],
        "args": ["api_key"],
        "desc": "设置你的OpenAI私有api_key",
    },
    "reset_openai_api_key": {
        "alias": ["reset_openai_api_key"],
        "desc": "重置为默认的api_key",
    },
    "set_gpt_model": {
        "alias": ["set_gpt_model"],
        "desc": "设置你的私有模型",
    },
    "reset_gpt_model": {
        "alias": ["reset_gpt_model"],
        "desc": "重置你的私有模型",
    },
    "gpt_model": {
        "alias": ["gpt_model"],
        "desc": "查询你使用的模型",
    },
    "id": {
        "alias": ["id", "用户"],
        "desc": "获取用户id",  # wechaty和wechatmp的用户id不会变化，可用于绑定管理员
    },
    "reset": {
        "alias": ["reset", "重置会话"],
        "desc": "重置会话",
    },
}

ADMIN_COMMANDS = {
    "resume": {
        "alias": ["resume", "恢复服务"],
        "desc": "恢复服务",
    },
    "stop": {
        "alias": ["stop", "暂停服务"],
        "desc": "暂停服务",
    },
    "reconf": {
        "alias": ["reconf", "重载配置"],
        "desc": "重载配置(不包含插件配置)",
    },
    "resetall": {
        "alias": ["resetall", "重置所有会话"],
        "desc": "重置所有会话",
    },
    "scanp": {
        "alias": ["scanp", "扫描插件"],
        "desc": "扫描插件目录是否有新插件",
    },
    "plist": {
        "alias": ["plist", "插件"],
        "desc": "打印当前插件列表",
    },
    "setpri": {
        "alias": ["setpri", "设置插件优先级"],
        "args": ["插件名", "优先级"],
        "desc": "设置指定插件的优先级，越大越优先",
    },
    "reloadp": {
        "alias": ["reloadp", "重载插件"],
        "args": ["插件名"],
        "desc": "重载指定插件配置",
    },
    "enablep": {
        "alias": ["enablep", "启用插件"],
        "args": ["插件名"],
        "desc": "启用指定插件",
    },
    "disablep": {
        "alias": ["disablep", "禁用插件"],
        "args": ["插件名"],
        "desc": "禁用指定插件",
    },
    "installp": {
        "alias": ["installp", "安装插件"],
        "args": ["仓库地址或插件名"],
        "desc": "安装指定插件",
    },
    "uninstallp": {
        "alias": ["uninstallp", "卸载插件"],
        "args": ["插件名"],
        "desc": "卸载指定插件",
    },
    "updatep": {
        "alias": ["updatep", "更新插件"],
        "args": ["插件名"],
        "desc": "更新指定插件",
    },
    "debug": {
        "alias": ["debug", "调试模式", "DEBUG"],
        "desc": "开启机器调试日志",
    },
}
```