# Python 테스트용

import subprocess
import platform

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
        print("오류 발생:", e)
        return None


import os

def get_os_username(hack=False):
    if hack:
        return "하영 정"
    username = os.getenv('USER') or os.getenv('USERNAME')
    if username: return username
    return False


macos_alert("DRAFT", "DRAFT가 시작되었습니다. DRAFT는 당신의 인간관계를 도와주는 앱입니다.", yes_label="시작시작하기시작하기시작하기시작하기시작하기시작하기시작하기시작하기하기", no_label="나중에", type="informational")
