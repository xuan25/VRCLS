export default {
  // 共通
  common: {
    minimize: '最小化',
    maximize: '最大化',
    exitMaximize: '最大化解除',
    close: '閉じる',
    save: '保存',
    cancel: 'キャンセル',
    confirm: '確認',
    enable: '有効',
    disable: '無効',
    on: 'オン',
    off: 'オフ',
    getConfig: '設定取得',
    saveConfig: '設定保存',
    saveAndRestart: '保存して再起動',
    restartService: 'サービス再起動',
    error: 'エラーが発生しました',
    copySuccess: 'コピー成功',
    copyFailed: 'コピー失敗'
  },
  
  // ヘッダーとメニュー
  header: {
    title: 'VRCLSパネル',
    home: 'ホーム',
    usageStats: '使用統計',
    controlModeConfig: '制御モード設定',
    programSettings: 'プログラム設定',
    logs: 'ログ'
  },
  
  // ホーム
  home: {
    micRecognitionResult: 'マイク認識結果',
    desktopRecognitionResult: 'デスクトップ音声認識結果',
    inputPlaceholder: '翻訳するテキストを入力してください',
    send: '送信'
  },
  
  // プログラム設定
  config: {
    programConfig: 'プログラム設定',
    serverUrl: 'サーバーURL',
    oscPort: 'OSCポート',
    oscIpAddress: 'OSC IPアドレス',
    defaultMode: 'デフォルトモード',
    control: '制御',
    translation: '翻訳',
    textSend: 'テキスト送信',
    bitmapLed: 'ビットマップLED',
    speechRecognitionLanguage: '音声認識言語',
    defaultTranslationLanguage: 'デフォルト翻訳言語',
    secondTranslationLanguage: '第二翻訳言語',
    thirdTranslationLanguage: '第三翻訳言語',
    separateDesktopAudioCapture: 'デスクトップ音声キャプチャ分離',
    useDesktopAudio: 'デスクトップ音声を使用',
    useVirtualSoundcardMic: '仮想サウンドカードマイクを使用',
    micUseLocalRecognitionModel: 'マイクローカル認識モデル使用',
    desktopAudioUseLocalRecognitionModel: 'デスクトップ音声ローカル認識モデル使用',
    steamvrPalmOutputDisplay: 'SteamVR手のひら出力表示',
    steamvrDisplayPosition: 'SteamVR表示位置',
    rightHand: '右手',
    leftHand: '左手',
    leftAndRightHand: '左手+右手',
    steamvrDisplaySize: 'SteamVR表示サイズ',
    ttsOutput: 'TTS出力',
    translationModeMicTranslationOutput: '翻訳モードマイク翻訳出力',
    textSendModeMicOriginalText: 'テキスト送信モードマイク原文',
    translationModeMicAndDesktopAudioTranslationOutput: '翻訳モードマイク+デスクトップ音声翻訳出力',
    ttsOutputSpeaker: 'TTS出力スピーカー',
    micTranslationEngine: 'マイク翻訳エンジン',
    desktopAudioTranslationEngine: 'デスクトップ音声翻訳エンジン',
    translationEngineAccessPointRegion: '翻訳エンジンアクセスポイント地域',
    mainlandChina: '中国本土',
    other: 'その他',
    oscOutput: 'OSC出力',
    pause: '一時停止',
    emotionRecognitionEmojiOutput: '感情認識絵文字出力',
    externalOscServerPort: '外部OSCサーバーポート',
    receiveExternalOscServerPort: '外部OSCサーバーポート受信',
    receiveExternalOscServerIpAddress: '外部OSCサーバーIPアドレス受信',
    openaiConfig: 'OpenAI設定',
    openaiApiKey: 'APIキー',
    openaiApiUrl: 'API URL',
    openaiModel: 'モデル',
    capOutputStyle: 'テーブル内表示形式',
    capOutputStyle1: 'すべての言語を出力',
    capOutputStyle2: 'デフォルト翻訳言語のみ出力',
    capOutputStyle3: 'デフォルト翻訳言語+認識原文'
  },
  
  // 音声制御設定
  voiceControl: {
    voiceControlConfig: '音声制御設定',
    microphone: 'マイク',
    systemDefaultMicrophone: 'システムデフォルトマイク',
    microphoneVoiceMode: 'マイク音声モード',
    continuousOn: '連続オン',
    keyToggle: 'キートグル',
    holdToTalk: '押し続けて話す',
    followVrcSwitch: 'VRCスイッチに追従(0.2秒遅延)',
    microphoneCustomThreshold: 'マイクカスタム閾値',
    microphoneKeyToggleHotkey: 'マイクキートグルホットキー',
    microphoneHoldKey: 'マイク押し続けて話すキー',
    desktopAudioSource: 'デスクトップ音声ソース/マイク',
    desktopAudioVoiceMode: 'デスクトップ音声音声モード',
    desktopAudioKeyToggleHotkey: 'デスクトップ音声キートグルホットキー',
    desktopAudioHoldKey: 'デスクトップ音声押し続けて話すキー',
    systemDefault: 'システムデフォルト',
    calibrateThreshold: '閾値キャリブレーション',
    desktopAudioCustomThreshold: 'デスクトップ音声カスタム閾値',
    calibrateThresholdTitle: '閾値キャリブレーション',
    calibrateThresholdDescription: 'キャリブレーションは適切な音声検出閾値を設定するのに役立ちます',
    calibrateMicThreshold: 'マイク閾値キャリブレーション',
    calibrateDesktopThreshold: 'デスクトップ音声閾値キャリブレーション',
    calibrationStep1: '背景ノイズの測定を準備中、静かにしてください',
    calibrationStep2: 'ノイズ測定開始...',
    calibrationStep3: 'ノイズ測定完了',
    calibrationStep4: '音声音量の測定を準備中、指示があったら通常の音量で話してください',
    calibrationStep5: '話し始めてください！',
    calibrationStep6: '音声測定完了',
    calibrationStep7: '計算されたVADエネルギー閾値',
    calibrationComplete: 'キャリブレーション完了',
    calibrationFailed: 'キャリブレーション失敗',
    noiseLevel: 'ノイズレベル',
    speechLevel: '音声レベル',
    calculatedThreshold: '計算された閾値'
  },
  
  // 翻訳エンジン
  translationEngines: {
    developerServer: '開発者サーバー',
    alibaba: 'アリババ',
    google: 'グーグル(中国本土では利用不可)',
    myMemory: 'MyMemory',
    baidu: '百度(壊れている)',
    modernMt: 'ModernMt',
    volcEngine: '火山翻訳',
    iciba: 'iCIBA',
    iflytek: 'iFlytek',
    bing: 'Bing',
    lingvanex: 'Lingvanex',
    yandex: 'Yandex',
    itranslate: 'iTranslate',
    deepl: 'DeepL',
    cloudTranslation: 'クラウド翻訳',
    qqTranSmart: 'QQ TranSmart',
    sogou: 'Sogou',
    qqFanyi: 'QQ Fanyi',
    youdao: 'Youdao',
    iflyrec: 'iFlyrec',
    hujiang: 'Hujiang',
    yeekit: 'Yeekit',
    openai: 'カスタムAI翻訳(openai互換インタフェース)'
  },
  
  // ツールチップ
  tooltips: {
    canSpeakChineseOutputJapanese: '中国語を話して日本語を出力',
    ifTranslationErrorCheckServerSupport: '翻訳エラーが発生した場合、サーバーサポートを確認してください',
    ifTranslationErrorTryChangeEngine: '翻訳エラーが発生した場合、エンジンの変更を試してください',
    onlySingleLetterKey: '単一の文字キーのみ許可',
    notRecommendedToEnable: '有効化は推奨されません',
    recommendCopyFromModelParams: '下のモデルパラメータからパラメータパスをコピーすることを推奨'
  },
  
  // ログ
  logs: {
    realTimeLogs: 'リアルタイムログ'
  },
  
  // テーブル列
  table: {
    text: 'テキスト',
    log: 'ログ',
    date: '日付',
    triggerCount: 'トリガー回数',
    parameterName: 'パラメータ名',
    parameterPath: 'パラメータパス',
    parameterType: 'パラメータタイプ'
  },
  
  // フォームラベル
  form: {
    username: 'ユーザー名',
    password: 'パスワード',
    defaultAction: 'デフォルトアクション',
    keyword: 'キーワード',
    addKeyword: 'キーワード追加',
    customScriptName: 'カスタムスクリプト名',
    customScriptDirectory: 'カスタムスクリプトディレクトリ',
    addScript: 'スクリプト追加',
    deleteSelectedScript: '選択されたスクリプトを削除',
    customScriptNameAndKeywords: 'カスタムスクリプト名とキーワード',
    customScriptExecutionActions: 'カスタムスクリプト実行アクション',
    action: 'アクション',
    vrcParameterPath: 'VRCパラメータパス',
    vrcParameterValue: 'VRCパラメータ値',
    vrcParameterType: 'VRCパラメータタイプ',
    duration: '持続時間',
    currentModelParameters: '現在のモデルパラメータ',
    modelName: 'モデル名',
    modelId: 'モデルID',
    modelOscFilePath: 'モデルOSCファイルパス',
    getModelParameters: 'モデルパラメータ取得',
    localRecognitionModelRealTimeTextOutputInterval: 'ローカル認識モデルリアルタイムテキスト出力間隔',
    translationModeVrcTextboxOutputStyle: '翻訳モードVRCテキストボックス出力スタイル',
    textSendModeVrcTextboxOutputStyle: 'テキスト送信モードVRCテキストボックス出力スタイル',
    externalTextboxTextEmbeddingTemplate: '外部テキストボックステキスト埋め込みテンプレート',
    bitmapScreenRowsAndColumns: 'ビットマップ画面行と列',
    rows: '行',
    columns: '列',
    bitmapScreenColorMode: 'ビットマップ画面カラーモード',
    dynamicVolumeThreshold: '動的音量閾値',
    translationTemplateDescription: '下の{translatedText}は翻訳に置き換えられ、{text}は原文に置き換えられ、{translatedText2}は第二言語翻訳、{translatedText3}は第三言語翻訳です',
    externalTemplateDescription: '下の{clientdata}はこのソフトウェアの出力内容に置き換えられ、{serverdata}は外部osc受信内容テキストボックス内容に置き換えられます',
    pleaseEnterText: 'テキストを入力してください',
    pleaseEnterName: '名前を入力してください',
    pleaseEnterVrcParameterPath: 'VRCパラメータパスを入力してください',
    pleaseEnterVrcParameterValue: 'VRCパラメータ値を入力してください',
    pleaseEnterDuration: '持続時間を入力してください'
  },
  
  // 統計ページ
  stats: {
    dailyRequestCount: '日次リクエスト数',
    displayDateCount: '表示日数：',
    successCount: '成功数',
    failureCount: '失敗数',
    refresh: '更新',
    times: '回'
  },
  
  // スクリプト設定
  scripts: {
    apiAccountConfig: 'APIアカウント設定',
    defaultScriptKeywordsConfig: 'デフォルトスクリプトキーワード設定',
    customScriptConfig: 'カスタムスクリプト設定',
    confirmDeleteScript: 'カスタムスクリプトを削除することを確認してください：',
    deleteSuccess: '削除成功',
    cancelDelete: '削除キャンセル'
  },
  
  // 設定ガイド
  guide: {
    setupGuide: '設定ガイド',
    simpleSetup: '設定ガイド',
    
    // 簡易設定ガイドステップ
    simpleStep1Title: 'VRChat OSC',
    simpleStep1Desc: 'VRChat OSC接続の設定',
    simpleStep2Title: '基本設定',
    simpleStep2Desc: 'デフォルトモードと言語の設定',
    simpleStep3Title: 'マイク設定',
    simpleStep3Desc: 'マイク関連設定の構成',
    simpleStep4Title: 'デスクトップ音声設定',
    simpleStep4Desc: 'デスクトップ音声キャプチャの設定',
    simpleStep5Title: '音声合成設定',
    simpleStep5Desc: 'TTS出力設定の構成',
    simpleStep6Title: 'SteamVR表示設定',
    simpleStep6Desc: 'SteamVR表示の設定',
    simpleStep7Title: '設定完了',
    simpleStep7Desc: 'すべての設定の確認',
    

    
    // VRChat OSC設定
    vrchatOscSetup: 'VRChat OSC設定',
    vrchatOscAlertTitle: 'VRChat OSC設定手順',
    vrchatOscStep1: '1. VRChatを開く',
    vrchatOscStep2: '2. ホイールメニューからオプション-OSC-有効化',
    vrchatOscStep3: '3. OSCデバッグでデジタルポートを開く',
    vrchatOscStep4: '4. ポートがデフォルト9000かチェックし、違う場合は修正',
    currentOscSettings: '現在のOSC設定',
    
    // ポートチェック
    portCheck: 'ポートチェック',
    portCheckTitle: 'OSCポートチェック',
    portCheckDesc: 'VRChatのOSCポート設定を確認し、下の設定と一致することを確認してください。',
    
    // 基本設定
    basicConfig: '基本設定',
    basicConfigTitle: '基本設定の説明',
    basicConfigDesc: 'デフォルトモード、音声認識言語、翻訳言語などの基本設定。',
    
    // マイク設定
    microphoneConfig: 'マイク設定',
    microphoneConfigTitle: 'マイク設定の説明',
    microphoneConfigDesc: 'マイクデバイス、音声モード、閾値、ホットキーなどの設定。',
    
    // デスクトップ音声設定
    desktopAudioConfig: 'デスクトップ音声設定',
    desktopAudioConfigTitle: 'デスクトップ音声設定の説明',
    desktopAudioConfigDesc: 'デスクトップ音声キャプチャ、翻訳エンジン、音声制御設定の構成。',
    
    // 翻訳機能設定
    translationConfig: '翻訳機能設定',
    translationFeatureTitle: '翻訳機能の説明',
    translationFeatureDesc: 'デスクトップ音声キャプチャを有効にすると、他のプレイヤーの音声を翻訳でき、多言語環境での会話をよりよく理解できます。',
    desktopAudioCapture: 'デスクトップ音声キャプチャ設定',
    
    // 音声制御設定
    voiceControlConfig: '音声制御設定',
    voiceControlTitle: '音声制御の説明',
    voiceControlDesc: 'マイクデバイス、音声モード、閾値などの音声制御関連設定。',
    
    // SteamVR設定
    steamvrConfig: 'SteamVR表示設定',
    steamvrTitle: 'SteamVR表示の説明',
    steamvrDesc: 'SteamVRでのテキスト表示位置、サイズなどの設定。',
    
    // TTS設定
    ttsConfig: 'TTS出力設定',
    ttsTitle: 'TTS出力の説明',
    ttsDesc: '音声合成出力モードとスピーカーデバイスの設定。',
    
    // 翻訳エンジン設定
    translationEngineConfig: '翻訳エンジン設定',
    translationEngineTitle: '翻訳エンジンの説明',
    translationEngineDesc: '異なる翻訳エンジンとアクセスポイント地域の選択。',
    
    // 設定完了
    setupComplete: '設定完了',
    setupCompleteTitle: '設定完了！',
    setupCompleteSubtitle: 'VRCLSの設定が完了し、使用準備が整いました。',
    configSummary: '設定サマリー',
    completeSetup: '設定完了',
    simpleSetupCompletedMessage: '設定が完了しました！VRCLSの使用を開始できます。',
    previous: '前へ',
    next: '次へ',
    startGuide: 'ガイド開始',
    skipGuide: 'ガイドをスキップ',
    skipGuideTitle: '設定ガイドをスキップ',
    skipGuideConfirm: '設定ガイドをスキップしますか？後でサイドバーから再開できます。',
    guideSkippedMessage: '設定ガイドをスキップしました。後で再開できます。',
    stepProgress: 'ステップ {current} / {total}'
  }
} 