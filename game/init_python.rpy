init python:
    def scroll_to_bottom():
        try:
            vp = renpy.get_displayable("chat_window", "chat_vp")
            if vp:
                adj = getattr(vp, "yadjustment", None)
                if adj:
                    adj.value = 50000   # 충분히 큰 값으로 설정
                else:
                    print("viewport has no yadjustment")
        except Exception as e:
            print("scroll error:", e)
    
    def add_chat(chat_log, chat):
        chat_log.append(chat)
        scroll_to_bottom()
        

    import platform
    import os
    import subprocess

    def os_noti(title, message):
        if platform.system() == "Darwin":
            return macos_noti(title, message)
        elif platform.system() == "Windows":
            return None
        
    def os_alert(title, message, yes_label="예", no_label=None, type="informational", no_wait=False):
        if platform.system() == "Darwin":
            return macos_alert(title, message, yes_label, no_label, type, no_wait)
        elif platform.system() == "Windows":
            return None

    def macos_noti(title, message):
        try:
            subprocess.run(["osascript", "-e", f'display notification "{message}" with title "{title}" sound name "Glass"'])
        except subprocess.CalledProcessError as e:
            print("Error displaying notification:", e)
            return None

    def macos_alert(title, message, yes_label="예", no_label=None, type="informational", no_wait=False):
        buttons = f'{{"{no_label}", "{yes_label}"}}' if no_label else f'{{"{yes_label}"}}'
        script = f'''
        display alert "{title}" message "{message}" as {type} buttons {buttons} default button "{yes_label}"
        '''
        try:
            if no_wait:
                # 비동기 처리
                subprocess.Popen(["osascript", "-e", script])
                return None
            else:
                # 동기 처리
                result = subprocess.run(
                    ["osascript", "-e", script],
                    text=True,
                    capture_output=True,
                    check=True
                )
                # 사용자가 누른 버튼 텍스트 추출
                if f'button returned:{yes_label}' in result.stdout:
                    return True
                else:
                    return False
        except subprocess.CalledProcessError as e:
            print("Error os alert:", e)
            return None
    
    def get_os_username(hack=False):
        if hack:
            return "하영 정"
        username = os.getenv('USER') or os.getenv('USERNAME')
        if username: return username
        return False

