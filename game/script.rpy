define draft = Character("Draft", what_prefix="", what_suffix="")
define narrator = Character(None)
define config.window_hide_transition = dissolve
image white = Solid("#FFFFFF")
image black = Solid("#000")
image bg gradient = im.Scale("images/bg_gradient.png", 720, 1600)

default name_input = ""
default player_name = "Player"
default plyaer_hobby = ""

default current_tab = "none"
default home_action = NullAction()
default message_action = NullAction()
default chat_back_action = NullAction()
default message_red_dot = True

label start:
    $ script_label = "start"
    jump onboarding_home    # @DEBUG

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

define chat_character = {
    "draft": {
        "name": "Draft AI",
        "avatar": "gui/avatar_draft.png"
    },
    "mom": {
        "name": "엄마",
        "avatar": "gui/avatar_mom.png"
    },
}

default onboarding_chat_mom_log = [
    { "from": "me", "text": "나 용돈좀." }, 
    { "from": "mom", "text": "밥은 먹었니?" }, 
    { "from": "mom", "text": "문자는 왜 안 보냈어?" }
]

default onboarding_chat_completed = {
    "mom": False
}

label onboarding_home_start:
    $ script_label = "onboarding_home_start"
    $ current_tab = "home"
    $ message_action = Jump("onboarding_message")
    $ home_action = NullAction()

    scene bg gradient
    show screen draft_at_home
    show screen bottom_nav
    show screen home_title

    draft "[player_name], 안녕하세요. DRAFT예요."

    menu:
        "안녕 DRAFT!":
            draft "안녕하세요, [player_name]님!"
        "오늘은 뭐해?":
            draft "오늘은 [player_name]님과 함께하는 날이에요."

    jump onboarding_home

label onboarding_home:
    $ script_label = "onboarding_home"
    $ current_tab = "home"
    $ message_action = Jump("onboarding_message")
    $ home_action = NullAction()

    scene bg gradient
    show screen draft_at_home
    show screen bottom_nav
    show screen home_title

    if all(onboarding_chat_completed.values()):
        # 모든 메시지를 확인했으면 chapter2로 넘어간다.
        draft "모든 메시지를 확인했어요!"
        jump chapter2

    call screen wait_for_action("새로운 메시지가 있어요. Message 탭을 확인해보세요.")

label onboarding_message:
    $ script_label = "onboarding_message"
    $ current_tab = "message"
    $ message_action = NullAction()
    $ home_action = Jump("onboarding_home")

    scene white
    hide screen draft_at_home
    show screen bottom_nav
    $ is_completed = all(onboarding_chat_completed.values())
    $ message_red_dot = is_completed == False

    $ chat_list_data = [
        {
            "id": "onboarding_chat_mom",
            "character": "mom",
            "preview": onboarding_chat_mom_log[-1]["text"],
            "unread": onboarding_chat_completed["mom"] == False
        },
    ]

    call screen chat_list(chat_list_data, wait_for_action=is_completed)
    jump onboarding_home


label onboarding_chat_mom:
    $ script_label = "onboarding_chat_mom"
    $ current_tab = "chat"
    $ chat_back_action = Jump("onboarding_message")

    hide screen bottom_nav
    scene white

    if onboarding_chat_completed["mom"]:
        show screen chat_window(onboarding_chat_mom_log, chat_character["mom"])
        call screen wait_for_action()
    
    show screen chat_window(onboarding_chat_mom_log, chat_character["mom"], menu_open=True)
    menu():
        "미안해요, 지금 답장해요!":
            $ onboarding_chat_mom_log.append({ "from": "me", "text": "미안해요, 지금 답장해요!" })
        "먹었어요! 문자 하려던 참이었어요.":
            $ onboarding_chat_mom_log.append({ "from": "me", "text": "먹었어요! 문자 하려던 참이었어요." })

    show screen chat_window(onboarding_chat_mom_log, chat_character["mom"], menu_open=False)

    call screen wait_for_click()
    $ onboarding_chat_mom_log.append({ "from": "other", "text": "그래, 알았다." })

    $ onboarding_chat_completed["mom"] = True
    call screen wait_for_action()


####### Chapter 2
default acheivement_data = {
    "icon": "gui/avatar_mom.png",
    "description": "당신의 친구와 커피 약속을 잡았어"
}

default chapter2_chat_mom_log = [
    { "from": "me", "text": "나 용돈좀." }, 
    { "from": "mom", "text": "밥은 먹었니?" }, 
    { "from": "mom", "text": "문자는 왜 안 보냈어?" }
]

default chapter2_chat_completed = {
    "mom": False
}

label chapter2:
    $ script_label = "chapter2"
    $ current_tab = "home"
    $ message_action = NullAction()
    $ home_action = NullAction()
    $ message_red_dot = True

    scene white
    with Fade(0.5, 0, 3.0)
    scene bg gradient

    show screen acheivement(acheivement_data)
    show screen home_title
    show screen draft_at_home
    show screen bottom_nav

    draft "좋은 아침이에요!"

label chapter2_home:
    $ script_label = "chapter2_home"
    $ current_tab = "home"
    $ message_action = Jump("chapter2_message")
    $ home_action = NullAction()

    scene bg gradient

    show screen acheivement(acheivement_data)
    show screen home_title
    show screen draft_at_home
    show screen bottom_nav

    call screen wait_for_action("새로운 메시지가 있어요. Message 탭을 확인해보세요.")

label chapter2_message:
    scene white
    $ script_label = "chapter2_message"
    $ current_tab = "message"
    $ message_action = NullAction()
    $ home_action = Jump("chapter2_home")
    show screen bottom_nav
    hide screen draft_at_home

    $ chat_list_data = [
        {
            "id": "chapter2_chat_mom",
            "character": "mom",
            "preview": chapter2_chat_mom_log[-1]["text"],
            "unread": chapter2_chat_completed["mom"] == False
        },
    ]

    $ is_completed = all(chapter2_chat_completed.values())
    $ print("is_completed:", is_completed)
    call screen chat_list(chat_list_data, wait_for_action=is_completed)
    $ message_red_dot = is_completed == False
    $ print("message_red_dot:", message_red_dot)
    jump chapter2_home

label chapter2_chat_mom:
    $ script_label = "chapter2_chat_mom"
    $ current_tab = "chat"
    $ chat_back_action = Jump("chapter2_message")

    hide screen bottom_nav
    hide screen draft_at_home
    scene white

    if chapter2_chat_completed["mom"]:
        show screen chat_window(chapter2_chat_mom_log, chat_character["mom"])
        call screen wait_for_action()

    show screen chat_window(chapter2_chat_mom_log, chat_character["mom"], menu_open=True)
    show screen fake_choice([
        "ì´ê²Œë¬´ìŠ¨ì¼ì•¼",
        "ž„ê°œë°œì¤‘"
    ])

    # 메시지 자동으로 답장하는 연출
    $ chapter2_chat_mom_log.append({ "from": "me", "text": "이건 DRAFT가 보낸 답장" })
    $ renpy.pause(0.5)
    $ chapter2_chat_mom_log.append({ "from": "me", "text": "이건 DRAFT가 보낸 답장" })
    $ renpy.pause(0.5)
    $ chapter2_chat_mom_log.append({ "from": "me", "text": "이건 DRAFT가 보낸 답장" })
    
    call screen wait_for_click()
    show screen chat_window(chapter2_chat_mom_log, chat_character["mom"], menu_open=False)
    $ chapter2_chat_mom_log.append({ "from": "mom", "text": "그래, 알았다." })
    hide screen fake_choice

    $ chapter2_chat_completed["mom"] = True
    call screen wait_for_action()
