import time
from datetime import datetime
from WeChatWindow import *
from trigger import * 
from tools import *
from config import *
from writer import *
from qianwen import *

def chat(chatStatus):
    global window
    global chat_list_panel
    global chat_list
    global notify_list
    global name
    global chat_shot
    global history_message_prompt
    if chatStatus == 'getMessage': # 获取聊天列表
        # 重新获得新消息
        time.sleep(1)
        try:
            window = get_window()    # 获取窗口句柄
        except:
            print("请打开微信窗口，等待微信窗口打开")
            return "getMessage"
        chat_list_panel = get_chat_list_panel(window)
        chat_list = chat_list_panel.GetChildren()
        notify_list = []
        for chat_shot in chat_list:
            if is_notify_with_text(chat_shot):
                name = find_control_with_control_type(chat_shot, "ButtonControl").Name
                if name in name_reply:
                    notify_list.append(chat_shot)
        if len(notify_list) == 0:
            return "getMessage"
        else:
            return "openMessage"
    elif chatStatus == 'openMessage': # 打开聊天列表，获取信息
        for chat_shot_inner  in notify_list:
            name=find_control_with_control_type(chat_shot_inner, "ButtonControl").Name
            if name in name_reply:
                chat_shot = chat_shot_inner
                chat_shot.Click(simulateMove=False, waitTime=1)
                try:
                    window.EditControl(Name=name)
                except:
                # 退回状态2
                    print("打开编辑失败")
                chat_text = get_chat_text(window)
                # history_message_prompt = history_message_prompt_tp.format(name, datetime.now(),chat_text, name)
                history_message_prompt = chat_text
                return "sendMessage"
    elif chatStatus == 'sendMessage': # 发送消息
        msg = get_msg(history_message_prompt)
        print(msg)
        #这里发送消息，可处理之前引入Ai 回答
        # 定义需要移除的子串
        phrase_to_remove = "眼睛睁大大 说"
        # 检查字符串是否包含该子串
        if phrase_to_remove in msg:
            # 移除子串
            msg = msg.replace(phrase_to_remove, "")
            msg.strip()
        try:
            send_msg(name, window,msg)
            fileup = auto.ButtonControl(Name="文件传输助手")
            fileup.Click(simulateMove=False, waitTime=1)
            print("发送成功")
        except Exception as e:
            print("发送失败:", e)
            
        if len(notify_list) <= 1:
            notify_list = []
            return "getMessage"
        else:
            notify_list = notify_list[1:]
            return "openMessage"