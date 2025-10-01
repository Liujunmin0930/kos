// 最终完整版：加入经纬度数据用于助推器返回
CLEARSCREEN.

SET csvFile TO "YZ1.csv".
PRINT "CSV文件: " + csvFile.
// 包含经纬度的完整数据列
LOG "Time,Altitude,Speed,Mass,Stage_CH4,Stage_LOX,Stage_CH4_Pct,Stage_LOX_Pct,Max_Thrust,Available_Thrust,TWR,Pitch,Yaw,Roll,Apoapsis,Periapsis,Orbital_Speed,Time_to_Ap,Dynamic_Pressure,Current_Pressure,Throttle,SAS,RCS,Gear,Current_Lat,Current_Lng,Launch_Lat,Launch_Lng" TO csvFile.

PRINT "星舰完整数据监控(含经纬度)启动...".
PRINT "按Ctrl+C停止".

// 记录发射台经纬度（程序启动时的位置）
SET launch_lat TO ROUND(SHIP:GEOPOSITION:LAT, 6).
SET launch_lng TO ROUND(SHIP:GEOPOSITION:LNG, 6).
PRINT "发射台位置: " + launch_lat + "°N, " + launch_lng + "°E".
PRINT "".

UNTIL FALSE {
    SET t TO ROUND(TIME:SECONDS, 1).
    SET h TO ROUND(SHIP:ALTITUDE, 0).
    SET vel TO ROUND(SHIP:VELOCITY:SURFACE:MAG, 0).
    SET m TO ROUND(SHIP:MASS, 2).
    
    // 燃料数据 (保持完全不变的成功代码)
    SET stage_ch4 TO 0.
    SET stage_lox TO 0.
    SET stage_ch4_cap TO 0.
    SET stage_lox_cap TO 0.
    
    FOR res IN STAGE:RESOURCES {
        IF res:NAME = "CooledLqdMethane" { 
            SET stage_ch4 TO res:AMOUNT.
            SET stage_ch4_cap TO res:CAPACITY.
        }
        IF res:NAME = "CooledLqdOxygen" { 
            SET stage_lox TO res:AMOUNT.
            SET stage_lox_cap TO res:CAPACITY.
        }
    }
    
    SET stage_ch4_pct TO 0.
    SET stage_lox_pct TO 0.
    IF stage_ch4_cap > 0 { SET stage_ch4_pct TO ROUND(100 * stage_ch4 / stage_ch4_cap, 1). }
    IF stage_lox_cap > 0 { SET stage_lox_pct TO ROUND(100 * stage_lox / stage_lox_cap, 1). }
    
    // 推力数据 (保持完全不变的成功代码)
    SET max_thrust TO ROUND(SHIP:MAXTHRUST, 1).
    SET avail_thrust TO ROUND(SHIP:AVAILABLETHRUST, 1).
    SET twr TO 0.
    IF m > 0 { SET twr TO ROUND(max_thrust / (m * 9.81), 2). }
    
    // 姿态数据 (保持完全不变的成功代码)
    SET pitch TO ROUND(90 - VANG(SHIP:UP:VECTOR, SHIP:FACING:VECTOR), 1).
    SET yaw TO ROUND(SHIP:FACING:YAW, 1).
    SET roll TO ROUND(SHIP:FACING:ROLL, 1).
    
    // 轨道数据 (保持完全不变的成功代码)
    SET ap_alt TO ROUND(SHIP:ORBIT:APOAPSIS, 0).
    SET pe_alt TO ROUND(SHIP:ORBIT:PERIAPSIS, 0).
    SET orbital_vel TO ROUND(SHIP:VELOCITY:ORBIT:MAG, 1).
    SET eta_ap TO ROUND(SHIP:ORBIT:ETA:APOAPSIS, 1).
    
    // 大气数据 (保持完全不变的成功代码)
    SET dynamic_pressure TO ROUND(SHIP:Q, 3).
    
    // 压力计算 (保持完全不变的成功代码)
    SET sea_level_pressure TO 1.0.
    SET scale_height TO 8400.
    SET pressure_ratio TO h / scale_height.
    
    SET current_pressure TO sea_level_pressure.
    IF pressure_ratio < 0.1 {
        SET current_pressure TO sea_level_pressure * (1 - pressure_ratio + pressure_ratio^2/2).
    } ELSE IF pressure_ratio < 1 {
        SET current_pressure TO sea_level_pressure * (1 - pressure_ratio + pressure_ratio^2/2 - pressure_ratio^3/6).
    } ELSE IF pressure_ratio < 3 {
        SET current_pressure TO sea_level_pressure / (1 + pressure_ratio + pressure_ratio^2/2).
    } ELSE {
        SET current_pressure TO 0.001.
    }
    SET current_pressure TO ROUND(current_pressure, 6).
    
    // 控制状态数据 (保持完全不变的成功代码)
    SET throttle_val TO ROUND(THROTTLE * 100, 1).
    SET sas_state TO SAS.
    SET rcs_state TO RCS.
    SET gear_state TO GEAR.
    
    // 新增：经纬度数据
    SET current_lat TO ROUND(SHIP:GEOPOSITION:LAT, 6).
    SET current_lng TO ROUND(SHIP:GEOPOSITION:LNG, 6).
    
    // 显示 (新增经纬度信息)
    PRINT "=== 星舰完整数据监控(含经纬度) ===        " AT (0,4).
    PRINT "级数: " + STAGE:NUMBER + "  时间: " + t + "s            " AT (0,5).
    PRINT "高度: " + h + "m  速度: " + vel + "m/s          " AT (0,6).
    PRINT "质量: " + m + "t  推重比: " + twr + "              " AT (0,7).
    PRINT "姿态: 俯仰" + pitch + "° 偏航" + yaw + "° 滚转" + roll + "°                    " AT (0,8).
    PRINT "轨道: Ap" + ap_alt + "m Pe" + pe_alt + "m 轨道速度" + orbital_vel + "m/s                    " AT (0,9).
    PRINT "大气: 动压" + dynamic_pressure + "kPa 压力" + current_pressure + "atm                    " AT (0,10).
    PRINT "控制: 油门" + throttle_val + "% SAS:" + sas_state + " RCS:" + rcs_state + " 起落架:" + gear_state + "                    " AT (0,11).
    PRINT "位置: " + current_lat + "°N " + current_lng + "°E (发射台:" + launch_lat + "°N " + launch_lng + "°E)                    " AT (0,12).
    PRINT "当前级 CH4: " + stage_ch4_pct + "% (" + ROUND(stage_ch4,0) + "/" + ROUND(stage_ch4_cap,0) + ")            " AT (0,13).
    PRINT "当前级 LOX: " + stage_lox_pct + "% (" + ROUND(stage_lox,0) + "/" + ROUND(stage_lox_cap,0) + ")            " AT (0,14).
    PRINT "推力: " + max_thrust + "kN (可用: " + avail_thrust + "kN)                 " AT (0,15).
    
    // 记录到CSV (新增经纬度数据)
    LOG t + "," + h + "," + vel + "," + m + "," + ROUND(stage_ch4,0) + "," + ROUND(stage_lox,0) + "," + stage_ch4_pct + "," + stage_lox_pct + "," + max_thrust + "," + avail_thrust + "," + twr + "," + pitch + "," + yaw + "," + roll + "," + ap_alt + "," + pe_alt + "," + orbital_vel + "," + eta_ap + "," + dynamic_pressure + "," + current_pressure + "," + throttle_val + "," + sas_state + "," + rcs_state + "," + gear_state + "," + current_lat + "," + current_lng + "," + launch_lat + "," + launch_lng TO csvFile.
    
    WAIT 0.5.
}
