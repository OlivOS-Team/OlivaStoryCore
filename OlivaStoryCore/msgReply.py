# -*- encoding: utf-8 -*-
'''
_______________________    _________________________________________
__  __ \__  /____  _/_ |  / /__    |__  __ \___  _/_  ____/__  ____/
_  / / /_  /  __  / __ | / /__  /| |_  / / /__  / _  /    __  __/   
/ /_/ /_  /____/ /  __ |/ / _  ___ |  /_/ /__/ /  / /___  _  /___   
\____/ /_____/___/  _____/  /_/  |_/_____/ /___/  \____/  /_____/   

@File      :   msgReply.py
@Author    :   lunzhiPenxil仑质
@Contact   :   lunzhipenxil@gmail.com
@License   :   AGPL
@Copyright :   (C) 2020-2021, OlivOS-Team
@Desc      :   None
'''

import OlivOS
import OlivaStoryCore
import OlivaDiceCore

import traceback
import json
import uuid

def logProc(Proc:OlivOS.pluginAPI.shallow, level, message, segment):
    Proc.log(
        log_level = level,
        log_message = message,
        log_segment = segment
    )

def globalLog(level, message, segment):
    if OlivaStoryCore.data.gProc is not None:
        logProc(OlivaStoryCore.data.gProc, level, message, segment)

def unity_init(plugin_event, Proc):
    pass

def data_init(plugin_event, Proc):
    OlivaStoryCore.data.gProc = Proc
    OlivaStoryCore.msgCustomManager.initMsgCustom(Proc.Proc_data['bot_info_dict'])
    OlivaStoryCore.userConfig.initUserConfigNoteDefault(Proc.Proc_data['bot_info_dict'])
    if 'replyContextPrefixFliter' in OlivaDiceCore.crossHook.dictHookList:
        OlivaDiceCore.crossHook.dictHookList['replyContextPrefixFliter'].append('story')

