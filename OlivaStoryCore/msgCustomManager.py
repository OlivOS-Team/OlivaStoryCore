# -*- encoding: utf-8 -*-
'''
_______________________    _________________________________________
__  __ \__  /____  _/_ |  / /__    |__  __ \___  _/_  ____/__  ____/
_  / / /_  /  __  / __ | / /__  /| |_  / / /__  / _  /    __  __/   
/ /_/ /_  /____/ /  __ |/ / _  ___ |  /_/ /__/ /  / /___  _  /___   
\____/ /_____/___/  _____/  /_/  |_/_____/ /___/  \____/  /_____/   

@File      :   msgCustomManager.py
@Author    :   lunzhiPenxil仑质
@Contact   :   lunzhipenxil@gmail.com
@License   :   AGPL
@Copyright :   (C) 2020-2021, OlivOS-Team
@Desc      :   None
'''

import OlivOS
import OlivaDiceCore
import OlivaStoryCore

import os
import json

def initMsgCustom(bot_info_dict):
    for bot_info_dict_this in bot_info_dict:
        if bot_info_dict_this not in OlivaDiceCore.msgCustom.dictStrCustomDict:
            OlivaDiceCore.msgCustom.dictStrCustomDict[bot_info_dict_this] = {}
        for dictStrCustom_this in OlivaStoryCore.msgCustom.dictStrCustom:
            if dictStrCustom_this not in OlivaDiceCore.msgCustom.dictStrCustomDict[bot_info_dict_this]:
                OlivaDiceCore.msgCustom.dictStrCustomDict[bot_info_dict_this][dictStrCustom_this] = OlivaStoryCore.msgCustom.dictStrCustom[dictStrCustom_this]
        for dictHelpDoc_this in OlivaStoryCore.msgCustom.dictHelpDocTemp:
            if dictHelpDoc_this not in OlivaDiceCore.helpDocData.dictHelpDoc[bot_info_dict_this]:
                OlivaDiceCore.helpDocData.dictHelpDoc[bot_info_dict_this][dictHelpDoc_this] = OlivaStoryCore.msgCustom.dictHelpDocTemp[dictHelpDoc_this]
    OlivaDiceCore.msgCustom.dictStrConst.update(OlivaStoryCore.msgCustom.dictStrConst)
    OlivaDiceCore.msgCustom.dictGValue.update(OlivaStoryCore.msgCustom.dictGValue)
    OlivaDiceCore.msgCustom.dictTValue.update(OlivaStoryCore.msgCustom.dictTValue)
    OlivaDiceCore.userConfig.dictUserConfigNoteDefault.update(OlivaStoryCore.msgCustom.dictUserConfigNoteDefault)
    for dictConsoleSwitchTemplate_this in OlivaStoryCore.msgCustom.dictConsoleSwitchTemplate:
        if dictConsoleSwitchTemplate_this in OlivaDiceCore.console.dictConsoleSwitchTemplate:
            OlivaDiceCore.console.dictConsoleSwitchTemplate[dictConsoleSwitchTemplate_this].update(
                OlivaStoryCore.msgCustom.dictConsoleSwitchTemplate[dictConsoleSwitchTemplate_this]
            )
    OlivaDiceCore.console.initConsoleSwitchByBotDict(bot_info_dict)
    OlivaDiceCore.console.readConsoleSwitch()
    OlivaDiceCore.console.saveConsoleSwitch()
