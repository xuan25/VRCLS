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
                    <el-card style="height: 400px;">
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
                                </el-select>
                            </el-form-item>
                            <el-form-item label="程序退出文本">
                                <el-input v-model="data.config.exitText"></el-input>
                            </el-form-item>
                        </el-form>
                    </el-card>
                </el-col>
                <el-col :span="8">
                    <el-card style="height: 400px;">
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
                    <el-card style="height: 400px;">
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
                scriptClick:0
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