def unity_reply(plugin_event, Proc):
    OlivaDiceCore.userConfig.setMsgCount()
    dictTValue = OlivaDiceCore.msgCustom.dictTValue.copy()
    dictTValue['tName'] = plugin_event.data.sender['name']
    dictStrCustom = OlivaDiceCore.msgCustom.dictStrCustomDict[plugin_event.bot_info.hash]
    dictGValue = OlivaDiceCore.msgCustom.dictGValue
    dictTValue.update(dictGValue)
    dictTValue = OlivaDiceCore.msgCustomManager.dictTValueInit(plugin_event, dictTValue)

    replyMsg = OlivaDiceCore.msgReply.replyMsg
    isMatchWordStart = OlivaDiceCore.msgReply.isMatchWordStart
    getMatchWordStartRight = OlivaDiceCore.msgReply.getMatchWordStartRight
    skipSpaceStart = OlivaDiceCore.msgReply.skipSpaceStart
    skipToRight = OlivaDiceCore.msgReply.skipToRight
    msgIsCommand = OlivaDiceCore.msgReply.msgIsCommand

    tmp_at_str = OlivOS.messageAPI.PARA.at(plugin_event.base_info['self_id']).CQ()
    tmp_at_str_sub = None
    if 'sub_self_id' in plugin_event.data.extend:
        if plugin_event.data.extend['sub_self_id'] != None:
            tmp_at_str_sub = OlivOS.messageAPI.PARA.at(plugin_event.data.extend['sub_self_id']).CQ()
    tmp_command_str_1 = '.'
    tmp_command_str_2 = '。'
    tmp_command_str_3 = '/'
    tmp_reast_str = plugin_event.data.message
    flag_force_reply = False
    flag_is_command = False
    flag_is_from_host = False
    flag_is_from_group = False
    flag_is_from_group_admin = False
    flag_is_from_group_have_admin = False
    flag_is_from_master = False
    if isMatchWordStart(tmp_reast_str, '[CQ:reply,id='):
        tmp_reast_str = skipToRight(tmp_reast_str, ']')
        tmp_reast_str = tmp_reast_str[1:]
        if isMatchWordStart(tmp_reast_str, tmp_at_str):
            tmp_reast_str = getMatchWordStartRight(tmp_reast_str, tmp_at_str)
            tmp_reast_str = skipSpaceStart(tmp_reast_str)
            flag_force_reply = True
    if isMatchWordStart(tmp_reast_str, tmp_at_str):
        tmp_reast_str = getMatchWordStartRight(tmp_reast_str, tmp_at_str)
        tmp_reast_str = skipSpaceStart(tmp_reast_str)
        flag_force_reply = True
    if tmp_at_str_sub != None:
        if isMatchWordStart(tmp_reast_str, tmp_at_str_sub):
            tmp_reast_str = getMatchWordStartRight(tmp_reast_str, tmp_at_str_sub)
            tmp_reast_str = skipSpaceStart(tmp_reast_str)
            flag_force_reply = True
    [tmp_reast_str, flag_is_command] = msgIsCommand(
        tmp_reast_str,
        OlivaDiceCore.crossHook.dictHookList['prefix']
    )

    tmp_hagID = None
    tmp_userId = plugin_event.data.user_id
    if plugin_event.plugin_info['func_type'] == 'group_message':
        if plugin_event.data.host_id != None:
            flag_is_from_host = True
        flag_is_from_group = True
    elif plugin_event.plugin_info['func_type'] == 'private_message':
        flag_is_from_group = False
    if flag_is_from_host and flag_is_from_group:
        tmp_hagID = '%s|%s' % (str(plugin_event.data.host_id), str(plugin_event.data.group_id))
    elif flag_is_from_group:
        tmp_hagID = str(plugin_event.data.group_id)

    if flag_is_command:
        tmp_hagID = None
        if plugin_event.plugin_info['func_type'] == 'group_message':
            if plugin_event.data.host_id != None:
                flag_is_from_host = True
            flag_is_from_group = True
        elif plugin_event.plugin_info['func_type'] == 'private_message':
            flag_is_from_group = False
        if flag_is_from_group:
            if 'role' in plugin_event.data.sender:
                flag_is_from_group_have_admin = True
                if plugin_event.data.sender['role'] in ['owner', 'admin']:
                    flag_is_from_group_admin = True
                elif plugin_event.data.sender['role'] in ['sub_admin']:
                    flag_is_from_group_admin = True
                    flag_is_from_group_sub_admin = True
        if flag_is_from_host and flag_is_from_group:
            tmp_hagID = '%s|%s' % (str(plugin_event.data.host_id), str(plugin_event.data.group_id))
        elif flag_is_from_group:
            tmp_hagID = str(plugin_event.data.group_id)
        flag_hostEnable = True
        if flag_is_from_host:
            flag_hostEnable = OlivaDiceCore.userConfig.getUserConfigByKey(
                userId = plugin_event.data.host_id,
                userType = 'host',
                platform = plugin_event.platform['platform'],
                userConfigKey = 'hostEnable',
                botHash = plugin_event.bot_info.hash
            )
        flag_hostLocalEnable = True
        if flag_is_from_host:
            flag_hostLocalEnable = OlivaDiceCore.userConfig.getUserConfigByKey(
                userId = plugin_event.data.host_id,
                userType = 'host',
                platform = plugin_event.platform['platform'],
                userConfigKey = 'hostLocalEnable',
                botHash = plugin_event.bot_info.hash
            )
        flag_groupEnable = True
        if flag_is_from_group:
            if flag_is_from_host:
                if flag_hostEnable:
                    flag_groupEnable = OlivaDiceCore.userConfig.getUserConfigByKey(
                        userId = tmp_hagID,
                        userType = 'group',
                        platform = plugin_event.platform['platform'],
                        userConfigKey = 'groupEnable',
                        botHash = plugin_event.bot_info.hash
                    )
                else:
                    flag_groupEnable = OlivaDiceCore.userConfig.getUserConfigByKey(
                        userId = tmp_hagID,
                        userType = 'group',
                        platform = plugin_event.platform['platform'],
                        userConfigKey = 'groupWithHostEnable',
                        botHash = plugin_event.bot_info.hash
                    )
            else:
                flag_groupEnable = OlivaDiceCore.userConfig.getUserConfigByKey(
                    userId = tmp_hagID,
                    userType = 'group',
                    platform = plugin_event.platform['platform'],
                    userConfigKey = 'groupEnable',
                    botHash = plugin_event.bot_info.hash
                )
        #此频道关闭时中断处理
        if not flag_hostLocalEnable and not flag_force_reply:
            return
        #此群关闭时中断处理
        if not flag_groupEnable and not flag_force_reply:
            return
        if isMatchWordStart(tmp_reast_str, 'story'):
            tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'story')
            tmp_reast_str = skipSpaceStart(tmp_reast_str)
            tmp_platform = plugin_event.platform['platform']
            tmp_botHash = plugin_event.bot_info.hash
            tmp_chat_token = f'{tmp_platform}|{tmp_hagID}'
            tmp_userId = plugin_event.data.user_id
            data_storyRuntime = OlivaStoryCore.storyEngine.getStoryRuntime(
                botHash = tmp_botHash,
                platform = tmp_platform,
                userId = tmp_userId
            )
            tmp_noteList = getNoteList(
                chatToken = tmp_chat_token,
                storyRuntime = data_storyRuntime
            )
            if type(data_storyRuntime) is not dict:
                data_storyRuntime = {}
            if isMatchWordStart(tmp_reast_str, 'end', isCommand = True):
                OlivaStoryCore.storyEngine.runStoryBySelectionIndex(
                    botHash = tmp_botHash,
                    platform = tmp_platform,
                    userId = tmp_userId,
                    chatToken = tmp_chat_token,
                    selectionIndex = -1
                )
                tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strStoryCoreStoryTallEnd'], dictTValue)
                replyMsg(plugin_event, tmp_reply_str)
            elif False and isMatchWordStart(tmp_reast_str, 'go'):
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'go')
                tmp_reast_str = skipSpaceStart(tmp_reast_str)
                tmp_go_index = tmp_reast_str
                try:
                    tmp_go_index = int(tmp_go_index)
                except:
                    tmp_go_index = None
                if tmp_go_index is not None:
                    tmp_go_index = tmp_go_index - 1
                    tmp_nodeData = OlivaStoryCore.storyEngine.runStoryBySelectionIndex(
                        botHash = tmp_botHash,
                        platform = tmp_platform,
                        userId = tmp_userId,
                        chatToken = tmp_chat_token,
                        selectionIndex = tmp_go_index
                    )
                    tmp_reply_str = getStoryTall(
                        plugin_event = plugin_event,
                        dictStrCustom = dictStrCustom,
                        dictTValue = dictTValue,
                        nodeData = tmp_nodeData,
                        noteList = tmp_noteList
                    )
                    if OlivaStoryCore.storyEngine.isStoryEnd(tmp_nodeData):
                        OlivaStoryCore.storyEngine.runStoryBySelectionIndex(
                            botHash = tmp_botHash,
                            platform = tmp_platform,
                            userId = tmp_userId,
                            chatToken = tmp_chat_token,
                            selectionIndex = -1
                        )
            elif len(tmp_reast_str) > 0:
                tmp_reast_str = tmp_reast_str.strip(' ')
                tmp_story_name = tmp_reast_str
                tmp_nodeData = OlivaStoryCore.storyEngine.startStory(
                    botHash = tmp_botHash,
                    platform = tmp_platform,
                    userId = tmp_userId,
                    storyName = tmp_story_name,
                    chatToken = tmp_chat_token
                )
                if tmp_nodeData is not None:
                    tmp_reply_str = getStoryTall(
                        plugin_event = plugin_event,
                        dictStrCustom = dictStrCustom,
                        dictTValue = dictTValue,
                        nodeData = tmp_nodeData,
                        flagIsStart = True,
                        noteList = tmp_noteList
                    )
                else:
                    tmp_reply_str = None
                    searchList = getStorySearchList(tmp_story_name, tmp_botHash)
                    if len(searchList) > 0:
                        dictTValue['tStoryCoreRecommend'] = '\n'.join([f'[.story {storyName_this}]' for storyName_this in searchList])
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strStoryCoreStoryRecommend'], dictTValue)
                    else:
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strStoryCoreStoryTallNone'], dictTValue)
                    if tmp_reply_str != None:
                        replyMsg(plugin_event, tmp_reply_str)
            else:
                tmp_reply_str = OlivaDiceCore.helpDoc.getHelp('story', tmp_botHash)
                if tmp_reply_str != None:
                    replyMsg(plugin_event, tmp_reply_str)
        else:
            tmp_platform = plugin_event.platform['platform']
            tmp_botHash = plugin_event.bot_info.hash
            tmp_chat_token = f'{tmp_platform}|{tmp_hagID}'
            data_storyRuntime = OlivaStoryCore.storyEngine.getStoryRuntime(
                botHash = tmp_botHash,
                platform = tmp_platform,
                userId = tmp_userId
            )
            tmp_noteList = getNoteList(
                chatToken = tmp_chat_token,
                storyRuntime = data_storyRuntime
            )
            if type(data_storyRuntime) is dict \
            and tmp_chat_token in data_storyRuntime \
            and 'storyNameNow' in data_storyRuntime[tmp_chat_token] \
            and type(data_storyRuntime[tmp_chat_token]['storyNameNow']) is str \
            and 'storyFlagNow' in data_storyRuntime[tmp_chat_token] \
            and type(data_storyRuntime[tmp_chat_token]['storyFlagNow']) is str:
                tmp_storyNode = OlivaStoryCore.storyEngine.getStoryNodeByFlag(
                    storyName = data_storyRuntime[tmp_chat_token]['storyNameNow'],
                    flag = data_storyRuntime[tmp_chat_token]['storyFlagNow'],
                    botHash = tmp_botHash
                )
                tmp_storyNode_type = OlivaStoryCore.storyEngine.getStoryNodeDataForStoryData(
                    dataKey = 'type',
                    storyData = tmp_storyNode
                )
                if tmp_storyNode_type == 'ra' \
                and isMatchWordStart(tmp_reast_str, 'ra'):
                    tmp_nodeData = OlivaStoryCore.storyEngine.runStoryBySelectionIndex(
                        botHash = tmp_botHash,
                        platform = tmp_platform,
                        userId = tmp_userId,
                        chatToken = tmp_chat_token,
                        selectionIndex = 'ra'
                    )
                    tmp_reply_str = getStoryTall(
                        plugin_event = plugin_event,
                        dictStrCustom = dictStrCustom,
                        dictTValue = dictTValue,
                        nodeData = tmp_nodeData,
                        noteList = tmp_noteList
                    )
                    if OlivaStoryCore.storyEngine.isStoryEnd(tmp_nodeData):
                        OlivaStoryCore.storyEngine.runStoryBySelectionIndex(
                            botHash = tmp_botHash,
                            platform = tmp_platform,
                            userId = tmp_userId,
                            chatToken = tmp_chat_token,
                            selectionIndex = -1
                        )
    else:
        tmp_platform = plugin_event.platform['platform']
        tmp_botHash = plugin_event.bot_info.hash
        tmp_chat_token = f'{tmp_platform}|{tmp_hagID}'
        data_storyRuntime = OlivaStoryCore.storyEngine.getStoryRuntime(
            botHash = tmp_botHash,
            platform = tmp_platform,
            userId = tmp_userId
        )
        tmp_noteList = getNoteList(
            chatToken = tmp_chat_token,
            storyRuntime = data_storyRuntime
        )
        tmp_reply_str = None
        if type(data_storyRuntime) is dict \
        and tmp_chat_token in data_storyRuntime:
            tmp_go_index = tmp_reast_str
            try:
                tmp_go_index = int(tmp_go_index)
            except:
                tmp_go_index = None
            if tmp_go_index is not None:
                tmp_go_index = tmp_go_index - 1
                tmp_nodeData = OlivaStoryCore.storyEngine.runStoryBySelectionIndex(
                    botHash = tmp_botHash,
                    platform = tmp_platform,
                    userId = tmp_userId,
                    chatToken = tmp_chat_token,
                    selectionIndex = tmp_go_index
                )
                tmp_reply_str = getStoryTall(
                    plugin_event = plugin_event,
                    dictStrCustom = dictStrCustom,
                    dictTValue = dictTValue,
                    nodeData = tmp_nodeData,
                    noteList = tmp_noteList
                )
                if OlivaStoryCore.storyEngine.isStoryEnd(tmp_nodeData):
                    OlivaStoryCore.storyEngine.runStoryBySelectionIndex(
                        botHash = tmp_botHash,
                        platform = tmp_platform,
                        userId = tmp_userId,
                        chatToken = tmp_chat_token,
                        selectionIndex = -1
                    )

