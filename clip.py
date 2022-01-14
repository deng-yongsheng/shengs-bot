import win32clipboard as w
import win32con


def get_text():
    """
    获取剪贴板文本
    :return:
    """
    w.OpenClipboard()
    d = w.GetClipboardData(win32con.CF_UNICODETEXT)
    w.CloseClipboard()
    return d


def set_text(astr: str):
    """
    设置剪切板文本
    :param astr:
    :return:
    """
    w.OpenClipboard()
    w.EmptyClipboard()
    w.SetClipboardData(win32con.CF_UNICODETEXT, astr)
    w.CloseClipboard()
