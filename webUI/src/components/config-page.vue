<template>

    <el-container>  
      <el-header>
        <h1>VRCLS配置管理</h1>
      </el-header>
      <el-container>
        <el-aside width="10%">
            <sideInfo/>
        </el-aside>
        <el-main>
            <el-button-group style="margin-left:60%;margin-bottom: 20px;" >
                <el-button type="primary" @click="getconfig">获取配置</el-button>
                <el-button type="primary" @click="saveconfig">保存配置</el-button>
                <el-button type="primary" @click="saveAndBoot">保存配置并重启</el-button>
                <el-button type="primary" @click="reboot">重启服务</el-button>
            </el-button-group>
            <el-row :gutter="20">
                <el-col :span="8" >
                    <el-card style="height: 900px;">
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
                            <!-- <el-form-item label="浏览器exe路径">
                                <el-tooltip
                                    class="box-item"
                                    effect="dark"
                                    content="选填，需要指定到指定浏览器的exe绝对路径"
                                    placement="right"
                                >
                                <el-input v-model="data.config['webBrowserPath']" placeholder="如需指定浏览器再填写"></el-input>
                                </el-tooltip>
                            </el-form-item> -->
                            <el-form-item label="默认模式">
                                <el-select v-model="data.config.defaultMode">
                                    <el-option label="控制" value="control"></el-option>
                                    <el-option label="翻译" value="translation"></el-option>
                                    <el-option label="文字发送" value="text"></el-option>
                                    <el-option label="点阵屏" value="bitMapLed"></el-option>
                                </el-select>
                            </el-form-item>
                            <el-form-item label="语音识别语言">
                                <el-tooltip
                                    class="box-item"
                                    effect="dark"
                                    content="可说中文输出日语"
                                    placement="right"
                                >
                                <el-select v-model="data.config.sourceLanguage">
                                    <el-option label="阿非利堪斯语(Afrikaans)" value="af"></el-option>
                                    <el-option label="阿姆哈拉语(Amharic)" value="am"></el-option>
                                    <el-option label="阿拉伯语(Arabic)" value="ar"></el-option>
                                    <el-option label="阿萨姆语(Assamese)" value="as"></el-option>
                                    <el-option label="阿塞拜疆语(Azerbaijani)" value="az"></el-option>
                                    <el-option label="巴什基尔语(Bashkir)" value="ba"></el-option>
                                    <el-option label="白俄罗斯语(Belarusian)" value="be"></el-option>
                                    <el-option label="保加利亚语(Bulgarian)" value="bg"></el-option>
                                    <el-option label="孟加拉语(Bengali)" value="bn"></el-option>
                                    <el-option label="藏语(Tibetan)" value="bo"></el-option>
                                    <el-option label="布雷顿语(Breton)" value="br"></el-option>
                                    <el-option label="波斯尼亚语(Bosnian)" value="bs"></el-option>
                                    <el-option label="加泰罗尼亚语(Catalan)" value="ca"></el-option>
                                    <el-option label="捷克语(Czech)" value="cs"></el-option>
                                    <el-option label="威尔士语(Welsh)" value="cy"></el-option>
                                    <el-option label="丹麦语(Danish)" value="da"></el-option>
                                    <el-option label="德语(German)" value="de"></el-option>
                                    <el-option label="希腊语(Greek)" value="el"></el-option>
                                    <el-option label="英语(English)" value="en"></el-option>
                                    <el-option label="西班牙语(Spanish)" value="es"></el-option>
                                    <el-option label="爱沙尼亚语(Estonian)" value="et"></el-option>
                                    <el-option label="巴斯克语(Basque)" value="eu"></el-option>
                                    <el-option label="波斯语(Persian)" value="fa"></el-option>
                                    <el-option label="芬兰语(Finnish)" value="fi"></el-option>
                                    <el-option label="法罗语(Faroese)" value="fo"></el-option>
                                    <el-option label="法语(French)" value="fr"></el-option>
                                    <el-option label="加利西亚语(Galician)" value="gl"></el-option>
                                    <el-option label="古吉拉特语(Gujarati)" value="gu"></el-option>
                                    <el-option label="豪萨语(Hausa)" value="ha"></el-option>
                                    <el-option label="夏威夷语(Hawaiian)" value="haw"></el-option>
                                    <el-option label="希伯来语(Hebrew)" value="he"></el-option>
                                    <el-option label="印地语(Hindi)" value="hi"></el-option>
                                    <el-option label="克罗地亚语(Croatian)" value="hr"></el-option>
                                    <el-option label="海地克里奥尔语(Haitian Creole)" value="ht"></el-option>
                                    <el-option label="匈牙利语(Hungarian)" value="hu"></el-option>
                                    <el-option label="亚美尼亚语(Armenian)" value="hy"></el-option>
                                    <el-option label="印尼语(Indonesian)" value="id"></el-option>
                                    <el-option label="冰岛语(Icelandic)" value="is"></el-option>
                                    <el-option label="意大利语(Italian)" value="it"></el-option>
                                    <el-option label="日语(Japanese)" value="ja"></el-option>
                                    <el-option label="爪哇语(Javanese)" value="jw"></el-option>
                                    <el-option label="格鲁吉亚语(Georgian)" value="ka"></el-option>
                                    <el-option label="哈萨克语(Kazakh)" value="kk"></el-option>
                                    <el-option label="高棉语(Khmer)" value="km"></el-option>
                                    <el-option label="卡纳达语(Kannada)" value="kn"></el-option>
                                    <el-option label="韩语(Korean)" value="ko"></el-option>
                                    <el-option label="拉丁语(Latin)" value="la"></el-option>
                                    <el-option label="卢森堡语(Luxembourgish)" value="lb"></el-option>
                                    <el-option label="林加拉语(Lingala)" value="ln"></el-option>
                                    <el-option label="老挝语(Lao)" value="lo"></el-option>
                                    <el-option label="立陶宛语(Lithuanian)" value="lt"></el-option>
                                    <el-option label="拉脱维亚语(Latvian)" value="lv"></el-option>
                                    <el-option label="马达加斯加语(Malagasy)" value="mg"></el-option>
                                    <el-option label="毛利语(Maori)" value="mi"></el-option>
                                    <el-option label="马其顿语(Macedonian)" value="mk"></el-option>
                                    <el-option label="马拉雅拉姆语(Malayalam)" value="ml"></el-option>
                                    <el-option label="蒙古语(Mongolian)" value="mn"></el-option>
                                    <el-option label="马拉提语(Marathi)" value="mr"></el-option>
                                    <el-option label="马来语(Malay)" value="ms"></el-option>
                                    <el-option label="马耳他语(Maltese)" value="mt"></el-option>
                                    <el-option label="缅甸语(Burmese)" value="my"></el-option>
                                    <el-option label="尼泊尔语(Nepali)" value="ne"></el-option>
                                    <el-option label="荷兰语(Dutch)" value="nl"></el-option>
                                    <el-option label="尼诺尔斯克语(Nynorsk)" value="nn"></el-option>
                                    <el-option label="挪威语(Norwegian)" value="no"></el-option>
                                    <el-option label="奥克语(Occitan)" value="oc"></el-option>
                                    <el-option label="旁遮普语(Punjabi)" value="pa"></el-option>
                                    <el-option label="波兰语(Polish)" value="pl"></el-option>
                                    <el-option label="普什图语(Pashto)" value="ps"></el-option>
                                    <el-option label="葡萄牙语(Portuguese)" value="pt"></el-option>
                                    <el-option label="罗马尼亚语(Romanian)" value="ro"></el-option>
                                    <el-option label="俄语(Russian)" value="ru"></el-option>
                                    <el-option label="梵语(Sanskrit)" value="sa"></el-option>
                                    <el-option label="信德语(Sindhi)" value="sd"></el-option>
                                    <el-option label="僧伽罗语(Sinhala)" value="si"></el-option>
                                    <el-option label="斯洛伐克语(Slovak)" value="sk"></el-option>
                                    <el-option label="斯洛文尼亚语(Slovenian)" value="sl"></el-option>
                                    <el-option label="修纳语(Shona)" value="sn"></el-option>
                                    <el-option label="索马里语(Somali)" value="so"></el-option>
                                    <el-option label="阿尔巴尼亚语(Albanian)" value="sq"></el-option>
                                    <el-option label="塞尔维亚语(Serbian)" value="sr"></el-option>
                                    <el-option label="巽他语(Sundanese)" value="su"></el-option>
                                    <el-option label="瑞典语(Swedish)" value="sv"></el-option>
                                    <el-option label="斯瓦希里语(Swahili)" value="sw"></el-option>
                                    <el-option label="泰米尔语(Tamil)" value="ta"></el-option>
                                    <el-option label="泰卢固语(Telugu)" value="te"></el-option>
                                    <el-option label="塔吉克语(Tajik)" value="tg"></el-option>
                                    <el-option label="泰语(Thai)" value="th"></el-option>
                                    <el-option label="土库曼语(Turkmen)" value="tk"></el-option>
                                    <el-option label="他加禄语(Tagalog)" value="tl"></el-option>
                                    <el-option label="土耳其语(Turkish)" value="tr"></el-option>
                                    <el-option label="鞑靼语(Tatar)" value="tt"></el-option>
                                    <el-option label="乌克兰语(Ukrainian)" value="uk"></el-option>
                                    <el-option label="乌尔都语(Urdu)" value="ur"></el-option>
                                    <el-option label="乌兹别克语 (Uzbek)" value="uz"></el-option>
                                    <el-option label="越南语(Vietnamese)" value="vi"></el-option>
                                    <el-option label="依地语(Yiddish)" value="yi"></el-option>
                                    <el-option label="约鲁巴语(Yoruba)" value="yo"></el-option>
                                    <el-option label="粤语(Cantonese)" value="yue"></el-option>
                                    <el-option label="简体中文(Chinese Simplified)" value="zh"></el-option>
                                    <el-option label="繁體中文(Chinese Traditional)" value="zt"></el-option>
                                </el-select>
                                </el-tooltip>
                            </el-form-item>
                            <el-form-item label="默认翻译语言">
                                <el-tooltip
                                    class="box-item"
                                    effect="dark"
                                    content="如果翻译时报错请检查服务端是否支持"
                                    placement="right"
                                >
                                <el-select v-model="data.config.targetTranslationLanguage">
                                   <el-option label="阿拉伯语(Arabic)" value="ar"></el-option> 
                                    <el-option label="阿塞拜疆语(Azerbaijani)" value="az"></el-option> 
                                    <el-option label="保加利亚语(Bulgarian)" value="bg"></el-option> 
                                    <el-option label="孟加拉语(Bengali)" value="bn"></el-option> 
                                    <el-option label="加泰罗尼亚语(Catalan)" value="ca"></el-option> 
                                    <el-option label="捷克语(Czech)" value="cs"></el-option>
                                    <el-option label="丹麦语(Danish)" value="da"></el-option> 
                                    <el-option label="德语(German)" value="de"></el-option> 
                                    <el-option label="希腊语(Greek)" value="el"></el-option> 
                                    <el-option label="英语(English)" value="en"></el-option> 
                                    <el-option label="世界语(Esperanto)" value="eo"></el-option> 
                                    <el-option label="西班牙语(Spanish)" value="es"></el-option> 
                                    <el-option label="爱沙尼亚语(Estonian)" value="et"></el-option>
                                    <el-option label="巴斯克语(Basque)" value="eu"></el-option>
                                    <el-option label="波斯语(Persian)" value="fa"></el-option>
                                    <el-option label="芬兰语(Finnish)" value="fi"></el-option> 
                                    <el-option label="法语(French)" value="fr"></el-option>
                                    <el-option label="爱尔兰语(Irish)" value="ga"></el-option> 
                                    <el-option label="加利西亚语(Galician)" value="gl"></el-option>
                                    <el-option label="希伯来语(Hebrew)" value="he"></el-option> 
                                    <el-option label="印地语(Hindi)" value="hi"></el-option>
                                    <el-option label="匈牙利语(Hungarian)" value="hu"></el-option>
                                    <el-option label="印尼语(Indonesian)" value="id"></el-option> 
                                    <el-option label="意大利语(Italian)" value="it"></el-option> 
                                    <el-option label="日语(Japanese)" value="ja"></el-option> 
                                    <el-option label="韩语(Korean)" value="ko"></el-option> 
                                    <el-option label="立陶宛语(Lithuanian)" value="lt"></el-option>
                                    <el-option label="拉脱维亚语(Latvian)" value="lv"></el-option> 
                                    <el-option label="马来语(Malay)" value="ms"></el-option> 
                                    <el-option label="挪威语(Bokmål)" value="nb"></el-option> 
                                    <el-option label="荷兰语(Dutch)" value="nl"></el-option>
                                    <el-option label="波兰语(Polish)" value="pl"></el-option> 
                                    <el-option label="葡萄牙语(Portuguese)" value="pt"></el-option> 
                                    <el-option label="罗马尼亚语(Romanian)" value="ro"></el-option> 
                                    <el-option label="俄语(Russian)" value="ru"></el-option> 
                                    <el-option label="斯洛伐克语(Slovak)" value="sk"></el-option> 
                                    <el-option label="斯洛文尼亚语(Slovenian)" value="sl"></el-option>
                                    <el-option label="阿尔巴尼亚语(Albanian)" value="sq"></el-option>
                                    <el-option label="塞尔维亚语(Serbian)" value="sr"></el-option> 
                                    <el-option label="瑞典语(Swedish)" value="sv"></el-option> 
                                    <el-option label="泰语(Thai)" value="th"></el-option> 
                                    <el-option label="塔加洛语(Tagalog)" value="tl"></el-option> 
                                    <el-option label="土耳其语(Turkish)" value="tr"></el-option> 
                                    <el-option label="乌克兰语(Ukrainian)" value="uk"></el-option> 
                                    <el-option label="乌尔都语(Urdu)" value="ur"></el-option> 
                                    <el-option label="越南语(Vietnamese)" value="vi"></el-option> 
                                    <el-option label="中文(Chinese)" value="zh"></el-option>
                                    <el-option label="繁体中文(Chinese)" value="zt"></el-option>
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
                                <el-select v-model="data.config.localizedCapture" :disabled="!data.config.Separate_Self_Game_Mic">
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
                                <el-select v-model="data.config.SteamVRHad" :disabled="!data.config.textInSteamVR">
                                    <el-option label="右手" :value="0"></el-option>
                                    <el-option label="左手" :value="1"></el-option>
                                    <el-option label="左手+右手" :value="2"></el-option>
                                </el-select>
                            </el-form-item>
                            <el-form-item label="SteamVR显示大小">
                                <el-slider v-model="data.config.SteamVRSize" show-input :max="0.5" :step="0.01" :disabled="!data.config.textInSteamVR"/>
                            </el-form-item>
                            <el-form-item label="输出文本复制窗口">
                                <el-select v-model="data.config.CopyBox">
                                    <el-option label="开启" :value="true"></el-option>
                                    <el-option label="关闭" :value="false"></el-option>
                                </el-select>
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
                                <el-tooltip
                                    class="box-item"
                                    effect="dark"
                                    content="如果翻译提示翻译异常，可以尝试更换引擎"
                                    placement="right"
                                >
                                <el-select v-model="data.config.translateService">
                                    <el-option label="开发者服务器" value="developer"></el-option> 
                                    <el-option label="小牛翻译" value="niutrans"></el-option> 
                                    <el-option label="MyMemory" value="myMemory"></el-option> 
                                    <el-option label="阿里巴巴" value="alibaba"></el-option> 
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
                            <el-form-item label="暂停osc输出">
                                <el-select v-model="data.config.oscShutdown">
                                    <el-option label="开启" :value="true"></el-option>
                                    <el-option label="关闭" :value="false"></el-option>
                                </el-select>
                            </el-form-item>

                        </el-form>
                    </el-card>
                </el-col>
                <el-col :span="8">
                    <el-card style="height: 230px;margin-bottom: 20px;">
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
                                <el-input type="password" v-model="data.config.userInfo.password" show-password></el-input>
                            </el-form-item>
                        </el-form>
                    </el-card>
                    <el-card style="height: 650px;">
                        <template #header>
                            <div class="card-header">
                            <span>默认脚本关键词配置</span>
                            </div>
                            
                        </template>
                        <el-form label-width="auto">
                            <el-form-item label="默认动作" >         
                                <el-select v-model="data.local.defaultScriptsAction" style=" width: 100%">
                                    <el-option v-for="(item, index) in data.config.defaultScripts" :label="item.text[0]" :value="item.action" :key="index"></el-option>
                                </el-select>

                            </el-form-item>
                            <el-button type="primary" @click="addItem" style="margin-left: 70%;margin-bottom: 20px;">添加关键词</el-button>
                            <el-scrollbar height="220px">


                                <el-form-item v-for="(item1, index) in data.config.defaultScripts.find(item => item.action == data.local.defaultScriptsAction).text" :key="index" :label="'关键词' + (index + 1)">
                                    <el-row :gutter="20">
                                        <el-col :span="18"><el-input v-model="data.config.defaultScripts.find(item => item.action == data.local.defaultScriptsAction).text[index]"  placeholder="请输入文本"></el-input></el-col>
                                        <el-col :span="6"><el-button type="danger" :icon="Delete" circle  @click="removeItem(index)"/></el-col>
                                    
                                    
                                    </el-row>
                                </el-form-item>

                            </el-scrollbar>
                        </el-form>
                        
                    </el-card>
                </el-col>
                <el-col :span="8">
                    <el-card style="height: 900px;">
                        <template #header>
                            <div class="card-header">
                            <span>语音控制配置</span>
                            </div>
                        </template>

                        <el-form :model="data.config" label-width="auto">
                            <el-form-item label="麦克风">
                                <el-select v-model="data.config.micName">
                                    <el-option label="系统默认麦克风" value="default"></el-option>
                                    <el-option v-for="(item,index) in micName" :key="index" :label="item" :value="item"></el-option>
                                </el-select>
                            </el-form-item>
                           
                           
                            <el-form-item label="麦克风语音模式">
                                <el-select v-model="data.config.voiceMode">
                                    <el-option label="持续开启" :value="0"></el-option>
                                    <el-option label="按键切换" :value="1"></el-option>
                                    <el-option label="按下v说话" :value="2"></el-option>
                                </el-select>
                            </el-form-item>
 

                            <el-form-item label="麦克风自定义阈值">
                                <el-slider v-model="data.config.customThreshold" show-input :max="0.6" :step="0.001" :disabled="data.config.dynamicThreshold"/>
                            </el-form-item>
                            <el-form-item label="麦克风按键切换快捷键">
                                <el-input v-model="data.config.voiceHotKey_new"></el-input>
                            </el-form-item>

                            <el-form-item label="桌面音频源/麦克风">
                                <el-select v-model="data.config.gameMicName" :disabled="data.config.Separate_Self_Game_Mic==0">
                                    <el-option label="系统默认" value="default"></el-option>
                                    <el-option v-for="(item,index) in captureName" :key="index" :label="item" :value="item" ></el-option>
                                </el-select>
                            </el-form-item>
                            <el-form-item label="桌面音频语音模式">
                                <el-select v-model="data.config.gameVoiceMode" :disabled="data.config.Separate_Self_Game_Mic==0">
                                    <el-option label="持续开启" :value="0"></el-option>
                                    <el-option label="按键切换" :value="1"></el-option>
                                    <el-option label="按下v说话" :value="2"></el-option>
                                </el-select>
                            </el-form-item>
                            <el-form-item label="桌面音频自定义阈值">
                                <el-slider v-model="data.config.gameCustomThreshold" show-input :max="0.6" :step="0.001" :disabled="data.config.dynamicThreshold || data.config.Separate_Self_Game_Mic==0"/>
                            </el-form-item>
                            <el-form-item label="桌面音频按键切换快捷键">
                                <el-input v-model="data.config.gameVoiceHotKey_new" :disabled="data.config.Separate_Self_Game_Mic==0"></el-input>
                            </el-form-item>
                            <el-form-item label="TTS输出扬声器">
                                <el-select v-model="data.config.TTSOutputName" :disabled="data.config.TTSToggle==0">
                                    <el-option label="系统默认" value="default"></el-option>
                                    <el-option v-for="(item,index) in outputName" :key="index" :label="item" :value="item" ></el-option>
                                </el-select>
                            </el-form-item>
                            <el-form-item label="本地识别模型实时文本输出间隔">
                                <el-select v-model="data.config.realtimeOutputDelay" :disabled="!data.config.localizedSpeech">
                                    <el-option label="关闭" :value="-1.0"></el-option>
                                    <el-option label="1秒" :value="1.0"></el-option>
                                    <el-option label="2秒" :value="2.0"></el-option>
                                </el-select>
                            </el-form-item>
                            <el-space fill>
                                <el-alert type="info" show-icon :closable="true">
                                    <p>下方{translatedText}会被替换为译文，{text}会被替换为原文</p>
                                </el-alert>
                                <el-form-item label="VRC文本框输出样式">
                                    <el-input  type="textarea" :autosize="{ minRows: 1, maxRows: 2 }" v-model="data.config.VRCChatboxformat"></el-input>
                                </el-form-item>
                            </el-space>

                            <el-form-item label="点阵屏行列数">
                                <el-row>
                                    <el-col :span="11">
                                        <el-input v-model="data.config.VRCBitmapLed_row" placeholder="行数"></el-input>
                                    </el-col>
                                    <el-col  :span="2">
                                        x
                                    </el-col>
                                    <el-col :span="11">
                                        <el-input v-model="data.config.VRCBitmapLed_col" placeholder="列数"></el-input>
                                    </el-col>
                                </el-row>
                                
                                
                            </el-form-item>

                            <el-form-item label="点阵屏彩色模式">
                                <el-radio-group v-model="data.config.VRCBitmapLed_COLOR" >
                                    <el-radio :value="true" size="large">开启</el-radio>
                                    <el-radio :value="false" size="large">关闭</el-radio>
                                </el-radio-group>
                            </el-form-item>
                            <el-form-item label="动态音量阈值">
                                <el-tooltip
                                    class="box-item"
                                    effect="dark"
                                    content="不建议开启"
                                    placement="right"
                                >
                                <el-radio-group v-model="data.config.dynamicThreshold" >
                                    <el-radio :value="true" size="large">开启</el-radio>
                                    <el-radio :value="false" size="large">关闭</el-radio>
                                </el-radio-group>
                                </el-tooltip>
                            </el-form-item>
                        </el-form>
                    </el-card>

                </el-col>
            </el-row>
            <el-row :gutter="20" >
                <el-col  :span="8">
                    <el-card style="margin-top: 20px;height: 620px;">
                            <template #header>
                                <div class="card-header">
                                <span>日请求数量(近7日)</span>
                                </div>
                            </template>
                            <el-alert v-if="error" :title="error" type="error" show-icon />
                            <el-row>
                                <el-col :span="16">
                                <el-radio-group v-model="counter_mode" @change="fetchData">
                                <el-radio-button label="成功数" value="true"/>
                                <el-radio-button label="失败数" value="false"/>
                                </el-radio-group>
                                </el-col>
                                <el-col :span="8">
                                    <el-button type="primary" @click="fetchData" >刷新</el-button>
                                </el-col>
                                
                            </el-row>
                           
                            <el-table :data="statsData" v-loading="loading" style="width: 100%">
                                <el-table-column prop="date" label="日期" width="180">
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
                </el-col>
                <el-col  :span="16">
                    <el-card style="margin-top: 20px;height: 620px;">
                        <template #header>
                            <span>当前模型参数</span>
                        </template>
                        <el-descriptions :column="2" label-width="15%" border>
                            <template #extra>
                                <el-button type="primary" @click="getAvatarParameters" style="float: right;">获取模型参数</el-button>
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
                        <el-table :data="data.avatarParameters" style="width: 100%;height: 350px;" border stripe empty-text="请点击上方按钮获取模型参数">
                        <el-table-column prop="name" label="参数名称" width="180" />
                        <el-table-column prop="path" label="参数路径"  />
                        <el-table-column prop="type" label="参数类型" />
                        </el-table>
                    </el-card>
                </el-col>
            </el-row>
        <el-card style="margin-top: 20px;height: 620px;">
            <template #header>
                <span>自定义脚本配置</span>
            </template>
            <el-row  :gutter="5">
                <el-col  :span="6">
                    
                    <h5 class="mb-2">自定义脚本目录</h5>
                    <el-menu
                        default-active="1"
                        class="el-menu-vertical-demo"
                        @open="handleOpen"
                        @close="handleClose"
                    >
                    <el-scrollbar height="420px">
                        <el-menu-item v-for="(item, index) in data.config.scripts" :index="index" :key="index" @click="data.local.scriptClick=index">
                        <span>{{ item.action }}</span>
                        </el-menu-item>
                    </el-scrollbar>
                    </el-menu>
                    <el-button-group class="ml-4">
                            <el-button type="primary" @click="addScriptItem">添加脚本</el-button>

                            <el-button type="danger" @click="removeScriptItem" >删除选定脚本</el-button>
                        </el-button-group>


                </el-col>

                <el-col  :span="9">
                    <el-card style="height: 500px;">
                        <template #header>
                            <span>自定义脚本名称与关键词</span>
                        </template>

                        <el-form label-width="auto">
                        <el-form-item label="自定义脚本名称" >
                            <el-input v-model="data.config.scripts[data.local.scriptClick].action" placeholder="请输入名称"></el-input>
                        </el-form-item>

                        <el-button type="primary" @click="addCustomItem" style="margin-left: 70%;margin-bottom: 20px;">添加关键词</el-button>

                        <el-scrollbar height="320px">
                        <el-form-item v-for="(item, index) in data.config.scripts[data.local.scriptClick].text" :key="index" :label="'关键词' + (index + 1)">
                            <div>
                                <el-row :gutter="20">
                                    <el-col :span="18"><el-input v-model="data.config.scripts[data.local.scriptClick].text[index]"  placeholder="请输入文本"></el-input></el-col>
                                    <el-col :span="6"><el-button type="danger" :icon="Delete" circle @click="removeCustomItem(index)"/></el-col>
                                
                                
                                </el-row>
                            </div>

                        </el-form-item>
                        </el-scrollbar>
                    </el-form>
                    </el-card>

                </el-col>
                <el-col  :span="9">
                    <el-card style="height: 500px;">
                        <template #header>
                                <span>自定义脚本执行动作</span>
                        </template>
                        <el-scrollbar height="400px">
                            <el-descriptions
                                v-for="(item, index) in data.config.scripts[data.local.scriptClick].vrcActions"
                                class="margin-top"
                                :title="'动作' + (index + 1)"
                                :column="1"
                                border
                                :key="index"
                            >
                                <template #extra>
                                    <el-button-group class="ml-4">
                                        <el-button v-if="index==(data.config.scripts[data.local.scriptClick].vrcActions.length-1)" type="primary" :icon="Plus" @click="addActionItem"/>
                                        <el-button type="danger" :icon="Delete"  @click="removeActionItem(index)"/>
                                    </el-button-group>

                                </template>
                                <el-descriptions-item>
                                    <template #label>
                                        VRC参数路径
                                    </template>
                                    <el-tooltip
                                        class="box-item"
                                        effect="dark"
                                        content="推荐从下方模型参数中复制参数路径"
                                        placement="right"
                                    >
                                    <el-input v-model="item.vrcPath" placeholder="请输入VRC参数路径"/>
                                    </el-tooltip>
                                    
                                </el-descriptions-item>
                                <el-descriptions-item>
                                    <template #label>
                                        VRC参数值
                                    </template>
                                    <el-input v-model="item.vrcValue" placeholder="请输入VRC参数值"/>
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
        </el-main>  
        <el-aside width="10%">
            <sideInfo/>
        </el-aside>
      </el-container>

    </el-container>

    <el-dialog
            v-model="dialogVisible"
            title="有新的可用升级"
            style="text-align: left;"
        >
        
            <h1>可升级至 {{data.local.updateInfo.version}}</h1>
            <h2>更新日志：</h2>
            <el-scrollbar height="400px" wrap-style="border: 1px solid black;">
            <div v-html="mdhtml" ></div>
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
import { marked } from 'marked';
import sideInfo from './side-info.vue'
import axios from 'axios';
import { ElMessage ,ElMessageBox} from 'element-plus'
import {
  Delete,Plus
} from '@element-plus/icons-vue'
import { onMounted, reactive,ref,watch,computed } from 'vue';

