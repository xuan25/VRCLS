import openvr
import time

# 初始化
vr_system = openvr.init(openvr.VRApplication_Other)
vr_input = openvr.VRInput()

# 定义动作集和动作（需与动作清单文件对应）
action_set_handle = openvr.VRActionSetHandle_t()
action_b_button = openvr.VRActionHandle_t()

# 创建动作集
vr_input.createActionSet("/actions/demo", "Demo Actions", action_set_handle)

# 创建数字动作（对应B键）
vr_input.createBooleanAction(
    action_set_handle,
    "/actions/demo/in/B_Button",
    "B Button Action",
    action_b_button
)

# 绑定按键（以Index控制器为例）
vr_input.suggestBindingsForController(
    "/user/hand/right",
    [
        (action_b_button, "/user/hand/right/input/b/click")
    ]
)

# 初始化动作数据
actions = openvr.VRActiveActionSet_t()
actions.ulActionSet = action_set_handle
actions.nPriority = 0

b_button_state = False

try:
    while True:
        # 更新动作状态
        vr_input.updateActionState([actions], openvr.k_ulInvalidActionHandle)
        
        # 获取B键状态
        action_data = openvr.InputDigitalActionData_t()
        vr_input.getDigitalActionData(
            action_b_button,
            byref(action_data),
            sizeof(action_data),
            openvr.k_ulInvalidInputValueHandle
        )
        
        if action_data.bState and not b_button_state:
            print("B键被按下！")
            b_button_state = True
        elif not action_b_data.bState and b_button_state:
            b_button_state = False
            
        time.sleep(0.015)

except KeyboardInterrupt:
    openvr.shutdown()
