<template>

    <el-container>
        <el-header height="10vh" class="custom-header pywebview-drag-region">
            <!-- 居中的标题，使用绝对定位 -->
            <el-text tag="b" class="header-title-centered">VRCLS面板</el-text>

            <!-- 右侧控件组 -->
            <div class="header-actions">
                <el-switch v-model="isDark" inline-prompt :active-icon="MoonIcon" :inactive-icon="SunIcon"
                    active-color="#2c2c2c" inactive-color="#f2f2f2" border-color="#dcdfe6" style="margin-right: 15px;"
                    @change="changeDark" />
                <el-tooltip content="最小化" placement="bottom">
                    <el-button :icon="MinusIcon" circle @click="handleMinimize" />
                </el-tooltip>
                <el-tooltip :content="data.local.maximized ? '退出最大化' : '最大化'" placement="bottom">
                    <el-button :icon="data.local.maximized ? RankIcon : FullScreenIcon" circle @click="toggleFullScreen" />
                </el-tooltip>
                <el-tooltip content="关闭" placement="bottom">
                    <el-button :icon="CloseIcon" circle @click="handleClose" />
                </el-tooltip>
            </div>
        </el-header>
        <el-container>
            <el-aside width="200">
                <h5 class="mb-2">{{ data.local.versionstr }}</h5>
                <el-menu default-active="1" class="el-menu-vertical-demo" @select="menuClick">
                    <!-- <el-sub-menu index="1">
                    <template #title>
                        <el-icon><location /></el-icon>
                        <span>Navigator One</span>
                    </template>
<el-menu-item-group title="Group One">
    <el-menu-item index="1-1">item one</el-menu-item>
    <el-menu-item index="1-2">item two</el-menu-item>
</el-menu-item-group>
<el-menu-item-group title="Group Two">
    <el-menu-item index="1-3">item three</el-menu-item>
</el-menu-item-group>
<el-sub-menu index="1-4">
    <template #title>item four</template>
    <el-menu-item index="1-4-1">item one</el-menu-item>
