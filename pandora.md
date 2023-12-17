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