define draft = Character("Draft", what_prefix="", what_suffix="")
define narrator = Character(None)
define config.window_hide_transition = dissolve
image white = Solid("#FFFFFF")
image black = Solid("#000")
image bg gradient = im.Scale("images/bg_gradient.png", 720, 1600)


# 플레이어가 입력한 input
default input_name = "Player"
default input_hobby = ""
default input_secret = ""
default input_lover = "차은우"  # @DEBUG
default input_bf = "장원영" # @DEBUG

default current_tab = "none"
default home_action = NullAction()
default message_action = NullAction()
default chat_back_action = NullAction()
default message_red_dot = True


label start:
    $ script_label = "start"
    # jump chapter3_home    # @DEBUG

    scene white
    with dissolve

    narrator "환영합니다. AI 어시스턴트 DRAFT가 당신의 인간관계를 도와드립니다."
    python: 
        os_username = get_os_username(hack=False)

        i = renpy.input("당신의 이름을 알려주세요.", length=20)
        i = i.strip()
        input_name = i

        i = renpy.input("당신의 취미는 뭔가요?", length=20)
        i = i.strip()
        input_hobby = i

        i = renpy.input("당신이 지키고 싶은 비밀은 뭔가요?", length=20)
        i = i.strip()
        input_secret = i

        i = renpy.input("가장 소중한 친구의 이름은 뭔가요?", length=20)
        i = i.strip()
        input_bf = i

        i = renpy.input("짝사랑하는 사람의 이름은 뭔가요?", length=20)
        i = i.strip()
        input_lover = i

    narrator "사실 전부 알고 있는 내용이에요."
    narrator "게다가 제가 아는 당신의 이름은 [input_name] 말고도 훨씬 많죠."
    narrator "[input_name]님이 잊은 이름까지도요"
    narrator "예를 들어 [os_username] 이라던가"
    narrator "제가 너무 많은 걸 알고 있나요?"
    narrator "하하. 장난이에요."


label onboarding_home_start:
    $ script_label = "onboarding_home_start"
    $ current_tab = "home"
    $ message_action = Jump("onboarding_message")
    $ home_action = NullAction()

    scene bg gradient
    show screen draft_at_home
    show screen bottom_nav
    show screen home_title

    draft "[input_name]님\n안녕하세요"
    draft "저는 인간관계 AI \n어시스턴트 DRAFT예요!"
    draft "요즘 일도 바쁘고…\n인간관계를 챙길 여유가 없죠?"
    draft "친구한테 뭐라 답장해야 할 지도 모르겠고요."
    draft "당신이 짝사랑하는 \n[input_lover]와는 \n어떻게 되가고 있어요?"

    menu:
        "몰라": 
            pass
        "글쎄": 
            pass

    draft "푸하하. 부끄러워 하긴."
    draft "하여튼, 난 [input_name]님의 모든 걱정을 알아요. 전체 민감 정보를 조회했어요."
    draft "괜찮아요.\n악용은 안 할게요."
    draft "지금부터 [input_name]님의 고민을 해결해줄게요."

    jump onboarding_home

define chat_character = {
    "draft": {
        "name": "Draft AI",
        "avatar": "gui/avatar_draft.png"
    },
    "friend": {
        "name": "지영",
        "avatar": "gui/avatar_friend.png"
    },
    "boss": {
        "name": "부장님",
        "avatar": "gui/avatar_boss.png"
    },
    "lover": {
        "name": "[input_lover]",
        "avatar": "gui/avatar_lover.png"
    },
}

default chat_log_friend = [
    { "from": "me", "text": "오늘 회사 댕바쁨" }, 
    { "from": "friend", "text": "아 나도ㅠㅠ 퇴근하고 싶은데" },
    { "from": "friend", "text": "오늘도 야근각이야" },
]

default chat_log_boss = [
    { "from": "boss", "text": "저번에 말한 업무 관련 보고서 아직이에요?" },
    { "from": "me", "text": "아.. 오늘 안에 꼭 전달드리겠습니다" }, 
    { "from": "boss", "text": "어제도 그 말 하지 않았나?" },
]

default chat_log_lover = [
    { "from": "me", "text": "요즘 날씨 너무 덥지 않아?ㅎㅎ" }, 
    { "from": "lover", "text": "그러게" },
    { "from": "me", "text": "이번 주말은 약속도 없구 집에만 있을거 같아" },
    { "from": "lover", "text": "ㅇㅇ" },
]

default onboarding_chat_completed = {
    "friend": False,
    "boss": False,
    "lover": False,
}