</el-sub-menu>
</el-sub-menu> -->
                    <el-menu-item index="1">
                        <el-icon><icon-menu /></el-icon>
                        <span>首页</span>
                    </el-menu-item>
                    <el-menu-item index="2">
                        <el-icon><icon-menu /></el-icon>
                        <span>用量统计</span>
                    </el-menu-item>
                    <el-menu-item index="3">
                        <el-icon><icon-menu /></el-icon>
                        <span>控制模式配置</span>
                    </el-menu-item>
                    <el-menu-item index="4">
                        <el-icon>
                            <setting />
                        </el-icon>
                        <span>程序设置</span>
                    </el-menu-item>
                    <el-menu-item index="5">
                        <el-icon>
                            <document />
                        </el-icon>
                        <span>日志</span>
                    </el-menu-item>
                </el-menu>
            </el-aside>
            <el-main>
                <el-button-group style="margin-left:50%;margin-bottom: 20px;"
                    v-if="data.local.clickedMenuItem == 3 || data.local.clickedMenuItem == 4">
                    <el-button type="primary" @click="getconfig">获取配置</el-button>
                    <el-button type="primary" @click="saveconfig">保存配置</el-button>
                    <el-button type="primary" @click="saveAndBoot">保存配置并重启</el-button>
                    <el-button type="primary" @click="reboot">重启服务</el-button>
                </el-button-group>
                <div v-if="data.local.clickedMenuItem == 1">

                    <el-row :gutter="20">
                        <el-col :span="20">
                            <el-row :gutter="20">


                                <el-col :span="data.config.Separate_Self_Game_Mic == 0 ? 24 : 12">
                                    <el-card class="log-container">
                                        <template #header>
                                            <div class="card-header">
                                                <span>麦克风识别结果</span>
                                            </div>
                                        </template>
                                        <el-table :data="data.local.micInfo" :show-header="false" height="65vh"
                                            @row-click="handleRowClick">
                                            <el-table-column prop="text" label="文本" />
                                        </el-table>
                                    </el-card>
                                </el-col>
                                <el-col :span="12" v-if="data.config.Separate_Self_Game_Mic != 0">
                                    <el-card class="log-container">
                                        <template #header>
                                            <div class="card-header">
                                                <span>桌面音频识别结果</span>
                                            </div>
                                        </template>
                                        <el-table :data="data.local.desktopInfo" :show-header="false" height="65vh"
                                            @row-click="handleRowClick">
                                            <el-table-column prop="text" label="文本" />
                                        </el-table>
                                    </el-card>

                                </el-col>
                            </el-row>
                            <div style="margin-top: 2vh;">

                            </div>
                            <el-input v-model="data.local.sendText" placeholder="请输入需要翻译的文字" @keyup.enter="sendText">

                                <template #append>
                                    <el-button type="primary" @click="sendText">发送</el-button>
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
                            <span>实时日志</span>
                        </div>
                    </template>
                    <el-input type="textarea" :rows="25" readonly v-model="data.local.loggerInfo" class="log-textarea"
                        resize="none"></el-input>
                </el-card>
                <div v-if="data.local.clickedMenuItem == 4">
                    <el-row :gutter="20">
                        <el-col :span="20">
                            <el-scrollbar height="75vh" :always="true">
                                <el-card style="margin-bottom: 20px;">
                                    <template #header>
                                        <div class="card-header">
                                            <span>程序配置</span>
                                        </div>

                                    </template>
                                    <el-form :model="data.config" label-width="auto">
                                        <el-form-item label="服务器URL">
                                            <el-input v-model="data.config.baseurl"></el-input>
                                        </el-form-item>
                                        <el-form-item label="OSC 端口">
                                            <el-input type="number" v-model="data.config['osc-port']"></el-input>
                                        </el-form-item>
                                        <el-form-item label="OSC IP 地址">
                                            <el-input v-model="data.config['osc-ip']"></el-input>
                                        </el-form-item>
                                        <el-form-item label="默认模式">
                                            <el-select v-model="data.config.defaultMode">
                                                <el-option label="控制" value="control"></el-option>
                                                <el-option label="翻译" value="translation"></el-option>
                                                <el-option label="文字发送" value="text"></el-option>
                                                <el-option label="点阵屏" value="bitMapLed"></el-option>
                                            </el-select>
                                        </el-form-item>
                                        <el-form-item label="语音识别语言">
                                            <el-tooltip class="box-item" effect="dark" content="可说中文输出日语"
                                                placement="right">
                                                <el-select v-model="data.config.sourceLanguage">
                                                    <el-option v-for="item in recognizeLanguageOption" :key="item.value"
                                                        :label="item.label" :value="item.value"></el-option>
                                                </el-select>
                                            </el-tooltip>
                                        </el-form-item>
                                        <el-form-item label="默认翻译语言">
                                            <el-tooltip class="box-item" effect="dark" content="如果翻译时报错请检查服务端是否支持"
                                                placement="right">
                                                <el-select v-model="data.config.targetTranslationLanguage">
                                                    <el-option v-for="item in computedTranslateLanguage"
                                                        :key="item.value" :label="item.label"
                                                        :value="item.value"></el-option>
                                                </el-select>
                                            </el-tooltip>
                                        </el-form-item>
                                        <el-form-item label="第二翻译语言">
                                            <el-tooltip class="box-item" effect="dark" content="如果翻译时报错请检查服务端是否支持"
                                                placement="right">
                                                <el-select v-model="data.config.targetTranslationLanguage2">
                                                    <el-option label="关闭" value="none"></el-option>
                                                    <el-option v-for="item in computedTranslateLanguage"
                                                        :key="item.value" :label="item.label"
                                                        :value="item.value"></el-option>
                                                </el-select>
                                            </el-tooltip>
                                        </el-form-item>
                                        <el-form-item label="第三翻译语言">
                                            <el-tooltip class="box-item" effect="dark" content="如果翻译时报错请检查服务端是否支持"
                                                placement="right">
                                                <el-select v-model="data.config.targetTranslationLanguage3">
                                                    <el-option label="关闭" value="none"></el-option>
                                                    <el-option v-for="item in computedTranslateLanguage"
                                                        :key="item.value" :label="item.label"
                                                        :value="item.value"></el-option>
                                                </el-select>
                                            </el-tooltip>
                                        </el-form-item>
                                        <el-form-item label="独立桌面音频捕捉">
                                            <!-- <el-select v-model="data.config.Separate_Self_Game_Mic" @change="getCapture"> -->
                                            <el-select v-model="data.config.Separate_Self_Game_Mic">
                                                <el-option label="关闭" :value="0"></el-option>
                                                <el-option label="使用桌面音频" :value="1"></el-option>
                                                <el-option label="使用虚拟声卡麦克风" :value="2"></el-option>
                                            </el-select>
                                        </el-form-item>
                                        <el-form-item label="麦克风使用本地识别模型">
                                            <el-select v-model="data.config.localizedSpeech">
                                                <el-option label="开启" :value="true"></el-option>
                                                <el-option label="关闭" :value="false"></el-option>
                                            </el-select>
                                        </el-form-item>
                                        <el-form-item label="桌面音频使用本地识别模型">
                                            <el-select v-model="data.config.localizedCapture"
                                                :disabled="!data.config.Separate_Self_Game_Mic">
                                                <el-option label="开启" :value="true"></el-option>
                                                <el-option label="关闭" :value="false"></el-option>
                                            </el-select>
                                        </el-form-item>
                                        <el-form-item label="SteamVR掌心输出显示">
                                            <el-select v-model="data.config.textInSteamVR">
                                                <el-option label="开启" :value="true"></el-option>
                                                <el-option label="关闭" :value="false"></el-option>
                                            </el-select>
                                        </el-form-item>
                                        <el-form-item label="SteamVR显示位置">
                                            <el-select v-model="data.config.SteamVRHad"
                                                :disabled="!data.config.textInSteamVR">
                                                <el-option label="右手" :value="0"></el-option>
                                                <el-option label="左手" :value="1"></el-option>
                                                <el-option label="左手+右手" :value="2"></el-option>
                                            </el-select>
                                        </el-form-item>
                                        <el-form-item label="SteamVR显示大小">
                                            <el-slider v-model="data.config.SteamVRSize" show-input :max="0.5"
                                                :step="0.01" :disabled="!data.config.textInSteamVR" />
                                        </el-form-item>
                                        <el-form-item label="语音合成输出">
                                            <el-select v-model="data.config.TTSToggle">
                                                <el-option label="关闭" :value="0"></el-option>
                                                <el-option label="翻译模式麦克风译文输出" :value="1"></el-option>
                                                <el-option label="文字发送模式麦克风原文" :value="2"></el-option>
                                                <el-option label="翻译模式麦克风+桌面音频译文输出" :value="3"></el-option>
                                            </el-select>
                                        </el-form-item>
                                        <el-form-item label="翻译引擎">
                                            <el-tooltip class="box-item" effect="dark" content="如果翻译提示翻译异常，可以尝试更换引擎"
                                                placement="right">
                                                <el-select v-model="data.config.translateService">
                                                    <el-option label="开发者服务器" value="developer"></el-option>
                                                    <el-option label="阿里巴巴" value="alibaba"></el-option>
                                                    <el-option label="谷歌(中国大陆地区不可用)" value="google"></el-option>
                                                    <el-option label="MyMemory" value="myMemory"></el-option>
                                                    <el-option label="百度(坏的)" value="baidu"></el-option>
                                                    <el-option label="ModernMt" value="modernMt"></el-option>
                                                    <el-option label="火山翻译" value="volcEngine"></el-option>
                                                    <el-option label="金山词霸" value="iciba"></el-option>
                                                    <el-option label="讯飞智能" value="iflytek"></el-option>
                                                    <el-option label="Bing" value="bing"></el-option>
                                                    <el-option label="Lingvanex" value="lingvanex"></el-option>
                                                    <el-option label="Yandex" value="yandex"></el-option>
                                                    <el-option label="Itranslate" value="itranslate"></el-option>
                                                    <el-option label="Deepl" value="deepl"></el-option>
                                                    <el-option label="云译" value="cloudTranslation"></el-option>
                                                    <el-option label="腾讯交互翻译" value="qqTranSmart"></el-option>
                                                    <el-option label="Itranslate" value="itranslate"></el-option>
                                                    <el-option label="搜狗" value="sogou"></el-option>
                                                    <el-option label="腾讯翻译君" value="qqFanyi"></el-option>
                                                    <el-option label="有道" value="youdao"></el-option>
                                                    <el-option label="讯飞听见" value="iflyrec"></el-option>
                                                    <el-option label="沪江" value="hujiang"></el-option>
                                                    <el-option label="中译语通" value="yeekit"></el-option>

                                                </el-select>
                                            </el-tooltip>
                                        </el-form-item>
                                        <el-form-item label="翻译引擎接入点地区">
                                            <el-select v-model="data.config.translateRegion">
                                                <el-option label="中国大陆地区" value="CN"></el-option>
                                                <el-option label="其他" value="EN"></el-option>
                                            </el-select>
                                        </el-form-item>
                                        <el-form-item label="osc输出">
                                            <el-select v-model="data.config.oscShutdown">
                                                <el-option label="暂停" :value="true"></el-option>
                                                <el-option label="开启" :value="false"></el-option>
                                            </el-select>
                                        </el-form-item>
                                        <el-form-item label="情绪识别emoji输出">
                                            <el-select v-model="data.config.filteremoji">
                                                <el-option label="关闭" value="true"></el-option>
                                                <el-option label="开启" value="false"></el-option>
                                            </el-select>
                                        </el-form-item>
                                        <el-form-item label="外源OSC服务端端口">
                                            <el-select v-model="data.config.enableOscServer">
                                                <el-option label="开启" :value="true"></el-option>
                                                <el-option label="关闭" :value="false"></el-option>
                                            </el-select>
                                        </el-form-item>
                                        <el-form-item label="接收外源OSC服务端 端口">
                                            <el-input type="number" v-model="data.config['oscServerPort']"></el-input>
                                        </el-form-item>
                                        <el-form-item label="接收外源OSC服务端 IP地址">
                                            <el-input v-model="data.config['oscServerIp']"></el-input>
                                        </el-form-item>
                                    </el-form>
                                </el-card>

                                <el-card style="margin-bottom: 20px;">
                                    <template #header>
                                        <div class="card-header">
                                            <span>语音控制配置</span>
                                        </div>
                                    </template>

                                    <el-form :model="data.config" label-width="auto">
                                        <el-form-item label="麦克风">
                                            <el-select v-model="data.config.micName">
                                                <el-option label="系统默认麦克风" value="default"></el-option>
                                                <el-option v-for="(item, index) in micName" :key="index" :label="item"
                                                    :value="item"></el-option>
                                            </el-select>
                                        </el-form-item>


                                        <el-form-item label="麦克风语音模式">
                                            <el-select v-model="data.config.voiceMode">
                                                <el-option label="持续开启" :value="0"></el-option>
                                                <el-option label="按键切换" :value="1"></el-option>
                                                <el-option label="按住说话" :value="2"></el-option>
                                            </el-select>
                                        </el-form-item>


                                        <el-form-item label="麦克风自定义阈值">
                                            <el-slider v-model="data.config.customThreshold" show-input :max="0.6"
                                                :step="0.001"
                                                :disabled="data.config.dynamicThreshold || data.config.localizedSpeech" />
                                        </el-form-item>
                                        <el-form-item label="麦克风按键切换快捷键">
                                            <el-input v-model="data.config.voiceHotKey_new"></el-input>
                                        </el-form-item>
                                        <el-form-item label="麦克风按住说话按键">
                                            <el-tooltip class="box-item" effect="dark" content="只允许单个字母按键"
                                                placement="right">
                                                <el-input v-model="data.config.micPressingKey" :maxlength="1"
                                                    @input="data.config.micPressingKey = $event.replace(/[^a-zA-Z]/g, '')"></el-input>
                                            </el-tooltip>
                                        </el-form-item>
                                        <el-form-item label="桌面音频源/麦克风">
                                            <el-select v-model="data.config.gameMicName"
                                                :disabled="data.config.Separate_Self_Game_Mic == 0">
                                                <el-option label="系统默认" value="default"></el-option>
                                                <el-option v-for="(item, index) in captureName" :key="index"
                                                    :label="item" :value="item"></el-option>
                                            </el-select>
                                        </el-form-item>
                                        <el-form-item label="桌面音频语音模式">
                                            <el-select v-model="data.config.gameVoiceMode"
                                                :disabled="data.config.Separate_Self_Game_Mic == 0">
                                                <el-option label="持续开启" :value="0"></el-option>
                                                <el-option label="按键切换" :value="1"></el-option>
                                                <el-option label="按住开启" :value="2"></el-option>
                                            </el-select>
                                        </el-form-item>
                                        <el-form-item label="桌面音频自定义阈值">
                                            <el-slider v-model="data.config.gameCustomThreshold" show-input :max="0.6"
                                                :step="0.001"
                                                :disabled="data.config.dynamicThreshold || data.config.Separate_Self_Game_Mic == 0 || data.config.localizedCapture" />
                                        </el-form-item>
                                        <el-form-item label="桌面音频按键切换快捷键">
                                            <el-input v-model="data.config.gameVoiceHotKey_new"
                                                :disabled="data.config.Separate_Self_Game_Mic == 0"></el-input>
                                        </el-form-item>
                                        <el-form-item label="桌面音频按住开启按键">
                                            <el-tooltip class="box-item" effect="dark" content="只允许单个字母按键"
                                                placement="right">
                                                <el-input v-model="data.config.capPressingKey"
                                                    :disabled="data.config.Separate_Self_Game_Mic == 0" :maxlength="1"
                                                    @input="data.config.capPressingKey = $event.replace(/[^a-zA-Z]/g, '')"></el-input>
                                            </el-tooltip>
                                        </el-form-item>
                                        <el-form-item label="TTS输出扬声器">
                                            <el-select v-model="data.config.TTSOutputName"
                                                :disabled="data.config.TTSToggle == 0">
                                                <el-option label="系统默认" value="default"></el-option>
                                                <el-option v-for="(item, index) in outputName" :key="index"
                                                    :label="item" :value="item"></el-option>
                                            </el-select>
                                        </el-form-item>
                                        <el-form-item label="本地识别模型实时文本输出间隔">
                                            <el-select v-model="data.config.realtimeOutputDelay"
                                                :disabled="!data.config.localizedSpeech">
                                                <el-option label="关闭" :value="-1.0"></el-option>
                                                <el-option label="1秒" :value="1.0"></el-option>
                                                <el-option label="2秒" :value="2.0"></el-option>
                                            </el-select>
                                        </el-form-item>
                                        <el-space fill>
                                            <el-alert type="info" show-icon :closable="true">
                                                <p>下方{translatedText}会被替换为译文，{text}会被替换为原文,{translatedText2}为第二语言译文，{translatedText3}为第三语言译文
                                                </p>
                                            </el-alert>
                                            <el-form-item label="翻译模式VRC文本框输出样式">
                                                <el-input type="textarea" :autosize="{ minRows: 1, maxRows: 5 }"
                                                    v-model="data.config.VRCChatboxformat_new"></el-input>
                                            </el-form-item>
                                            <el-form-item label="文本发送模式VRC文本框输出样式">
                                                <el-input type="textarea" :autosize="{ minRows: 1, maxRows: 5 }"
                                                    v-model="data.config.VRCChatboxformat_text"></el-input>
                                            </el-form-item>
                                            <el-alert type="info" show-icon :closable="true">
                                                <p>下方{clientdata}会被替换为本软件输出内容，{serverdata}会被替换为外部osc接收内容的文本框内容
                                                </p>
                                            </el-alert>
                                            <el-form-item label="外源文本框文字嵌入模板">
                                                <el-input type="textarea" :autosize="{ minRows: 1, maxRows: 5 }"
                                                    v-model="data.config.chatboxOscMixTemplate"></el-input>
                                            </el-form-item>
                                        </el-space>


                                        <el-form-item label="点阵屏行列数">
                                            <el-row>
                                                <el-col :span="11">
                                                    <el-input v-model="data.config.VRCBitmapLed_row"
                                                        placeholder="行数"></el-input>
                                                </el-col>
                                                <el-col :span="2">
                                                    x
                                                </el-col>
                                                <el-col :span="11">
                                                    <el-input v-model="data.config.VRCBitmapLed_col"
                                                        placeholder="列数"></el-input>
                                                </el-col>
                                            </el-row>


                                        </el-form-item>

                                        <el-form-item label="点阵屏彩色模式">
                                            <el-radio-group v-model="data.config.VRCBitmapLed_COLOR">
                                                <el-radio :value="true" size="large">开启</el-radio>
                                                <el-radio :value="false" size="large">关闭</el-radio>
                                            </el-radio-group>
                                        </el-form-item>
                                        <el-form-item label="动态音量阈值">
                                            <el-tooltip class="box-item" effect="dark" content="不建议开启"
                                                placement="right">
                                                <el-radio-group v-model="data.config.dynamicThreshold">
                                                    <el-radio :value="true" size="large">开启</el-radio>
                                                    <el-radio :value="false" size="large">关闭</el-radio>
                                                </el-radio-group>
                                            </el-tooltip>
                                        </el-form-item>
                                    </el-form>
                                </el-card>

                                <el-card style="margin-bottom: 20px;">
                                    <template #header>
                                        <div class="card-header">
                                            <span>api账户配置</span>
                                        </div>

                                    </template>
                                    <el-form :model="data.config" label-width="auto">
                                        <el-form-item label="用户名">
                                            <el-input v-model="data.config.userInfo.username"></el-input>
                                        </el-form-item>
                                        <el-form-item label="密码">
                                            <el-input type="password" v-model="data.config.userInfo.password"
                                                show-password></el-input>
                                        </el-form-item>
                                    </el-form>
                                </el-card>
                                <el-card style="margin-bottom: 20px;">
                                    <template #header>
                                        <div class="card-header">
                                            <span>默认脚本关键词配置</span>
                                        </div>

                                    </template>
                                    <el-form label-width="auto">
                                        <el-form-item label="默认动作">
                                            <el-select v-model="data.local.defaultScriptsAction" style=" width: 100%">
                                                <el-option v-for="(item, index) in data.config.defaultScripts"
                                                    :label="item.text[0]" :value="item.action" :key="index"></el-option>
                                            </el-select>

                                        </el-form-item>
                                        <el-button type="primary" @click="addItem"
                                            style="margin-left: 70%;margin-bottom: 20px;">添加关键词</el-button>
                                        <el-scrollbar height="220px">


                                            <el-form-item
                                                v-for="(item1, index) in data.config.defaultScripts.find(item => item.action == data.local.defaultScriptsAction).text"
                                                :key="index" :label="'关键词' + (index + 1)">
                                                <el-row :gutter="20">
                                                    <el-col :span="18"><el-input
                                                            v-model="data.config.defaultScripts.find(item => item.action == data.local.defaultScriptsAction).text[index]"
                                                            placeholder="请输入文本"></el-input></el-col>
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
                                <span>日请求数量</span>
                            </div>
                        </template>
                        <el-alert v-if="error" :title="error" type="error" show-icon />
                        <el-row>
                            <el-col :span="8">
                                <el-text class="mx-1">显示日期数：</el-text>
                                <el-input-number v-model="data.local.logDayNum" :min="1" />
                            </el-col>
                            <el-col :span="8">
                                <el-radio-group v-model="counter_mode" @change="fetchData">
                                    <el-radio-button label="成功数" value="true" />
                                    <el-radio-button label="失败数" value="false" />
                                </el-radio-group>
                            </el-col>
                            <el-col :span="8">
                                <el-button type="primary" @click="fetchData">刷新</el-button>
                            </el-col>

                        </el-row>

                        <el-table :data="statsData" v-loading="loading" height="60vh" style="width: 100%">
                            <el-table-column prop="date" label="日期">
                                <template #default="{ row }">
                                    {{ formatDate(row.date) }}
                                </template>
                            </el-table-column>

                            <el-table-column prop="count" label="触发次数">
                                <template #default="{ row }">
                                    <el-tag :type="row.count > 0 ? 'success' : 'info'">
                                        {{ row.count }} 次
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
                                <span>自定义脚本配置</span>
                            </template>
                            <el-row :gutter="5">
                                <el-col :span="6">

                                    <h5 class="mb-2">自定义脚本目录</h5>
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
                                        <el-button type="primary" @click="addScriptItem">添加脚本</el-button>

                                        <el-button type="danger" @click="removeScriptItem">删除选定脚本</el-button>
                                    </el-button-group>


                                </el-col>

                                <el-col :span="9">
                                    <el-card style="height: 500px;">
                                        <template #header>
                                            <span>自定义脚本名称与关键词</span>
                                        </template>

                                        <el-form label-width="auto">
                                            <el-form-item label="自定义脚本名称">
                                                <el-input v-model="data.config.scripts[data.local.scriptClick].action"
                                                    placeholder="请输入名称"></el-input>
                                            </el-form-item>

                                            <el-button type="primary" @click="addCustomItem"
                                                style="margin-left: 70%;margin-bottom: 20px;">添加关键词</el-button>

                                            <el-scrollbar height="320px">
                                                <el-form-item
                                                    v-for="(item, index) in data.config.scripts[data.local.scriptClick].text"
                                                    :key="index" :label="'关键词' + (index + 1)">
                                                    <div>
                                                        <el-row :gutter="20">
                                                            <el-col :span="18"><el-input
                                                                    v-model="data.config.scripts[data.local.scriptClick].text[index]"
                                                                    placeholder="请输入文本"></el-input></el-col>
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
                                            <span>自定义脚本执行动作</span>
                                        </template>
                                        <el-scrollbar height="400px">
                                            <el-descriptions
                                                v-for="(item, index) in data.config.scripts[data.local.scriptClick].vrcActions"
                                                class="margin-top" :title="'动作' + (index + 1)" :column="1" border
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
                                                        VRC参数路径
                                                    </template>
                                                    <el-tooltip class="box-item" effect="dark"
                                                        content="推荐从下方模型参数中复制参数路径" placement="right">
                                                        <el-input v-model="item.vrcPath" placeholder="请输入VRC参数路径" />
                                                    </el-tooltip>

                                                </el-descriptions-item>
                                                <el-descriptions-item>
                                                    <template #label>
                                                        VRC参数值
                                                    </template>
                                                    <el-input v-model="item.vrcValue" placeholder="请输入VRC参数值" />
                                                </el-descriptions-item>
                                                <el-descriptions-item>
                                                    <template #label>
                                                        VRC参数类型
                                                    </template>
                                                    <el-select v-model="item.vrcValueType">
                                                        <el-option label="Bool" value="bool"></el-option>
                                                        <el-option label="Float" value="float"></el-option>
                                                        <el-option label="Int" value="int"></el-option>
                                                    </el-select>
                                                </el-descriptions-item>
                                                <el-descriptions-item>
                                                    <template #label>
                                                        持续时间
                                                    </template>
                                                    <el-input v-model="item.sleeptime" placeholder="请输入持续时间" />
                                                </el-descriptions-item>
                                            </el-descriptions>
                                        </el-scrollbar>
                                    </el-card>
                                </el-col>
                            </el-row>




                        </el-card>

                        <el-card style="margin-top: 20px;height: 620px;">
                            <template #header>
                                <span>当前模型参数</span>
                            </template>
                            <el-descriptions :column="2" label-width="15%" border>
                                <template #extra>
                                    <el-button type="primary" @click="getAvatarParameters"
                                        style="float: right;">获取模型参数</el-button>
                                </template>
                                <el-descriptions-item>
                                    <template #label>
                                        模型名称
                                    </template>
                                    {{ data.avatarInfo.avatarName }}
                                </el-descriptions-item>
                                <el-descriptions-item>
                                    <template #label>
                                        模型ID
                                    </template>
                                    {{ data.avatarInfo.avatarID }}
                                </el-descriptions-item>
                                <el-descriptions-item :span="2">
                                    <template #label>
                                        模型OSC文件路径
                                    </template>
                                    {{ data.avatarInfo.filePath }}
                                </el-descriptions-item>
                            </el-descriptions>
                            <el-table :data="data.avatarParameters" style="width: 100%;height: 350px;" border stripe
                                empty-text="请点击上方按钮获取模型参数">
                                <el-table-column prop="name" label="参数名称" width="180" />
                                <el-table-column prop="path" label="参数路径" />
                                <el-table-column prop="type" label="参数类型" />
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
</template>

