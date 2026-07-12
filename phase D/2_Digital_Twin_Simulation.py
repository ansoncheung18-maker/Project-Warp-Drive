# -*- coding: utf-8 -*-
"""
Project Warp Drive - Phase D
數位雙生模擬 (Digital Twin Simulation) - 修正版 v3.0
作者: Anson Cheung (14歲)
日期: 2026-07-11

修正內容:
  - 修正 while 循環條件，等佢可以喺曲率泡形成之前就開始執行
  - 加入更清晰嘅進度顯示
"""

import math
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# ============================================================
# 1. 設定中文字體
# ============================================================
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

print("=" * 70)
print("Project Warp Drive - Phase D")
print("數位雙生模擬 (Digital Twin Simulation) - 修正版 v3.0")
print(f"執行日期: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
print("=" * 70)


# ============================================================
# 2. 參數設定
# ============================================================

print("\n[1] 系統參數設定:")
print("-" * 70)

CASIMIR_OUTPUT = 1.66e36  # J/s
STORAGE_CAPACITY = CASIMIR_OUTPUT * 24 * 3600
STORAGE_EFFICIENCY = 0.99
BUBBLE_FORMATION_THRESHOLD = 0.80
BUBBLE_STABILITY_TARGET = 0.95

AI_MONITOR_FREQ = 9.914e9
AI_RESPONSE_TIME = 0.49e-9
AI_MONITOR_JITTER = 0.05

SHIELDING_EFFICIENCY = 0.9975
HAWKING_RADIATION = 2.59e-34

DISTANCE_LY = 100
TARGET_SPEED_C = 1500
MAX_SPEED_C = 3000
LIGHT_SPEED = 3e8
SECONDS_PER_DAY = 24 * 3600
SECONDS_PER_YEAR = 365 * SECONDS_PER_DAY

DT = 10.0  # 秒/步

print(f"  Casimir 陣列產能: {CASIMIR_OUTPUT:.2e} J/s")
print(f"  儲存環容量: {STORAGE_CAPACITY:.2e} J")
print(f"  儲存效率: {STORAGE_EFFICIENCY*100}%")
print(f"  曲率泡成形門檻: {BUBBLE_FORMATION_THRESHOLD*100}%")
print(f"  AI 監測頻率: {AI_MONITOR_FREQ/1e9:.3f} GHz")
print(f"  AI 反應時間: {AI_RESPONSE_TIME*1e9:.2f} ns")
print(f"  場腔屏蔽效率: {SHIELDING_EFFICIENCY*100:.2f}%")
print(f"  目標速度: {TARGET_SPEED_C} c")
print(f"  時間步長: {DT} 秒")


# ============================================================
# 3. 數位雙生模擬類 (修正版 v3.0)
# ============================================================

class DigitalTwin:
    def __init__(self, config):
        self.config = config
        self.reset()
    
    def reset(self):
        self.stored_energy = 0.0
        self.total_generated = 0.0
        self.total_consumed = 0.0
        
        self.bubble_formed = False
        self.bubble_radius = 0.0
        self.bubble_stability = 0.0
        self.bubble_speed = 0.0
        self.bubble_formation_time = 0.0
        
        self.distance_traveled = 0.0
        self.current_time = 0.0
        self.mission_complete = False
        
        self.ai_events = 0
        self.ai_failures = 0
        self.storage_phase_complete = False
        self.formation_attempted = False
        
        self.history = {
            'time': [],
            'stored_energy': [],
            'bubble_speed': [],
            'bubble_stability': [],
            'distance': [],
            'ai_response_time': [],
            'hawking_radiation': [],
        }
        
        self.faults = {
            'casimir_degradation': 0.0,
            'storage_leak': 0.0,
            'ai_delay': 0.0,
            'shielding_degradation': 0.0,
        }
    
    def set_fault(self, fault_type, value):
        if fault_type in self.faults:
            self.faults[fault_type] = min(1.0, max(0.0, value))
    
    def generate_negative_energy(self, dt):
        output = CASIMIR_OUTPUT * dt
        output *= (1 - self.faults['casimir_degradation'] * 0.5)
        output *= (1 + np.random.normal(0, 0.05))
        return max(0, output)
    
    def store_energy(self, energy):
        stored = energy * STORAGE_EFFICIENCY
        stored *= (1 - self.faults['storage_leak'] * 0.1)
        
        if self.stored_energy + stored > STORAGE_CAPACITY:
            stored = STORAGE_CAPACITY - self.stored_energy
        
        self.stored_energy += stored
        self.total_generated += energy
        return stored
    
    def consume_energy(self, power, dt):
        energy_needed = power * dt
        
        if self.faults['ai_delay'] > 0:
            waste = energy_needed * self.faults['ai_delay'] * 0.1
            energy_needed += waste
        
        if self.stored_energy >= energy_needed:
            self.stored_energy -= energy_needed
            self.total_consumed += energy_needed
            return True
        else:
            return False
    
    def calculate_bubble_power(self, speed_c):
        BASE_POWER = 1.0e10
        power = BASE_POWER * speed_c
        
        hawking = HAWKING_RADIATION * (1 - SHIELDING_EFFICIENCY)
        if self.faults['shielding_degradation'] > 0:
            hawking *= (1 + self.faults['shielding_degradation'] * 10)
        
        return power + hawking
    
    def update_ai(self, dt):
        self.ai_events += 1
        response = AI_RESPONSE_TIME * (1 + np.random.normal(0, AI_MONITOR_JITTER))
        
        if self.faults['ai_delay'] > 0:
            response *= (1 + self.faults['ai_delay'] * 10)
        
        if response > 1e-6:
            self.ai_failures += 1
            return False
        
        self.history['ai_response_time'].append(response)
        return True
    
    def check_bubble_stability(self, speed_c):
        stability = 1.0
        stability -= (speed_c / MAX_SPEED_C) * 0.05
        
        if self.ai_failures > 10:
            stability -= 0.1
        
        energy_ratio = self.stored_energy / STORAGE_CAPACITY
        stability += (energy_ratio - 0.5) * 0.05
        
        hawking_power = HAWKING_RADIATION * (1 - SHIELDING_EFFICIENCY)
        if self.faults['shielding_degradation'] > 0:
            hawking_power *= (1 + self.faults['shielding_degradation'] * 10)
        stability -= hawking_power * 1e33
        
        stability = max(0.0, min(1.0, stability))
        return stability
    
    def step(self, dt, speed_c):
        # 1. 產生負能量
        generated = self.generate_negative_energy(dt)
        self.store_energy(generated)
        
        # 2. 檢查儲存進度 (只顯示一次)
        if not self.storage_phase_complete:
            energy_ratio = self.stored_energy / STORAGE_CAPACITY
            if energy_ratio >= BUBBLE_FORMATION_THRESHOLD:
                self.storage_phase_complete = True
                print(f"\n  ✅ 儲存階段完成！時間: {self.current_time/3600:.2f} 小時")
                print(f"     儲存能量: {self.stored_energy:.2e} J")
                print(f"     能量比例: {energy_ratio*100:.1f}%")
        
        # 3. 如果儲存完成但曲率泡未形成，開始形成
        if self.storage_phase_complete and not self.bubble_formed:
            self.bubble_formed = True
            self.bubble_formation_time = self.current_time
            self.bubble_radius = 500.0
            print(f"\n  ✅ 曲率泡形成！時間: {self.current_time/3600:.2f} 小時")
        
        # 4. 航行
        if self.bubble_formed and not self.mission_complete:
            bubble_power = self.calculate_bubble_power(speed_c)
            energy_sufficient = self.consume_energy(bubble_power, dt)
            ai_ok = self.update_ai(dt)
            self.bubble_stability = self.check_bubble_stability(speed_c)
            
            if not energy_sufficient or self.bubble_stability < 0.5 or not ai_ok:
                self.bubble_formed = False
                return False
            
            distance_per_sec = speed_c * LIGHT_SPEED / (SECONDS_PER_YEAR * LIGHT_SPEED)
            self.distance_traveled += distance_per_sec * dt
            
            if self.distance_traveled >= DISTANCE_LY:
                self.mission_complete = True
                print(f"\n  🎉 旅程完成！時間: {self.current_time/3600:.2f} 小時")
                print(f"     行駛距離: {self.distance_traveled:.2f} 光年")
        
        # 5. 更新歷史
        self.current_time += dt
        self.history['time'].append(self.current_time)
        self.history['stored_energy'].append(self.stored_energy)
        self.history['bubble_speed'].append(self.bubble_speed if self.bubble_formed else 0)
        self.history['bubble_stability'].append(self.bubble_stability)
        self.history['distance'].append(self.distance_traveled)
        
        hawking = HAWKING_RADIATION * (1 - SHIELDING_EFFICIENCY)
        if self.faults['shielding_degradation'] > 0:
            hawking *= (1 + self.faults['shielding_degradation'] * 10)
        self.history['hawking_radiation'].append(hawking)
        
        return True
    
    def run_mission(self, speed_c, max_steps=500000):
        print(f"\n[2] 執行任務 (速度: {speed_c} c):")
        print("-" * 70)
        
        self.reset()
        step_count = 0
        
        travel_time_days = (DISTANCE_LY * SECONDS_PER_YEAR) / speed_c / SECONDS_PER_DAY
        storage_time_days = STORAGE_CAPACITY * BUBBLE_FORMATION_THRESHOLD / (CASIMIR_OUTPUT * SECONDS_PER_DAY)
        print(f"   預計航行時間: {travel_time_days:.2f} 日")
        print(f"   預計儲存時間: {storage_time_days:.6f} 日 ({storage_time_days*24:.6f} 小時)")
        
        # 修正: while 條件唔好要求 bubble_formed
        while not self.mission_complete and step_count < max_steps:
            success = self.step(DT, speed_c)
            step_count += 1
            
            if not success:
                break
            
            # 顯示進度 (每 5000 步)
            if step_count % 5000 == 0:
                days = self.current_time / SECONDS_PER_DAY
                if self.bubble_formed:
                    progress = self.distance_traveled / DISTANCE_LY * 100
                    print(f"   {days:.4f} 日: 進度 {progress:.1f}%, 穩定性 {self.bubble_stability:.3f}")
                else:
                    energy_ratio = self.stored_energy / STORAGE_CAPACITY * 100
                    print(f"   {days:.4f} 日: 儲存中... {energy_ratio:.1f}%")
        
        if step_count >= max_steps and not self.mission_complete:
            print(f"\n  ⚠️ 達到最大模擬步數 ({max_steps})，終止模擬")
        
        return self.mission_complete


# ============================================================
# 4. 執行模擬
# ============================================================

twin = DigitalTwin({})

# ============================================================
# 情景 1：正常航行 (1,500c)
# ============================================================

print("\n" + "=" * 70)
print("[情景 1] 正常航行 (1,500c)")
print("=" * 70)

success = twin.run_mission(1500, max_steps=500000)

if success:
    print(f"\n✅ 任務成功！")
    print(f"   總時間: {twin.current_time / SECONDS_PER_DAY:.2f} 日")
    print(f"   總能量消耗: {twin.total_consumed:.2e} J")
    print(f"   最終穩定性: {twin.bubble_stability:.3f}")
else:
    print(f"\n❌ 任務失敗")
    print(f"   行駛距離: {twin.distance_traveled:.2f} 光年")
    if not twin.storage_phase_complete:
        print(f"   原因: 儲存階段未完成 (能量不足)")
    else:
        print(f"   原因: 曲率泡崩塌")

# ============================================================
# 情景 5：蒙特卡羅模擬 (10 次)
# ============================================================

print("\n" + "=" * 70)
print("[情景 5] 蒙特卡羅模擬 (10 次, 1,500c)")
print("=" * 70)

success_count = 0
failure_count = 0

for i in range(10):
    twin.reset()
    success = twin.run_mission(1500, max_steps=500000)
    
    if success:
        success_count += 1
    else:
        failure_count += 1

success_rate = success_count / 10 * 100

print(f"\n📊 蒙特卡羅結果 (10 次):")
print(f"   成功率: {success_rate:.1f}%")
print(f"   成功次數: {success_count}")
print(f"   失敗次數: {failure_count}")

# ============================================================
# 5. 儲存結果
# ============================================================

with open("digital_twin_simulation_results.txt", "w", encoding="utf-8") as f:
    f.write("=" * 70 + "\n")
    f.write("Project Warp Drive - Phase D\n")
    f.write("數位雙生模擬結果 (修正版 v3.0)\n")
    f.write(f"執行日期: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    f.write("=" * 70 + "\n\n")
    
    f.write("[情景 1] 正常航行 (1,500c):\n")
    twin.reset()
    success = twin.run_mission(1500, max_steps=500000)
    f.write(f"  成功: {'是' if success else '否'}\n")
    if success:
        f.write(f"  航行時間: {twin.current_time / SECONDS_PER_DAY:.2f} 日\n")
    else:
        f.write(f"  行駛距離: {twin.distance_traveled:.2f} 光年\n")
    f.write("\n")
    
    f.write("[情景 5] 蒙特卡羅 (10 次):\n")
    f.write(f"  成功率: {success_rate:.1f}%\n")
    f.write("=" * 70 + "\n")

print("\n[結果] 已儲存至: digital_twin_simulation_results.txt")

print("\n" + "=" * 70)
print("Phase D 數位雙生模擬完成！🚀")
print("=" * 70)
