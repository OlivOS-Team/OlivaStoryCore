import OlivaDiceCore
import OlivaStoryCore

import os
import json
import traceback
import copy
import codecs
try:
    import pyjson5
except:
    pass

storyList = {}

storyNodeDefault = {
    "flag": None,
    "text": None,
    "selection": [],
    "type": None,
    "endFlag": None,
    "raSkillName": None,
    "raSkillType": None,
    "raMap": []
}

def data_init(plugin_event, Proc):
    releaseDir(OlivaStoryCore.data.dataDirRoot)
    initStoryList(Proc.Proc_data['bot_info_dict'])
    pass

def initStoryList(botInfo):
    releaseDir(f'{OlivaStoryCore.data.dataDirRoot}/unity')
    releaseDir(f'{OlivaStoryCore.data.dataDirRoot}/unity/extend')
    releaseDir(f'{OlivaStoryCore.data.dataDirRoot}/unity/extend/story')
    initStoryListByBotHash('unity')
    for botHash in botInfo:
        releaseDir(f'{OlivaStoryCore.data.dataDirRoot}/{botHash}')
        releaseDir(f'{OlivaStoryCore.data.dataDirRoot}/{botHash}/extend')
        releaseDir(f'{OlivaStoryCore.data.dataDirRoot}/{botHash}/extend/story')
        initStoryListByBotHash(botHash)


def initStoryListByBotHash(botHash:str):
    storyList.setdefault(botHash, {})
    fileStoryList = os.listdir(f'{OlivaStoryCore.data.dataDirRoot}/{botHash}/extend/story')
    for filePath in fileStoryList:
        objStoryThis = None
        try:
            with open(f'{OlivaStoryCore.data.dataDirRoot}/{botHash}/extend/story/{filePath}', 'rb') as filePath_f:
                filePath_fs = formatUTF8WithBOM(filePath_f.read()).decode('utf-8')
                try:
                    objStoryThis = pyjson5.loads(filePath_fs)
                except:
                    objStoryThis = json.loads(filePath_fs)
        except:
            traceback.print_exc()
            OlivaStoryCore.msgReply.globalLog(
                level = 3,
                message = f'扩展故事文件加载失败: {filePath}',
                segment = [('OlivaStory', 'default'), ('Init', 'default')]
            )
        if type(objStoryThis) is dict \
        and 'name' in objStoryThis \
        and type(objStoryThis['name']) is str \
        and 'ingress' in objStoryThis \
        and 'story' in objStoryThis \
        and type(objStoryThis['story']) is list:
            storyList[botHash][objStoryThis['name']] = copy.deepcopy(objStoryThis)
            OlivaStoryCore.msgReply.globalLog(
                level = 2,
                message = f'扩展故事文件已加载: {objStoryThis["name"]}',
                segment = [('OlivaStory', 'default'), ('Init', 'default')]
            )
    if botHash != 'unity':
        for objStoryName in storyList['unity']:
            storyListThis = storyList['unity'][objStoryName]
            storyList[botHash].setdefault(storyListThis['name'], storyListThis)

def getStoryRuntime(
    botHash,
    platform,
    userId
):
    res = OlivaDiceCore.userConfig.getUserConfigByKey(
        userId = userId,
        userType = 'user',
        platform = platform,
        userConfigKey = 'storyRuntime',
        botHash = botHash
    )
    if type(res) is not dict:
        res = {}
    return res

def setStoryRuntime(
    botHash,
    platform,
    userId,
    storyRuntime
):
    res = OlivaDiceCore.userConfig.setUserConfigByKey(
        userId = userId,
        userType = 'user',
        platform = platform,
        userConfigKey = 'storyRuntime',
        botHash = botHash,
        userConfigValue = storyRuntime
    )
    OlivaDiceCore.userConfig.writeUserConfigByUserHash(
        userHash = OlivaDiceCore.userConfig.getUserHash(
            userId = userId,
            userType = 'user',
            platform = platform
        )
    )
    return res

def getStory(botHash, storyName):
    res = None
    if botHash in OlivaStoryCore.storyEngine.storyList \
    and storyName in OlivaStoryCore.storyEngine.storyList[botHash] \
    and type(OlivaStoryCore.storyEngine.storyList[botHash][storyName]) is dict \
    and 'name' in OlivaStoryCore.storyEngine.storyList[botHash][storyName] \
    and type(OlivaStoryCore.storyEngine.storyList[botHash][storyName]['name']) is str \
    and 'ingress' in OlivaStoryCore.storyEngine.storyList[botHash][storyName] \
    and 'story' in OlivaStoryCore.storyEngine.storyList[botHash][storyName] \
    and type(OlivaStoryCore.storyEngine.storyList[botHash][storyName]['story']) is list:
        res = OlivaStoryCore.storyEngine.storyList[botHash][storyName]
    return res

