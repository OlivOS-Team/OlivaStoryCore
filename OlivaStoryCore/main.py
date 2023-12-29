# -*- encoding: utf-8 -*-
'''
_______________________    _________________________________________
__  __ \__  /____  _/_ |  / /__    |__  __ \___  _/_  ____/__  ____/
_  / / /_  /  __  / __ | / /__  /| |_  / / /__  / _  /    __  __/   
/ /_/ /_  /____/ /  __ |/ / _  ___ |  /_/ /__/ /  / /___  _  /___   
\____/ /_____/___/  _____/  /_/  |_/_____/ /___/  \____/  /_____/   

@File      :   main.py
@Author    :   lunzhiPenxil仑质
@Contact   :   lunzhipenxil@gmail.com
@License   :   AGPL
@Copyright :   (C) 2020-2021, OlivOS-Team
@Desc      :   None
'''

import OlivOS
import OlivaStoryCore
import OlivaDiceCore

class Event(object):
    def init(plugin_event, Proc):
        OlivaStoryCore.msgReply.unity_init(plugin_event, Proc)

    def init_after(plugin_event, Proc):
        OlivaDiceCore.crossHook.dictHookList['model'].append(['OlivaStoryCore', OlivaStoryCore.data.OlivaStoryCore_ver_short])
        OlivaStoryCore.msgReply.data_init(plugin_event, Proc)
        OlivaStoryCore.storyEngine.data_init(plugin_event, Proc)

    def private_message(plugin_event, Proc):
        OlivaStoryCore.msgReply.unity_reply(plugin_event, Proc)

    def group_message(plugin_event, Proc):
        OlivaStoryCore.msgReply.unity_reply(plugin_event, Proc)

    def poke(plugin_event, Proc):
        pass
