export default {
  // Common
  common: {
    minimize: 'Minimize',
    maximize: 'Maximize',
    exitMaximize: 'Exit Maximize',
    close: 'Close',
    save: 'Save',
    cancel: 'Cancel',
    confirm: 'Confirm',
    enable: 'Enable',
    disable: 'Disable',
    on: 'On',
    off: 'Off',
    getConfig: 'Get Config',
    saveConfig: 'Save Config',
    saveAndRestart: 'Save & Restart',
    restartService: 'Restart Service',
    error: 'Error Occurred',
    copySuccess: 'Copy Success',
    copyFailed: 'Copy Failed'
  },
  
  // Header and menu
  header: {
    title: 'VRCLS Panel',
    home: 'Home',
    usageStats: 'Usage Stats',
    controlModeConfig: 'Control Mode Config',
    programSettings: 'Program Settings',
    logs: 'Logs'
  },
  
  // Home
  home: {
    micRecognitionResult: 'Microphone Recognition Result',
    desktopRecognitionResult: 'Desktop Audio Recognition Result',
    inputPlaceholder: 'Enter text to translate',
    send: 'Send'
  },
  
  // Program config
  config: {
    programConfig: 'Program Configuration',
    serverUrl: 'Server URL',
    oscPort: 'OSC Port',
    oscIpAddress: 'OSC IP Address',
    defaultMode: 'Default Mode',
    control: 'Control',
    translation: 'Translation',
    textSend: 'Text Send',
    bitmapLed: 'Bitmap LED',
    speechRecognitionLanguage: 'Speech Recognition Language',
    defaultTranslationLanguage: 'Default Translation Language',
    secondTranslationLanguage: 'Second Translation Language',
    thirdTranslationLanguage: 'Third Translation Language',
    separateDesktopAudioCapture: 'Separate Desktop Audio Capture',
    useDesktopAudio: 'Use Desktop Audio',
    useVirtualSoundcardMic: 'Use Virtual Soundcard Microphone',
    micUseLocalRecognitionModel: 'Microphone Use Local Recognition Model',
    desktopAudioUseLocalRecognitionModel: 'Desktop Audio Use Local Recognition Model',
    steamvrPalmOutputDisplay: 'SteamVR Palm Output Display',
    steamvrDisplayPosition: 'SteamVR Display Position',
    rightHand: 'Right Hand',
    leftHand: 'Left Hand',
    leftAndRightHand: 'Left + Right Hand',
    steamvrDisplaySize: 'SteamVR Display Size',
    ttsOutput: 'TTS Output',
    translationModeMicTranslationOutput: 'Translation Mode Microphone Translation Output',
    textSendModeMicOriginalText: 'Text Send Mode Microphone Original Text',
    translationModeMicAndDesktopAudioTranslationOutput: 'Translation Mode Microphone + Desktop Audio Translation Output',
    ttsOutputSpeaker: 'TTS Output Speaker',
    micTranslationEngine: 'Microphone Translation Engine',
    desktopAudioTranslationEngine: 'Desktop Audio Translation Engine',
    translationEngineAccessPointRegion: 'Translation Engine Access Point Region',
    mainlandChina: 'Mainland China',
    other: 'Other',
    oscOutput: 'OSC Output',
    pause: 'Pause',
    emotionRecognitionEmojiOutput: 'Emotion Recognition Emoji Output',
    externalOscServerPort: 'External OSC Server Port',
    receiveExternalOscServerPort: 'Receive External OSC Server Port',
    receiveExternalOscServerIpAddress: 'Receive External OSC Server IP Address'
  },
  
  // Voice control config
  voiceControl: {
    voiceControlConfig: 'Voice Control Configuration',
    microphone: 'Microphone',
    systemDefaultMicrophone: 'System Default Microphone',
    microphoneVoiceMode: 'Microphone Voice Mode',
    continuousOn: 'Continuous On',
    keyToggle: 'Key Toggle',
    holdToTalk: 'Hold to Talk',
    followVrcSwitch: 'Follow VRC Switch (0.2s delay)',
    microphoneCustomThreshold: 'Microphone Custom Threshold',
    microphoneKeyToggleHotkey: 'Microphone Key Toggle Hotkey',
    microphoneHoldKey: 'Microphone Hold to Talk Key',
    desktopAudioSource: 'Desktop Audio Source/Microphone',
    desktopAudioVoiceMode: 'Desktop Audio Voice Mode',
    desktopAudioKeyToggleHotkey: 'Desktop Audio Key Toggle Hotkey',
    desktopAudioHoldKey: 'Desktop Audio Hold to Talk Key',
    systemDefault: 'System Default',
    calibrateThreshold: 'Calibrate Threshold',
    desktopAudioCustomThreshold: 'Desktop Audio Custom Threshold',
    calibrateThresholdTitle: 'Threshold Calibration',
    calibrateThresholdDescription: 'Calibration will help you set appropriate voice detection threshold',
    calibrateMicThreshold: 'Calibrate Microphone Threshold',
    calibrateDesktopThreshold: 'Calibrate Desktop Audio Threshold',
    calibrationStep1: 'Preparing to measure background noise, please stay quiet',
    calibrationStep2: 'Starting noise measurement...',
    calibrationStep3: 'Noise measurement completed',
    calibrationStep4: 'Preparing to measure speech volume, please speak at normal volume when prompted',
    calibrationStep5: 'Please start speaking!',
    calibrationStep6: 'Speech measurement completed',
    calibrationStep7: 'Calculated VAD energy threshold',
    calibrationComplete: 'Calibration completed',
    calibrationFailed: 'Calibration failed',
    noiseLevel: 'Noise Level',
    speechLevel: 'Speech Level',
    calculatedThreshold: 'Calculated Threshold'
  },
  
  // Translation engines
  translationEngines: {
    developerServer: 'Developer Server',
    alibaba: 'Alibaba',
    google: 'Google (Not available in Mainland China)',
    myMemory: 'MyMemory',
    baidu: 'Baidu (Broken)',
    modernMt: 'ModernMt',
    volcEngine: 'VolcEngine',
    iciba: 'iCIBA',
    iflytek: 'iFlytek',
    bing: 'Bing',
    lingvanex: 'Lingvanex',
    yandex: 'Yandex',
    itranslate: 'iTranslate',
    deepl: 'DeepL',
    cloudTranslation: 'Cloud Translation',
    qqTranSmart: 'QQ TranSmart',
    sogou: 'Sogou',
    qqFanyi: 'QQ Fanyi',
    youdao: 'Youdao',
    iflyrec: 'iFlyrec',
    hujiang: 'Hujiang',
    yeekit: 'Yeekit'
  },
  
  // Tooltips
  tooltips: {
    canSpeakChineseOutputJapanese: 'Can speak Chinese output Japanese',
    ifTranslationErrorCheckServerSupport: 'If translation error occurs, check server support',
    ifTranslationErrorTryChangeEngine: 'If translation error occurs, try changing engine',
    onlySingleLetterKey: 'Only single letter keys allowed',
    notRecommendedToEnable: 'Not recommended to enable',
    recommendCopyFromModelParams: 'Recommended to copy parameter path from model parameters below'
  },
  
  // Logs
  logs: {
    realTimeLogs: 'Real-time Logs'
  },
  
  // Table columns
  table: {
    text: 'Text',
    log: 'Log',
    date: 'Date',
    triggerCount: 'Trigger Count',
    parameterName: 'Parameter Name',
    parameterPath: 'Parameter Path',
    parameterType: 'Parameter Type'
  },
  
  // Form labels
  form: {
    username: 'Username',
    password: 'Password',
    defaultAction: 'Default Action',
    keyword: 'Keyword',
    addKeyword: 'Add Keyword',
    customScriptName: 'Custom Script Name',
    customScriptDirectory: 'Custom Script Directory',
    addScript: 'Add Script',
    deleteSelectedScript: 'Delete Selected Script',
    customScriptNameAndKeywords: 'Custom Script Name and Keywords',
    customScriptExecutionActions: 'Custom Script Execution Actions',
    action: 'Action',
    vrcParameterPath: 'VRC Parameter Path',
    vrcParameterValue: 'VRC Parameter Value',
    vrcParameterType: 'VRC Parameter Type',
    duration: 'Duration',
    currentModelParameters: 'Current Model Parameters',
    modelName: 'Model Name',
    modelId: 'Model ID',
    modelOscFilePath: 'Model OSC File Path',
    getModelParameters: 'Get Model Parameters',
    localRecognitionModelRealTimeTextOutputInterval: 'Local Recognition Model Real-time Text Output Interval',
    translationModeVrcTextboxOutputStyle: 'Translation Mode VRC Textbox Output Style',
    textSendModeVrcTextboxOutputStyle: 'Text Send Mode VRC Textbox Output Style',
    externalTextboxTextEmbeddingTemplate: 'External Textbox Text Embedding Template',
    bitmapScreenRowsAndColumns: 'Bitmap Screen Rows and Columns',
    rows: 'Rows',
    columns: 'Columns',
    bitmapScreenColorMode: 'Bitmap Screen Color Mode',
    dynamicVolumeThreshold: 'Dynamic Volume Threshold',
    translationTemplateDescription: 'Below {translatedText} will be replaced with translation, {text} will be replaced with original text, {translatedText2} is second language translation, {translatedText3} is third language translation',
    externalTemplateDescription: 'Below {clientdata} will be replaced with this software output content, {serverdata} will be replaced with external osc received content textbox content',
    pleaseEnterText: 'Please enter text',
    pleaseEnterName: 'Please enter name',
    pleaseEnterVrcParameterPath: 'Please enter VRC parameter path',
    pleaseEnterVrcParameterValue: 'Please enter VRC parameter value',
    pleaseEnterDuration: 'Please enter duration'
  },
  
  // Stats page
  stats: {
    dailyRequestCount: 'Daily Request Count',
    displayDateCount: 'Display Date Count:',
    successCount: 'Success Count',
    failureCount: 'Failure Count',
    refresh: 'Refresh',
    times: 'times'
  },
  
  // Script config
  scripts: {
    apiAccountConfig: 'API Account Configuration',
    defaultScriptKeywordsConfig: 'Default Script Keywords Configuration',
    customScriptConfig: 'Custom Script Configuration',
    confirmDeleteScript: 'Please confirm to delete custom script:',
    deleteSuccess: 'Delete Success',
    cancelDelete: 'Cancel Delete'
  },
  
  // Setup guide
  guide: {
    setupGuide: 'Setup Guide',
    simpleSetup: 'Setup Guide',
    
    // Simple setup guide steps
    simpleStep1Title: 'VRChat OSC',
    simpleStep1Desc: 'Configure VRChat OSC connection',
    simpleStep2Title: 'Basic Config',
    simpleStep2Desc: 'Set default mode and languages',
    simpleStep3Title: 'Microphone Config',
    simpleStep3Desc: 'Configure microphone settings',
    simpleStep4Title: 'Desktop Audio Config',
    simpleStep4Desc: 'Configure desktop audio capture',
    simpleStep5Title: 'TTS Config',
    simpleStep5Desc: 'Configure TTS output settings',
    simpleStep6Title: 'SteamVR Display Config',
    simpleStep6Desc: 'Configure SteamVR display',
    simpleStep7Title: 'Complete Setup',
    simpleStep7Desc: 'Confirm all settings',
    

    
    // VRChat OSC configuration
    vrchatOscSetup: 'VRChat OSC Configuration',
    vrchatOscAlertTitle: 'VRChat OSC Setup Steps',
    vrchatOscStep1: '1. Open VRChat',
    vrchatOscStep2: '2. Go to Options-OSC-Enable via wheel menu',
    vrchatOscStep3: '3. Open digital port via OSC debug',
    vrchatOscStep4: '4. Check if port is default 9000, modify if not',
    currentOscSettings: 'Current OSC Settings',
    
    // Port check
    portCheck: 'Port Check',
    portCheckTitle: 'OSC Port Check',
    portCheckDesc: 'Please check the OSC port settings in VRChat to ensure consistency with the configuration below.',
    
    // Basic configuration
    basicConfig: 'Basic Configuration',
    basicConfigTitle: 'Basic Configuration Description',
    basicConfigDesc: 'Set default mode, speech recognition language, and translation languages.',
    
    // Microphone configuration
    microphoneConfig: 'Microphone Configuration',
    microphoneConfigTitle: 'Microphone Configuration Description',
    microphoneConfigDesc: 'Configure microphone device, voice mode, threshold, and hotkeys.',
    
    // Desktop audio configuration
    desktopAudioConfig: 'Desktop Audio Configuration',
    desktopAudioConfigTitle: 'Desktop Audio Configuration Description',
    desktopAudioConfigDesc: 'Configure desktop audio capture, translation engine, and voice control settings.',
    
    // Translation feature configuration
    translationConfig: 'Translation Feature Configuration',
    translationFeatureTitle: 'Translation Feature Description',
    translationFeatureDesc: 'Enabling desktop audio capture can translate other players\' speech, helping you better understand conversations in multilingual environments.',
    desktopAudioCapture: 'Desktop Audio Capture Settings',
    
    // Voice control configuration
    voiceControlConfig: 'Voice Control Configuration',
    voiceControlTitle: 'Voice Control Description',
    voiceControlDesc: 'Configure microphone device, voice mode, and threshold settings.',
    
    // SteamVR configuration
    steamvrConfig: 'SteamVR Display Configuration',
    steamvrTitle: 'SteamVR Display Description',
    steamvrDesc: 'Configure text display position, size, and other settings in SteamVR.',
    
    // TTS configuration
    ttsConfig: 'TTS Output Configuration',
    ttsTitle: 'TTS Output Description',
    ttsDesc: 'Configure text-to-speech output mode and speaker device.',
    
    // Translation engine configuration
    translationEngineConfig: 'Translation Engine Configuration',
    translationEngineTitle: 'Translation Engine Description',
    translationEngineDesc: 'Select different translation engines and access point regions.',
    
    // Complete setup
    setupComplete: 'Setup Complete',
    setupCompleteTitle: 'Setup Complete!',
    setupCompleteSubtitle: 'Your VRCLS has completed configuration and is ready to use.',
    configSummary: 'Configuration Summary',
    completeSetup: 'Complete Setup',
    simpleSetupCompletedMessage: 'Setup completed! You can now start using VRCLS.',
    previous: 'Previous',
    next: 'Next',
    startGuide: 'Start Guide',
    skipGuide: 'Skip Guide',
    skipGuideTitle: 'Skip Setup Guide',
    skipGuideConfirm: 'Are you sure you want to skip the setup guide? You can reopen it later from the sidebar.',
    guideSkippedMessage: 'Setup guide skipped. You can reopen it later.',
    stepProgress: 'Step {current} / {total}'
  }
} 