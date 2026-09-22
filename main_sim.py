import matplotlib.pyplot as plt
import numpy as np

# -------------------------------------------------------------------------
# 1. RF LINK BUDGET SIMULATION (VHF 144 MHz + Repeater Coverage)
# -------------------------------------------------------------------------
distances_km = np.linspace(0.5, 35, 200)
freq_mhz = 144.0  # VHF DMR carrier frequency
tx_power_dbm = 37.0  # 5W Transceiver output
gain_tx_dbi = 9.0  # Directional antenna gain
gain_rx_dbi = 3.0  # Handheld terminal antenna gain
rx_sensitivity = -118.0  # DMR voice threshold (dBm)

# Free Space Path Loss + Terrain/Forest Obstruction (0.75 dB/km)
fspl = 20 * np.log10(distances_km) + 20 * np.log10(freq_mhz) + 32.44
terrain_loss = 0.75 * distances_km
rx_power_direct = tx_power_dbm + gain_tx_dbi + gain_rx_dbi - fspl - terrain_loss

# With Repeater at 15 km
rx_power_repeater = rx_power_direct.copy()
repeater_idx = np.where(distances_km >= 15.0)[0]
dist_from_rep = distances_km[repeater_idx] - 15.0
dist_from_rep[0] = 0.1
fspl_rep = 20 * np.log10(dist_from_rep) + 20 * np.log10(freq_mhz) + 32.44
rx_power_repeater[repeater_idx] = (
    tx_power_dbm + gain_tx_dbi + gain_rx_dbi - fspl_rep - (0.75 * dist_from_rep)
)

# -------------------------------------------------------------------------
# 2. 24-HOUR SOLAR AUTONOMY & BATTERY STORAGE SIMULATION
# -------------------------------------------------------------------------
hours = np.arange(0, 25)
irradiance = np.maximum(0, 1000 * np.sin((hours - 6) * np.pi / 12))
irradiance[hours < 6] = 0
irradiance[hours > 18] = 0

panel_capacity_w = 60.0  # 60W Solar PV panel
solar_gen_wh = (irradiance / 1000.0) * panel_capacity_w

# System load: RPi controller + SIM7600 + VHF transceiver
base_load_w = 4.5
burst_load_w = 12.0
hourly_load_wh = np.array([
    burst_load_w if h in [9, 10, 14, 19, 20] else base_load_w for h in hours
])

battery_capacity_wh = 12 * 20  # 12V 20Ah Battery = 240 Wh
battery_soc = [85.0]

for i in range(len(hours) - 1):
  net_energy = solar_gen_wh[i] - hourly_load_wh[i]
  delta_soc = (net_energy / battery_capacity_wh) * 100.0
  next_soc = np.clip(battery_soc[-1] + delta_soc, 15.0, 100.0)
  battery_soc.append(next_soc)

# -------------------------------------------------------------------------
# 3. PLOT SIMULATION RESULTS
# -------------------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Plot 1: RF Link Budget
ax1.plot(
    distances_km,
    rx_power_direct,
    "r--",
    label="Direct Link (Without Repeater)",
)
ax1.plot(
    distances_km,
    rx_power_repeater,
    "b-",
    linewidth=2,
    label="SOLLINK (With Repeater at 15 km)",
)
ax1.axhline(
    y=rx_sensitivity,
    color="black",
    linestyle=":",
    label="DMR Limit (-118 dBm)",
)
ax1.set_title("VHF Link Budget vs Distance in Forest/Hills")
ax1.set_xlabel("Distance (km)")
ax1.set_ylabel("Received Power (dBm)")
ax1.grid(True, linestyle="--", alpha=0.6)
ax1.legend()

# Plot 2: Solar & Battery Reserve
ax2.plot(hours, battery_soc, "g-", linewidth=2.5, label="Battery SOC (%)")
ax2.plot(
    hours,
    solar_gen_wh,
    "orange",
    linestyle="--",
    label="Solar Generation (W)",
)
ax2.axhline(
    y=20.0,
    color="red",
    linestyle=":",
    label="Critical Battery Reserve (20%)",
)
ax2.set_title("24-Hour Solar Harvesting & Battery Reserve")
ax2.set_xlabel("Hour of Day (0 - 24)")
ax2.set_ylabel("Percentage (%) / Power (W)")
ax2.grid(True, linestyle="--", alpha=0.6)
ax2.legend()

plt.tight_layout()
plt.savefig("sollink_simulation_result.png", dpi=300)
plt.show()