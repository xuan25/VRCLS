<template>

    <el-container>
        <el-header height="10vh" class="custom-header pywebview-drag-region">
            <!-- 居中的标题，使用绝对定位 -->
            <el-text tag="b" class="header-title-centered">{{ $t('header.title') }}</el-text>

            <!-- 右侧控件组 -->
            <div class="header-actions">
                <!-- 语言选择器 -->
                <el-select v-model="currentLocale" @change="changeLocale" style="margin-right: 15px; width: 100px;">
                    <el-option label="中文" value="zh" />
                    <el-option label="English" value="en" />
                    <el-option label="日本語" value="ja" />
                </el-select>
                <el-switch v-model="isDark" inline-prompt :active-icon="MoonIcon" :inactive-icon="SunIcon"
                    active-color="#2c2c2c" inactive-color="#f2f2f2" border-color="#dcdfe6" style="margin-right: 15px;"
                    @change="changeDark" />
                <el-tooltip :content="$t('common.minimize')" placement="bottom">
                    <el-button :icon="MinusIcon" circle @click="handleMinimize" />
                </el-tooltip>
                <el-tooltip :content="data.local.maximized ? $t('common.exitMaximize') : $t('common.maximize')" placement="bottom">
                    <el-button :icon="data.local.maximized ? RankIcon : FullScreenIcon" circle @click="toggleFullScreen" />
                </el-tooltip>
                <el-tooltip :content="$t('common.close')" placement="bottom">
                    <el-button :icon="CloseIcon" circle @click="handleClose" />
                </el-tooltip>
            </div>
        </el-header>
        <el-container>
            <el-aside width="200">
                <h5 class="mb-2">{{ data.local.versionstr }}</h5>
                <el-menu default-active="1" class="el-menu-vertical-demo" @select="menuClick">
                    <el-menu-item index="1">
                        <el-icon><icon-menu /></el-icon>
                        <span>{{ $t('header.home') }}</span>
                    </el-menu-item>
                    <el-menu-item index="2">
                        <el-icon><icon-menu /></el-icon>
                        <span>{{ $t('header.usageStats') }}</span>
                    </el-menu-item>
                    <el-menu-item index="3">
                        <el-icon><icon-menu /></el-icon>
                        <span>{{ $t('header.controlModeConfig') }}</span>
                    </el-menu-item>
                    <el-menu-item index="4">
                        <el-icon>
                            <setting />
                        </el-icon>
                        <span>{{ $t('header.programSettings') }}</span>
                    </el-menu-item>
                    <el-menu-item index="5">
                        <el-icon>
                            <document />
                        </el-icon>
                        <span>{{ $t('header.logs') }}</span>
                    </el-menu-item>
                </el-menu>
                
                <!-- 配置引导按钮 -->
                <div style="padding: 10px;">
                    <el-button type="primary" style="width: 100%;" @click="showSimpleGuide = true">
                        {{ $t('guide.setupGuide') }}
                    </el-button>
                </div>
            </el-aside>
            <el-main>
                <!-- 简易配置引导 -->
                <el-dialog v-model="showSimpleGuide" :title="$t('guide.simpleSetup')" width="800px" :close-on-click-modal="false" :close-on-press-escape="false" :show-close="false">
                    <div class="guide-container">
                        <el-steps :active="currentSimpleStep" finish-status="success" align-center>
                            <el-step :title="$t('guide.simpleStep1Title')" :description="$t('guide.simpleStep1Desc')" />
                            <el-step :title="$t('guide.simpleStep2Title')" :description="$t('guide.simpleStep2Desc')" />
                            <el-step :title="$t('guide.simpleStep3Title')" :description="$t('guide.simpleStep3Desc')" />
                            <el-step :title="$t('guide.simpleStep4Title')" :description="$t('guide.simpleStep4Desc')" />
                            <el-step :title="$t('guide.simpleStep5Title')" :description="$t('guide.simpleStep5Desc')" />
                            <el-step :title="$t('guide.simpleStep6Title')" :description="$t('guide.simpleStep6Desc')" />
                            <el-step :title="$t('guide.simpleStep7Title')" :description="$t('guide.simpleStep7Desc')" />
                        </el-steps>

                        <div class="guide-content">
                            <!-- 步骤进度指示器 -->
                            <div class="guide-progress-indicator">
                                <el-progress :percentage="(currentSimpleStep + 1) * 14.28" :show-text="false" />
                                <p class="progress-text">{{ $t('guide.stepProgress', { current: currentSimpleStep + 1, total: 7 }) }}</p>
                            </div>
                            
                            <!-- 步骤1: VRChat OSC配置 -->
                            <div v-if="currentSimpleStep === 0" class="guide-step">
                                <h3>{{ $t('guide.vrchatOscSetup') }}</h3>
                                <div class="guide-instructions">
                                    <el-alert :title="$t('guide.vrchatOscAlertTitle')" type="info" show-icon :closable="false">
                                        <template #default>
                                            <div class="guide-instruction-list">
                                                <p>{{ $t('guide.vrchatOscStep1') }}</p>
                                                <p>{{ $t('guide.vrchatOscStep2') }}</p>
                                                <p>{{ $t('guide.vrchatOscStep3') }}</p>
                                                <p>{{ $t('guide.vrchatOscStep4') }}</p>
                                            </div>
                                        </template>
                                    </el-alert>
                                    
                                    <div class="guide-config-section">
                                        <h4>{{ $t('guide.currentOscSettings') }}</h4>
                                        <el-form label-width="120px">
                                            <el-form-item :label="$t('config.oscPort')">
                                                <el-input v-model="data.config['osc-port']" type="number" />
                                            </el-form-item>
                                            <el-form-item :label="$t('config.oscIpAddress')">
                                                <el-input v-model="data.config['osc-ip']" />
                                            </el-form-item>
                                        </el-form>
                                    </div>
                                </div>
                            </div>

                            <!-- 步骤2: 基础配置 -->
                            <div v-if="currentSimpleStep === 1" class="guide-step">
                                <h3>{{ $t('guide.basicConfig') }}</h3>
                                <div class="guide-instructions">
                                    <el-alert :title="$t('guide.basicConfigTitle')" type="success" show-icon :closable="false">
                                        <template #default>
                                            <p>{{ $t('guide.basicConfigDesc') }}</p>
                                        </template>
                                    </el-alert>
                                    
                                    <div class="guide-config-section">
                                        <el-form label-width="150px">
                                            <el-form-item :label="$t('config.defaultMode')">
                                                <el-select v-model="data.config.defaultMode" style="width: 100%">
                                                    <el-option :label="$t('config.control')" value="control"></el-option>
                                                    <el-option :label="$t('config.translation')" value="translation"></el-option>
                                                    <el-option :label="$t('config.textSend')" value="text"></el-option>
                                                    <el-option :label="$t('config.bitmapLed')" value="bitMapLed"></el-option>
                                                </el-select>
                                            </el-form-item>
                                            <el-form-item :label="$t('config.speechRecognitionLanguage')">
                                                <el-select v-model="data.config.sourceLanguage" style="width: 100%">
                                                    <el-option v-for="item in recognizeLanguageOption" :key="item.value"
                                                        :label="item.label" :value="item.value"></el-option>
                                                </el-select>
                                            </el-form-item>
                                            <el-form-item :label="$t('config.defaultTranslationLanguage')">
                                                <el-select v-model="data.config.targetTranslationLanguage" style="width: 100%">
                                                    <el-option v-for="item in computedTranslateLanguage"
                                                        :key="item.value" :label="item.label"
                                                        :value="item.value"></el-option>
                                                </el-select>
                                            </el-form-item>
                                            <el-form-item :label="$t('config.secondTranslationLanguage')">
                                                <el-select v-model="data.config.targetTranslationLanguage2" style="width: 100%">
                                                    <el-option :label="$t('common.off')" value="none"></el-option>
                                                    <el-option v-for="item in computedTranslateLanguage"
                                                        :key="item.value" :label="item.label"
                                                        :value="item.value"></el-option>
                                                </el-select>
                                            </el-form-item>
                                            <el-form-item :label="$t('config.thirdTranslationLanguage')">
                                                <el-select v-model="data.config.targetTranslationLanguage3" style="width: 100%">
                                                    <el-option :label="$t('common.off')" value="none"></el-option>
                                                    <el-option v-for="item in computedTranslateLanguage"
                                                        :key="item.value" :label="item.label"
                                                        :value="item.value"></el-option>
                                                </el-select>
                                            </el-form-item>
                                        </el-form>
                                    </div>
                                </div>
                            </div>

                            <!-- 步骤3: 麦克风配置 -->
                            <div v-if="currentSimpleStep === 2" class="guide-step">
                                <h3>{{ $t('guide.microphoneConfig') }}</h3>
                                <div class="guide-instructions">
                                    <el-alert :title="$t('guide.microphoneConfigTitle')" type="info" show-icon :closable="false">
                                        <template #default>
                                            <p>{{ $t('guide.microphoneConfigDesc') }}</p>
                                        </template>
                                    </el-alert>
                                    
                                    <div class="guide-config-section">
                                        <el-form label-width="150px">
                                            <el-form-item :label="$t('config.micUseLocalRecognitionModel')">
                                                <el-select v-model="data.config.localizedSpeech" style="width: 100%">
                                                    <el-option :label="$t('common.on')" :value="true"></el-option>
                                                    <el-option :label="$t('common.off')" :value="false"></el-option>
                                                </el-select>
                                            </el-form-item>
                                            <el-form-item :label="$t('config.micTranslationEngine')">
                                                <el-select v-model="data.config.translateService" style="width: 100%">
                                                    <el-option v-for="engine in translationEngines" :key="engine.value" :label="engine.label" :value="engine.value"></el-option>
                                                </el-select>
                                            </el-form-item>
                                            <el-form-item :label="$t('voiceControl.microphone')">
                                                <el-select v-model="data.config.micName" style="width: 100%">
                                                    <el-option :label="$t('voiceControl.systemDefaultMicrophone')" value="default"></el-option>
                                                    <el-option v-for="(item, index) in micName" :key="index" :label="item"
                                                        :value="item"></el-option>
                                                </el-select>
                                            </el-form-item>
                                            <el-form-item :label="$t('voiceControl.microphoneVoiceMode')">
                                                <el-select v-model="data.config.voiceMode" style="width: 100%">
                                                    <el-option :label="$t('voiceControl.continuousOn')" :value="0"></el-option>
                                                    <el-option :label="$t('voiceControl.keyToggle')" :value="1"></el-option>
                                                    <el-option :label="$t('voiceControl.holdToTalk')" :value="2"></el-option>
                                                    <el-option :label="$t('voiceControl.followVrcSwitch')" :value="3"></el-option>
                                                </el-select>
                                            </el-form-item>
                                            <el-form-item :label="$t('voiceControl.microphoneCustomThreshold')">
                                                <el-slider v-model="data.config.customThreshold" show-input :max="0.6"
                                                :step="0.001"
                                                :disabled="data.config.dynamicThreshold || data.config.localizedSpeech" />
                                            <div style="margin-top: 10px; text-align: right;">
                                                <el-button type="primary" @click="startCalibration('mic')" 
                                                    :disabled="data.config.dynamicThreshold || data.config.localizedSpeech">
                                                    {{ $t('voiceControl.calibrateThreshold') }}
                                                </el-button>
                                            </div>
                                            </el-form-item>
                                            <el-form-item :label="$t('voiceControl.microphoneKeyToggleHotkey')">
                                                <el-input v-model="data.config.voiceHotKey_new" />
                                            </el-form-item>
                                            <el-form-item :label="$t('voiceControl.microphoneHoldKey')">
                                                <el-input v-model="data.config.micPressingKey" :maxlength="1" @input="data.config.micPressingKey = $event.replace(/[^a-zA-Z]/g, '')" />
                                            </el-form-item>
                                        </el-form>
                                    </div>
                                </div>
                            </div>

                            <!-- 步骤4: 桌面音频配置 -->
                            <div v-if="currentSimpleStep === 3" class="guide-step">
                                <h3>{{ $t('guide.desktopAudioConfig') }}</h3>
                                <div class="guide-instructions">
                                    <el-alert :title="$t('guide.desktopAudioConfigTitle')" type="info" show-icon :closable="false">
                                        <template #default>
                                            <p>{{ $t('guide.desktopAudioConfigDesc') }}</p>
                                        </template>
                                    </el-alert>
                                    
                                    <div class="guide-config-section">
                                        <el-form label-width="150px">
                                            <el-form-item :label="$t('config.separateDesktopAudioCapture')">
                                                <el-select v-model="data.config.Separate_Self_Game_Mic" style="width: 100%">
                                                    <el-option :label="$t('common.off')" :value="0"></el-option>
                                                    <el-option :label="$t('config.useDesktopAudio')" :value="1"></el-option>
                                                    <el-option :label="$t('config.useVirtualSoundcardMic')" :value="2"></el-option>
                                                </el-select>
                                            </el-form-item>
                                            <el-form-item :label="$t('config.desktopAudioUseLocalRecognitionModel')" v-if="data.config.Separate_Self_Game_Mic != 0">
                                                <el-select v-model="data.config.localizedCapture" style="width: 100%">
                                                    <el-option :label="$t('common.on')" :value="true"></el-option>
                                                    <el-option :label="$t('common.off')" :value="false"></el-option>
                                                </el-select>
                                            </el-form-item>
                                            <el-form-item :label="$t('config.desktopAudioTranslationEngine')" v-if="data.config.Separate_Self_Game_Mic != 0">
                                                <el-select v-model="data.config.translateServicecap" style="width: 100%">
                                                    <el-option v-for="engine in translationEngines" :key="engine.value" :label="engine.label" :value="engine.value"></el-option>
                                                </el-select>
                                            </el-form-item>
                                            <el-form-item :label="$t('voiceControl.desktopAudioSource')" v-if="data.config.Separate_Self_Game_Mic != 0">
                                                <el-select v-model="data.config.gameMicName" style="width: 100%">
                                                    <el-option :label="$t('voiceControl.systemDefault')" value="default"></el-option>
                                                    <el-option v-for="(item, index) in captureName" :key="index" :label="item" :value="item"></el-option>
                                                </el-select>
                                            </el-form-item>
                                            <el-form-item :label="$t('voiceControl.desktopAudioVoiceMode')" v-if="data.config.Separate_Self_Game_Mic != 0">
                                                <el-select v-model="data.config.gameVoiceMode" style="width: 100%">
                                                    <el-option :label="$t('voiceControl.continuousOn')" :value="0"></el-option>
                                                    <el-option :label="$t('voiceControl.keyToggle')" :value="1"></el-option>
                                                    <el-option :label="$t('voiceControl.holdToTalk')" :value="2"></el-option>
                                                    <el-option :label="$t('voiceControl.followVrcSwitch')" :value="3"></el-option>
                                                </el-select>
                                            </el-form-item>
                                            <el-form-item :label="$t('voiceControl.desktopAudioCustomThreshold')" v-if="data.config.Separate_Self_Game_Mic != 0">
                                                <el-slider v-model="data.config.customThreshold" show-input :max="0.6"
                                                :step="0.001"
                                                :disabled="data.config.dynamicThreshold || data.config.localizedSpeech" />
                                                <div style="margin-top: 10px; text-align: right;">
                                                    <el-button type="primary" @click="startCalibration('mic')" 
                                                        :disabled="data.config.dynamicThreshold || data.config.localizedSpeech">
                                                        {{ $t('voiceControl.calibrateThreshold') }}
                                                    </el-button>
                                                </div>
                                            </el-form-item>
                                            <el-form-item :label="$t('voiceControl.desktopAudioKeyToggleHotkey')" v-if="data.config.Separate_Self_Game_Mic != 0">
                                                <el-input v-model="data.config.gameVoiceHotKey_new" />
                                            </el-form-item>
                                            <el-form-item :label="$t('voiceControl.desktopAudioHoldKey')" v-if="data.config.Separate_Self_Game_Mic != 0">
                                                <el-input v-model="data.config.capPressingKey" :maxlength="1" @input="data.config.capPressingKey = $event.replace(/[^a-zA-Z]/g, '')" />
                                            </el-form-item>
                                        </el-form>
                                    </div>
                                </div>
                            </div>

                            <!-- 步骤5: 语音合成配置 -->
                            <div v-if="currentSimpleStep === 4" class="guide-step">
                                <h3>{{ $t('guide.ttsConfig') }}</h3>
                                <div class="guide-instructions">
                                    <el-alert :title="$t('guide.ttsTitle')" type="info" show-icon :closable="false">
                                        <template #default>
                                            <p>{{ $t('guide.ttsDesc') }}</p>
                                        </template>
                                    </el-alert>
                                    
                                    <div class="guide-config-section">
                                        <el-form label-width="150px">
                                            <el-form-item :label="$t('config.ttsOutput')">
                                                <el-select v-model="data.config.TTSToggle" style="width: 100%">
                                                    <el-option :label="$t('common.off')" :value="0"></el-option>
                                                    <el-option :label="$t('config.translationModeMicTranslationOutput')" :value="1"></el-option>
                                                    <el-option :label="$t('config.textSendModeMicOriginalText')" :value="2"></el-option>
                                                    <el-option :label="$t('config.translationModeMicAndDesktopAudioTranslationOutput')" :value="3"></el-option>
                                                </el-select>
                                            </el-form-item>
                                            <el-form-item :label="$t('config.ttsOutputSpeaker')" v-if="data.config.TTSToggle != 0">
                                                <el-select v-model="data.config.TTSOutputName" style="width: 100%">
                                                    <el-option :label="$t('voiceControl.systemDefault')" value="default"></el-option>
                                                    <el-option v-for="(item, index) in outputName" :key="index" :label="item" :value="item"></el-option>
                                                </el-select>
                                            </el-form-item>
                                        </el-form>
                                    </div>
                                </div>
                            </div>

                            <!-- 步骤6: SteamVR显示配置 -->
                            <div v-if="currentSimpleStep === 5" class="guide-step">
                                <h3>{{ $t('guide.steamvrConfig') }}</h3>
                                <div class="guide-instructions">
                                    <el-alert :title="$t('guide.steamvrTitle')" type="warning" show-icon :closable="false">
                                        <template #default>
                                            <p>{{ $t('guide.steamvrDesc') }}</p>
                                        </template>
                                    </el-alert>
                                    
                                    <div class="guide-config-section">
                                        <el-form label-width="150px">
                                            <el-form-item :label="$t('config.steamvrPalmOutputDisplay')">
                                                <el-select v-model="data.config.textInSteamVR" style="width: 100%">
                                                    <el-option :label="$t('common.on')" :value="true"></el-option>
                                                    <el-option :label="$t('common.off')" :value="false"></el-option>
                                                </el-select>
                                            </el-form-item>
                                            <el-form-item :label="$t('config.steamvrDisplayPosition')" v-if="data.config.textInSteamVR">
                                                <el-select v-model="data.config.SteamVRHad" style="width: 100%">
                                                    <el-option :label="$t('config.rightHand')" :value="0"></el-option>
                                                    <el-option :label="$t('config.leftHand')" :value="1"></el-option>
                                                    <el-option :label="$t('config.leftAndRightHand')" :value="2"></el-option>
                                                </el-select>
                                            </el-form-item>
                                            <el-form-item :label="$t('config.steamvrDisplaySize')" v-if="data.config.textInSteamVR">
                                                <el-slider v-model="data.config.SteamVRSize" show-input :max="0.5" :step="0.01" />
                                            </el-form-item>
                                        </el-form>
                                    </div>
                                </div>
                            </div>

                            <!-- 步骤7: 完成配置 -->
                            <div v-if="currentSimpleStep === 6" class="guide-step">
                                <h3>{{ $t('guide.setupComplete') }}</h3>
                                <div class="guide-instructions">
                                    <el-result icon="success" :title="$t('guide.setupCompleteTitle')" :sub-title="$t('guide.setupCompleteSubtitle')">
                                        <template #extra>
                                            <div class="guide-summary">
                                                <h4>{{ $t('guide.configSummary') }}</h4>
                                                <el-descriptions :column="1" border>
                                                    <el-descriptions-item :label="$t('config.oscPort')">
                                                        {{ data.config['osc-port'] }}
                                                    </el-descriptions-item>
                                                    <el-descriptions-item :label="$t('config.oscIpAddress')">
                                                        {{ data.config['osc-ip'] }}
                                                    </el-descriptions-item>
                                                    <el-descriptions-item :label="$t('config.defaultMode')">
                                                        {{ data.config.defaultMode === 'control' ? $t('config.control') : 
                                                           data.config.defaultMode === 'translation' ? $t('config.translation') : 
                                                           data.config.defaultMode === 'text' ? $t('config.textSend') : 
                                                           $t('config.bitmapLed') }}
                                                    </el-descriptions-item>
                                                    <el-descriptions-item :label="$t('config.speechRecognitionLanguage')">
                                                        {{ recognizeLanguageOption.find(item => item.value === data.config.sourceLanguage)?.label }}
                                                    </el-descriptions-item>
                                                    <el-descriptions-item :label="$t('config.defaultTranslationLanguage')">
                                                        {{ computedTranslateLanguage.find(item => item.value === data.config.targetTranslationLanguage)?.label }}
                                                    </el-descriptions-item>
                                                </el-descriptions>
                                            </div>
                                        </template>
                                    </el-result>
                                </div>
                            </div>
                        </div>

                        <div class="guide-actions">
                            <div>
                                <el-button @click="previousSimpleStep" :disabled="currentSimpleStep === 0">
                                    {{ $t('guide.previous') }}
                                </el-button>
                                <el-button type="primary" @click="nextSimpleStep" v-if="currentSimpleStep < 6">
                                    {{ $t('guide.next') }}
                                </el-button>
                                <el-button type="success" @click="completeSimpleGuide" v-if="currentSimpleStep === 6">
                                    {{ $t('guide.completeSetup') }}
                                </el-button>
                            </div>
                            <div>
                                <el-button @click="skipSimpleGuide" type="info" plain>
                                    {{ $t('guide.skipGuide') }}
                                </el-button>
                            </div>
                        </div>
                    </div>
                </el-dialog>



                <el-button-group style="margin-left:50%;margin-bottom: 20px;"
                    v-if="data.local.clickedMenuItem == 3 || data.local.clickedMenuItem == 4">
                    <el-button type="primary" @click="getconfig">{{ $t('common.getConfig') }}</el-button>
                    <el-button type="primary" @click="saveconfig">{{ $t('common.saveConfig') }}</el-button>
                    <el-button type="primary" @click="saveAndBoot">{{ $t('common.saveAndRestart') }}</el-button>
                    <el-button type="primary" @click="reboot">{{ $t('common.restartService') }}</el-button>
                </el-button-group>
                <div v-if="data.local.clickedMenuItem == 1">

                    <el-row :gutter="20">
                        <el-col :span="20">
                            <el-row :gutter="20">


                                <el-col :span="data.config.Separate_Self_Game_Mic == 0 ? 24 : 12">
                                    <el-card class="log-container">
                                        <template #header>
                                            <div class="card-header">
                                                <span>{{ $t('home.micRecognitionResult') }}</span>
                                                <el-switch 
                                                    v-model="data.local.micEnabled" 
                                                    @change="toggleMicAudio"
                                                    :active-text="$t('common.enable')"
                                                    :inactive-text="$t('common.disable')"
                                                    style="float: right;"
                                                />
                                            </div>
                                        </template>
                                        <el-table :data="data.local.micInfo" :show-header="false" height="65vh"
                                            @row-click="handleRowClick">
                                            <el-table-column prop="text" :label="$t('table.text')" />
                                        </el-table>
                                    </el-card>
                                </el-col>
                                <el-col :span="12" v-if="data.config.Separate_Self_Game_Mic != 0">
                                    <el-card class="log-container">
                                        <template #header>
                                            <div class="card-header">
                                                <span>{{ $t('home.desktopRecognitionResult') }}</span>
                                                <el-switch 
                                                    v-model="data.local.desktopEnabled" 
                                                    @change="toggleDesktopAudio"
                                                    :active-text="$t('common.enable')"
                                                    :inactive-text="$t('common.disable')"
                                                    style="float: right;"
                                                />
                                            </div>
                                        </template>
                                        <el-table :data="data.local.desktopInfo" :show-header="false" height="65vh"
                                            @row-click="handleRowClick">
                                            <el-table-column prop="text" :label="$t('table.text')" />
                                        </el-table>
                                    </el-card>

                                </el-col>
                            </el-row>
                            <div style="margin-top: 2vh;">

                            </div>
                            <el-input v-model="data.local.sendText" :placeholder="$t('home.inputPlaceholder')" @keyup.enter="sendText">

                                <template #append>
                                    <el-button type="primary" @click="sendText">{{ $t('home.send') }}</el-button>
                                </template>
                            </el-input>
                        </el-col>
                        <el-col :span="4">
                            <sideInfo />
                        </el-col>
                    </el-row>

                </div>

                <el-card class="log-container" v-if="data.local.clickedMenuItem == 5">
                    <template #header>
                        <div class="card-header">
                            <span>{{ $t('logs.realTimeLogs') }}</span>
                        </div>
                    </template>
                    <el-table :data="data.local.loggerInfo" :show-header="false" height="65vh"
                        @row-click="handleRowClick">
                        <el-table-column :label="$t('table.log')">
                            <template #default="{ row }">
                                {{ row }}
                            </template>
                        </el-table-column>
                    </el-table>
                </el-card>
                <div v-if="data.local.clickedMenuItem == 4">
                    <el-row :gutter="20">
                        <el-col :span="20">
                            <el-scrollbar height="75vh" :always="true">
                                <el-card style="margin-bottom: 20px;">
                                    <template #header>
                                        <div class="card-header">
                                            <span>{{ $t('config.programConfig') }}</span>
                                        </div>

                                    </template>
                                    <el-form :model="data.config" label-width="auto">
                                        <el-form-item :label="$t('config.serverUrl')">
                                            <el-input v-model="data.config.baseurl"></el-input>
                                        </el-form-item>
                                        <el-form-item :label="$t('config.oscPort')">
                                            <el-input type="number" v-model="data.config['osc-port']"></el-input>
                                        </el-form-item>
                                        <el-form-item :label="$t('config.oscIpAddress')">
                                            <el-input v-model="data.config['osc-ip']"></el-input>
                                        </el-form-item>
                                        <el-form-item :label="$t('config.defaultMode')">
                                            <el-select v-model="data.config.defaultMode">
                                                <el-option :label="$t('config.control')" value="control"></el-option>
                                                <el-option :label="$t('config.translation')" value="translation"></el-option>
                                                <el-option :label="$t('config.textSend')" value="text"></el-option>
                                                <el-option :label="$t('config.bitmapLed')" value="bitMapLed"></el-option>
                                            </el-select>
                                        </el-form-item>
                                        <el-form-item :label="$t('config.speechRecognitionLanguage')">
                                            <el-tooltip class="box-item" effect="dark" :content="$t('tooltips.canSpeakChineseOutputJapanese')"
                                                placement="right">
                                                <el-select v-model="data.config.sourceLanguage">
                                                    <el-option v-for="item in recognizeLanguageOption" :key="item.value"
                                                        :label="item.label" :value="item.value"></el-option>
                                                </el-select>
                                            </el-tooltip>
                                        </el-form-item>
                                        <el-form-item :label="$t('config.defaultTranslationLanguage')">
                                            <el-tooltip class="box-item" effect="dark" :content="$t('tooltips.ifTranslationErrorCheckServerSupport')"
                                                placement="right">
                                                <el-select v-model="data.config.targetTranslationLanguage">
                                                    <el-option v-for="item in computedTranslateLanguage"
                                                        :key="item.value" :label="item.label"
                                                        :value="item.value"></el-option>
                                                </el-select>
                                            </el-tooltip>
                                        </el-form-item>
                                        <el-form-item :label="$t('config.secondTranslationLanguage')">
                                            <el-tooltip class="box-item" effect="dark" :content="$t('tooltips.ifTranslationErrorCheckServerSupport')"
                                                placement="right">
                                                <el-select v-model="data.config.targetTranslationLanguage2">
                                                    <el-option :label="$t('common.off')" value="none"></el-option>
                                                    <el-option v-for="item in computedTranslateLanguage"
                                                        :key="item.value" :label="item.label"
                                                        :value="item.value"></el-option>
                                                </el-select>
                                            </el-tooltip>
                                        </el-form-item>
                                        <el-form-item :label="$t('config.thirdTranslationLanguage')">
                                            <el-tooltip class="box-item" effect="dark" :content="$t('tooltips.ifTranslationErrorCheckServerSupport')"
                                                placement="right">
                                                <el-select v-model="data.config.targetTranslationLanguage3">
                                                    <el-option :label="$t('common.off')" value="none"></el-option>
                                                    <el-option v-for="item in computedTranslateLanguage"
                                                        :key="item.value" :label="item.label"
                                                        :value="item.value"></el-option>
                                                </el-select>
                                            </el-tooltip>
                                        </el-form-item>
                                        <el-form-item :label="$t('config.separateDesktopAudioCapture')">
                                            <!-- <el-select v-model="data.config.Separate_Self_Game_Mic" @change="getCapture"> -->
                                            <el-select v-model="data.config.Separate_Self_Game_Mic">
                                                <el-option :label="$t('common.off')" :value="0"></el-option>
                                                <el-option :label="$t('config.useDesktopAudio')" :value="1"></el-option>
                                                <el-option :label="$t('config.useVirtualSoundcardMic')" :value="2"></el-option>
                                            </el-select>
                                        </el-form-item>
                                        <el-form-item :label="$t('config.micUseLocalRecognitionModel')">
                                            <el-select v-model="data.config.localizedSpeech">
                                                <el-option :label="$t('common.on')" :value="true"></el-option>
                                                <el-option :label="$t('common.off')" :value="false"></el-option>
                                            </el-select>
                                        </el-form-item>
                                        <el-form-item :label="$t('config.desktopAudioUseLocalRecognitionModel')">
                                            <el-select v-model="data.config.localizedCapture"
                                                :disabled="!data.config.Separate_Self_Game_Mic">
                                                <el-option :label="$t('common.on')" :value="true"></el-option>
                                                <el-option :label="$t('common.off')" :value="false"></el-option>
                                            </el-select>
                                        </el-form-item>
                                        <el-form-item :label="$t('config.steamvrPalmOutputDisplay')">
                                            <el-select v-model="data.config.textInSteamVR">
                                                <el-option :label="$t('common.on')" :value="true"></el-option>
                                                <el-option :label="$t('common.off')" :value="false"></el-option>
                                            </el-select>
                                        </el-form-item>
                                        <el-form-item :label="$t('config.steamvrDisplayPosition')">
                                            <el-select v-model="data.config.SteamVRHad"
                                                :disabled="!data.config.textInSteamVR">
                                                <el-option :label="$t('config.rightHand')" :value="0"></el-option>
                                                <el-option :label="$t('config.leftHand')" :value="1"></el-option>
                                                <el-option :label="$t('config.leftAndRightHand')" :value="2"></el-option>
                                            </el-select>
                                        </el-form-item>
                                        <el-form-item :label="$t('config.steamvrDisplaySize')">
                                            <el-slider v-model="data.config.SteamVRSize" show-input :max="0.5"
                                                :step="0.01" :disabled="!data.config.textInSteamVR" />
                                        </el-form-item>
                                        <el-form-item :label="$t('config.ttsOutput')">
                                            <el-select v-model="data.config.TTSToggle">
                                                <el-option :label="$t('common.off')" :value="0"></el-option>
                                                <el-option :label="$t('config.translationModeMicTranslationOutput')" :value="1"></el-option>
                                                <el-option :label="$t('config.textSendModeMicOriginalText')" :value="2"></el-option>
                                                <el-option :label="$t('config.translationModeMicAndDesktopAudioTranslationOutput')" :value="3"></el-option>
                                            </el-select>
                                        </el-form-item>
                                        <el-form-item :label="$t('config.micTranslationEngine')">
                                            <el-tooltip class="box-item" effect="dark" :content="$t('tooltips.ifTranslationErrorTryChangeEngine')"
                                                placement="right">
                                                <el-select v-model="data.config.translateService">
                                                    <el-option v-for="engine in translationEngines" :key="engine.value" :label="engine.label" :value="engine.value"></el-option>
                                                </el-select>
                                            </el-tooltip>
                                        </el-form-item>
                                         <el-form-item :label="$t('config.desktopAudioTranslationEngine')">
                                            <el-tooltip class="box-item" effect="dark" :content="$t('tooltips.ifTranslationErrorTryChangeEngine')"
                                                placement="right">
                                                <el-select v-model="data.config.translateServicecap">
                                                    <el-option v-for="engine in translationEngines" :key="engine.value" :label="engine.label" :value="engine.value"></el-option>
                                                </el-select>
                                            </el-tooltip>
                                        </el-form-item>
                                        <el-form-item :label="$t('config.translationEngineAccessPointRegion')">
                                            <el-select v-model="data.config.translateRegion">
                                                <el-option :label="$t('config.mainlandChina')" value="CN"></el-option>
                                                <el-option :label="$t('config.other')" value="EN"></el-option>
                                            </el-select>
                                        </el-form-item>
                                        
                                        <!-- OpenAI配置 -->
                                        <el-form-item v-if="data.config.translateService === 'openai' || data.config.translateServicecap === 'openai'" :label="$t('config.openaiConfig')">
                                            <el-alert type="info" show-icon :closable="false" style="margin-bottom: 10px;">
                                                <p>{{ $t('config.openaiConfig') }}</p>
                                            </el-alert>
                                            <el-form-item :label="$t('config.openaiApiKey')">
                                                <el-input v-model="data.config.openai_config.api_key" type="password" :placeholder="$t('config.openaiApiKey')"></el-input>
                                            </el-form-item>
                                            <el-form-item :label="$t('config.openaiApiUrl')">
                                                <el-input v-model="data.config.openai_config.base_url" placeholder="https://open.bigmodel.cn/api/paas/v4/"></el-input>
                                            </el-form-item>
                                            <el-form-item :label="$t('config.openaiModel')">
                                                <el-input v-model="data.config.openai_config.model" placeholder="glm-4-flash"></el-input>
                                            </el-form-item>
                                        </el-form-item>
                                        <el-form-item :label="$t('config.oscOutput')">
                                            <el-select v-model="data.config.oscShutdown">
                                                <el-option :label="$t('config.pause')" :value="true"></el-option>
                                                <el-option :label="$t('common.on')" :value="false"></el-option>
                                            </el-select>
                                        </el-form-item>
                                        <el-form-item :label="$t('config.emotionRecognitionEmojiOutput')">
                                            <el-select v-model="data.config.filteremoji">
                                                <el-option :label="$t('common.off')" value="true"></el-option>
                                                <el-option :label="$t('common.on')" value="false"></el-option>
                                            </el-select>
                                        </el-form-item>
                                        <el-form-item :label="$t('config.externalOscServerPort')">
                                            <el-select v-model="data.config.enableOscServer">
                                                <el-option :label="$t('common.on')" :value="true"></el-option>
                                                <el-option :label="$t('common.off')" :value="false"></el-option>
                                            </el-select>
                                        </el-form-item>
                                        <el-form-item :label="$t('config.receiveExternalOscServerPort')">
                                            <el-input type="number" v-model="data.config['oscServerPort']"></el-input>
                                        </el-form-item>
                                        <el-form-item :label="$t('config.receiveExternalOscServerIpAddress')">
                                            <el-input v-model="data.config['oscServerIp']"></el-input>
                                        </el-form-item>
                                    </el-form>
                                </el-card>

                                <el-card style="margin-bottom: 20px;">
                                    <template #header>
                                        <div class="card-header">
                                            <span>{{ $t('voiceControl.voiceControlConfig') }}</span>
                                        </div>
                                    </template>

                                    <el-form :model="data.config" label-width="auto">
                                        <el-form-item :label="$t('voiceControl.microphone')">
                                            <el-select v-model="data.config.micName">
                                                <el-option :label="$t('voiceControl.systemDefaultMicrophone')" value="default"></el-option>
                                                <el-option v-for="(item, index) in micName" :key="index" :label="item"
                                                    :value="item"></el-option>
                                            </el-select>
                                        </el-form-item>


                                        <el-form-item :label="$t('voiceControl.microphoneVoiceMode')">
                                            <el-select v-model="data.config.voiceMode">
                                                <el-option :label="$t('voiceControl.continuousOn')" :value="0"></el-option>
                                                <el-option :label="$t('voiceControl.keyToggle')" :value="1"></el-option>
                                                <el-option :label="$t('voiceControl.holdToTalk')" :value="2"></el-option>
                                                <el-option :label="$t('voiceControl.followVrcSwitch')" :value="3"></el-option>
                                            </el-select>
                                        </el-form-item>


                                        <el-form-item :label="$t('voiceControl.microphoneCustomThreshold')">
                                            <el-slider v-model="data.config.customThreshold" show-input :max="0.6"
                                                :step="0.001"
                                                :disabled="data.config.dynamicThreshold || data.config.localizedSpeech" />
                                            <div style="margin-top: 10px; text-align: right;">
                                                <el-button type="primary" @click="startCalibration('mic')" 
                                                    :disabled="data.config.dynamicThreshold || data.config.localizedSpeech">
                                                    {{ $t('voiceControl.calibrateThreshold') }}
                                                </el-button>
                                            </div>
                                        </el-form-item>
                                        <el-form-item :label="$t('voiceControl.microphoneKeyToggleHotkey')">
                                            <el-input v-model="data.config.voiceHotKey_new"></el-input>
                                        </el-form-item>
                                        <el-form-item :label="$t('voiceControl.microphoneHoldKey')">
                                            <el-tooltip class="box-item" effect="dark" :content="$t('tooltips.onlySingleLetterKey')"
                                                placement="right">
                                                <el-input v-model="data.config.micPressingKey" :maxlength="1"
                                                    @input="data.config.micPressingKey = $event.replace(/[^a-zA-Z]/g, '')"></el-input>
                                            </el-tooltip>
                                        </el-form-item>
                                        <el-form-item :label="$t('voiceControl.desktopAudioSource')">
                                            <el-select v-model="data.config.gameMicName"
                                                :disabled="data.config.Separate_Self_Game_Mic == 0">
                                                <el-option :label="$t('voiceControl.systemDefault')" value="default"></el-option>
                                                <el-option v-for="(item, index) in captureName" :key="index"
                                                    :label="item" :value="item"></el-option>
                                            </el-select>
                                        </el-form-item>
                                        <el-form-item :label="$t('voiceControl.desktopAudioVoiceMode')">
                                            <el-select v-model="data.config.gameVoiceMode"
                                                :disabled="data.config.Separate_Self_Game_Mic == 0">
                                                <el-option :label="$t('voiceControl.continuousOn')" :value="0"></el-option>
                                                <el-option :label="$t('voiceControl.keyToggle')" :value="1"></el-option>
                                                <el-option :label="$t('voiceControl.holdToTalk')" :value="2"></el-option>
                                                <el-option :label="$t('voiceControl.followVrcSwitch')" :value="3"></el-option>
                                            </el-select>
                                        </el-form-item>
                                        <el-form-item :label="$t('voiceControl.desktopAudioCustomThreshold')">
                                            <el-slider v-model="data.config.gameCustomThreshold" show-input :max="0.6"
                                                :step="0.001"
                                                :disabled="data.config.dynamicThreshold || data.config.Separate_Self_Game_Mic == 0 || data.config.localizedCapture" />
                                            <div style="margin-top: 10px; text-align: right;">
                                                <el-button type="primary" @click="startCalibration('cap')" 
                                                    :disabled="data.config.dynamicThreshold || data.config.Separate_Self_Game_Mic == 0 || data.config.localizedCapture">
                                                    {{ $t('voiceControl.calibrateThreshold') }}
                                                </el-button>
                                            </div>
                                        </el-form-item>
                                        <el-form-item :label="$t('voiceControl.desktopAudioKeyToggleHotkey')">
                                            <el-input v-model="data.config.gameVoiceHotKey_new"
                                                :disabled="data.config.Separate_Self_Game_Mic == 0"></el-input>
                                        </el-form-item>
                                        <el-form-item :label="$t('voiceControl.desktopAudioHoldKey')">
                                            <el-tooltip class="box-item" effect="dark" :content="$t('tooltips.onlySingleLetterKey')"
                                                placement="right">
                                                <el-input v-model="data.config.capPressingKey"
                                                    :disabled="data.config.Separate_Self_Game_Mic == 0" :maxlength="1"
                                                    @input="data.config.capPressingKey = $event.replace(/[^a-zA-Z]/g, '')"></el-input>
                                            </el-tooltip>
                                        </el-form-item>
                                        <el-form-item :label="$t('config.ttsOutputSpeaker')">
                                            <el-select v-model="data.config.TTSOutputName"
                                                :disabled="data.config.TTSToggle == 0">
                                                <el-option :label="$t('voiceControl.systemDefault')" value="default"></el-option>
                                                <el-option v-for="(item, index) in outputName" :key="index"
                                                    :label="item" :value="item"></el-option>
                                            </el-select>
                                        </el-form-item>
                                        <el-form-item :label="$t('form.localRecognitionModelRealTimeTextOutputInterval')">
                                            <el-select v-model="data.config.realtimeOutputDelay"
                                                :disabled="!data.config.localizedSpeech">
                                                <el-option :label="$t('common.off')" :value="-1.0"></el-option>
                                                <el-option label="1秒" :value="1.0"></el-option>
                                                <el-option label="2秒" :value="2.0"></el-option>
                                            </el-select>
                                        </el-form-item>
                                        <el-space fill>
                                            <el-alert type="info" show-icon :closable="true">
                                                <p>{{ $t('form.translationTemplateDescription') }}</p>
                                            </el-alert>
                                            <el-form-item :label="$t('form.translationModeVrcTextboxOutputStyle')">
                                                <el-input type="textarea" :autosize="{ minRows: 1, maxRows: 5 }"
                                                    v-model="data.config.VRCChatboxformat_new"></el-input>
                                            </el-form-item>
                                            <el-form-item :label="$t('form.textSendModeVrcTextboxOutputStyle')">
                                                <el-input type="textarea" :autosize="{ minRows: 1, maxRows: 5 }"
                                                    v-model="data.config.VRCChatboxformat_text"></el-input>
                                            </el-form-item>
                                            <el-alert type="info" show-icon :closable="true">
                                                <p>{{ $t('form.externalTemplateDescription') }}</p>
                                            </el-alert>
                                            <el-form-item :label="$t('form.externalTextboxTextEmbeddingTemplate')">
                                                <el-input type="textarea" :autosize="{ minRows: 1, maxRows: 5 }"
                                                    v-model="data.config.chatboxOscMixTemplate"></el-input>
                                            </el-form-item>
                                        </el-space>


                                        <el-form-item :label="$t('form.bitmapScreenRowsAndColumns')">
                                            <el-row>
                                                <el-col :span="11">
                                                    <el-input v-model="data.config.VRCBitmapLed_row"
                                                        :placeholder="$t('form.rows')"></el-input>
                                                </el-col>
                                                <el-col :span="2">
                                                    x
                                                </el-col>
                                                <el-col :span="11">
                                                    <el-input v-model="data.config.VRCBitmapLed_col"
                                                        :placeholder="$t('form.columns')"></el-input>
                                                </el-col>
                                            </el-row>


                                        </el-form-item>

                                        <el-form-item :label="$t('form.bitmapScreenColorMode')">
                                            <el-radio-group v-model="data.config.VRCBitmapLed_COLOR">
                                                <el-radio :value="true" size="large">{{ $t('common.on') }}</el-radio>
                                                <el-radio :value="false" size="large">{{ $t('common.off') }}</el-radio>
                                            </el-radio-group>
                                        </el-form-item>
                                        <el-form-item :label="$t('form.dynamicVolumeThreshold')">
                                            <el-tooltip class="box-item" effect="dark" :content="$t('tooltips.notRecommendedToEnable')"
                                                placement="right">
                                                <el-radio-group v-model="data.config.dynamicThreshold">
                                                    <el-radio :value="true" size="large">{{ $t('common.on') }}</el-radio>
                                                    <el-radio :value="false" size="large">{{ $t('common.off') }}</el-radio>
                                                </el-radio-group>
                                            </el-tooltip>
                                        </el-form-item>
                                    </el-form>
                                </el-card>

                                <el-card style="margin-bottom: 20px;">
                                    <template #header>
                                        <div class="card-header">
                                            <span>{{ $t('scripts.apiAccountConfig') }}</span>
                                        </div>

                                    </template>
                                    <el-form :model="data.config" label-width="auto">
                                        <el-form-item :label="$t('form.username')">
                                            <el-input v-model="data.config.userInfo.username"></el-input>
                                        </el-form-item>
                                        <el-form-item :label="$t('form.password')">
                                            <el-input type="password" v-model="data.config.userInfo.password"
                                                show-password></el-input>
                                        </el-form-item>
                                    </el-form>
                                </el-card>
                                <el-card style="margin-bottom: 20px;">
                                    <template #header>
                                        <div class="card-header">
                                            <span>{{ $t('scripts.defaultScriptKeywordsConfig') }}</span>
                                        </div>

                                    </template>
                                    <el-form label-width="auto">
                                        <el-form-item :label="$t('form.defaultAction')">
                                            <el-select v-model="data.local.defaultScriptsAction" style=" width: 100%">
                                                <el-option v-for="(item, index) in data.config.defaultScripts"
                                                    :label="item.text[0]" :value="item.action" :key="index"></el-option>
                                            </el-select>

                                        </el-form-item>
                                        <el-button type="primary" @click="addItem"
                                            style="margin-left: 70%;margin-bottom: 20px;">{{ $t('form.addKeyword') }}</el-button>
                                        <el-scrollbar height="220px">


                                            <el-form-item
                                                v-for="(item1, index) in data.config.defaultScripts.find(item => item.action == data.local.defaultScriptsAction).text"
                                                :key="index" :label="$t('form.keyword') + (index + 1)">
                                                <el-row :gutter="20">
                                                    <el-col :span="18"><el-input
                                                            v-model="data.config.defaultScripts.find(item => item.action == data.local.defaultScriptsAction).text[index]"
                                                            :placeholder="$t('form.pleaseEnterText')"></el-input></el-col>
                                                    <el-col :span="6"><el-button type="danger" :icon="Delete" circle
                                                            @click="removeItem(index)" /></el-col>


                                                </el-row>
                                            </el-form-item>

                                        </el-scrollbar>
                                    </el-form>

                                </el-card>
                            </el-scrollbar>
                        </el-col>
                        <el-col :span="4">
                            <sideInfoFour />
                        </el-col>
                    </el-row>
                </div>
                <div v-if="data.local.clickedMenuItem == 2">
                    <el-card style="margin-top: 20px;height: 80vh;">
                        <template #header>
                            <div class="card-header">
                                <span>{{ $t('stats.dailyRequestCount') }}</span>
                            </div>
                        </template>
                        <el-alert v-if="error" :title="error" type="error" show-icon />
                        <el-row>
                            <el-col :span="8">
                                <el-text class="mx-1">{{ $t('stats.displayDateCount') }}</el-text>
                                <el-input-number v-model="data.local.logDayNum" :min="1" />
                            </el-col>
                            <el-col :span="8">
                                <el-radio-group v-model="counter_mode" @change="fetchData">
                                    <el-radio-button :label="$t('stats.successCount')" value="true" />
                                    <el-radio-button :label="$t('stats.failureCount')" value="false" />
                                </el-radio-group>
                            </el-col>
                            <el-col :span="8">
                                <el-button type="primary" @click="fetchData">{{ $t('stats.refresh') }}</el-button>
                            </el-col>

                        </el-row>

                        <el-table :data="statsData" v-loading="loading" height="60vh" style="width: 100%">
                            <el-table-column prop="date" :label="$t('table.date')">
                                <template #default="{ row }">
                                    {{ formatDate(row.date) }}
                                </template>
                            </el-table-column>

                            <el-table-column prop="count" :label="$t('table.triggerCount')">
                                <template #default="{ row }">
                                    <el-tag :type="row.count > 0 ? 'success' : 'info'">
                                        {{ row.count }} {{ $t('stats.times') }}
                                    </el-tag>
                                </template>
                            </el-table-column>
                        </el-table>
                    </el-card>
                </div>
                <div v-if="data.local.clickedMenuItem == 3">
                    <el-scrollbar height="75vh" :always="true">


                        <el-card style="margin-top: 20px;height: 620px;">
                            <template #header>
                                <span>{{ $t('scripts.customScriptConfig') }}</span>
                            </template>
                            <el-row :gutter="5">
                                <el-col :span="6">

                                    <h5 class="mb-2">{{ $t('form.customScriptDirectory') }}</h5>
                                    <el-menu default-active="1" class="el-menu-vertical-demo" @open="handleOpen"
                                        @close="handleClose">
                                        <el-scrollbar height="420px">
                                            <el-menu-item v-for="(item, index) in data.config.scripts" :index="index"
                                                :key="index" @click="data.local.scriptClick = index">
                                                <span>{{ item.action }}</span>
                                            </el-menu-item>
                                        </el-scrollbar>
                                    </el-menu>
                                    <el-button-group class="ml-4">
                                        <el-button type="primary" @click="addScriptItem">{{ $t('form.addScript') }}</el-button>

                                        <el-button type="danger" @click="removeScriptItem">{{ $t('form.deleteSelectedScript') }}</el-button>
                                    </el-button-group>


                                </el-col>

                                <el-col :span="9">
                                    <el-card style="height: 500px;">
                                        <template #header>
                                            <span>{{ $t('form.customScriptNameAndKeywords') }}</span>
                                        </template>

                                        <el-form label-width="auto">
                                            <el-form-item :label="$t('form.customScriptName')">
                                                <el-input v-model="data.config.scripts[data.local.scriptClick].action"
                                                    :placeholder="$t('form.pleaseEnterName')"></el-input>
                                            </el-form-item>

                                            <el-button type="primary" @click="addCustomItem"
                                                style="margin-left: 70%;margin-bottom: 20px;">{{ $t('form.addKeyword') }}</el-button>

                                            <el-scrollbar height="320px">
                                                <el-form-item
                                                    v-for="(item, index) in data.config.scripts[data.local.scriptClick].text"
                                                    :key="index" :label="$t('form.keyword') + (index + 1)">
                                                    <div>
                                                        <el-row :gutter="20">
                                                            <el-col :span="18"><el-input
                                                                    v-model="data.config.scripts[data.local.scriptClick].text[index]"
                                                                    :placeholder="$t('form.pleaseEnterText')"></el-input></el-col>
                                                            <el-col :span="6"><el-button type="danger" :icon="Delete"
                                                                    circle @click="removeCustomItem(index)" /></el-col>


                                                        </el-row>
                                                    </div>

                                                </el-form-item>
                                            </el-scrollbar>
                                        </el-form>
                                    </el-card>

                                </el-col>
                                <el-col :span="9">
                                    <el-card style="height: 500px;">
                                        <template #header>
                                            <span>{{ $t('form.customScriptExecutionActions') }}</span>
                                        </template>
                                        <el-scrollbar height="400px">
                                            <el-descriptions
                                                v-for="(item, index) in data.config.scripts[data.local.scriptClick].vrcActions"
                                                class="margin-top" :title="$t('form.action') + (index + 1)" :column="1" border
                                                :key="index">
                                                <template #extra>
                                                    <el-button-group class="ml-4">
                                                        <el-button
                                                            v-if="index == (data.config.scripts[data.local.scriptClick].vrcActions.length - 1)"
                                                            type="primary" :icon="Plus" @click="addActionItem" />
                                                        <el-button type="danger" :icon="Delete"
                                                            @click="removeActionItem(index)" />
                                                    </el-button-group>

                                                </template>
                                                <el-descriptions-item>
                                                    <template #label>
                                                        {{ $t('form.vrcParameterPath') }}
                                                    </template>
                                                    <el-tooltip class="box-item" effect="dark"
                                                        :content="$t('tooltips.recommendCopyFromModelParams')" placement="right">
                                                        <el-input v-model="item.vrcPath" :placeholder="$t('form.pleaseEnterVrcParameterPath')" />
                                                    </el-tooltip>

                                                </el-descriptions-item>
                                                <el-descriptions-item>
                                                    <template #label>
                                                        {{ $t('form.vrcParameterValue') }}
                                                    </template>
                                                    <el-input v-model="item.vrcValue" :placeholder="$t('form.pleaseEnterVrcParameterValue')" />
                                                </el-descriptions-item>
                                                <el-descriptions-item>
                                                    <template #label>
                                                        {{ $t('form.vrcParameterType') }}
                                                    </template>
                                                    <el-select v-model="item.vrcValueType">
                                                        <el-option label="Bool" value="bool"></el-option>
                                                        <el-option label="Float" value="float"></el-option>
                                                        <el-option label="Int" value="int"></el-option>
                                                    </el-select>
                                                </el-descriptions-item>
                                                <el-descriptions-item>
                                                    <template #label>
                                                        {{ $t('form.duration') }}
                                                    </template>
                                                    <el-input v-model="item.sleeptime" :placeholder="$t('form.pleaseEnterDuration')" />
                                                </el-descriptions-item>
                                            </el-descriptions>
                                        </el-scrollbar>
                                    </el-card>
                                </el-col>
                            </el-row>




                        </el-card>

                        <el-card style="margin-top: 20px;height: 620px;">
                            <template #header>
                                <span>{{ $t('form.currentModelParameters') }}</span>
                            </template>
                            <el-descriptions :column="2" label-width="15%" border>
                                <template #extra>
                                    <el-button type="primary" @click="getAvatarParameters"
                                        style="float: right;">{{ $t('form.getModelParameters') }}</el-button>
                                </template>
                                <el-descriptions-item>
                                    <template #label>
                                        {{ $t('form.modelName') }}
                                    </template>
                                    {{ data.avatarInfo.avatarName }}
                                </el-descriptions-item>
                                <el-descriptions-item>
                                    <template #label>
                                        {{ $t('form.modelId') }}
                                    </template>
                                    {{ data.avatarInfo.avatarID }}
                                </el-descriptions-item>
                                <el-descriptions-item :span="2">
                                    <template #label>
                                        {{ $t('form.modelOscFilePath') }}
                                    </template>
                                    {{ data.avatarInfo.filePath }}
                                </el-descriptions-item>
                            </el-descriptions>
                            <el-table :data="data.avatarParameters" style="width: 100%;height: 350px;" border stripe
                                :empty-text="$t('form.getModelParameters')">
                                <el-table-column prop="name" :label="$t('table.parameterName')" width="180" />
                                <el-table-column prop="path" :label="$t('table.parameterPath')" />
                                <el-table-column prop="type" :label="$t('table.parameterType')" />
                            </el-table>
                        </el-card>
                    </el-scrollbar>
                </div>
            </el-main>
        </el-container>

    </el-container>

    <el-dialog v-model="dialogVisible" title="有新的可用升级" style="text-align: left;">

        <h1>可升级至 {{ data.local.updateInfo.version }}</h1>
        <h2>更新日志：</h2>
        <el-scrollbar height="400px" wrap-style="border: 1px solid black;">
            <div v-html="mdhtml"></div>
        </el-scrollbar>

        <template #footer>
            <div class="dialog-footer">
                <el-button @click="dialogVisible = false">取消</el-button>
                <el-button type="primary" @click="upgrade">
                    更新
                </el-button>
            </div>
        </template>
    </el-dialog>

    <!-- 阈值校准对话框 -->
    <el-dialog v-model="calibrationDialogVisible" :title="$t('voiceControl.calibrateThresholdTitle')" width="500px">
        <div class="calibration-content">
            <p>{{ $t('voiceControl.calibrateThresholdDescription') }}</p>
            
            <div class="calibration-status">
                <el-alert 
                    :title="calibrationStatus.title" 
                    :type="calibrationStatus.type" 
                    :description="calibrationStatus.description"
                    show-icon
                    :closable="false"
                />
            </div>

            <div v-if="calibrationData.noiseLevel" class="calibration-data">
                <el-row :gutter="20">
                    <el-col :span="12">
                        <div class="data-item">
                            <span class="label">{{ $t('voiceControl.noiseLevel') }}:</span>
                            <span class="value">{{ calibrationData.noiseLevel }}</span>
                        </div>
                    </el-col>
                    <el-col :span="12" v-if="calibrationData.speechLevel">
                        <div class="data-item">
                            <span class="label">{{ $t('voiceControl.speechLevel') }}:</span>
                            <span class="value">{{ calibrationData.speechLevel }}</span>
                        </div>
                    </el-col>
                </el-row>
                <div v-if="calibrationData.calculatedThreshold" class="data-item">
                    <span class="label">{{ $t('voiceControl.calculatedThreshold') }}:</span>
                    <span class="value">{{ calibrationData.calculatedThreshold }}</span>
                </div>
            </div>

            <div class="calibration-progress" v-if="calibrationInProgress">
                <el-progress :percentage="calibrationProgress" :show-text="false" />
                <p class="progress-text">{{ calibrationProgressText }}</p>
            </div>
        </div>

        <template #footer>
            <div class="dialog-footer">
                <el-button @click="cancelCalibration" :disabled="calibrationInProgress">
                    {{ $t('common.cancel') }}
                </el-button>
                <el-button type="primary" @click="applyCalibration" 
                    :disabled="!calibrationData.calculatedThreshold || calibrationInProgress">
                    {{ $t('common.confirm') }}
                </el-button>
            </div>
        </template>
    </el-dialog>