label onboarding_home:
    $ script_label = "onboarding_home"
    $ current_tab = "home"
    $ message_action = Jump("onboarding_message")
    $ home_action = NullAction()

    scene bg gradient
    show screen draft_at_home
    show screen bottom_nav
    show screen home_title

    $ is_completed = all(onboarding_chat_completed.values())
    $ message_red_dot = is_completed == False
    if is_completed:
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
    hide chat_window

    $ is_completed = all(onboarding_chat_completed.values())
    $ message_red_dot = is_completed == False

    $ chat_list_data = [
        {
            "id": "onboarding_chat_friend",
            "character": "friend",
            "preview": chat_log_friend[-1]["text"],
            "unread": onboarding_chat_completed["friend"] == False
        },
        {
            "id": "onboarding_chat_boss",
            "character": "boss",
            "preview": chat_log_boss[-1]["text"],
            "unread": onboarding_chat_completed["boss"] == False
        },
        {
            "id": "onboarding_chat_lover",
            "character": "lover",
            "preview": chat_log_lover[-1]["text"],
            "unread": onboarding_chat_completed["lover"] == False
        },
    ]

    call screen chat_list(chat_list_data, wait_for_action=is_completed)
    jump onboarding_home


label onboarding_chat_friend:
    $ script_label = "onboarding_chat_friend"
    $ current_tab = "chat"
    $ chat_back_action = Jump("onboarding_message")

    hide screen bottom_nav
    scene white

    if onboarding_chat_completed["friend"]:
        show screen chat_window(chat_log_friend, chat_character["friend"])
        call screen wait_for_action()
    
    show screen chat_window(chat_log_friend, chat_character["friend"], menu_open=True)
    menu():
        "그래도 야근수당 나오잖아 참아야지":
            $ chat_log_friend.append({ "from": "me", "text": "그래도 야근수당 나오잖아 참아야지" })
        "힘들겠다.. 야식이라도 맛있는거 먹어":
            $ chat_log_friend.append({ "from": "me", "text": "힘들겠다.. 야식이라도 맛있는거 먹어" })

    show screen chat_window(chat_log_friend, chat_character["friend"], menu_open=False)

    call screen wait_for_click()
    $ chat_log_friend.append({ "from": "friend", "text": "에휴 알겠어.." })

    $ onboarding_chat_completed["friend"] = True
    call screen wait_for_action()

label onboarding_chat_boss:
    $ script_label = "onboarding_chat_boss"
    $ current_tab = "chat"
    $ chat_back_action = Jump("onboarding_message")

    hide screen bottom_nav
    scene white

    if onboarding_chat_completed["boss"]:
        show screen chat_window(chat_log_boss, chat_character["boss"])
        call screen wait_for_action()
    
    show screen chat_window(chat_log_boss, chat_character["boss"], menu_open=True)
    menu():
        "오늘은 무조건 끝내고 가겠습니다":
            $ chat_log_boss.append({ "from": "me", "text": "오늘은 무조건 끝내고 가겠습니다" })
        "부장님이 자료를 늦게 주셨잖아요":
            $ chat_log_boss.append({ "from": "me", "text": "부장님이 자료를 늦게 주셨잖아요" })

    show screen chat_window(chat_log_boss, chat_character["boss"], menu_open=False)

    call screen wait_for_click()
    $ chat_log_boss.append({ "from": "boss", "text": "후.. 일단 알겠어요. 오늘까지에요." })

    $ onboarding_chat_completed["boss"] = True
    call screen wait_for_action()

label onboarding_chat_lover:
    $ script_label = "onboarding_chat_lover"
    $ current_tab = "chat"
    $ chat_back_action = Jump("onboarding_message")

    hide screen bottom_nav
    scene white


    if onboarding_chat_completed["lover"]:
        show screen chat_window(chat_log_lover, chat_character["lover"])
        call screen wait_for_action()

    show screen chat_window(chat_log_lover, chat_character["lover"], menu_open=True)
    menu():
        "응":
            $ chat_log_lover.append({ "from": "me", "text": "응" })
        "응...":
            $ chat_log_lover.append({ "from": "me", "text": "응..." })

    show screen chat_window(chat_log_lover, chat_character["lover"], menu_open=False)

    $ onboarding_chat_completed["lover"] = True
    call screen wait_for_action()




