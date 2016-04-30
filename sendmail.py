# coding:utf-8
import smtplib
from email.mime.text import MIMEText
#   收件人列表
mailto_list = ["842794369@qq.com"]
#   设置服务器
mail_host = "smtp.163.com"
#   用户名
mail_user = "fengeric0910"
#   密码
mail_pass = "******"
#   发件箱后缀
mail_postfix = "163.com"
# to_list：收件人；sub：主题；content：邮件内容


def send_mail(to_list, sub, content):
    # 这里的hello可以任意设置，收到信后，将按照设置显示
    me = "fengeric0910@163.com" + "<" + mail_user + "@" + mail_postfix + ">"
    # msg = MIMEText(cobbntent, subtype='html', charset='gb2312')
    # 创建一个实例，这里设置为html格式邮件
    msg = MIMEText(content, _subtype='plain')    # 设置为文本格式邮件
    msg['Subject'] = sub    # 设置主题
    msg['From'] = me
    msg['To'] = ";".join(to_list)  # 将收件人列表以“;”隔开
    try:
        s = smtplib.SMTP()
        s.connect(mail_host)  # 连接smtp服务器
        s.login(mail_user, mail_pass)  # 登陆服务器
        s.sendmail(me, to_list, msg.as_string())  # 发送邮件
        s.close()
        return True
    except Exception, e:
        print str(e)
        return False