</template>

<script setup>
import { useDark, useToggle } from '@vueuse/core'
import { useI18n } from 'vue-i18n'
// import { Moon as MoonIcon, Sunny as SunIcon } from '@element-plus/icons-vue'; // Element Plus 图标
import {
    Moon as MoonIcon,
    Sunny as SunIcon,
    Minus as MinusIcon,
    FullScreen as FullScreenIcon,
    Close as CloseIcon,
    Rank as RankIcon, // 用于退出全屏的图标，也可以选择其他
} from '@element-plus/icons-vue';

const { t, locale } = useI18n()
const currentLocale = ref(locale.value)

// 语言切换函数
const changeLocale = (newLocale) => {
    locale.value = newLocale
    localStorage.setItem('locale', newLocale)
}



// 翻译引擎选项
const translationEngines = computed(() => [
    { label: t('translationEngines.developerServer'), value: 'developer' },
    { label: t('translationEngines.openai'), value: 'openai' },
    { label: t('translationEngines.alibaba'), value: 'alibaba' },
    { label: t('translationEngines.google'), value: 'google' },
    { label: t('translationEngines.myMemory'), value: 'myMemory' },
    { label: t('translationEngines.baidu'), value: 'baidu' },
    { label: t('translationEngines.modernMt'), value: 'modernMt' },
    { label: t('translationEngines.volcEngine'), value: 'volcEngine' },
    { label: t('translationEngines.iciba'), value: 'iciba' },
    { label: t('translationEngines.iflytek'), value: 'iflytek' },
    { label: t('translationEngines.bing'), value: 'bing' },
    { label: t('translationEngines.lingvanex'), value: 'lingvanex' },
    { label: t('translationEngines.yandex'), value: 'yandex' },
    { label: t('translationEngines.itranslate'), value: 'itranslate' },
    { label: t('translationEngines.deepl'), value: 'deepl' },
    { label: t('translationEngines.cloudTranslation'), value: 'cloudTranslation' },
    { label: t('translationEngines.qqTranSmart'), value: 'qqTranSmart' },
    { label: t('translationEngines.sogou'), value: 'sogou' },
    { label: t('translationEngines.qqFanyi'), value: 'qqFanyi' },
    { label: t('translationEngines.youdao'), value: 'youdao' },
    { label: t('translationEngines.iflyrec'), value: 'iflyrec' },
    { label: t('translationEngines.hujiang'), value: 'hujiang' },
    { label: t('translationEngines.yeekit'), value: 'yeekit' }
    
])
const isDark = useDark()
const toggleDark = useToggle(isDark)

