
def steamvr_process(logger, queue, params):
    import pythoncom
    pythoncom.CoInitializeEx(pythoncom.COINIT_MULTITHREADED)
    import time
    import openvr
    from ..module.steamvr import VRTextOverlay
    textOverlay = VRTextOverlay()
    MAX_RETRIES = 10  # 最大重试次数
    retry_count = 0
    is_two_hand=params["config"].get("SteamVRHad")==2
    def safe_shutdown():
        try:
            if textOverlay.overlay_handle:
                textOverlay.overlay.hideOverlay(textOverlay.overlay_handle)
                textOverlay.overlay.destroyOverlay(textOverlay.overlay_handle)
            # openvr.shutdown()
            logger.put({"text":"VR资源已安全释放","level":"info"})
        except Exception as e:
            logger.put({"text":f"关闭资源时出错:{str(e)}","level":"error"})

    try:
        # 带重试的初始化
        while retry_count < MAX_RETRIES and params['running']:
            try:
                if not textOverlay.initialize(logger, params):
                    raise RuntimeError("SteamVR初始化失败")
                # logger.put({"text":"SteamVR初始化成功","level":"info"})
                last_success = time.time()
                check_interval = 10  # 手柄状态检查间隔
                error_count = 0
                retry_count=0
                MAX_ERRORS = 5  # 最大连续错误次数
                textOverlay._create_text_texture()
                textOverlay.overlay.setOverlayWidthInMeters(textOverlay.overlay_handle,params["config"].get("SteamVRSize")*(1.5 if params["config"].get("Separate_Self_Game_Mic")!=0 else 1.0))
                textOverlay.overlay.showOverlay(textOverlay.overlay_handle)
                if is_two_hand:
                    textOverlay.overlay.setOverlayWidthInMeters(textOverlay.overlay_handle_1,params["config"].get("SteamVRSize")*(1.5 if params["config"].get("Separate_Self_Game_Mic")!=0 else 1.0))
                    textOverlay.overlay.showOverlay(textOverlay.overlay_handle_1)
                logger.put({"text":f"掌心显示启动完毕","level":"info"})
                # 主循环
                while params['running']:
                    try:
                        # 定期设备检查
                        if time.time() - last_success > check_interval:
                            
                            if params["config"].get("SteamVRHad") ==2:
                                current_status = textOverlay.set_overlay_to_hand(0) and textOverlay.set_overlay_to_hand(1,True)
                            else:
                                current_status = textOverlay.set_overlay_to_hand(params["config"].get("SteamVRHad"))
                                

                            if not current_status:
                                logger.put({"text":"控制器连接状态异常，尝试恢复...","level":"debug"})
                                textOverlay.overlay.hideOverlay(textOverlay.overlay_handle)
                                if is_two_hand:textOverlay.overlay.hideOverlay(textOverlay.overlay_handle_1)
                                time.sleep(1)
                                textOverlay.overlay.showOverlay(textOverlay.overlay_handle)
                                if params["config"].get("SteamVRHad") ==2:
                                    textOverlay.overlay.showOverlay(textOverlay.overlay_handle_1)
                                    status_tmp = textOverlay.set_overlay_to_hand(0) and textOverlay.set_overlay_to_hand(1,True)
                                else:
                                    status_tmp = textOverlay.set_overlay_to_hand(params["config"].get("SteamVRHad"))
                             
                                if status_tmp:
                                    last_success = time.time()
                                    logger.put({"text":"控制器连接恢复成功","level":"info"})
                                else: continue
                            else:
                                last_success = time.time()
                            
                        error=0
                        # 处理消息队列
                        if not queue.empty():
                            text = queue.get()
                            logger.put({"text":f"开始处理新的文本更新","level":"debug"})
                            
                            
                            # 带重试的更新操作
                            for _ in range(3):  # 最多重试3次
                                try:
                                    textOverlay.update_text(text)
                                    error=200
                                    break
                                except openvr.openvr.error_code.OverlayError_RequestFailed:
                                    logger.put({"text":f"[steamvr异常]OpenVR错误: {str(type(oe))}，尝试恢复初始化,{error}","level":"debug"})
                                    safe_shutdown()
                                    time.sleep(5)
                                    if not textOverlay.initialize(logger, params):
                                        raise RuntimeError("[steamvr异常]SteamVR初始化失败")
                                    time.sleep(1)
                                    textOverlay._create_text_texture()  # 重新创建纹理
                                    time.sleep(1)
                                except openvr.error_code.OverlayError as oe:
                                    error+=1
                                    logger.put({"text":f"[steamvr异常]OpenVR错误: {str(type(oe))}，尝试恢复...,{error}","level":"debug"})
                                    textOverlay._create_text_texture()  # 重新创建纹理
                                    time.sleep(1)
                                    
                            
                            # 强制更新Overlay属性
                            textOverlay.overlay.setOverlayWidthInMeters(textOverlay.overlay_handle, params["config"].get("SteamVRSize")*(1.0 if params["config"].get("Separate_Self_Game_Mic")==0 or params["config"].get("SteamVRHad") ==2 else 1.5))
                            textOverlay.overlay.setOverlayAlpha(textOverlay.overlay_handle, 1.0)
                            if params["config"].get("SteamVRHad") ==2:
                                # 强制更新Overlay属性
                                textOverlay.overlay.setOverlayWidthInMeters(textOverlay.overlay_handle_1, params["config"].get("SteamVRSize")*(1.0 if params["config"].get("Separate_Self_Game_Mic")==0 or params["config"].get("SteamVRHad") ==2 else 1.5))
                                textOverlay.overlay.setOverlayAlpha(textOverlay.overlay_handle_1, 1.0)
                        time.sleep(0.1)
                        if error ==200:error_count = 0  # 重置错误计数器

                    except Exception as inner_e:
                        error_count += 1
                        logger.put({"text":f"[steamvr异常][运行时错误] {str(type(inner_e))} ({error_count}/{MAX_ERRORS})","level":"debug"})
                        if error_count >= MAX_ERRORS:
                            logger.put({"text":"[steamvr异常]达到最大错误次数，尝试重新初始化...","level":"error"})
                            safe_shutdown()
                            time.sleep(5)
                            break  # 退出内层循环进行重新初始化

                # 正常退出循环
                if not params['running']:
                    break

            except Exception as init_e:
                retry_count += 1
                logger.put({"text":f"[steamvr异常]初始化失败 ({retry_count}/{MAX_RETRIES}): {str(type(init_e))}","level":"error"})
                safe_shutdown()
                time.sleep(5)  # 指数退避
                
        if retry_count >= MAX_RETRIES:
            logger.put({"text":"[steamvr异常]达到最大重试次数，SteamVR功能终止","level":"error"})

    except Exception as outer_e:
        logger.put({"text":f"[steamvr异常][未捕获的异常] {str(type(outer_e))}|| {str(outer_e)}","level":"error"})
    finally:
        safe_shutdown()
        # 确保释放所有VR资源
        # for _ in range(3):
        #     try:
        #         openvr.shutdown()
        #     except:
        #         pass
        #     time.sleep(1)
