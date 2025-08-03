define draft = Character("Draft", what_prefix="", what_suffix="")
define narrator = Character(None)
define config.window_hide_transition = dissolve
image white = Solid("#e6e6e6")

default name_input = ""
default player_name = "Player"
default plyaer_hobby = ""

label start:
    $ script_label = "start"

    scene white
    with dissolve

    narrator "환영합니다. AI 어시스턴트 DRAFT가 당신의 인간관계를 도와드립니다."
    $ name_input = ""
    python: 
        name_input = renpy.input("당신의 이름을 알려주세요.", length=20)
        name_input = name_input.strip()
        player_name = name_input

        hobby_input = renpy.input("당신의 취미는 뭔가요?", length=20)
        hobby_input = hobby_input.strip()

    narrator "사실 전부 알고 있는 내용이에요."
    narrator "하지만 당신의 진짜 이름과 다르네요?"
    narrator "장난이에요."
    jump main

label main:
    $ script_label = "main"


    scene white
    with fade

    "이건 아래쪽에 뜨는 메시지입니다."
