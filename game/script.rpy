define draft = Character("Draft", what_prefix="", what_suffix="")
define narrator = Character(None)
define config.window_hide_transition = dissolve
image white = Solid("#e6e6e6")

default name_input = ""
default player_name = "Player"
default plyaer_hobby = ""

default current_tab = "none"
default home_action = NullAction()
default message_action = NullAction()

label start:
    $ script_label = "start"
    jump onboarding_home

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

screen wait_at_home(what):
    # Define screen elements and their actions
    $ script_label = "wait_for_action"
    textbutton "Continue" action Return()
    frame: 
        xsize 400
        ysize gui.textbox_height
        xalign 0.1
        yalign gui.textbox_yalign
        
        background "#f6f6f6"
        text what xalign 0.5 yalign 0.5


label onboarding_home:
    $ script_label = "onboarding_home"
    $ current_tab = "home"
    $ message_action = Jump("onboarding_message")
    $ home_action = NullAction()

    scene white
    show screen draft_at_home
    show screen bottom_nav
    draft "[player_name], 안녕하세요. DRAFT예요."
    call screen wait_at_home("새로운 메시지가 있어요. Message 탭을 확인해보세요.")


label onboarding_message:
    $ script_label = "onboarding_message"
    $ current_tab = "message"
    $ message_action = NullAction()
    $ home_action = NullAction()

    hide screen draft_at_home
    scene white
    show screen bottom_nav
    narrator "메시지를 보내는 법을 알려드릴게요."
    
