import smtplib
from email.mime.text import MIMEText

## 构建邮件格式
subject = "0902测试"
content = """
    好好学习，天天向上
"""
## 发送人
sender = "lsj2740@163.com"
## 接收人
recver = "django_ajax@163.com"
password = "l1103602740"   ## 发送人登录邮箱的密码

message = MIMEText(content,"plain","utf-8")
        ##  内容    内容类型    编码
message["Subject"] = subject
message["From"] = sender
message["To"] = recver

## 发送邮件
smtp = smtplib.SMTP_SSL("smtp.163.com", 465)
smtp.login(sender, password)   ## 登录发送人的邮箱
smtp.sendmail(sender, recver, message.as_string())
# sender,  发送人
# recver,   接收人  可以是一个列表 []
# message.as_string()  发送内容
# as_string 类似于json的封装方式，目的是为了在协议上传输发送内容

smtp.close()