def getNoteList(
    chatToken:str,
    storyRuntime:dict
):
    res = None
    if type(storyRuntime) is dict \
    and chatToken in storyRuntime \
    and type(storyRuntime[chatToken]) is dict \
    and 'storyNoteList' in storyRuntime[chatToken] \
    and type(storyRuntime[chatToken]['storyNoteList']) is list:
        res = storyRuntime[chatToken]['storyNoteList']
    return res

def getStoryTall(
    plugin_event,
    dictStrCustom,
    dictTValue,
    nodeData,
    flagIsStart = False,
    noteList = None
):
    selection_str_list = []
    tmp_platform = plugin_event.platform['platform']
    tmp_model = plugin_event.platform['model']
    replyMsg = OlivaDiceCore.msgReply.replyMsg
    res = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strStoryCoreStoryTallBreak'], dictTValue)
    if flagIsStart:
        res = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strStoryCoreStoryTallNone'], dictTValue)
    if nodeData is not None:
        dictTValue['tStoryCoreResult'] = OlivaStoryCore.storyEngine.getStoryNodeDataForStoryData(
            dataKey = 'text',
            storyData = nodeData
        )
        selection = OlivaStoryCore.storyEngine.getStoryNodeDataForStoryData(
            dataKey = 'selection',
            storyData = nodeData
        )
        tmp_nodeData_type = OlivaStoryCore.storyEngine.getStoryNodeDataForStoryData(
            dataKey = 'type',
            storyData = nodeData
        )
        if tmp_nodeData_type == None:
            if len(selection) > 0:
                tmp_selection_list = []
                for i in range(len(selection)):
                    if noteList is None \
                    or (type(noteList) is list \
                        and OlivaStoryCore.storyEngine.haveStoryNote(
                            selectionData = selection[i],
                            storyNoteList = noteList
                        )
                    ):
                        tmp_str = f"{i + 1} - {selection[i]['text']}"
                        tmp_selection_list.append(tmp_str)
                        selection_str_list.append([f"{i + 1}", tmp_str])
                if len(tmp_selection_list) > 0:
                    dictTValue['tStoryCoreSelection'] = '选项如下：\n%s' % ('\n'.join(tmp_selection_list))
                else:
                    dictTValue['tStoryCoreSelection'] = '道路的尽头'
            else:
                dictTValue['tStoryCoreSelection'] = '选择的尽头'
        elif tmp_nodeData_type == 'end':
            dictTValue['tStoryCoreSelection'] = '道路的尽头'
        elif tmp_nodeData_type == 'ra':
            dictTValue['tStoryCoreSelection'] = '使用[.ra]指令完成检定以继续'
        dictTValue['tStoryCoreResult'] = nodeData.get('text', [])
        res = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strStoryCoreStoryTall'], dictTValue)
    if res is not None:
        replyMsg(plugin_event, res)
    if len(selection_str_list) > 0:
        if tmp_platform == 'kaiheila' \
        and tmp_model not in ['text']:
            try:
                if plugin_event.indeAPI.hasAPI('create_message'):
                    msg_list = [
                        {
                            "type": "card",
                            "theme": "primary",
                            "color": "#009FE9",
                            "size": "lg",
                            "modules": [
                                {
                                    "type": "action-group",
                                    "elements": [
                                        {
                                            "type": "button",
                                            "theme": "info",
                                            "value": f'{selection_str[0]}',
                                            "click": "return-val",
                                            "text": {
                                                "type": "plain-text",
                                                "content": f'{selection_str[1]}'
                                            }
                                        }
                                    ]
                                } for selection_str in selection_str_list
                            ] + [
                                {
                                    "type": "context",
                                    "elements": [
                                        {
                                          "type": "plain-text",
                                          "content": "OlivaDice - 青果核心掷骰机器人"
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                    if plugin_event.plugin_info['func_type'] == 'group_message':
                        plugin_event.indeAPI.create_message(
                            chat_type = 'group',
                            chat_id = plugin_event.data.group_id,
                            content_type = 10,
                            content = json.dumps(msg_list, ensure_ascii=False)
                        )
                    elif plugin_event.plugin_info['func_type'] == 'private_message':
                        plugin_event.indeAPI.create_message(
                            chat_type = 'private',
                            chat_id = plugin_event.data.user_id,
                            content_type = 10,
                            content = json.dumps(msg_list, ensure_ascii=False)
                        )
            except Exception as e:
                traceback.print_exc()
        
        elif tmp_platform == 'mhyVila':
            try:
                if plugin_event.indeAPI.hasAPI('create_message'):
                    msg_list = {
                        "content": {
                            "text": "选项如下："
                        },
                        "panel": {
                            "big_component_group_list": [
                                [
                                    {
                                        "id": str(uuid.uuid4()),
                                        "text": f'{selection_str[1][:9]}...' if len(selection_str[1]) > 12 else f'{selection_str[1]}',
                                        "type": 1,
                                        "extra": f'{selection_str[0]}',
                                        "need_callback": False,
                                        "c_type": 2,
                                        "input": f'{selection_str[0]}',
                                        "link": ""
                                    }
                                ] for selection_str in selection_str_list
                            ]
                        }
                    }
                    if plugin_event.plugin_info['func_type'] == 'group_message':
                        plugin_event.indeAPI.create_message(
                            chat_type = 'group',
                            chat_id = plugin_event.data.group_id,
                            object_name = 'MHY:Text',
                            content = msg_list,
                            host_id = plugin_event.data.host_id
                        )
            except Exception as e:
                traceback.print_exc()
    return res

def getStorySearchList(storyName_search:str, botHash:str):
    res = []
    tmp_RecommendRank_list = []
    if botHash in OlivaStoryCore.storyEngine.storyList:
        for storyName_this in OlivaStoryCore.storyEngine.storyList[botHash]:
            tmp_RecommendRank_list.append([
                OlivaDiceCore.helpDoc.getRecommendRank(
                    storyName_search,
                    storyName_this
                ),
                storyName_this
            ])
        tmp_RecommendRank_list.sort(key = lambda x : x[0])
    tmp_count_max = min(8, len(tmp_RecommendRank_list))
    count = 0
    while count < tmp_count_max:
        if tmp_RecommendRank_list[count][0] < 1000:
            if len(tmp_RecommendRank_list[count][1]) < 25:
                res.append(tmp_RecommendRank_list[count][1])
        count += 1
    return res