const changeDark = () => {
    toggleDark(!data.config.darkmode)
    data.config.darkmode = (!data.config.darkmode)
}
import { marked } from 'marked';
import sideInfo from './side-info.vue'
import sideInfoFour from './side-info-four.vue'
import axios from 'axios';
import { io } from 'socket.io-client'
import { ElMessage, ElMessageBox, ElNotification } from 'element-plus'
import {
    Delete, Plus
} from '@element-plus/icons-vue'
import { onMounted, reactive, ref, watch, computed } from 'vue';
import {
    Menu as IconMenu,
    Setting,
} from '@element-plus/icons-vue'
import useClipboard from 'vue-clipboard3';

const socket = io()

const dialogVisible = ref(false)
const captureName = ref([]);

// 配置引导相关数据
const showSimpleGuide = ref(false)
const currentSimpleStep = ref(0)
const hasCompletedFirstTimeSetup = ref(false)

// 校准相关数据
const calibrationDialogVisible = ref(false)
const calibrationInProgress = ref(false)
const calibrationProgress = ref(0)
const calibrationProgressText = ref('')
const currentCalibrationMode = ref('')
const calibrationData = ref({
    noiseLevel: '',
    speechLevel: '',
    calculatedThreshold: ''
})
const calibrationStatus = ref({
    title: '',
    type: 'info',
    description: ''
})
const menuClick = (key) => {
    data.local.clickedMenuItem = key
}