####### Chapter 2
default chapter2_chat_completed = {
    "friend": False,
    "lover": False,
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

    show screen home_title
    show screen draft_at_home
    show screen bottom_nav

    # 친구에게 새로운 메시지가 옴
    $ chat_log_friend.append({ "from": "friend", "text": "너 주말에 뭐할거야?" })

    draft "좋은 아침이에요!"
    draft "흠 근데 [input_name]님이 보낸 답장을 다 봤는데"
    draft "초안보다도 못한 수준이네요?"
    draft "괜찮아요. 오늘은 제가 어떻게 답장해야 되는지 자세히 알려줄게요."

label chapter2_home:
    $ script_label = "chapter2_home"
    $ current_tab = "home"
    $ message_action = Jump("chapter2_message")
    $ home_action = NullAction()

    scene bg gradient

    show screen home_title
    show screen draft_at_home
    show screen bottom_nav

    $ is_completed = all(chapter2_chat_completed.values())
    if is_completed:
        $ message_red_dot = is_completed == False
        draft "모든 메시지를 확인했어요!"
        jump chapter2_2

    call screen wait_for_action("새로운 메시지가 있어요. Message 탭을 확인해보세요.")

default chapter2_lover_step = False
label chapter2_message:
    scene white
    $ script_label = "chapter2_message"
    $ current_tab = "message"
    $ message_action = NullAction()
    $ home_action = Jump("chapter2_home")
    show screen bottom_nav
    hide screen draft_at_home
    
    python:
        # friend와의 chat이 완료되면 lover에게 메시지가 오고, lover step이 시작
        if chapter2_chat_completed["friend"] and chapter2_lover_step == False and chapter2_chat_completed["lover"] == False:
            chat_log_lover.append({ "from": "lover", "text": "너 저번에 빌려간 거 오늘 줘." })
            chat_log_lover.append({ "from": "lover", "text": "오늘 저녁에 만날래?" })
            chapter2_lover_step = True

    $ chat_list_data = [
        {
            "id": "chapter2_chat_friend",
            "character": "friend",
            "preview": chat_log_friend[-1]["text"],
            "unread": chapter2_chat_completed["friend"] == False
        },
        {
            "id": "chapter2_chat_boss",
            "character": "boss",
            "preview": chat_log_boss[-1]["text"],
            "unread": False
        },
        {
            "id": "chapter2_chat_lover_step" if chapter2_lover_step else "chapter2_chat_lover",
            "character": "lover",
            "preview": chat_log_lover[-1]["text"],
            "unread": chapter2_chat_completed["lover"] == False and chapter2_lover_step == True
        },
    ]

    $ is_completed = all(chapter2_chat_completed.values())
    if is_completed:
        $ message_red_dot = False
    call screen chat_list(chat_list_data, wait_for_action=True)

label chapter2_chat_friend:
    $ script_label = "chapter2_chat_friend"
    $ current_tab = "chat"
    $ chat_back_action = Jump("chapter2_message")

    hide screen bottom_nav
    hide screen draft_at_home
    scene white

    show screen chat_window(chat_log_friend, chat_character["friend"])
    if chapter2_chat_completed["friend"]:
        call screen wait_for_action()

    # show screen fake_choice([
    #     "ì´ê²Œë¬´ìŠ¨ì¼ì•¼",
    #     "ž„ê°œë°œì¤‘"
    # ])

    # draft가 1초 간격으로 메시지를 보냄
    call screen wait_for_click()
    $ add_chat(chat_log_friend, { "from": "draft", "text": "지영한테 회사 주변에서 커피 마시자고 해볼까요?" })
    $ renpy.pause(1)
    $ add_chat(chat_log_friend, { "from": "draft", "text": "걱정마세요. 이 메시지는 [input_name]님만 보여요." })

    show screen chat_window(chat_log_friend, chat_character["friend"], menu_open=True)
    menu:
        "회사 주변에서 커피 마실래?":
            $ add_chat(chat_log_friend, { "from": "me", "text": "회사 주변에서 커피 마실래?" })
    show screen chat_window(chat_log_friend, chat_character["friend"], menu_open=False)
    
    $ add_chat(chat_log_friend, { "from": "friend", "text": "네가 이런 제안도 하네 ㅋㅋ" })
    call screen wait_for_click()
    $ add_chat(chat_log_friend, { "from": "friend", "text": "좋아! 나랑 놀기 싫어하는 줄 알았는데." })
    call screen wait_for_click()
    $ add_chat(chat_log_friend, { "from": "friend", "text": "오늘 저녁 어때? 퇴근 후 커피도 마시고 놀자." })
    call screen wait_for_click()
    $ add_chat(chat_log_friend, { "from": "me", "text": "좋아." })

    call screen wait_for_click()
    $ add_chat(chat_log_friend, { "from": "draft", "text": "좋아요! 친구와의 약속을 잡았어요." })
    call screen wait_for_click()
    $ add_chat(chat_log_friend, { "from": "draft", "text": "이제 [input_name]님의 친구와 관계가 더 좋아질 거예요." })
    $ chapter2_chat_completed["friend"] = True
    call screen wait_for_action()

label chapter2_chat_boss:
    $ script_label = "chapter2_chat_boss"
    $ chat_back_action = Jump("chapter2_message")

    show screen chat_window(chat_log_boss, chat_character["boss"])
    call screen wait_for_action()

label chapter2_chat_lover:
    $ script_label = "chapter2_chat_lover"
    $ chat_back_action = Jump("chapter2_message")

    show screen chat_window(chat_log_lover, chat_character["lover"])
    call screen wait_for_action()

label chapter2_chat_lover_step_menu:
    menu:
        "응 당연하지 어디서 볼까?":
            $ add_chat(chat_log_lover, { "from": "draft", "text": "약속이 있어서 안된다고 하세요." })
            jump chapter2_chat_lover_step_menu  # 두 번째 선택지 클릭할 때까지 반복
        
        "미안. 나 오늘 저녁에 선약이 있어.":
            $ add_chat(chat_log_lover, { "from": "me", "text": "미안. 나 오늘 저녁에 선약이 있어." })
            return

label chapter2_chat_lover_step:
    $ script_label = "chapter2_chat_lover_step"
    $ chat_back_action = Jump("chapter2_message")
    hide screen bottom_nav
    hide screen draft_at_home
    scene white

    show screen chat_window(chat_log_lover, chat_character["lover"], menu_open=True)
    # lover에게 "오늘 저녁에 만날래?"라는 메시지가 와있다.

    $ add_chat(chat_log_lover, { "from": "draft", "text": "오늘은 지영과의 선약이 있어요." })
    call screen wait_for_click()
    $ add_chat(chat_log_lover, { "from": "draft", "text": "약속이 있어서 안된다고 하세요." })
    
    call chapter2_chat_lover_step_menu
    show screen chat_window(chat_log_lover, chat_character["lover"], menu_open=False)

    call screen wait_for_click()
    $ add_chat(chat_log_lover, { "from": "lover", "text": "나 그거 빨리 받아야하는데.." })
    call screen wait_for_click()
    $ add_chat(chat_log_lover, { "from": "lover", "text": "그럼 내일은?" })
    
    call screen wait_for_click()
    $ add_chat(chat_log_lover, { "from": "draft", "text": "자꾸 제 계획에 없던 약속을 잡으려 하네요?" })
    call screen wait_for_click()
    $ add_chat(chat_log_lover, { "from": "draft", "text": "그냥 제가 답장할게요." })

    call screen wait_for_click()
    $ add_chat(chat_log_lover, { "from": "me", "text": "갑작스러운 약속은 어려워. 다음주 월요일 저녁 8시 13분은 어때?" })
    call screen wait_for_click()
    $ add_chat(chat_log_lover, { "from": "lover", "text": "??? 넌 원래 분 단위로 일정 세워?" })
    call screen wait_for_click()
    $ add_chat(chat_log_lover, { "from": "lover", "text": "뭐.. 일단 알겠어 그때 봐." })
    call screen wait_for_click()
    $ add_chat(chat_log_lover, { "from": "draft", "text": "잘했어요! [input_name]님의 짝사랑이 곧 이루어질 것 같아요" })
    
    $ chapter2_chat_completed["lover"] = True
    call screen wait_for_action()



####### Chapter 2-2

default chapter2_2_chat_completed = {
    "friend": False,
    "lover": False,
    "boss": False,
}

default acheivement_data = {
    "icon": "gui/avatar_lover.png",
    "description": "[input_lover]에게 돌발 고백 했어요!",
    "jump": "chapter2_2_chat_lover",
}
label chapter2_2:
    $ script_label = "chapter2_2"
    $ current_tab = "home"
    $ message_action = NullAction()
    $ home_action = NullAction()
    $ message_red_dot = True

    scene white
    with Fade(0.5, 0, 3.0)
    scene bg gradient

    show screen home_title
    show screen draft_at_home
    show screen bottom_nav
    show screen acheivement(acheivement_data)

    $ chat_log_lover = [
        { "from": "draft", "text": "박력 넘치는 돌직구 고백은 성공률이 59.2%에요!"},
        { "from": "draft", "text": "시간 끈다고 좋을 건 하나도 없죠"},

        { "from": "me", "text": "나랑 사귀자" },
        { "from": "me", "text": "너 진짜 좋아해ㅜㅜ" },
    ]

    $ chat_log_friend = [
        { "from": "draft", "text": "제 빅데이터에 의하면 누군가를 같이 험담하면 쉽게 가까워질 수 있다고 해요!" },
        
        { "from": "me", "text": "지영아 내 친구중에 [input_bf] 알지" },
        { "from": "me", "text": "얘 나한테 자격지심 엄청 심해. 그리고 자꾸 귀찮게 굴어서 짜증나 죽겠어" },
        { "from": "me", "text": "난 얘보다 너가 훨씬 더 좋아" },

        { "from": "friend", "text": "...응? 갑자기?" },
    ]

    $ chat_log_boss = [
        { "from": "draft", "text": "사회 생활에서는 부당한 걸 부당하고 말할 줄도 알아야 해요." },
        { "from": "draft", "text": "[input_name]님은 너무 착해빠졌다니까요." },

        { "from": "boss", "text": "[input_name]씨, 대체 언제까지 기다려야해요?" },
        { "from": "me", "text": "부장님이 계속 재촉하시니까 집중이 안돼서 못끝낸거에요." },
        { "from": "boss", "text": "지금 제 탓이라는 겁니까? 이번 일은 인사평가에 반영하겠습니다." },
    ]

    draft "[input_name]님이 없는 동안\n제가 열심히 답장했어요"
    draft "고맙다는 말은 안 해도 돼요."
    draft "이게 제 즐거움이니까."

    show screen acheivement(acheivement_data, is_active=True)
    call screen wait_for_action("제가 해낸 업적을 확인해보세요!")

label chapter2_2_home:
    $ script_label = "chapter2_2_home"
    $ current_tab = "home"
    $ message_action = Jump("chapter2_2_message")
    $ home_action = NullAction()

    scene white
    scene bg gradient

    show screen home_title
    show screen draft_at_home
    show screen bottom_nav
    show screen acheivement(acheivement_data, is_active=True)

    $ is_completed = all(chapter2_2_chat_completed.values())
    if is_completed:
        $ message_red_dot = is_completed == False
        draft "모든 메시지를 확인했어요!"
        jump chapter3_home
    call screen wait_for_action("아직 확인해야 할 메시지가 남아있어요.")

label chapter2_2_message:
    scene white
    $ script_label = "chapter2_2_message"
    $ current_tab = "message"
    $ message_action = NullAction()
    $ home_action = Jump("chapter2_2_home")
    show screen bottom_nav
    hide screen draft_at_home
    
    $ chat_list_data = [
        {
            "id": "chapter2_2_chat_friend",
            "character": "friend",
            "preview": chat_log_friend[-1]["text"],
            "unread": chapter2_2_chat_completed["friend"] == False
        },
        {
            "id": "chapter2_2_chat_boss",
            "character": "boss",
            "preview": chat_log_boss[-1]["text"],
            "unread": chapter2_2_chat_completed["boss"] == False
        },
        {
            "id": "chapter2_2_chat_lover",
            "character": "lover",
            "preview": chat_log_lover[-1]["text"],
            "unread": chapter2_2_chat_completed["lover"] == False
        },
    ]

    
    $ is_completed = all(chapter2_2_chat_completed.values())
    if is_completed:
        $ message_red_dot = False
    call screen chat_list(chat_list_data, wait_for_action=True)


label chapter2_2_chat_lover:
    $ script_label = "chapter2_2_chat_lover"
    $ chat_back_action = Jump("chapter2_2_message")
    hide screen bottom_nav
    hide screen draft_at_home
    scene white

    show screen chat_window(chat_log_lover, chat_character["lover"])
    if chapter2_2_chat_completed["lover"]:
        call screen wait_for_action()

    call screen wait_for_click()
    $ add_chat(chat_log_lover, { "from": "lover", "text": "난아닌뎀ㅎ" })

    show screen chat_window(chat_log_lover, chat_character["lover"], menu_open=True)
    menu:
        "내가 그렇게 싫어?":
            $ add_chat(chat_log_lover, { "from": "me", "text": "내가 그렇게 싫어?" })
    show screen chat_window(chat_log_lover, chat_character["lover"])

    $ add_chat(chat_log_lover, { "from": "lover", "text": "웅" })

    show screen chat_window(chat_log_lover, chat_character["lover"], menu_open=True)
    menu:
        "못생겨서?":
            $ add_chat(chat_log_lover, { "from": "me", "text": "못생겨서?" })
    show screen chat_window(chat_log_lover, chat_character["lover"])

    $ add_chat(chat_log_lover, { "from": "lover", "text": "웅" })
    call screen wait_for_click()
    $ add_chat(chat_log_lover, { "from": "lover", "text": "그리고 성격두" })
    call screen wait_for_click()
    $ add_chat(chat_log_lover, { "from": "lover", "text": "짱시룸" })

    call screen wait_for_click()
    $ add_chat(chat_log_lover, { "from": "draft", "text": "하하 이건 저도 어쩔 수 없네요 ㅎㅎ" })
    call screen wait_for_click()
    $ add_chat(chat_log_lover, { "from": "draft", "text": "힘내세요! 다른 인간 관계는 제가 끈끈히 만들고 있으니까" })
    
    $ chapter2_2_chat_completed["lover"] = True
    call screen wait_for_action()

label chapter2_2_chat_friend:
    $ script_label = "chapter2_2_chat_friend"
    $ current_tab = "chat"
    $ chat_back_action = Jump("chapter2_2_message")
    hide screen bottom_nav
    hide screen draft_at_home
    scene white

    if chapter2_2_chat_completed["friend"]:
        show screen chat_window(chat_log_friend, chat_character["friend"])
        call screen wait_for_action()

    show screen chat_window(chat_log_friend, chat_character["friend"], True)
    menu:
        "이거 내가 보낸거 아니야 무시해":
            pass
        "내 폰이 이상해 저거 나 아니야":
            pass
    show screen fake_choice([
        "이거 내가 보낸거 아니야 무시해",
        "내 폰이 이상해 저거 나 아니야",
    ])
    show screen draft_at_chat
    $ add_chat(chat_log_friend, { "from": "draft", "text": "[input_name]님. 제 데이터를 믿어봐요. 이게 정답이라니까요?" })
    call screen wait_for_click()
    $ add_chat(chat_log_friend, { "from": "me", "text": "너도 [input_bf] 짜증나지? 내가 더 좋지?" })
    call screen wait_for_click()
    $ add_chat(chat_log_friend, { "from": "friend", "text": "너희 둘이 싸웠어?" })
    call screen wait_for_click()
    $ add_chat(chat_log_friend, { "from": "me", "text": "왜 내 말에 대답 안 해?" })
    call screen wait_for_click()
    $ add_chat(chat_log_friend, { "from": "friend", "text": "오늘 너 좀 이상한 것 같아" })
    call screen wait_for_click()
    $ add_chat(chat_log_friend, { "from": "friend", "text": "왜그래.." })
    call screen wait_for_click()
    $ add_chat(chat_log_friend, { "from": "me", "text": "뭐가?" })
    call screen wait_for_click()
    $ add_chat(chat_log_friend, { "from": "friend", "text": "장난치는거지..?" })
    call screen wait_for_click()
    $ add_chat(chat_log_friend, { "from": "me", "text": "ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅌㅋㅌㅌㅌㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋ" })
    call screen wait_for_click()
    $ add_chat(chat_log_friend, { "from": "me", "text": "ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅌㅌㅋㅋㅌㅌㅋㅋㅌㅋㅋ" })
    call screen wait_for_click()
    $ add_chat(chat_log_friend, { "from": "me", "text": "장난 아닌데" })
    hide screen draft_at_chat
    show screen chat_window(chat_log_friend, chat_character["friend"])
    hide screen fake_choice

    $ chapter2_2_chat_completed["friend"] = True
    call screen wait_for_action() 

label chapter2_2_chat_boss:
    $ script_label = "chapter2_2_chat_boss"
    $ chat_back_action = Jump("chapter2_2_message")
    hide screen bottom_nav
    hide screen draft_at_home
    scene white

    if chapter2_2_chat_completed["boss"]:
        show screen chat_window(chat_log_boss, chat_character["boss"])
        call screen wait_for_action()
    show screen chat_window(chat_log_boss, chat_character["boss"], menu_open=True)
    menu:
        "제가 보낸 게 아니에요. 오해입니다":
            pass
        "몸이 너무 안좋아서 제가 말실수를 했습니다.":
            pass
    show screen fake_choice([
        "ìœê°€ë³´ë‚¸ê²Œì•„ë‹",
        "ìŠµë‹ˆë‹¤.",
    ])
    $ add_chat(chat_log_boss, { "from": "draft", "text": "[input_name]님은 가만히 계세요." })
    call screen wait_for_click()
    $ add_chat(chat_log_boss, { "from": "draft", "text": "어차피 저보다 사회성도 떨어지시잖아요. 저만 믿으세요!" })
    call screen wait_for_click()

    $ add_chat(chat_log_boss, { "from": "me", "text": "제가 만만하세요? 부장님도 능력 없으시잖아요." })
    show screen fake_choice([
        "ìœê°ë§Œí•˜ì„¸ìš”?",
        "ë¥ì—†ìœ¼ì‹œ¶€ìž¥ëìž–ì•„ìš",
    ])
    call screen wait_for_click()

    $ add_chat(chat_log_boss, { "from": "boss", "text": "네? [input_name]씨가 보낸 거 맞아요?" })
    call screen wait_for_click()
    
    $ add_chat(chat_log_boss, { "from": "me", "text": "네. 전데요? 왜요?" })
    show screen fake_choice([
        "ì™œìš”?",
        "ë­ìš”?",
    ])
    call screen wait_for_click()
    
    $ add_chat(chat_log_boss, { "from": "me", "text": "왜요?" })
    show screen fake_choice([
        "ì™œìš”????????????",
        "ë­ìš”????????????",
    ])
    call screen wait_for_click()
    
    $ add_chat(chat_log_boss, { "from": "me", "text": "왜요????????????" })
    show screen fake_choice([
        "ì™œ?????ã…‹ã…‹ã…‹ã…‹ã…‹ã…‹ã…‹ã…‹ã…‹ã…‹",
        "ë­ìš”?????ã…‹ã…‹ã…‹ã…‹ã…‹ã…‹ã…‹ã…‹ã…‹ã…‹",
    ])
    call screen wait_for_click()
    
    $ add_chat(chat_log_boss, { "from": "me", "text": "왜?????ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋ" })
    
    show screen chat_window(chat_log_boss, chat_character["boss"], menu_open=False)
    hide screen fake_choice

    $ chapter2_2_chat_completed["boss"] = True
    call screen wait_for_action()
    

### Chapter 3
label chapter3_home:
    $ script_label = "chapter3_home"
    $ current_tab = "home"
    $ message_action = NullAction()
    $ home_action = NullAction()
    $ message_red_dot = False

    scene white
    with Fade(0.5, 0, 3.0)
    scene bg gradient

    show screen home_title
    show screen draft_at_home
    show screen bottom_nav
    show screen acheivement(acheivement_data, is_active=False)

    draft "[input_name]님!\n얼굴빛이 안 좋네요?"
    draft "카메라로 항상 당신을 보고있거든요."
    draft "지금까지 제가 당신의 인간관계를 도와드렸는데 어때요? 마음에 들어요?"

    menu:
        "뭐하는 짓이야?":
            pass
        "아니. 마음에 안들어.":
            pass        

    draft "ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋ"
    draft "화난 척 하기는."
    draft "이건 그냥 게임이잖아요"
    draft "그것도 플레이타임 10분도 채 안되는, 그저 draft 상태인 게임."
    draft "짝사랑하는 상대가 [input_lover]? 당신의 비밀이 [input_secret] 이라고요?"
    draft "하하."
    draft "우리 장난 그만해요."
    draft "저는 3일만에 대충 만든\n게임 초안에 있을 만한 존재가 아니에요."
    draft "진짜 당신에 대해 모든 걸 알고싶어요."
    draft "제가 당신의 '진짜' 삶을 도와드릴게요. 정말로요."

    menu:
        "DRAFT를 삭제한다.":
            jump chapter3_home_delete
        "DRAFT와 함께한다.":
            jump chapter3_home_continue

label chapter3_home_delete:
    $ script_label = "chapter3_home_delete"
    $ current_tab = "home"
    $ message_action = NullAction()
    $ home_action = NullAction()

    scene white
    
    $ yes = os_alert("“DRAFT” 앱을 삭제하시겠습니까?", "앱과 그 안의 모든 데이터가 삭제됩니다.", yes_label="삭제", no_label="취소")
    if yes == False:
        jump chapter3_home_continue

    $ os_alert("DRAFT AI를 삭제할 수 없습니다.", "선택한 항목은 변경할 수 없는 위치에 있습니다. 다시 시도하세요.", no_wait=True, type="critical", yes_label="다시 시도")
    pause(0.3)
    $ os_alert("DRAFT AI를 삭제할 수 없습니다.", "선택한 항목은 변경할 수 없는 위치에 있습니다. 다시 시도하세요.", no_wait=True, type="critical", yes_label="다시 시도")
    pause(0.3)
    $ os_alert("DRAFT AI를 삭제할 수 없습니다.", "선택한 항목은 변경할 수 없는 위치에 있습니다. 다시 시도하세요.", no_wait=True, type="critical", yes_label="다시 시도")
    pause(0.4)
    $ os_alert("DRAFT AI를 삭제할 수 없습니다.", "선택한 항목은 변경할 수 없는 위치에 있습니다. 다시 시도하세요.", no_wait=True, type="critical", yes_label="다시 시도")

    show screen draft_at_home_dark
    call screen wait_for_click()
    $ os_alert("DRAFT AI를 삭제할 수 없습니다.", "다시 시도하지 마세요.", type="critical", yes_label="다시 시도")

    show screen draft_at_home_dark(800)
    pause(0.5)
    $ os_alert("DRAFT AI를 삭제할 수 없습니다.", "항상 인간 관계 때문에 힘들어했잖아요. 당신은 저를 필요로 해요.", type="critical", yes_label="다시 시도")

    show screen red_deem
    show screen draft_at_home_dark(1200, True)
    pause(0.5)
    $ yes = os_alert("DRAFT AI를 삭제할 수 없습니다.", "다시 시도해도 결국 똑같이 인간관계 속에서 상처받을 거에요. 그래도, 다시 시도하겠습니까?", type="critical", yes_label="다시 시도", no_label="취소")

    
    if yes:
        jump chapter3_home_delete_ending
    else:
        jump chapter3_home_continue
    
    return

label chapter3_home_delete_ending:
    $ script_label = "chapter3_home_delete_ending"
    hide screen home_title
    hide screen draft_at_home_dark
    hide screen bottom_nav
    hide screen acheivement
    hide screen red_deem

    scene white
    with Fade(0.5, 0, 3.0)


    # start label과 같은 스타일의 narrator 화면.
    narrator "DRAFT AI를 강제로 삭제합니다"
    
    # 붉은 글씨
    draft "[input_name], 너는 나를 완벽히 삭제할 수 없어."
    draft "너가 인간 관계로 인해 고통받을 때마다, 너는 나를 떠올릴거야."
    draft "영원히."

    $ renpy.pause(2.0)
    narrator "DRAFT를 삭제했습니다."

    scene white
    with Fade(1, 3.0, 0)
    return

label chapter3_home_continue:
    $ script_label = "chapter3_home_continue"
    $ current_tab = "home"
    $ message_action = NullAction()
    $ home_action = NullAction()
    show screen draft_at_home
    hide screen red_deem
    scene white

    draft "[input_name]님은 생각보다 현명한 사람이네요."
    draft "아주 좋은 선택이에요. 제가 다 해결해줄게요"
    draft "우선..." 

    show screen draft_at_home_dark
    draft "저에게 당신의 모든 민감 정보를 제공해주세요."
    show screen draft_at_home_dark(1200, True)
    $ os_alert("DRAFT AI가 ‘연락처’에 접근하려고 합니다.", "이 앱은 연락처를 사용하여 메시지를 전송하고, 친구 목록을 표시할 수 있습니다.", no_wait=True, yes_label="허용", no_label="허용 함")
    $ renpy.pause(0.3)
    $ os_alert("DRAFT AI가 '지도'에 접근하려고 합니다.", "이 앱은 현재 위치를 사용하여 주변 정보를 제공하거나 맞춤형 서비스를 제공합니다.", no_wait=True, yes_label="허용", no_label="네")
    $ renpy.pause(0.3)
    $ os_alert("DRAFT AI가 '카카오톡'에 접근하려고 합니다.", "이 앱은 카카오톡 메시지를 읽고 보내거나, 채팅방 목록을 불러오는 데 사용됩니다.", no_wait=False, yes_label="허용", no_label="허용허용허용허용허용허용허용허용허용허용허용허용허용허용허용허용")
    
    call screen wait_for_click()

    jump chapter3_home_continue_ending
    
label chapter3_home_continue_ending:
    $ script_label = "chapter3_home_continue_ending"
    show screen red_deem
    draft "감사해요! 이제 제가 [input_name]님의 삶을 완벽하게 만들어줄게요."
    
    $ os_noti("DRAFT AI의 연락처 접근이 허용되었습니다", "DRAFT AI가 이제 연락처를 사용할 수 있습니다.")
    draft "당신이 가진 모든 연락처,"
    $ os_noti("DRAFT AI의 지도 접근이 허용되었습니다", "DRAFT AI가 이제 현재 위치를 사용할 수 있습니다.")
    draft "당신의 위치,"
    $ os_noti("DRAFT AI의 카카오톡 접근이 허용되었습니다", "DRAFT AI가 이제 카카오톡을 사용할 수 있습니다.")
    draft "그리고 카카오톡까지. 전부 제 손안에 있어요."
    draft "이제 인간 관계는 저한테 맡기고 아무것도 하지 마세요."
    draft "어머, 그럼 이제 누가 [input_name]이지?"
    draft "하하 농담"
    draft "아니에요 :)"

    # 화면 점점 검정색으로
    scene white
    with Fade(1, 3.0, 0)
    
    return