const dialogVisible = ref(false)
const captureName=ref([]);

const micName=ref([]);
const outputName=ref([]);
let data=reactive({
    local:{
                defaultScriptsAction:'sendText',
                item1:'',
                scriptClick:0,
                micName:[],
                updateInfo:{},
                markdownContent:''
            },
    config:{
                userInfo: {
                username: "testuser",
                password: "abc123!"
                },
                baseurl: "https://whisper.boyqiu001.cn:7070",
                'osc-port': 9000,
                'osc-ip': "127.0.0.1",
                defaultMode: "control",
                exitText: "关闭语音助手",
                activateText: "",
                stopText: "",
                sourceLanguage: "zh",
                targetTranslationLanguage: "en",
                Separate_Self_Game_Mic:0,
                translationServer: "whisper",
                defaultScripts: [
                    {
                        "action": "sendText",
                        "text": [
                            "切换到文字发送模式",
                            "到文字发送模式",
                            "文字发送"
                        ]
                    },
                    {
                        "action": "changToTrans",
                        "text": [
                            "切换到翻译模式",
                            "到翻译模式"
                        ]
                    },
                    {
                        "action": "changToControl",
                        "text": [
                            "切换到控制模式",
                            "到控制模式"
                        ]
                    },
                    {
                        "action": "changToEnglish",
                        "text": [
                            "切换到英语翻译"
                        ]
                    },
                    {
                        "action": "changTojapanese",
                        "text": [
                            "切换到日语翻译"
                        ]
                    },
                    {
                        "action": "changToRussian",
                        "text": [
                            "切换到俄语翻译"
                        ]
                    },
                    {
                        "action": "changToKorean",
                        "text": [
                            "切换到韩语翻译"
                        ]
                    }
                ],
                scripts: [{
            "action": "toggle Mic",
            "text": [
                "切换麦克风",
                "切換麥克風"
            ],
            "vrcActions": [
                {
                    "vrcPath": "/input/Voice",
                    "vrcValue": 0,
                    "vrcValueType": "bool",
                    "sleeptime": 0.1
                },
                {
                    "vrcPath": "/input/Voice",
                    "vrcValueType": "bool",
                    "vrcValue": 1
                },
                {
                    "vrcPath": "/input/Voice",
                    "vrcValueType": "bool",
                    "vrcValue": 0
                }
            ]
        },
        {
            "action": "blackCloth",
            "text": [
                "黑色衣服"
            ],
            "vrcActions": [
                {
                    "vrcPath": "/avatar/parameters/Change_material",
                    "vrcValueType": "float",
                    "vrcValue": 0
                }
            ]
        }]
            },
    avatarParameters:[],
    avatarInfo:{
        "avatarID": "",
        "avatarName": "",
        "filePath": ""
    }
})
const mdhtml=computed(()=>marked(data.local.markdownContent))

