define draft = Character("Draft", what_prefix="", what_suffix="")
define narrator = Character(None, window_background="#f6f6f6", window_xalign=0.5, window_yalign=0.5, window_xsize=500, window_ysize=160)
define config.window_hide_transition = dissolve
image white = Solid("#e6e6e6")

label start:
    scene white
    with dissolve
    narrator "새로 산 핸드폰을 켜자, 알 수 없는 앱이 자동 실행되었다."
    draft "안녕하세요. 주인님."
    menu:
        "안녕?":
            jump respond_gently

label respond_gently:
    draft "반응해주셔서 기쁘네요. 앞으로는 제가 도와드릴게요."
    return
