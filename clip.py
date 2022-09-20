import platform
import subprocess
WIN = False
plat = platform.system()
if plat == "Windows":
    WIN = True
if WIN:
    import win32clipboard as wc
    import win32con

def set_clip(data):
    if WIN:
        wc.OpenClipboard()
        try:
            wc.EmptyClipboard()
            copy_text = wc.SetClipboardText(data)
        except:
            traceback.print_exc()
        finally:
            wc.CloseClipboard()
        return
    p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
    p.stdin.write(data.encode(sys.stdout.encoding))
    p.stdin.close()
    p.communicate()


def get_clip():
    copy_text = None
    if WIN:
        wc.OpenClipboard()
        try:
            copy_text = str(wc.GetClipboardData(win32con.CF_UNICODETEXT))
        except:
            traceback.print_exc()
        finally:
            wc.CloseClipboard()
        copy_text= copy_text
    if not copy_text:
        p = subprocess.Popen(['pbpaste'], stdout=subprocess.PIPE)
        retcode = p.wait()
        copy_text = p.stdout.read()
    return copy_text