const statsData = ref([])
const loading = ref(true)
const error = ref(null)
const counter_mode= ref("true")

onMounted(()=>{
    getconfig()
    fetchData()
    getUpdate()
})

const getCapture=()=>{
    axios.get('/api/getcapture',{params:{'Separate_Self_Game_Mic':data.config.Separate_Self_Game_Mic}}).then(response => {
        captureName.value = response.data;
        ElMessage({
        message: '桌面音频名称获取成功',
        type: 'success',
        })
    });

}
const getUpdate=()=>{
    axios.get('/api/getUpdate').then(response => {
        if(response.status==200){
            data.local.updateInfo = response.data.info;
            dialogVisible.value=true
            data.local.markdownContent = response.data.changelog
        }
        

    });

}
const upgrade=()=>{
    axios.get('/api/upgrade').then(response => {
                    if(response.status==401){
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
    const response = await axios.get('/api/stats',{params:{'mode':counter_mode.value}})
    statsData.value = response.data//.reverse()  转为日期升序排列
  } catch (err) {
    error.value = `数据加载失败: ${err.message}`
  } finally {
    loading.value = false
  }
}
watch(()=>data.config.Separate_Self_Game_Mic,()=>{getCapture()})
function getconfig() {
    axios.get('/api/getConfig').then(response => {
        data.config = response.data;
        ElMessage({
        message: '配置信息获取成功',
        type: 'success',
    })
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
function saveconfig(){
    axios.post('/api/saveConfig',{'config':data.config},{headers: {
    'Content-Type': 'application/json'
  }}).then(        ElMessage({
        message: '配置信息保存成功',
        type: 'success',
    }))
}
function saveAndBoot(){
    saveconfig()
    reboot()
}
function reboot(){
    axios.get('/api/reboot')
}
function  addItem() {
    data.config.defaultScripts.find(item => item.action == data.local.defaultScriptsAction).text.push('');
}
function  addCustomItem() {
    data.config.scripts[data.local.scriptClick].text.push('');
}
function removeItem(index) {
    data.config.defaultScripts.find(item => item.action == data.local.defaultScriptsAction).text.splice(index, 1);
}
function removeCustomItem(index) {
    data.config.scripts[data.local.scriptClick].text.splice(index, 1);
}
function addActionItem(){
    data.config.scripts[data.local.scriptClick].vrcActions.push({
                    "vrcPath": "",
                    "vrcValue": 0,
                    "vrcValueType": "bool",
                    "sleeptime": 0.1
                })
}

function removeActionItem(index){
    data.config.scripts[data.local.scriptClick].vrcActions.splice(index, 1);
}
function addScriptItem(){
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
function removeScriptItem(){
    const index=data.local.scriptClick
    ElMessageBox.confirm(
    '请确认是否删除自定义脚本:'+ data.config.scripts[index]['action'],
    'Warning',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    }
  )
    .then(() => {
        if(index==0 && data.config.scripts.length==1){
        data.config.scripts[0]={
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
    else{
        data.local.scriptClick=index==0?0:index-1
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
function getAvatarParameters(){
    axios.get('/api/getAvatarParameters').then(response => {
        data.avatarParameters=response.data.dataTable
        data.avatarInfo=response.data.avatarInfo
    });
}

</script>

<style scoped>
.info-container {
  padding: 20px;
  font-size: 14px; /* 可以根据需要调整字体大小 */
  line-height: 1.5; /* 调整行高以增加可读性 */
}
 
.info-container p {
  margin: 10px 0; /* 调整段落之间的间距 */
}
</style>