const { toClipboard } = useClipboard();
const handleRowClick = async (row) => {
    try {
        // 如果row是字符串（日志），直接复制；如果是对象（桌面音频或麦克风），复制text属性
        const textToCopy = typeof row === 'string' ? row : row.text;
        await toClipboard(textToCopy);
        ElMessage.success(t('common.copySuccess'));
    } catch (err) {
        ElMessage.error(t('common.copyFailed'));
        console.log(err);
    }
};
const micName = ref([]);
const outputName = ref([]);

let data = reactive({
    local: {
        configGetOK: false,
        defaultScriptsAction: 'sendText',
        item1: '',
        scriptClick: 0,
        micName: [],
        updateInfo: {},
        markdownContent: '',
        clickedMenuItem: 1,
        loggerInfo: [],
        desktopInfo: [],
        micInfo: [],
        versionstr: '',
        logDayNum: 7,
        sendText: '',
        maximized: false,
        micEnabled: true,
        desktopEnabled: true
    },
    config: {
    },
    avatarParameters: [],
    avatarInfo: {
        "avatarID": "",
        "avatarName": "",
        "filePath": ""
    }
})

// Socket事件监听
socket.on('log', (log) => {
    if (log.level == 'error') {
        ElNotification({
            title: t('common.error'),
            message: log.text,
            duration: log.text.includes("[steamvr异常]") ? 4500 : 0,
            type: 'error',
        })
    }
    data.local.loggerInfo.unshift(log.timestamp + ': ' + log.level + ' - ' + log.text)
})

