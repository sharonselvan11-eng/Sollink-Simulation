import matplotlib.patches as patches
import matplotlib.pyplot as plt


def draw_block(ax, x, y, w, h, text, color="#e1f5fe", edge="#0288d1"):
  rect = patches.FancyBboxPatch(
      (x, y),
      w,
      h,
      boxstyle="round,pad=0.02,rounding_size=0.1",
      facecolor=color,
      edgecolor=edge,
      linewidth=2,
  )
  ax.add_patch(rect)
  ax.text(
      x + w / 2,
      y + h / 2,
      text,
      horizontalalignment="center",
      verticalalignment="center",
      fontsize=10,
      fontweight="bold",
      color="#1a237e",
  )


def draw_wire(ax, x1, y1, x2, y2, label=""):
  ax.annotate(
      "",
      xy=(x2, y2),
      xytext=(x1, y1),
      arrowprops=dict(
          arrowstyle="-|>",
          color="#37474f",
          lw=1.8,
          mutation_scale=15,
          shrinkA=0,
          shrinkB=0,
      ),
  )
  if label:
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    ax.text(
        mx,
        my + 0.15,
        label,
        fontsize=8,
        fontweight="bold",
        color="#c2185b",
        horizontalalignment="center",
        bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor="none"),
    )


fig, ax = plt.subplots(figsize=(15, 9))
ax.set_xlim(-1, 15)
ax.set_ylim(-1, 9)
ax.axis("off")

# Title
ax.text(
    7,
    8.5,
    "SOLLINK Hardware Circuit & Interconnect Architecture",
    fontsize=16,
    fontweight="bold",
    ha="center",
    color="#0d47a1",
)

# 1. Power Blocks
draw_block(
    ax,
    0,
    6,
    2.6,
    1.4,
    "Solar PV Panel\n(18V-21V, 60W-100W)",
    color="#fff3e0",
    edge="#f57c00",
)
draw_block(
    ax,
    4.5,
    6,
    2.6,
    1.4,
    "MPPT Solar Charge\nController",
    color="#fff8e1",
    edge="#ffa000",
)
draw_block(
    ax,
    4.5,
    3.5,
    2.6,
    1.4,
    "12V 20Ah Battery\n(LiFePO4 / Lead-Acid)",
    color="#e8f5e9",
    edge="#388e3c",
)
draw_block(
    ax,
    4.5,
    1,
    2.6,
    1.2,
    "Buck DC-DC Stepdown\n(12V -> 5V 3A)",
    color="#ede7f6",
    edge="#512da8",
)

# 2. Control & Gateway Blocks
draw_block(
    ax,
    9,
    4.5,
    3.0,
    2.2,
    "Smart Controller\n(Raspberry Pi / MCU)\n- Telemetry Sensing\n- PTT Signal Routing\n- AT Gateway Logic",
    color="#e1f5fe",
    edge="#0288d1",
)
draw_block(
    ax,
    13,
    5.5,
    2.0,
    1.4,
    "SIM7600 4G\nGSM Gateway",
    color="#fce4ec",
    edge="#c2185b",
)
draw_block(
    ax,
    9,
    1.2,
    3.0,
    1.4,
    "VHF/UHF DMR\nTransceiver Module\n(SA818 / DRA818)",
    color="#e0f2f1",
    edge="#00796b",
)
draw_block(
    ax, 13, 3.5, 2.0, 1.2, "16x2 LCD Screen\n(I2C 0x27)", color="#f3e5f5", edge="#7b1fa2"
)

# 3. Wiring Connections
draw_wire(ax, 2.6, 6.7, 4.5, 6.7, "18V DC")
draw_wire(ax, 5.8, 6.0, 5.8, 4.9, "Charge Bus")
draw_wire(ax, 5.8, 3.5, 5.8, 2.2, "12V Direct")
draw_wire(ax, 7.1, 1.6, 9.0, 1.6, "12V Supply")
draw_wire(ax, 7.1, 1.9, 9.0, 4.8, "5V System VCC")
draw_wire(ax, 7.1, 4.2, 9.0, 5.5, "Batt Sense (ADC)")

draw_wire(ax, 12.0, 6.2, 13.0, 6.2, "UART (AT Cmds)")
draw_wire(ax, 12.0, 5.0, 13.0, 4.1, "I2C (SDA/SCL)")
draw_wire(ax, 10.5, 4.5, 10.5, 2.6, "Audio I/O + PTT")

# External Antennas
ax.plot([14.0, 14.0, 13.7, 14.3, 14.0], [6.9, 7.5, 7.8, 7.8, 7.5], color="red", lw=2)
ax.text(
    14.0, 8.0, "Cellular Antenna", ha="center", fontsize=8, fontweight="bold"
)

ax.plot([10.5, 10.5, 10.2, 10.8, 10.5], [0, -0.4, -0.7, -0.7, -0.4], color="#00796b", lw=2)
ax.text(
    10.5,
    -0.9,
    "High-Gain VHF/UHF Yagi",
    ha="center",
    fontsize=8,
    fontweight="bold",
)

plt.tight_layout()
plt.savefig("circuit_schematic.png", dpi=300, bbox_inches="tight")
plt.show()