def getStoryNodeByFlagForData(
    storyData,
    flag
):
    res = None
    story = storyData
    if story is not None:
        for storyNode in story['story']:
            if type(storyNode) is dict \
            and 'flag' in storyNode \
            and 'text' in storyNode \
            and str(storyNode['flag']) == str(flag):
                res = storyNode
                break
    return res

def getStoryNodeByFlag(
    storyName,
    flag,
    botHash
):
    res = getStoryNodeByFlagForData(
        storyData = getStory(
            botHash = botHash,
            storyName = storyName
        ),
        flag = flag
    )
    return res

def getStoryNodeDataForStoryData(
    dataKey:str,
    storyData:dict
):
    global storyNodeDefault
    res = None
    if storyData is not None:
        res = storyData.get(dataKey, copy.deepcopy(storyNodeDefault.get(dataKey, None)))
    return res

def getStoryNodeData(
    storyName:str,
    flag:str,
    dataKey:str,
    botHash:str
):
    res = getStoryNodeDataForStoryData(
        storyData = getStoryNodeByFlag(
            storyName = storyName,
            flag = flag,
            botHash = botHash
        ),
        dataKey = dataKey
    )
    return res

def setStoryNoteList(listData:list, nodeData:dict):
    res = listData
    if type(listData) is not list:
        res = []
    if type(nodeData) is dict \
    and 'hideNote' in nodeData \
    and type(nodeData['hideNote']) is list:
        for hideNote_item in nodeData['hideNote']:
            if type(hideNote_item) is str \
            and hideNote_item not in res:
                res.append(hideNote_item)
    return res

def haveStoryNote(
    selectionData:dict,
    storyNoteList:list
):
    res = False
    if type(selectionData) is dict \
    and 'hideNote' in selectionData \
    and type(selectionData['hideNote']) is str \
    and type(storyNoteList) is list \
    and selectionData['hideNote'] in storyNoteList:
        res = True
    elif type(selectionData) is dict \
    and 'hideNote' not in selectionData:
        res = True
    return res

def startStory(
    botHash:str,
    platform:str,
    userId:str,
    storyName:str,
    chatToken:str
):
    res = None
    story = getStory(botHash, storyName)
    if story is not None:
        tmp_story_runtime = getStoryRuntime(
            botHash = botHash,
            platform = platform,
            userId = userId
        )
        tmp_storyNode = getStoryNodeByFlagForData(
            storyData = story,
            flag = story['ingress']
        )
        res = tmp_storyNode
        if res is not None:
            tmp_story_runtime[chatToken] = {
                'storyNameNow': storyName,
                'storyFlagNow': story['ingress'],
                'storyNoteList': setStoryNoteList([], tmp_storyNode)
            }
            setStoryRuntime(
                botHash = botHash,
                platform = platform,
                userId = userId,
                storyRuntime = tmp_story_runtime
            )
    return res

