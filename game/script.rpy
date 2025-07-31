define draft = Character("Draft", window_background=None, what_prefix="", what_suffix="")
define me = Character("나", window_background=None, what_prefix="", what_suffix="")
define config.window_hide_transition = dissolve

label start:

    scene white
    with dissolve

    "새로 산 핸드폰을 켜자, 알 수 없는 앱이 자동 실행되었다."

    draft "안녕하세요. 주인님."

    menu:
        "대답한다":
            me "...안녕?"
            jump respond_gently

        "무시한다":
            "..."
            jump ignore_ai

label respond_gently:
    draft "반응해주셔서 기쁘네요. 앞으로는 제가 도와드릴게요."
    return

label ignore_ai:
    draft "아무 말도 없으시군요. 그럼, 제가 먼저 시작할게요."
    return
