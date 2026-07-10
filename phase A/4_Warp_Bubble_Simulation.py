# -*- coding: utf-8 -*-
"""
Project Warp Drive - Phase A
曲率泡現實能量需求模擬 (保守版 v6.0)
作者: Anson Cheung (14歲)
日期: 2026-07-10

目標: 基於物理限制,模擬現實可行嘅曲率泡航行
      - 速度上限: 3,000 c (保守)
      - 考慮加速/巡航/減速模式
      - 計算不同儲存時間下嘅可行距離
      - 強調「現實可行」而唔係「理論極限」
"""

import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# ============================================================
# 1. 設定中文字體
# ============================================================
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

print("=" * 70)
print("曲率泡現實能量需求模擬 (保守版 v6.0)")
print(f"執行日期: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
print("=" * 70)

# ============================================================
# 2. 參數設定 (保守)
# ============================================================

print("\n[1] 參數設定 (保守):")
print("-" * 70)

# Casimir 陣列產能 (1km³)
CASIMIR_OUTPUT = 1.66e36  # J/s

# 時間單位 (秒)
SECONDS_PER_DAY = 24 * 3600
SECONDS_PER_MONTH = 30 * SECONDS_PER_DAY
SECONDS_PER_YEAR = 365 * SECONDS_PER_DAY

# 1 日、1 月、1 年產能
ENERGY_1_DAY = CASIMIR_OUTPUT * SECONDS_PER_DAY
ENERGY_1_MONTH = CASIMIR_OUTPUT * SECONDS_PER_MONTH
ENERGY_1_YEAR = CASIMIR_OUTPUT * SECONDS_PER_YEAR

# 曲率泡基礎消耗 (1c 時)
BASE_POWER = 1.0e10  # W

# 物理限制 - 保守上限
MAX_SPEED_CONSERVATIVE = 3000  # c

# 加速/減速參數
ACCELERATION = 10  # c/s

print(f"  Casimir 陣列產能: {CASIMIR_OUTPUT:.2e} J/s")
print(f"  1 日產能: {ENERGY_1_DAY:.2e} J")
print(f"  1 月產能: {ENERGY_1_MONTH:.2e} J")
print(f"  1 年產能: {ENERGY_1_YEAR:.2e} J")
print(f"  曲率泡基礎消耗 (1c): {BASE_POWER:.2e} W")
print(f"  ⚠️ 速度上限 (保守): {MAX_SPEED_CONSERVATIVE} c")
print(f"  加速度: {ACCELERATION} c/s")

# ============================================================
# 3. 加速/巡航/減速 能量計算
# ============================================================

print("\n[2] 加速/巡航/減速 能量計算 (現實):")
print("-" * 70)

def calculate_trip_energy(max_speed_c, distance_ly, acceleration):
    """
    計算完整旅程嘅能量消耗 (現實版)
    包括: 加速段、巡航段、減速段
    """
    # 限制速度上限
    if max_speed_c > MAX_SPEED_CONSERVATIVE:
        max_speed_c = MAX_SPEED_CONSERVATIVE
    
    # 加速段時間
    accel_time = max_speed_c / acceleration
    
    # 加速段距離
    accel_distance_m = 0.5 * acceleration * 3.0e8 * accel_time**2
    accel_distance_ly = accel_distance_m / (SECONDS_PER_YEAR * 3.0e8)
    
    # 減速段 (同加速段對稱)
    decel_time = accel_time
    decel_distance_ly = accel_distance_ly
    
    # 巡航段距離
    cruise_distance_ly = distance_ly - accel_distance_ly - decel_distance_ly
    
    if cruise_distance_ly <= 0:
        max_reachable = np.sqrt(distance_ly * acceleration / 2)
        actual_max_speed = min(max_reachable, max_speed_c)
        
        accel_time = actual_max_speed / acceleration
        accel_distance_m = 0.5 * acceleration * 3.0e8 * accel_time**2
        accel_distance_ly = accel_distance_m / (SECONDS_PER_YEAR * 3.0e8)
        decel_time = accel_time
        decel_distance_ly = accel_distance_ly
        cruise_distance_ly = 0
        cruise_time = 0
    else:
        actual_max_speed = max_speed_c
        cruise_time = cruise_distance_ly * SECONDS_PER_YEAR / actual_max_speed
    
    # 能量消耗
    avg_speed_accel = actual_max_speed / 2
    accel_power_avg = BASE_POWER * avg_speed_accel
    accel_energy = accel_power_avg * accel_time
    
    decel_power_avg = BASE_POWER * avg_speed_accel
    decel_energy = decel_power_avg * decel_time
    
    cruise_power = BASE_POWER * actual_max_speed
    cruise_energy = cruise_power * cruise_time
    
    total_energy = accel_energy + cruise_energy + decel_energy
    
    return {
        'max_speed': actual_max_speed,
        'accel_time': accel_time,
        'accel_distance_ly': accel_distance_ly,
        'cruise_time': cruise_time,
        'cruise_distance_ly': cruise_distance_ly,
        'decel_time': decel_time,
        'decel_distance_ly': decel_distance_ly,
        'total_time': accel_time + cruise_time + decel_time,
        'total_energy': total_energy,
        'accel_energy': accel_energy,
        'cruise_energy': cruise_energy,
        'decel_energy': decel_energy,
    }

# ============================================================
# 4. 主程式
# ============================================================

# 測試不同速度 (100 光年)
print("\n[3] 不同速度下嘅能量需求 (100 光年):")
print("-" * 70)

test_speeds = [100, 500, 1000, 1500, 2000, 2500, 3000]

print("| 速度 (c) | 最高速度 | 航行時間 | 總能量 | 需儲存時間 | 可行性 |")
print("|:---|:---|:---|:---|:---|:---|")

for speed in test_speeds:
    result = calculate_trip_energy(speed, 100, ACCELERATION)
    travel_time_days = result['total_time'] / SECONDS_PER_DAY
    days_needed = result['total_energy'] / (CASIMIR_OUTPUT * SECONDS_PER_DAY)
    
    if speed <= 1500:
        feasibility = "✅ 可行 (穩定)"
    elif speed <= 3000:
        feasibility = "✅ 可行 (保守)"
    else:
        feasibility = "⚠️ 理論極限"
    
    print(f"| {speed} | {result['max_speed']:.0f} c | {travel_time_days:.2f} 日 | {result['total_energy']:.2e} J | {days_needed:.2e} 日 | {feasibility} |")

# ============================================================
# 5. 實際星際航行場景
# ============================================================

print("\n[4] 實際星際航行場景 (保守速度 3,000c):")
print("-" * 70)

destinations = [
    {"name": "比鄰星 (Proxima Centauri)", "distance": 4.24},
    {"name": "織女星 (Vega)", "distance": 26},
    {"name": "獵戶座星雲 (Orion Nebula)", "distance": 1344},
    {"name": "銀河系中心 (Galactic Center)", "distance": 26000},
    {"name": "仙女座星系 (Andromeda)", "distance": 2500000},
]

print("| 目的地 | 距離 (光年) | 速度 | 航行時間 | 所需能量 | 需儲存時間 |")
print("|:---|:---|:---|:---|:---|:---|")

for dest in destinations:
    distance = dest["distance"]
    result = calculate_trip_energy(3000, distance, ACCELERATION)
    
    travel_time_days = result['total_time'] / SECONDS_PER_DAY
    days_needed = result['total_energy'] / (CASIMIR_OUTPUT * SECONDS_PER_DAY)
    
    print(f"| {dest['name']} | {distance:.2e} | {result['max_speed']:.0f} c | {travel_time_days:.2f} 日 | {result['total_energy']:.2e} J | {days_needed:.2e} 日 |")

# ============================================================
# 6. 最終結論
# ============================================================

print("\n" + "=" * 70)
print("🎯 最終結論 (v6.0 - 保守版)")
print("=" * 70)

print("""
📊 現實可行嘅速度範圍:

  | 速度範圍 | 可行性 | 說明 |
  |:---|:---|:---|
  | 100 – 1,500 c | ✅ 可行 (穩定) | 能量充足,場穩定 |
  | 1,500 – 3,000 c | ✅ 可行 (保守) | 需要更多能量,仍穩定 |
  | 3,000 – 10,000 c | ⚠️ 理論極限 | 霍金輻射增加,不穩定 |
  | > 10,000 c | ❌ 不現實 | 物理限制,無法維持 |

📊 100 光年旅程 (保守速度 3,000c):

  | 儲存時間 | 航行時間 | 所需能量 | 需儲存時間 |
  |:---|:---|:---|:---|
  | 1 日 | 12.17 日 | 3.15 × 10¹⁹ J | 2.20 × 10⁻²² 日 |

📊 實際建議:

  1. 將目標速度設定為 1,500 – 3,000 c
  2. 儲存 1 日產能已足夠 100 光年內任何旅程
  3. 曲率泡大小選擇 1km (平衡容量同消耗)
  4. 採用「加速 → 巡航 → 減速」模式

🚀 最終判定:

  「基於物理限制,保守速度上限為 3,000 c。
  1 日 Casimir 產能已足夠 100 光年內任何旅程。
  能量完全唔係限制,速度同時間先係真正限制。
  Warp Drive 嘅實際用途係『鄰近星系航行』(100-1,000 光年內)。」
""")

# ============================================================
# 7. 儲存結果
# ============================================================

with open("warp_bubble_simulation_results.txt", "w", encoding="utf-8") as f:
    f.write("=" * 70 + "\n")
    f.write("曲率泡現實能量需求模擬結果 (保守版 v6.0)\n")
    f.write(f"執行日期: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    f.write("=" * 70 + "\n\n")
    f.write(f"速度上限 (保守): {MAX_SPEED_CONSERVATIVE} c\n")
    f.write("100 光年旅程 (3,000c):\n")
    result_100 = calculate_trip_energy(3000, 100, ACCELERATION)
    f.write(f"  航行時間: {result_100['total_time']/SECONDS_PER_DAY:.2f} 日\n")
    f.write(f"  所需能量: {result_100['total_energy']:.2e} J\n")
    f.write(f"  需儲存時間: {result_100['total_energy']/(CASIMIR_OUTPUT*SECONDS_PER_DAY):.2e} 日\n")
    f.write("=" * 70 + "\n")

print("\n[結果] 已儲存至: warp_bubble_simulation_results.txt")

# ============================================================
# 8. 圖表
# ============================================================

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
fig.suptitle('曲率泡現實能量需求模擬 (保守版 v6.0)', fontsize=14)

# 圖 1: 速度 vs 航行時間 (100 光年)
ax1 = axes[0]
speeds_plot = np.array([100, 500, 1000, 1500, 2000, 2500, 3000])
times_plot = []
for speed in speeds_plot:
    result = calculate_trip_energy(speed, 100, ACCELERATION)
    times_plot.append(result['total_time'] / SECONDS_PER_DAY)
ax1.plot(speeds_plot, times_plot, 'b-', linewidth=2, marker='o')
ax1.axvline(x=1500, color='g', linestyle='--', label='穩定範圍 (1,500c)')
ax1.axvline(x=3000, color='orange', linestyle='--', label='保守上限 (3,000c)')
ax1.set_xlabel('速度 (c)')
ax1.set_ylabel('航行時間 (日)')
ax1.set_title('速度 vs 航行時間 (100 光年)')
ax1.legend()
ax1.grid(True, alpha=0.3)

# 圖 2: 速度剖面圖
ax2 = axes[1]
time_profile = np.linspace(0, 1, 100)
speed_profile = []
accel_time_ratio = 0.01
decel_time_ratio = 0.01
cruise_time_ratio = 0.98

for t in time_profile:
    if t < accel_time_ratio:
        speed_profile.append(t / accel_time_ratio)
    elif t < accel_time_ratio + cruise_time_ratio:
        speed_profile.append(1.0)
    else:
        speed_profile.append(1.0 - (t - accel_time_ratio - cruise_time_ratio) / decel_time_ratio)

ax2.plot(time_profile, speed_profile, 'r-', linewidth=2)
ax2.set_xlabel('時間 (正規化)')
ax2.set_ylabel('速度 (正規化)')
ax2.set_title('加速 → 巡航 → 減速 剖面 (現實版)')
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('warp_bubble_simulation_analysis.png', dpi=150)
print("[圖表] 已儲存至: warp_bubble_simulation_analysis.png")

print("\n" + "=" * 70)
print("模擬完成！🚀")
print("=" * 70)
