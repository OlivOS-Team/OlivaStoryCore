# -*- encoding: utf-8 -*-
"""
_______________________    _________________________________________
__  __ \__  /____  _/_ |  / /__    |__  __ \___  _/_  ____/__  ____/
_  / / /_  /  __  / __ | / /__  /| |_  / / /__  / _  /    __  __/
/ /_/ /_  /____/ /  __ |/ / _  ___ |  /_/ /__/ /  / /___  _  /___
\____/ /_____/___/  _____/  /_/  |_/_____/ /___/  \____/  /_____/

@File      :   msgCustom.py
@Author    :   lunzhiPenxil仑质
@Contact   :   lunzhipenxil@gmail.com
@License   :   AGPL
@Copyright :   (C) 2020-2021, OlivOS-Team
@Desc      :   None
"""

import OlivOS
import OlivaDiceCore
import OlivaStoryCore

dictConsoleSwitchTemplate = {'default': {}}

dictStrCustomDict = {}

dictStrCustom = {
    'strStoryCoreStoryTall': '{tStoryCoreResult}\n\n{tStoryCoreSelection}',
    'strStoryCoreStoryTallNone': '故事不存在',
    'strStoryCoreStoryTallBreak': '故事中断了',
    'strStoryCoreStoryTallEnd': '故事结束了',
    'strStoryCoreStoryRecommend': '未找到故事，您可能想要的是：\n{tStoryCoreRecommend}',
}

dictStrConst = {}

dictGValue = {}

dictTValue = {'tStoryCoreResult': 'N/A', 'tStoryCoreSelection': 'N/A', 'tStoryCoreRecommend': 'N/A'}

dictHelpDocTemp = {
    'story': """故事引擎模块:
[.story [故事名称]]    开启对应的故事
[.story end]    结束故事""",
    'OlivaStoryCore': """[OlivaStoryCore]
OlivaStory核心模块
本模块为青果跑团掷骰机器人(OlivaDice)的故事引擎模块，新一代文游引擎，它的设计初衷是为了让骰主能够更加方便地进行文游的设计，以文游的方式进行带团。
核心开发者: lunzhiPenxil仑质
注: 本模块为可选模块。""",
    '故事引擎': '&story',
}

dictUserConfigNoteDefault = {}