socket.on('cap', (log) => {
    data.local.desktopInfo.unshift({ text: log.text })
})

socket.on('mic', (log) => {
    data.local.micInfo.unshift({ text: log.text })
})

// 校准相关的socket事件监听
socket.on('noiceIssue', (data) => {
    if (calibrationInProgress.value) {
        calibrationStatus.value = {
            title: t('voiceControl.calibrationStep1'),
            type: 'info',
            description: data.text
        }
        calibrationProgress.value = 10
        calibrationProgressText.value = data.text
    }
})

socket.on('startNoice', (data) => {
    if (calibrationInProgress.value) {
        calibrationStatus.value = {
            title: t('voiceControl.calibrationStep2'),
            type: 'info',
            description: data.text
        }
        calibrationProgress.value = 20
        calibrationProgressText.value = data.text
    }
})

socket.on('noiseLevel', (data) => {
    if (calibrationInProgress.value) {
        calibrationData.value.noiseLevel = data.text
        calibrationStatus.value = {
            title: t('voiceControl.calibrationStep3'),
            type: 'success',
            description: data.text
        }
        calibrationProgress.value = 40
        calibrationProgressText.value = data.text
    }
})

socket.on('speekIssue', (data) => {
    if (calibrationInProgress.value) {
        calibrationStatus.value = {
            title: t('voiceControl.calibrationStep4'),
            type: 'info',
            description: data.text
        }
        calibrationProgress.value = 50
        calibrationProgressText.value = data.text
    }
})