<script setup>
import { useDark, useToggle } from '@vueuse/core'
// import { Moon as MoonIcon, Sunny as SunIcon } from '@element-plus/icons-vue'; // Element Plus 图标
import {
    Moon as MoonIcon,
    Sunny as SunIcon,
    Minus as MinusIcon,
    FullScreen as FullScreenIcon,
    Close as CloseIcon,
    Rank as RankIcon, // 用于退出全屏的图标，也可以选择其他
} from '@element-plus/icons-vue';
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
    Document,
    Menu as IconMenu,
    Setting,
} from '@element-plus/icons-vue'
import useClipboard from 'vue-clipboard3';

const socket = io()
socket.on('log', (log) => {
    if (log.level == 'error') {
        ElNotification({
            title: '发生错误',
            message: log.text,
            duration: log.text.includes("[steamvr异常]") ? 4500 : 0,
            type: 'error',
        })
    }
    data.local.loggerInfo += log.timestamp + ': ' + log.level + ' - ' + log.text + '\n'
})
socket.on('cap', (log) => {

    data.local.desktopInfo.unshift({ text: log.text })
})
socket.on('mic', (log) => {
    data.local.micInfo.unshift({ text: log.text })
})
const dialogVisible = ref(false)
const captureName = ref([]);
const menuClick = (key, keyPath) => {
    data.local.clickedMenuItem = key
}

const { toClipboard } = useClipboard();
const handleRowClick = async (row) => {
    try {
        await toClipboard(row.text);
        ElMessage.success('复制成功');
    } catch (err) {
        ElMessage.error('复制失败');
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
        loggerInfo: '',
        desktopInfo: [],
        micInfo: [],
        versionstr: '',
        logDayNum: 7,
        sendText: '',
        maximized:false


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

    axios.get('/api/verion').then(response => {
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
        "action": "脚本",
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
        '请确认是否删除自定义脚本:' + data.config.scripts[index]['action'],
        'Warning',
        {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning',
        }
    )
        .then(() => {
            if (index == 0 && data.config.scripts.length == 1) {
                data.config.scripts[0] = {
                    "action": "脚本",
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
                message: '删除成功',
            })
        })
        .catch(() => {
            ElMessage({
                type: 'info',
                message: '取消删除',
            })
        })

}
function getAvatarParameters() {
    axios.get('/api/getAvatarParameters').then(response => {
        data.avatarParameters = response.data.dataTable
        data.avatarInfo = response.data.avatarInfo
    });
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
</style>