def runStoryBySelectionIndex(
    botHash:str,
    platform:str,
    userId:str,
    chatToken:str,
    selectionIndex:'None|str|int' = None
):
    res = None
    tmp_story_runtime = getStoryRuntime(
        botHash = botHash,
        platform = platform,
        userId = userId
    )
    storyFlagNext = None
    flagNeedSave = False
    if chatToken in tmp_story_runtime \
    and type(tmp_story_runtime[chatToken]) is dict \
    and 'storyNameNow' in tmp_story_runtime[chatToken] \
    and type(tmp_story_runtime[chatToken]['storyNameNow']) is str \
    and 'storyFlagNow' in tmp_story_runtime[chatToken] \
    and type(tmp_story_runtime[chatToken]['storyFlagNow']) is str:
        story = getStory(botHash, tmp_story_runtime[chatToken]['storyNameNow'])
        if story is not None:
            tmp_storyNode = getStoryNodeByFlagForData(
                storyData = story,
                flag = tmp_story_runtime[chatToken]['storyFlagNow']
            )
            tmp_story_runtime[chatToken]['storyNoteList'] = setStoryNoteList(
                tmp_story_runtime[chatToken].get('storyNoteList', []),
                tmp_storyNode
            )
            tmp_storyNode_selection = getStoryNodeDataForStoryData(
                dataKey = 'selection',
                storyData = tmp_storyNode
            )
            tmp_storyNode_type = getStoryNodeDataForStoryData(
                dataKey = 'type',
                storyData = tmp_storyNode
            )
            selectionIndex_new = None
            if tmp_storyNode_type == None \
            and type(selectionIndex) is int:
                selectionIndex_new = selectionIndex
            elif tmp_storyNode_type == 'ra' \
            and selectionIndex == 'ra':
                tmp_storyNode_raSkillName = getStoryNodeDataForStoryData(
                    dataKey = 'raSkillName',
                    storyData = tmp_storyNode
                )
                tmp_storyNode_raSkillValue = getStoryNodeDataForStoryData(
                    dataKey = 'raSkillValue',
                    storyData = tmp_storyNode
                )
                tmp_storyNode_raMap = getStoryNodeDataForStoryData(
                    dataKey = 'raMap',
                    storyData = tmp_storyNode
                )
                tmp_userData_raRollValue = OlivaDiceCore.userConfig.getUserConfigByKey(
                    userConfigKey = 'RDRecordInt',
                    botHash = botHash,
                    userId = userId,
                    userType = 'user',
                    platform = platform
                )
                tmp_userData_raSkillValue = OlivaDiceCore.userConfig.getUserConfigByKey(
                    userConfigKey = 'RDRecordSkillInt',
                    botHash = botHash,
                    userId = userId,
                    userType = 'user',
                    platform = platform
                )
                if tmp_storyNode_raSkillName is not None \
                and type(tmp_userData_raRollValue) is int \
                and type(tmp_userData_raSkillValue) is int \
                and ((type(tmp_storyNode_raSkillValue) is int \
                        and tmp_userData_raSkillValue == tmp_storyNode_raSkillValue) \
                    or tmp_storyNode_raSkillValue is None) \
                and type(tmp_storyNode_raMap) is list:
                    for tmp_storyNode_raMap_item in tmp_storyNode_raMap:
                        if type(tmp_storyNode_raMap_item) is dict \
                        and 'para' in tmp_storyNode_raMap_item \
                        and type(tmp_storyNode_raMap_item['para']) is str \
                        and 'selection' in tmp_storyNode_raMap_item \
                        and type(tmp_storyNode_raMap_item['selection']) is int:
                            res_this = False
                            tmp_storyNode_raMap_item_para = tmp_storyNode_raMap_item['para']
                            tmp_value_dict = {
                                'raRollValue': str(tmp_userData_raRollValue),
                                'raSkillValue': str(tmp_userData_raSkillValue)
                            }
                            try:
                                tmp_storyNode_raMap_item_para = tmp_storyNode_raMap_item_para.format_map(tmp_value_dict)
                                res_this = eval(tmp_storyNode_raMap_item_para)
                            except:
                                res_this = False
                                traceback.print_exc()
                            if type(res_this) is not bool:
                                res_this = False
                            if res_this is True:
                                selectionIndex_new = tmp_storyNode_raMap_item['selection']
                                break
            if type(selectionIndex_new) is int:
                if len(tmp_storyNode_selection) > selectionIndex_new \
                and 0 <= selectionIndex_new \
                and type(tmp_storyNode_selection[selectionIndex_new]) is dict:
                    if 'to' in tmp_storyNode_selection[selectionIndex_new] \
                    and 'toType' in tmp_storyNode_selection[selectionIndex_new] \
                    and 'jump' == tmp_storyNode_selection[selectionIndex_new]['toType']:
                        if haveStoryNote(
                            selectionData = tmp_storyNode_selection[selectionIndex_new],
                            storyNoteList = tmp_story_runtime[chatToken].get('storyNoteList', [])
                        ):
                            res = getStoryNodeByFlagForData(
                                storyData = story,
                                flag = tmp_storyNode_selection[selectionIndex_new]['to']
                            )
                            if res is not None:
                                storyFlagNext = tmp_storyNode_selection[selectionIndex_new]['to']
    if storyFlagNext is not None:
        tmp_story_runtime[chatToken]['storyFlagNow'] = storyFlagNext
        flagNeedSave = True
    elif chatToken in tmp_story_runtime:
        tmp_story_runtime.pop(chatToken)
        flagNeedSave = True
    if flagNeedSave:
        setStoryRuntime(
            botHash = botHash,
            platform = platform,
            userId = userId,
            storyRuntime = tmp_story_runtime
        )
    return res

def isStoryEnd(nodeData:dict):
    res = False
    if type(nodeData) is dict \
    and 'flag' in nodeData \
    and type(nodeData['flag']) is str \
    and 'text' in nodeData \
    and type(nodeData['text']) is str \
    and 'type' in nodeData \
    and nodeData['type'] == 'end' \
    and 'endFlag' in nodeData \
    and type(nodeData['endFlag']) is str:
        res = True
    return res

def releaseDir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def formatUTF8WithBOM(data:bytes):
    res = data
    if res[:3] == codecs.BOM_UTF8:
        res = res[3:]
    return res