socket.on('startSpeek', (data) => {
    if (calibrationInProgress.value) {
        calibrationStatus.value = {
            title: t('voiceControl.calibrationStep5'),
            type: 'warning',
            description: data.text
        }
        calibrationProgress.value = 70
        calibrationProgressText.value = data.text
    }
})

socket.on('speekLevel', (data) => {
    if (calibrationInProgress.value) {
        calibrationData.value.speechLevel = data.text
        calibrationStatus.value = {
            title: t('voiceControl.calibrationStep6'),
            type: 'success',
            description: data.text
        }
        calibrationProgress.value = 90
        calibrationProgressText.value = data.text
    }
})

socket.on('vadLevel', (data) => {
    if (calibrationInProgress.value) {
        calibrationData.value.calculatedThreshold = data.text
        calibrationStatus.value = {
            title: t('voiceControl.calibrationStep7'),
            type: 'success',
            description: data.text
        }
        calibrationProgress.value = 100
        calibrationProgressText.value = t('voiceControl.calibrationComplete')
        calibrationInProgress.value = false
    }
})

watch(() => data.config, () => {
    if (data.local.configGetOK) {
        saveconfig();
    }
}, { deep: true })
const mdhtml = computed(() => marked(data.local.markdownContent))

const statsData = ref([])
const loading = ref(true)
const error = ref(null)
const counter_mode = ref("true")

onMounted(() => {
    getconfig()
    fetchData()
    getUpdate()

    axios.get('/api/version').then(response => {
        data.local.versionstr = response.data['text'];
    });
})

const getCapture = () => {
    axios.get('/api/getcapture', { params: { 'Separate_Self_Game_Mic': data.config.Separate_Self_Game_Mic } }).then(response => {
        captureName.value = response.data;
        ElMessage({
            message: '桌面音频名称获取成功',
            type: 'success',
        })
    });

}
const getUpdate = () => {
    axios.get('/api/getUpdate').then(response => {
        if (response.status == 200) {
            data.local.updateInfo = response.data.info;
            dialogVisible.value = true
            data.local.markdownContent = response.data.changelog
        }


    });

}

const upgrade = () => {
    axios.get('/api/upgrade').then(response => {
        if (response.status == 401) {
            window.location.reload();
        }
    }
    )
    ElMessage({
        type: 'success',
        message: '开始更新',
    })
}

