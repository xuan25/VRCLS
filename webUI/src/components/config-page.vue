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
                    <el-card style="height: 500px;">
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
                            <el-form-item label="麦克风">
                                <el-select v-model="data.config.micIndex">
                                    <el-option label="系统默认麦克风" :value="-1"></el-option>
                                    <el-option v-for="(item,index) in data.local.micName" :key="index" :label="item" :value="index"></el-option>
                                </el-select>
                            </el-form-item>
                            <el-form-item label="默认模式">
                                <el-select v-model="data.config.defaultMode">
                                    <el-option label="控制" value="control"></el-option>
                                    <el-option label="翻译" value="translation"></el-option>
                                    <el-option label="文字发送" value="text"></el-option>
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
                                    <el-option label="中文(Chinese)" value="zh"></el-option>
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
                            <el-form-item label="程序退出文本">
                                <el-input v-model="data.config.exitText"></el-input>
                            </el-form-item>
                        </el-form>
                    </el-card>
                </el-col>
                <el-col :span="8">
                    <el-card style="height: 500px;">
                        <template #header>
                            <div class="card-header">
                            <span>用户信息配置</span>
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
                </el-col>
                <el-col :span="8">
                    <el-card style="height: 500px;">
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
            <el-card style="margin-top: 20px;height: 600px;">
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
        </el-main>  
        <el-aside width="10%">
            <sideInfo/>
        </el-aside>
      </el-container>

    </el-container>
</template>

<script setup>
import sideInfo from './side-info.vue'
import axios from 'axios';
import { ElMessage ,ElMessageBox} from 'element-plus'
import {
  Delete,Plus
} from '@element-plus/icons-vue'
import { onMounted, reactive } from 'vue';

let data=reactive({
    local:{
                defaultScriptsAction:'sendText',
                item1:'',
                scriptClick:0,
                micName:[]
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




onMounted(()=>{
    getconfig()
})
function getconfig() {
    axios.get('/api/getConfig').then(response => {
        data.config = response.data;
        ElMessage({
        message: '配置信息获取成功',
        type: 'success',
    })
    });
    axios.get('/api/getMics').then(response => {
        data.local.micName = response.data;
        ElMessage({
        message: '麦克风名称获取成功',
        type: 'success',
    })
    });
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

