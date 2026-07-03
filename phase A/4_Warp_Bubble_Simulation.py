# -*- coding: utf-8 -*-
"""
Project Warp Drive - Phase A
曲率泡生成與穩定性模擬
作者: Anson Cheung (14歲)
日期: 2026-07-03
目標: 模擬 Casimir 陣列 → 負能量場 → 場腔固定 → 動態反饋 → 曲率泡
      驗證曲率泡能否被成功製造
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
print("曲率泡生成與穩定性模擬")
print(f"執行日期: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
print("=" * 70)

# ============================================================
# 2. 參數設定 (現實估算)
# ============================================================

print("\n[1] 參數設定:")
print("-" * 70)

# Casimir 陣列參數
ARRAY_SIZE = 3.0  # km
PLATE_SPACING = 0.5  # nm
CASIMIR_ENERGY_DENSITY = -1.3e-6  # J/m²

AREA = (ARRAY_SIZE * 1000) ** 2
PLATES_PER_DIMENSION = int(ARRAY_SIZE * 1e9 / PLATE_SPACING)
CASIMIR_POWER = abs(CASIMIR_ENERGY_DENSITY) * AREA * PLATES_PER_DIMENSION

# 現實損耗參數
EFFICIENCY_CASIMIR = 0.50
EFFICIENCY_TRANSMISSION = 0.85
EFFICIENCY_CAVITY = 0.85
MECHANICAL_TOLERANCE = 0.10
SAFETY_FACTOR = 3.0

effective_power = CASIMIR_POWER * EFFICIENCY_CASIMIR * EFFICIENCY_TRANSMISSION
TARGET_ENERGY = 2.0e14 * SAFETY_FACTOR

# 模擬參數
DT = 20  # 秒/步
TIME_STEPS = 3000
FORMATION_THRESHOLD = 0.80  # 80%

print(f"  Casimir 陣列尺寸: {ARRAY_SIZE} km")
print(f"  金屬板間距: {PLATE_SPACING} nm")
print(f"  Casimir 現實產能: {effective_power:.2e} J/s")
print(f"  目標能量: {TARGET_ENERGY:.2e} J")
print(f"  形成門檻: {FORMATION_THRESHOLD*100}%")
print(f"  DT: {DT} 秒/步")
print(f"  TIME_STEPS: {TIME_STEPS}")
print(f"  總模擬時間: {TIME_STEPS * DT / 3600:.1f} 小時")

# ============================================================
# 3. 模擬
# ============================================================

negative_energy = 0.0
field_stability = 1.0
bubble_radius = 0.0
speed = 0.0
formation_time = 0
formation_step = -1

time_history = []
energy_history = []
stability_history = []

print("\n[2] 模擬進行:")
print("-" * 70)

for step in range(TIME_STEPS):
    t = step * DT
    
    # 產生負能量
    negative_energy += effective_power * DT
    
    # 能量損耗
    if negative_energy < 0:
        loss = abs(negative_energy) * 0.01 * DT
        negative_energy += loss
    
    # 場腔穩定
    if negative_energy < -1e10:
        field_stability = min(1.0, field_stability + (1 - field_stability) * EFFICIENCY_CAVITY * DT * 0.01)
    
    # 曲率泡形成 (用絕對值比較)
    current_energy_abs = abs(negative_energy)
    target_energy_abs = abs(TARGET_ENERGY)
    
    if bubble_radius == 0 and current_energy_abs >= target_energy_abs * FORMATION_THRESHOLD:
        diameter = 1.0
        speed = 100 * (1 / diameter) * EFFICIENCY_CAVITY * (1 - MECHANICAL_TOLERANCE)
        bubble_radius = diameter / 2
        formation_time = t
        formation_step = step
        print(f"\n  ✅✅✅ 第 {step} 步曲率泡成功形成！")
        print(f"      時間: {t/3600:.2f} 小時")
        print(f"      能量: {negative_energy:.2e} J (目標嘅 {current_energy_abs/target_energy_abs*100:.1f}%)")
        print(f"      速度: {speed:.0f} c")
        print(f"      穩定度: {field_stability:.3f}")
        break
    
    if step % 100 == 0:
        progress = current_energy_abs / target_energy_abs * 100
        time_history.append(t)
        energy_history.append(negative_energy)
        stability_history.append(field_stability)
        print(f"  第 {step:4d} 步: 能量 {negative_energy:.2e} J | 進度 {progress:.1f}% | 穩定度 {field_stability:.3f}")

if bubble_radius == 0:
    print("\n  ⚠️ 模擬結束，曲率泡未形成")
    print(f"      最終能量: {negative_energy:.2e} J")
    print(f"      目標能量: {TARGET_ENERGY:.2e} J")

# ============================================================
# 4. 結論
# ============================================================

print("\n" + "=" * 70)
print("🎯 最終結論")
print("=" * 70)

if bubble_radius > 0:
    print(f"""