// 日期格式化
const formatDate = (dateString) => {
    const date = new Date(dateString)
    return `${date.getFullYear()}年${(date.getMonth() + 1).toString().padStart(2, '0')}月${date.getDate().toString().padStart(2, '0')}日`
}
// 获取数据
const fetchData = async () => {
    try {
        const response = await axios.get('/api/stats', { params: { 'mode': counter_mode.value, 'dayNum': data.local.logDayNum } })
        statsData.value = response.data//.reverse()  转为日期升序排列
    } catch (err) {
        error.value = `数据加载失败: ${err.message}`
    } finally {
        loading.value = false
    }
}
watch(() => data.config.Separate_Self_Game_Mic, () => { getCapture() })
function getconfig() {
    axios.get('/api/getConfig').then(response => {
        data.config = response.data;
        data.local.configGetOK = true
        ElMessage({
            message: '配置信息获取成功',
            type: 'success',
        })
        toggleDark(data.config['darkmode'])
        
        // 配置加载完成后检查首次配置引导
        checkFirstTimeSetup()
    });

    axios.get('/api/getMics').then(response => {
        micName.value = response.data;
        ElMessage({
            message: '麦克风名称获取成功',
            type: 'success',
        })
    });
    axios.get('/api/getOutputs').then(response => {
        outputName.value = response.data;
        ElMessage({
            message: '扬声器名称获取成功',
            type: 'success',
        })
    });
    
    // 获取麦克风状态
    axios.get('/api/getMicStatus').then(response => {
        if (response.status === 200) {
            data.local.micEnabled = response.data.micEnabled;
            data.local.desktopEnabled = response.data.desktopEnabled;
        }
    }).catch(error => {
        console.error('获取麦克风状态失败:', error);
    });
    
    getCapture()
}
function saveconfig() {
    axios.post('/api/saveConfig', { 'config': data.config }, {
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(response => {
        if (response.status == 401) {
            ElMessage({ message: response.data['text'], type: 'error', })
        }
        if (response.status == 200) {
            ElMessage({ message: '配置保存完毕,重启服务后生效', type: 'success', })
        }
        if (response.status == 220) {
            ElMessage({ message: '配置保存完毕,请关闭整个程序后再重启程序', type: 'warning', })
        }

    })
}
function sendText() {
    axios.post('/api/sendTextandTranslate', { 'text': data.local.sendText }, {
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(response => {
        if (response.status == 401) {
            ElMessage({ message: response.data['text'], type: 'error', })
        }
        if (response.status == 200) {
            ElMessage({ message: '文字翻译发送成功', type: 'success', })
            data.local.sendText = ''
        }
    })
}
function handleClose(){
    axios.get('/api/closewindow')
}
function toggleFullScreen(){
    if(data.local.maximized)axios.get('/api/windowrestore') 
    else axios.get('/api/maximize')
    data.local.maximized= !data.local.maximized
}
function handleMinimize(){
    axios.get('/api/minimize')
}

function toggleMicAudio(enabled) {
    axios.get('/api/toggleMicAudio', { 
        params: { enabled: enabled } 
    }).then(response => {
        if (response.status == 200) {
            // 更新本地状态
            data.local.micEnabled = enabled;
            ElMessage({
                message: enabled ? '麦克风音频已启用' : '麦克风音频已弃用',
                type: 'success',
            })
        } else {
            ElMessage({
                message: '操作失败',
                type: 'error',
            })
        }
    }).catch(error => {
        ElMessage({
            message: '操作失败: ' + error.message,
            type: 'error',
        })
    })
}

function toggleDesktopAudio(enabled) {
    axios.get('/api/toggleDesktopAudio', { 
        params: { enabled: enabled } 
    }).then(response => {
        if (response.status == 200) {
            // 更新本地状态
            data.local.desktopEnabled = enabled;
            ElMessage({
                message: enabled ? '桌面音频已启用' : '桌面音频已弃用',
                type: 'success',
            })
        } else {
            ElMessage({
                message: '操作失败',
                type: 'error',
            })
        }
    }).catch(error => {
        ElMessage({
            message: '操作失败: ' + error.message,
            type: 'error',
        })
    })
}

function saveAndBoot() {
    saveconfig()
    reboot()
}
function reboot() {
    axios.get('/api/reboot')
}
function addItem() {
    data.config.defaultScripts.find(item => item.action == data.local.defaultScriptsAction).text.push('');
}
function addCustomItem() {
    data.config.scripts[data.local.scriptClick].text.push('');
}
function removeItem(index) {
    data.config.defaultScripts.find(item => item.action == data.local.defaultScriptsAction).text.splice(index, 1);
}
function removeCustomItem(index) {
    data.config.scripts[data.local.scriptClick].text.splice(index, 1);
}
function addActionItem() {
    data.config.scripts[data.local.scriptClick].vrcActions.push({
        "vrcPath": "",
        "vrcValue": 0,
        "vrcValueType": "bool",
        "sleeptime": 0.1
    })
}

function removeActionItem(index) {
    data.config.scripts[data.local.scriptClick].vrcActions.splice(index, 1);
}
function addScriptItem() {
    data.config.scripts.push({
        "action": t('form.action'),
        "text": [""],
        "vrcActions": [{
            "vrcPath": "",
            "vrcValueType": "bool",
            "vrcValue": 0,
            "sleeptime": 0.1
        }]
    })
}
function removeScriptItem() {
    const index = data.local.scriptClick
    ElMessageBox.confirm(
        t('scripts.confirmDeleteScript') + data.config.scripts[index]['action'],
        'Warning',
        {
            confirmButtonText: t('common.confirm'),
            cancelButtonText: t('common.cancel'),
            type: 'warning',
        }
    )
        .then(() => {
            if (index == 0 && data.config.scripts.length == 1) {
                data.config.scripts[0] = {
                    "action": t('form.action'),
                    "text": [""],
                    "vrcActions": [{
                        "vrcPath": "",
                        "vrcValueType": "bool",
                        "vrcValue": 0,
                        "sleeptime": 0.1
                    }]
                }

                return
            }
            else {
                data.local.scriptClick = index == 0 ? 0 : index - 1
                data.config.scripts.splice(index, 1);
            }

            ElMessage({
                type: 'success',
                message: t('scripts.deleteSuccess'),
            })
        })
        .catch(() => {
            ElMessage({
                type: 'info',
                message: t('scripts.cancelDelete'),
            })
        })

}
function getAvatarParameters() {
    axios.get('/api/getAvatarParameters').then(response => {
        data.avatarParameters = response.data.dataTable
        data.avatarInfo = response.data.avatarInfo
    });
}

// 校准相关方法
function startCalibration(mode) {
    currentCalibrationMode.value = mode
    calibrationDialogVisible.value = true
    calibrationInProgress.value = true
    calibrationProgress.value = 0
    calibrationProgressText.value = ''
    
    // 重置校准数据
    calibrationData.value = {
        noiseLevel: '',
        speechLevel: '',
        calculatedThreshold: ''
    }
    
    // 设置初始状态
    calibrationStatus.value = {
        title: mode === 'mic' ? t('voiceControl.calibrateMicThreshold') : t('voiceControl.calibrateDesktopThreshold'),
        type: 'info',
        description: t('voiceControl.calibrateThresholdDescription')
    }
    
    // 调用后端校准API
    axios.get('/api/vadCalibrate', { 
        params: { mode: mode } 
    }).then(response => {
        if (response.status === 200 && response.data.success) {
            // 校准成功，数据会通过socket事件更新
            console.log('Calibration started successfully')
        } else {
            throw new Error(response.data.error || '校准失败')
        }
    }).catch(error => {
        console.error('Calibration failed:', error)
        calibrationStatus.value = {
            title: t('voiceControl.calibrationFailed'),
            type: 'error',
            description: error.response?.data?.error || error.message || '校准失败'
        }
        calibrationInProgress.value = false
        ElMessage.error(t('voiceControl.calibrationFailed'))
    })
}

function cancelCalibration() {
    calibrationDialogVisible.value = false
    calibrationInProgress.value = false
    calibrationProgress.value = 0
    calibrationProgressText.value = ''
    calibrationData.value = {
        noiseLevel: '',
        speechLevel: '',
        calculatedThreshold: ''
    }
}

function applyCalibration() {
    if (calibrationData.value.calculatedThreshold) {
        const threshold = parseFloat(calibrationData.value.calculatedThreshold)
        if (currentCalibrationMode.value === 'mic') {
            data.config.customThreshold = threshold
        } else if (currentCalibrationMode.value === 'cap') {
            data.config.gameCustomThreshold = threshold
        }
        
        ElMessage.success(t('voiceControl.calibrationComplete'))
        calibrationDialogVisible.value = false
    }
}

// 首次配置引导相关方法
function checkFirstTimeSetup() {
    // 检查是否已经完成过首次配置
    const hasSetup = localStorage.getItem('hasCompletedFirstTimeSetup')
    if (!hasSetup && data.local.configGetOK) {
        // 检查配置是否为空或默认值，如果是则显示引导
        const isFirstTime = !data.config['osc-port'] || 
                           !data.config['osc-ip'] || 
                           !data.config.sourceLanguage || 
                           !data.config.targetTranslationLanguage
        
        // 设置默认值
        if (!data.config['osc-port']) data.config['osc-port'] = 9000
        if (!data.config['osc-ip']) data.config['osc-ip'] = '127.0.0.1'
        if (!data.config.sourceLanguage) data.config.sourceLanguage = 'zh'
        if (!data.config.targetTranslationLanguage) data.config.targetTranslationLanguage = 'en'
        
        if (isFirstTime) {
            showSimpleGuide.value = true
        }
    }
}

// 简易配置引导方法
function nextSimpleStep() {
    if (currentSimpleStep.value < 6) {
        currentSimpleStep.value++
    }
}

function previousSimpleStep() {
    if (currentSimpleStep.value > 0) {
        currentSimpleStep.value--
    }
}

function completeSimpleGuide() {
    // 保存配置
    saveconfig()
    
    // 标记已完成首次配置
    localStorage.setItem('hasCompletedFirstTimeSetup', 'true')
    hasCompletedFirstTimeSetup.value = true
    
    // 关闭引导对话框
    showSimpleGuide.value = false
    currentSimpleStep.value = 0
    
    ElMessage.success(t('guide.simpleSetupCompletedMessage'))
}

function skipSimpleGuide() {
    ElMessageBox.confirm(
        t('guide.skipGuideConfirm'),
        t('guide.skipGuideTitle'),
        {
            confirmButtonText: t('common.confirm'),
            cancelButtonText: t('common.cancel'),
            type: 'warning',
        }
    ).then(() => {
        // 保存当前配置
        saveconfig()
        
        // 标记已完成首次配置
        localStorage.setItem('hasCompletedFirstTimeSetup', 'true')
        hasCompletedFirstTimeSetup.value = true
        
        // 关闭引导对话框
        showSimpleGuide.value = false
        currentSimpleStep.value = 0
        
        ElMessage.success(t('guide.guideSkippedMessage'))
    }).catch(() => {
        // 用户取消跳过
    })
}






const recognizeLanguageOption = [
    { label: '阿非利堪斯语(Afrikaans)', value: 'af' },
    { label: '阿姆哈拉语(Amharic)', value: 'am' },
    { label: '阿拉伯语(Arabic)', value: 'ar' },
    { label: '阿萨姆语(Assamese)', value: 'as' },
    { label: '阿塞拜疆语(Azerbaijani)', value: 'az' },
    { label: '巴什基尔语(Bashkir)', value: 'ba' },
    { label: '白俄罗斯语(Belarusian)', value: 'be' },
    { label: '保加利亚语(Bulgarian)', value: 'bg' },
    { label: '孟加拉语(Bengali)', value: 'bn' },
    { label: '藏语(Tibetan)', value: 'bo' },
    { label: '布雷顿语(Breton)', value: 'br' },
    { label: '波斯尼亚语(Bosnian)', value: 'bs' },
    { label: '加泰罗尼亚语(Catalan)', value: 'ca' },
    { label: '捷克语(Czech)', value: 'cs' },
    { label: '威尔士语(Welsh)', value: 'cy' },
    { label: '丹麦语(Danish)', value: 'da' },
    { label: '德语(German)', value: 'de' },
    { label: '希腊语(Greek)', value: 'el' },
    { label: '英语(English)', value: 'en' },
    { label: '西班牙语(Spanish)', value: 'es' },
    { label: '爱沙尼亚语(Estonian)', value: 'et' },
    { label: '巴斯克语(Basque)', value: 'eu' },
    { label: '波斯语(Persian)', value: 'fa' },
    { label: '芬兰语(Finnish)', value: 'fi' },
    { label: '法罗语(Faroese)', value: 'fo' },
    { label: '法语(French)', value: 'fr' },
    { label: '加利西亚语(Galician)', value: 'gl' },
    { label: '古吉拉特语(Gujarati)', value: 'gu' },
    { label: '豪萨语(Hausa)', value: 'ha' },
    { label: '夏威夷语(Hawaiian)', value: 'haw' },
    { label: '希伯来语(Hebrew)', value: 'he' },
    { label: '印地语(Hindi)', value: 'hi' },
    { label: '克罗地亚语(Croatian)', value: 'hr' },
    { label: '海地克里奥尔语(Haitian Creole)', value: 'ht' },
    { label: '匈牙利语(Hungarian)', value: 'hu' },
    { label: '亚美尼亚语(Armenian)', value: 'hy' },
    { label: '印尼语(Indonesian)', value: 'id' },
    { label: '冰岛语(Icelandic)', value: 'is' },
    { label: '意大利语(Italian)', value: 'it' },
    { label: '日语(Japanese)', value: 'ja' },
    { label: '爪哇语(Javanese)', value: 'jw' },
    { label: '格鲁吉亚语(Georgian)', value: 'ka' },
    { label: '哈萨克语(Kazakh)', value: 'kk' },
    { label: '高棉语(Khmer)', value: 'km' },
    { label: '卡纳达语(Kannada)', value: 'kn' },
    { label: '韩语(Korean)', value: 'ko' },
    { label: '拉丁语(Latin)', value: 'la' },
    { label: '卢森堡语(Luxembourgish)', value: 'lb' },
    { label: '林加拉语(Lingala)', value: 'ln' },
    { label: '老挝语(Lao)', value: 'lo' },
    { label: '立陶宛语(Lithuanian)', value: 'lt' },
    { label: '拉脱维亚语(Latvian)', value: 'lv' },
    { label: '马达加斯加语(Malagasy)', value: 'mg' },
    { label: '毛利语(Maori)', value: 'mi' },
    { label: '马其顿语(Macedonian)', value: 'mk' },
    { label: '马拉雅拉姆语(Malayalam)', value: 'ml' },
    { label: '蒙古语(Mongolian)', value: 'mn' },
    { label: '马拉提语(Marathi)', value: 'mr' },
    { label: '马来语(Malay)', value: 'ms' },
    { label: '马耳他语(Maltese)', value: 'mt' },
    { label: '缅甸语(Burmese)', value: 'my' },
    { label: '尼泊尔语(Nepali)', value: 'ne' },
    { label: '荷兰语(Dutch)', value: 'nl' },
    { label: '尼诺尔斯克语(Nynorsk)', value: 'nn' },
    { label: '挪威语(Norwegian)', value: 'no' },
    { label: '奥克语(Occitan)', value: 'oc' },
    { label: '旁遮普语(Punjabi)', value: 'pa' },
    { label: '波兰语(Polish)', value: 'pl' },
    { label: '普什图语(Pashto)', value: 'ps' },
    { label: '葡萄牙语(Portuguese)', value: 'pt' },
    { label: '罗马尼亚语(Romanian)', value: 'ro' },
    { label: '俄语(Russian)', value: 'ru' },
    { label: '梵语(Sanskrit)', value: 'sa' },
    { label: '信德语(Sindhi)', value: 'sd' },
    { label: '僧伽罗语(Sinhala)', value: 'si' },
    { label: '斯洛伐克语(Slovak)', value: 'sk' },
    { label: '斯洛文尼亚语(Slovenian)', value: 'sl' },
    { label: '修纳语(Shona)', value: 'sn' },
    { label: '索马里语(Somali)', value: 'so' },
    { label: '阿尔巴尼亚语(Albanian)', value: 'sq' },
    { label: '塞尔维亚语(Serbian)', value: 'sr' },
    { label: '巽他语(Sundanese)', value: 'su' },
    { label: '瑞典语(Swedish)', value: 'sv' },
    { label: '斯瓦希里语(Swahili)', value: 'sw' },
    { label: '泰米尔语(Tamil)', value: 'ta' },
    { label: '泰卢固语(Telugu)', value: 'te' },
    { label: '塔吉克语(Tajik)', value: 'tg' },
    { label: '泰语(Thai)', value: 'th' },
    { label: '土库曼语(Turkmen)', value: 'tk' },
    { label: '他加禄语(Tagalog)', value: 'tl' },
    { label: '土耳其语(Turkish)', value: 'tr' },
    { label: '鞑靼语(Tatar)', value: 'tt' },
    { label: '乌克兰语(Ukrainian)', value: 'uk' },
    { label: '乌尔都语(Urdu)', value: 'ur' },
    { label: '乌兹别克语 (Uzbek)', value: 'uz' },
    { label: '越南语(Vietnamese)', value: 'vi' },
    { label: '依地语(Yiddish)', value: 'yi' },
    { label: '约鲁巴语(Yoruba)', value: 'yo' },
    { label: '粤语(Cantonese)', value: 'yue' },
    { label: '简体中文(Chinese Simplified)', value: 'zh' },
    { label: '繁體中文(Chinese Traditional)', value: 'zt' }
]

const translateLanguageOption = [
    { label: '阿拉伯语(Arabic)', value: 'ar' },
    { label: '阿塞拜疆语(Azerbaijani)', value: 'az' },
    { label: '保加利亚语(Bulgarian)', value: 'bg' },
    { label: '孟加拉语(Bengali)', value: 'bn' },
    { label: '加泰罗尼亚语(Catalan)', value: 'ca' },
    { label: '捷克语(Czech)', value: 'cs' },
    { label: '丹麦语(Danish)', value: 'da' },
    { label: '德语(German)', value: 'de' },
    { label: '希腊语(Greek)', value: 'el' },
    { label: '英语(English)', value: 'en' },
    { label: '世界语(Esperanto)', value: 'eo' },
    { label: '西班牙语(Spanish)', value: 'es' },
    { label: '爱沙尼亚语(Estonian)', value: 'et' },
    { label: '巴斯克语(Basque)', value: 'eu' },
    { label: '波斯语(Persian)', value: 'fa' },
    { label: '芬兰语(Finnish)', value: 'fi' },
    { label: '法语(French)', value: 'fr' },
    { label: '爱尔兰语(Irish)', value: 'ga' },
    { label: '加利西亚语(Galician)', value: 'gl' },
    { label: '希伯来语(Hebrew)', value: 'he' },
    { label: '印地语(Hindi)', value: 'hi' },
    { label: '匈牙利语(Hungarian)', value: 'hu' },
    { label: '印尼语(Indonesian)', value: 'id' },
    { label: '意大利语(Italian)', value: 'it' },
    { label: '日语(Japanese)', value: 'ja' },
    { label: '韩语(Korean)', value: 'ko' },
    { label: '立陶宛语(Lithuanian)', value: 'lt' },
    { label: '拉脱维亚语(Latvian)', value: 'lv' },
    { label: '马来语(Malay)', value: 'ms' },
    { label: '挪威语(Bokmål)', value: 'nb' },
    { label: '荷兰语(Dutch)', value: 'nl' },
    { label: '波兰语(Polish)', value: 'pl' },
    { label: '葡萄牙语(Portuguese)', value: 'pt' },
    { label: '罗马尼亚语(Romanian)', value: 'ro' },
    { label: '俄语(Russian)', value: 'ru' },
    { label: '斯洛伐克语(Slovak)', value: 'sk' },
    { label: '斯洛文尼亚语(Slovenian)', value: 'sl' },
    { label: '阿尔巴尼亚语(Albanian)', value: 'sq' },
    { label: '塞尔维亚语(Serbian)', value: 'sr' },
    { label: '瑞典语(Swedish)', value: 'sv' },
    { label: '泰语(Thai)', value: 'th' },
    { label: '塔加洛语(Tagalog)', value: 'tl' },
    { label: '土耳其语(Turkish)', value: 'tr' },
    { label: '乌克兰语(Ukrainian)', value: 'uk' },
    { label: '乌尔都语(Urdu)', value: 'ur' },
    { label: '越南语(Vietnamese)', value: 'vi' },
    { label: '中文(Chinese)', value: 'zh' },
    { label: '繁体中文(Chinese)', value: 'zt' }
]
const computedTranslateLanguage = computed(() => {

    if (data.config.sourceLanguage != 'zh' && data.config.sourceLanguage != 'zt') {
        return translateLanguageOption.filter(item => item.value != data.config.sourceLanguage)
    }
    else {
        return translateLanguageOption.filter(item => item.value != 'zh' && item.value != 'zt')
    }


})
</script>

<style scoped>
.info-container {
    padding: 20px;
    font-size: 14px;
    /* 可以根据需要调整字体大小 */
    line-height: 1.5;
    /* 调整行高以增加可读性 */
}

.info-container p {
    margin: 10px 0;
    /* 调整段落之间的间距 */
}

.custom-header {
    position: relative; /* 关键：为绝对定位的子元素提供定位上下文 */
    display: flex;
    align-items: center; /* 垂直居中 header-actions 里的内容 */
    justify-content: flex-end; /* 将 header-actions 推到最右边 */
    background-color: #f5f7fa;
    border-bottom: 1px solid #e4e7ed;
    padding: 0 20px; /* 给头部一些内边距 */
    box-sizing: border-box; /* 确保 padding 不会影响宽度计算导致内容溢出 */

}

/* 暗黑模式下的头部样式 */
.dark .custom-header {
    background-color: #141414;
    border-bottom: 1px solid #303030;
}

.header-title-centered {
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%); /* 水平垂直居中 */
    font-size: 20px;
    font-weight: bold; /* el-text tag="b" 的效果 */
    color: #303133; /* 浅色模式下的标题颜色 */
    /* 如果 el-text 自动处理暗色模式颜色，则下面这行可能不需要 */
    /* 或者如果需要强制指定，则取消注释 */
}

.dark .header-title-centered {
    color: #e0e0e0; /* 暗黑模式下的标题颜色 */
}

.header-actions {
    display: flex;
    align-items: center;
    /* z-index: 1; */ /* 如果标题覆盖了按钮，可以尝试给 actions 加一个 z-index */
}

.header-actions .el-button {
    margin-left: 10px; /* 按钮之间的间距 */
}

.header-actions .el-button:hover {
    color: var(--el-color-primary);
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.card-header span {
    flex: 1;
    text-align: center;
}

/* 校准对话框样式 */
.calibration-content {
    padding: 20px 0;
}

.calibration-status {
    margin: 20px 0;
}

.calibration-data {
    margin: 20px 0;
    padding: 15px;
    background-color: #f5f7fa;
    border-radius: 8px;
}

.data-item {
    margin: 10px 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.data-item .label {
    font-weight: bold;
    color: #606266;
}

.data-item .value {
    font-family: monospace;
    color: #409eff;
    font-weight: bold;
}

.calibration-progress {
    margin: 20px 0;
}

.progress-text {
    text-align: center;
    margin-top: 10px;
    color: #606266;
    font-size: 14px;
}

.dark .calibration-data {
    background-color: #2b2b2b;
}

.dark .data-item .label {
    color: #e0e0e0;
}

.dark .data-item .value {
    color: #67c23a;
}

.dark .progress-text {
    color: #e0e0e0;
}

/* 首次配置引导样式 */
.guide-container {
    padding: 20px 0;
}

.guide-content {
    margin: 30px 0;
    min-height: 400px;
}

.guide-progress-indicator {
    margin-bottom: 20px;
    text-align: center;
}

.guide-progress-indicator .progress-text {
    margin-top: 10px;
    color: #606266;
    font-size: 14px;
}

.guide-step {
    padding: 20px;
}

.guide-step h3 {
    margin-bottom: 20px;
    color: #303133;
    font-size: 18px;
    font-weight: bold;
    text-align: center;
    padding-bottom: 10px;
    border-bottom: 2px solid #409eff;
}

.guide-instructions {
    margin-bottom: 20px;
}

.guide-instruction-list {
    margin: 10px 0;
}

.guide-instruction-list p {
    margin: 8px 0;
    line-height: 1.6;
}

.guide-config-section {
    margin-top: 20px;
    padding: 15px;
    background-color: #f8f9fa;
    border-radius: 8px;
    border: 1px solid #e9ecef;
}

.guide-config-section h4 {
    margin-bottom: 15px;
    color: #495057;
    font-size: 16px;
}

.guide-summary {
    margin-top: 20px;
}

.guide-summary h4 {
    margin-bottom: 15px;
    color: #495057;
}

.guide-actions {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 30px;
    padding-top: 20px;
    border-top: 1px solid #e4e7ed;
}

.guide-actions > div {
    display: flex;
    gap: 10px;
}

/* 暗黑模式下的引导样式 */
.dark .guide-step h3 {
    color: #e0e0e0;
}

.dark .guide-config-section {
    background-color: #2b2b2b;
    border-color: #404040;
}

.dark .guide-config-section h4 {
    color: #e0e0e0;
}

.dark .guide-summary h4 {
    color: #e0e0e0;
}

.dark .guide-actions {
    border-top-color: #404040;
}

.dark .guide-progress-indicator .progress-text {
    color: #e0e0e0;
}
</style>
