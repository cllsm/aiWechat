import win32gui
import uiautomation as auto
from tools import *
from config import warn_word
def get_window():
    hwnd = win32gui.FindWindow("TrayNotifywnd", "微信")
    if hwnd == 0:
        print("未找到微信窗口")
        raise Exception("未检测到微信进程！")
    window = auto.WindowControl(searchDepth=1, ClassName="WeChatMainWndForPC", Name="微信")# 设置窗口前置
    # window.SetActive()
    # window.SetTopmost()
    return window
def get_chat_list_panel(window):
    return window.ListControl(name='会话')
def get_chat_text(window):
    chat_list = get_chat_lines(window)
    text = ""
    for tu in chat_list:
        t = __to_text(tu)
        if t is not None:
            t = t.replace(warn_word,"")
            text = text + "\n" + t
    return text
def get_chat_lines(window):
    chat_list = []
    try:
        chat_lines = window.ListControl(Name='消息').GetChildren()
    except:
        chat_lines = window.ListControl(Name='会话').GetChildren()
    for chat_line in chat_lines:
        chat_list.append(__classify_chat_type(chat_line))
    if len(chat_list) > 1:
        chat_list = chat_list[1:]
    return chat_list
def __to_text(tu):
    if tu is None:
        return None
    if tu[0] == "time":
        return "当前时间：" + tu[1]
    elif tu[0] == "nudge":
        return tu[1] + " 拍了拍我"
    elif tu[0] == "recall":
        return tu[1] + " 撤回了一条消息"
    elif tu[0] == "chat":
        return tu[1] + " 说 " + tu[2]
    return None
def __classify_chat_type(chat_line):
    children = chat_line.GetChildren()
    if len(children) == 1 and children[0].ControlTypeName == 'TextControl':
        return "time", children[0].Name, None
    elif find_control_with_text_list(chat_line, ["拍了拍", "tickled"]) is not None:
        return "nudge", find_control_with_text_list(chat_line, ["拍了拍", "tickled"]).Name, None
    elif find_control_with_text_list(chat_line, ["撤回了一条消息", "recalled a message"]) is not None:
        return "recall", find_control_with_text_list(chat_line, ["撤回了一条消息", "recalled a message"]).Name, None
    elif find_control_with_control_type(chat_line, "ButtonControl") is not None:
        return "chat", find_control_with_control_type(chat_line, "ButtonControl").Name, chat_line.Name