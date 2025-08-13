export default {
  // 通用
  common: {
    minimize: '最小化',
    maximize: '最大化',
    exitMaximize: '退出最大化',
    close: '关闭',
    save: '保存',
    cancel: '取消',
    confirm: '确认',
    enable: '启用',
    disable: '弃用',
    on: '开启',
    off: '关闭',
    getConfig: '获取配置',
    saveConfig: '保存配置',
    saveAndRestart: '保存配置并重启',
    restartService: '重启服务',
    error: '发生错误',
    copySuccess: '复制成功',
    copyFailed: '复制失败'
  },
  
  // 标题和菜单
  header: {
    title: 'VRCLS面板',
    home: '首页',
    usageStats: '用量统计',
    controlModeConfig: '控制模式配置',
    programSettings: '程序设置',
    logs: '日志'
  },
  
  // 首页
  home: {
    micRecognitionResult: '麦克风识别结果',
    desktopRecognitionResult: '桌面音频识别结果',
    inputPlaceholder: '请输入需要翻译的文字',
    send: '发送'
  },
  
  // 程序配置
  config: {
    programConfig: '程序配置',
    serverUrl: '服务器URL',
    oscPort: 'OSC 端口',
    oscIpAddress: 'OSC IP 地址',
    defaultMode: '默认模式',
    control: '控制',
    translation: '翻译',
    textSend: '文字发送',
    bitmapLed: '点阵屏',
    speechRecognitionLanguage: '语音识别语言',
    defaultTranslationLanguage: '默认翻译语言',
    secondTranslationLanguage: '第二翻译语言',
    thirdTranslationLanguage: '第三翻译语言',
    separateDesktopAudioCapture: '独立桌面音频捕捉',
    useDesktopAudio: '使用桌面音频',
    useVirtualSoundcardMic: '使用虚拟声卡麦克风',
    micUseLocalRecognitionModel: '麦克风使用本地识别模型',
    desktopAudioUseLocalRecognitionModel: '桌面音频使用本地识别模型',
    steamvrPalmOutputDisplay: 'SteamVR掌心输出显示',
    steamvrDisplayPosition: 'SteamVR显示位置',
    rightHand: '右手',
    leftHand: '左手',
    leftAndRightHand: '左手+右手',
    steamvrDisplaySize: 'SteamVR显示大小',
    ttsOutput: '语音合成输出',
    translationModeMicTranslationOutput: '翻译模式麦克风译文输出',
    textSendModeMicOriginalText: '文字发送模式麦克风原文',
    translationModeMicAndDesktopAudioTranslationOutput: '翻译模式麦克风+桌面音频译文输出',
    ttsOutputSpeaker: 'TTS输出扬声器',
    micTranslationEngine: '麦克风翻译引擎',
    desktopAudioTranslationEngine: '桌面音频翻译引擎',
    translationEngineAccessPointRegion: '翻译引擎接入点地区',
    mainlandChina: '中国大陆地区',
    other: '其他',
    oscOutput: 'osc输出',
    pause: '暂停',
    emotionRecognitionEmojiOutput: '情绪识别emoji输出',
    externalOscServerPort: '外源OSC服务端端口',
    receiveExternalOscServerPort: '接收外源OSC服务端 端口',
    receiveExternalOscServerIpAddress: '接收外源OSC服务端 IP地址',
    openaiConfig: 'OpenAI配置',
    openaiApiKey: 'API密钥',
    openaiApiUrl: 'API地址',
    openaiModel: '模型',
    capOutputStyle: '表格内显示格式',
    capOutputStyle1: '所有语言全部输出',
    capOutputStyle2: '只输出默认翻译语言译文',
    capOutputStyle3: '默认翻译语言译文+识别原文'
  },
  
  // 语音控制配置
  voiceControl: {
    voiceControlConfig: '语音控制配置',
    microphone: '麦克风',
    systemDefaultMicrophone: '系统默认麦克风',
    microphoneVoiceMode: '麦克风语音模式',
    continuousOn: '持续开启',
    keyToggle: '按键切换',
    holdToTalk: '按住说话',
    followVrcSwitch: '随VRC开关(0.2s延迟)',
    microphoneCustomThreshold: '麦克风自定义阈值',
    microphoneKeyToggleHotkey: '麦克风按键切换快捷键',
    microphoneHoldKey: '麦克风按住说话按键',
    desktopAudioSource: '桌面音频源/麦克风',
    desktopAudioVoiceMode: '桌面音频语音模式',
    desktopAudioKeyToggleHotkey: '桌面音频按键切换快捷键',
    desktopAudioHoldKey: '桌面音频按住开启按键',
    systemDefault: '系统默认',
    calibrateThreshold: '校准阈值',
    desktopAudioCustomThreshold: '桌面音频自定义阈值',
    calibrateThresholdTitle: '阈值校准',
    calibrateThresholdDescription: '校准将帮助您设置合适的语音检测阈值',
    calibrateMicThreshold: '校准麦克风阈值',
    calibrateDesktopThreshold: '校准桌面音频阈值',
    calibrationStep1: '准备测量背景噪音，请保持安静',
    calibrationStep2: '开始测量噪音...',
    calibrationStep3: '噪音测量完成',
    calibrationStep4: '准备测量说话音量，请在提示后用正常音量说话',
    calibrationStep5: '请开始说话！',
    calibrationStep6: '说话测量完成',
    calibrationStep7: '计算得到的 VAD 能量阈值',
    calibrationComplete: '校准完成',
    calibrationFailed: '校准失败',
    noiseLevel: '噪音水平',
    speechLevel: '说话水平',
    calculatedThreshold: '计算阈值'
  },
  
  // 翻译引擎选项
  translationEngines: {
    developerServer: '开发者服务器',
    alibaba: '阿里巴巴',
    google: '谷歌(中国大陆地区不可用)',
    myMemory: 'MyMemory',
    baidu: '百度(坏的)',
    modernMt: 'ModernMt',
    volcEngine: '火山翻译',
    iciba: '金山词霸',
    iflytek: '讯飞智能',
    bing: 'Bing',
    lingvanex: 'Lingvanex',
    yandex: 'Yandex',
    itranslate: 'Itranslate',
    deepl: 'Deepl',
    cloudTranslation: '云译',
    qqTranSmart: '腾讯交互翻译',
    sogou: '搜狗',
    qqFanyi: '腾讯翻译君',
    youdao: '有道',
    iflyrec: '讯飞听见',
    hujiang: '沪江',
    yeekit: '中译语通',
    openai: '自定义AI翻译(openai兼容接口)'
  },
  
  // 工具提示
  tooltips: {
    canSpeakChineseOutputJapanese: '可说中文输出日语',
    ifTranslationErrorCheckServerSupport: '如果翻译时报错请检查服务端是否支持',
    ifTranslationErrorTryChangeEngine: '如果翻译提示翻译异常，可以尝试更换引擎',
    onlySingleLetterKey: '只允许单个字母按键',
    notRecommendedToEnable: '不建议开启',
    recommendCopyFromModelParams: '推荐从下方模型参数中复制参数路径'
  },
  
  // 日志
  logs: {
    realTimeLogs: '实时日志'
  },
  
  // 表格列
  table: {
    text: '文本',
    log: '日志',
    date: '日期',
    triggerCount: '触发次数',
    parameterName: '参数名称',
    parameterPath: '参数路径',
    parameterType: '参数类型'
  },
  
  // 表单标签
  form: {
    username: '用户名',
    password: '密码',
    defaultAction: '默认动作',
    keyword: '关键词',
    addKeyword: '添加关键词',
    customScriptName: '自定义脚本名称',
    customScriptDirectory: '自定义脚本目录',
    addScript: '添加脚本',
    deleteSelectedScript: '删除选定脚本',
    customScriptNameAndKeywords: '自定义脚本名称与关键词',
    customScriptExecutionActions: '自定义脚本执行动作',
    action: '动作',
    vrcParameterPath: 'VRC参数路径',
    vrcParameterValue: 'VRC参数值',
    vrcParameterType: 'VRC参数类型',
    duration: '持续时间',
    currentModelParameters: '当前模型参数',
    modelName: '模型名称',
    modelId: '模型ID',
    modelOscFilePath: '模型OSC文件路径',
    getModelParameters: '获取模型参数',
    localRecognitionModelRealTimeTextOutputInterval: '本地识别模型实时文本输出间隔',
    translationModeVrcTextboxOutputStyle: '翻译模式VRC文本框输出样式',
    textSendModeVrcTextboxOutputStyle: '文本发送模式VRC文本框输出样式',
    externalTextboxTextEmbeddingTemplate: '外源文本框文字嵌入模板',
    bitmapScreenRowsAndColumns: '点阵屏行列数',
    rows: '行数',
    columns: '列数',
    bitmapScreenColorMode: '点阵屏彩色模式',
    dynamicVolumeThreshold: '动态音量阈值',
    translationTemplateDescription: '下方{translatedText}会被替换为译文，{text}会被替换为原文,{translatedText2}为第二语言译文，{translatedText3}为第三语言译文',
    externalTemplateDescription: '下方{clientdata}会被替换为本软件输出内容，{serverdata}会被替换为外部osc接收内容的文本框内容',
    pleaseEnterText: '请输入文本',
    pleaseEnterName: '请输入名称',
    pleaseEnterVrcParameterPath: '请输入VRC参数路径',
    pleaseEnterVrcParameterValue: '请输入VRC参数值',
    pleaseEnterDuration: '请输入持续时间'
  },
  
  // 统计页面
  stats: {
    dailyRequestCount: '日请求数量',
    displayDateCount: '显示日期数：',
    successCount: '成功数',
    failureCount: '失败数',
    refresh: '刷新',
    times: '次'
  },
  
  // 脚本配置
  scripts: {
    apiAccountConfig: 'api账户配置',
    defaultScriptKeywordsConfig: '默认脚本关键词配置',
    customScriptConfig: '自定义脚本配置',
    confirmDeleteScript: '请确认是否删除自定义脚本:',
    deleteSuccess: '删除成功',
    cancelDelete: '取消删除'
  },
  
  // 配置引导
  guide: {
    setupGuide: '配置引导',
    simpleSetup: '配置引导',
    
    // 简易配置引导步骤
    simpleStep1Title: 'VRChat OSC',
    simpleStep1Desc: '配置VRChat OSC连接',
    simpleStep2Title: '基础配置',
    simpleStep2Desc: '设置默认模式和语言',
    simpleStep3Title: '麦克风配置',
    simpleStep3Desc: '配置麦克风相关设置',
    simpleStep4Title: '桌面音频配置',
    simpleStep4Desc: '配置桌面音频捕捉',
    simpleStep5Title: '语音合成配置',
    simpleStep5Desc: '配置TTS输出设置',
    simpleStep6Title: 'SteamVR显示配置',
    simpleStep6Desc: '配置SteamVR显示',
    simpleStep7Title: '完成配置',
    simpleStep7Desc: '确认所有设置',
    

    
    // VRChat OSC配置
    vrchatOscSetup: 'VRChat OSC配置',
    vrchatOscAlertTitle: 'VRChat OSC配置步骤',
    vrchatOscStep1: '1. 打开VRChat',
    vrchatOscStep2: '2. 通过轮盘菜单进入选项-OSC-开启',
    vrchatOscStep3: '3. 通过OSC调试打开数字端口',
    vrchatOscStep4: '4. 检查端口是否为默认9000，如果不是请修改',
    currentOscSettings: '当前OSC设置',
    
    // 端口检查
    portCheck: '端口检查',
    portCheckTitle: 'OSC端口检查',
    portCheckDesc: '请检查VRChat中的OSC端口设置，确保与下方配置保持一致。',
    
    // 基础配置
    basicConfig: '基础配置',
    basicConfigTitle: '基础配置说明',
    basicConfigDesc: '设置默认模式、语音识别语言和翻译语言等基础配置。',
    
    // 麦克风配置
    microphoneConfig: '麦克风配置',
    microphoneConfigTitle: '麦克风配置说明',
    microphoneConfigDesc: '配置麦克风设备、语音模式、阈值和快捷键等设置。',
    
    // 桌面音频配置
    desktopAudioConfig: '桌面音频配置',
    desktopAudioConfigTitle: '桌面音频配置说明',
    desktopAudioConfigDesc: '配置桌面音频捕捉、翻译引擎和语音控制等设置。',
    
    // 翻译功能配置
    translationConfig: '翻译功能配置',
    translationFeatureTitle: '翻译功能说明',
    translationFeatureDesc: '启用桌面音频捕捉可以翻译其他玩家的语音，让您更好地理解多语言环境中的对话。',
    desktopAudioCapture: '桌面音频捕捉设置',
    
    // 语音控制配置
    voiceControlConfig: '语音控制配置',
    voiceControlTitle: '语音控制说明',
    voiceControlDesc: '配置麦克风设备、语音模式和阈值等语音控制相关设置。',
    
    // SteamVR配置
    steamvrConfig: 'SteamVR显示配置',
    steamvrTitle: 'SteamVR显示说明',
    steamvrDesc: '配置在SteamVR中的文本显示位置、大小等设置。',
    
    // TTS配置
    ttsConfig: 'TTS输出配置',
    ttsTitle: 'TTS输出说明',
    ttsDesc: '配置语音合成输出模式和扬声器设备。',
    
    // 翻译引擎配置
    translationEngineConfig: '翻译引擎配置',
    translationEngineTitle: '翻译引擎说明',
    translationEngineDesc: '选择不同的翻译引擎和接入点地区。',
    
    // 完成配置
    setupComplete: '配置完成',
    setupCompleteTitle: '配置完成！',
    setupCompleteSubtitle: '您的VRCLS已经完成配置，现在可以开始使用了。',
    configSummary: '配置摘要',
    completeSetup: '完成配置',
    simpleSetupCompletedMessage: '配置完成！您可以开始使用VRCLS了。',
    previous: '上一步',
    next: '下一步',
    startGuide: '开始引导',
    skipGuide: '跳过引导',
    skipGuideTitle: '跳过配置引导',
    skipGuideConfirm: '确定要跳过配置引导吗？您可以稍后在侧边栏重新打开引导。',
    guideSkippedMessage: '已跳过配置引导，您可以稍后重新打开。',
    stepProgress: '步骤 {current} / {total}'
  }
} 