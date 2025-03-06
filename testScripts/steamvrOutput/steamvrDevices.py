import openvr

def get_device_info(vr_system, index):
    if not vr_system.isTrackedDeviceConnected(index):
        return None
    
    device_class = vr_system.getTrackedDeviceClass(index)
    device_type = {
        openvr.TrackedDeviceClass_Invalid: "Invalid",
        openvr.TrackedDeviceClass_HMD: "HMD",
        openvr.TrackedDeviceClass_Controller: "Controller",
        openvr.TrackedDeviceClass_GenericTracker: "GenericTracker",
        openvr.TrackedDeviceClass_TrackingReference: "TrackingReference",
        openvr.TrackedDeviceClass_DisplayRedirect: "DisplayRedirect"
    }.get(device_class, "Unknown")

    info = {
        "index": index,
        "type": device_type,
        "model": "N/A",
        "serial": "N/A",
        "battery": "N/A",
        "role": "N/A"
    }

    # 获取设备基础信息
    try:
        info["model"] = vr_system.getStringTrackedDeviceProperty(index, openvr.Prop_ModelNumber_String)
        info["serial"] = vr_system.getStringTrackedDeviceProperty(index, openvr.Prop_SerialNumber_String)
    except openvr.OpenVRError:
        pass

    # 如果是控制器类型
    if device_class == openvr.TrackedDeviceClass_Controller:
        try:
            role = vr_system.getControllerRoleForTrackedDeviceIndex(index)
            info["role"] = {
                openvr.TrackedControllerRole_Invalid: "Invalid",
                openvr.TrackedControllerRole_LeftHand: "Left Hand",
                openvr.TrackedControllerRole_RightHand: "Right Hand"
            }.get(role, "Unknown")
        except openvr.OpenVRError:
            pass

        # 获取电池电量
        battery = vr_system.getFloatTrackedDeviceProperty(index, openvr.Prop_DeviceBatteryPercentage_Float)
        info["battery"] = f"{battery*100:.1f}%"

    return info

def main():
    try:
        openvr.init(openvr.VRApplication_Background)
        vr = openvr.VRSystem()
    except Exception as e:
        print(f"初始化失败，请确保SteamVR已运行: {str(e)}")
        return

    print("========== SteamVR设备列表 ==========")
    for i in range(openvr.k_unMaxTrackedDeviceCount):
        device = get_device_info(vr, i)
        if device and device["type"] != "Invalid":
            try:
                print(f"设备 #{device['index']}")
                print(f"类型: {device['type']}")
                print(f"型号: {device['model']}")
                print(f"序列号: {device['serial']}")
                if device["type"] == "Controller":
                    print(f"角色: {device['role']}")
                    # print(f"电量: {device['battery']}")
            except Exception as e:
                print(e)
            print("-" * 30)

    openvr.shutdown()

if __name__ == "__main__":
    import sys
    original_stdout = sys.stdout  # 备份原始输出流
    try:
        with open('vr_output.txt', 'w', encoding='utf-8') as f:
            sys.stdout = f         # 重定向标准输出到文件
            main()
    finally:
        sys.stdout = original_stdout  # 还原输出流
    input("程序执行完毕，按回车键退出...")