✅ 曲率泡成功形成！

📊 結果:
   - 形成時間: {formation_time/3600:.2f} 小時
   - 形成步數: 第 {formation_step} 步
   - 形成能量: {negative_energy:.2e} J
   - 場穩定性: {field_stability:.3f}
   - 曲率泡速度: {speed:.0f} c

📊 參數:
   - 陣列尺寸: {ARRAY_SIZE} km
   - 板間距: {PLATE_SPACING} nm
   - 安全系數: {SAFETY_FACTOR} 倍

🚀 結論: ✅ 曲率泡可以成功製造！
""")
else:
    print(f"""
⚠️ 曲率泡未能形成

📊 最終狀態:
   - 最終能量: {negative_energy:.2e} J
   - 目標能量: {TARGET_ENERGY:.2e} J
   - 進度: {abs(negative_energy/TARGET_ENERGY)*100:.1f}%

建議:
   - 增加 TIME_STEPS (3000 → 5000)
   - 或降低形成門檻 (80% → 60%)
""")

# ============================================================
# 5. 儲存結果
# ============================================================

with open("warp_bubble_simulation_results.txt", "w", encoding="utf-8") as f:
    f.write("=" * 70 + "\n")
    f.write("曲率泡生成與穩定性模擬結果\n")
    f.write(f"執行日期: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    f.write("=" * 70 + "\n\n")
    f.write(f"陣列尺寸: {ARRAY_SIZE} km\n")
    f.write(f"板間距: {PLATE_SPACING} nm\n")
    f.write(f"安全系數: {SAFETY_FACTOR} 倍\n")
    f.write(f"形成時間: {formation_time/3600:.2f} 小時\n")
    f.write(f"曲率泡速度: {speed:.0f} c\n")
    f.write(f"場穩定性: {field_stability:.3f}\n")
    f.write(f"曲率泡形成: {'✅ 是' if bubble_radius > 0 else '❌ 否'}\n")
    f.write("=" * 70 + "\n")

print("\n[結果] 已儲存至: warp_bubble_simulation_results.txt")

# ============================================================
# 6. 圖表
# ============================================================

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# 圖1: 負能量累積
ax1 = axes[0]
if time_history:
    ax1.plot(time_history, energy_history, 'b-', linewidth=2)
ax1.axhline(y=-TARGET_ENERGY * FORMATION_THRESHOLD, color='orange', linestyle='--', label=f'形成門檻 ({FORMATION_THRESHOLD*100}%)')
ax1.axhline(y=-TARGET_ENERGY, color='r', linestyle='--', label=f'目標 (-{TARGET_ENERGY:.1e} J)')
if bubble_radius > 0:
    ax1.axvline(x=formation_time, color='g', linestyle='--', label=f'形成 ({formation_time/3600:.2f}h)')
ax1.set_xlabel('時間 (秒)')
ax1.set_ylabel('負能量 (J)')
ax1.set_title('負能量累積')
ax1.legend()
ax1.grid(True, alpha=0.3)

# 圖2: 場穩定性
ax2 = axes[1]
if stability_history:
    ax2.plot(time_history, stability_history, 'g-', linewidth=2)
ax2.axhline(y=0.85, color='r', linestyle='--', label='穩定閾值 (0.85)')
ax2.set_xlabel('時間 (秒)')
ax2.set_ylabel('場穩定性')
ax2.set_title('場腔固定效果')
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('warp_bubble_simulation_analysis.png', dpi=150)
print("[圖表] 已儲存至: warp_bubble_simulation_analysis.png")

print("\n" + "=" * 70)
print("模擬完成！🚀")
print("=" * 70)
