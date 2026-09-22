import threading
import time
import tkinter as tk
from tkinter import ttk


class SollinkHardwareSim:

  def __init__(self, root):
    self.root = root
    self.root.title("SOLLINK Gateway & Controller Simulation")
    self.root.geometry("640x700")
    self.root.configure(bg="#1e1e1e")

    self.is_transmitting = False

    # Header
    title = tk.Label(
        root,
        text="SOLLINK HARDWARE CONTROLLER",
        font=("Consolas", 16, "bold"),
        fg="#00e676",
        bg="#1e1e1e",
    )
    title.pack(pady=10)

    # 16x2 LCD Display Mockup
    lcd_frame = tk.Frame(
        root, bg="#0d2818", bd=6, relief="ridge", padx=10, pady=10
    )
    lcd_frame.pack(pady=10)

    self.lcd_line1 = tk.Label(
        lcd_frame,
        text="SOLLINK ONLINE  ",
        font=("Consolas", 20, "bold"),
        fg="#00ff66",
        bg="#041f0e",
        width=18,
        anchor="w",
    )
    self.lcd_line1.pack()

    self.lcd_line2 = tk.Label(
        lcd_frame,
        text="BATT: 14.4V [OK]",
        font=("Consolas", 20, "bold"),
        fg="#00ff66",
        bg="#041f0e",
        width=18,
        anchor="w",
    )
    self.lcd_line2.pack(pady=(4, 0))

    # Controls & Indicators Frame
    ctrl_frame = tk.Frame(root, bg="#1e1e1e")
    ctrl_frame.pack(pady=15, fill="x", padx=40)

    # Solar / Battery Potentiometer Slider
    slider_label = tk.Label(
        ctrl_frame,
        text="Solar / Battery Level (Potentiometer):",
        font=("Segoe UI", 11),
        fg="white",
        bg="#1e1e1e",
    )
    slider_label.pack(anchor="w")

    self.volt_slider = ttk.Scale(
        ctrl_frame, from_=9.0, to=14.8, orient="horizontal", command=self.update_lcd
    )
    self.volt_slider.set(13.8)
    self.volt_slider.pack(fill="x", pady=6)

    # LED Indicator Canvas
    led_frame = tk.Frame(root, bg="#1e1e1e")
    led_frame.pack(pady=10)

    self.canvas_rf = tk.Canvas(
        led_frame, width=30, height=30, bg="#1e1e1e", highlightthickness=0
    )
    self.led_rf = self.canvas_rf.create_oval(
        5, 5, 25, 25, fill="#1c3b57", outline="#444444"
    )
    self.canvas_rf.grid(row=0, column=0, padx=5)
    tk.Label(
        led_frame,
        text="VHF/UHF RX",
        font=("Segoe UI", 10, "bold"),
        fg="#4fc3f7",
        bg="#1e1e1e",
    ).grid(row=0, column=1, padx=(0, 20))

    self.canvas_gsm = tk.Canvas(
        led_frame, width=30, height=30, bg="#1e1e1e", highlightthickness=0
    )
    self.led_gsm = self.canvas_gsm.create_oval(
        5, 5, 25, 25, fill="#4a3f00", outline="#444444"
    )
    self.canvas_gsm.grid(row=0, column=2, padx=5)
    tk.Label(
        led_frame,
        text="GSM 4G TX",
        font=("Segoe UI", 10, "bold"),
        fg="#ffd54f",
        bg="#1e1e1e",
    ).grid(row=0, column=3)

    # RF Trigger Button
    self.btn_trigger = tk.Button(
        root,
        text="TRIGGER REMOTE RF PACKET",
        font=("Segoe UI", 12, "bold"),
        bg="#0288d1",
        fg="white",
        activebackground="#0277bd",
        command=self.on_rf_trigger,
        padx=15,
        pady=8,
    )
    self.btn_trigger.pack(pady=10)

    # Serial Terminal Mockup
    serial_label = tk.Label(
        root,
        text="SIM7600 GSM & Microcontroller UART Console:",
        font=("Consolas", 10),
        fg="#888888",
        bg="#1e1e1e",
    )
    serial_label.pack(anchor="w", padx=40, pady=(10, 2))

    self.console = tk.Text(
        root,
        height=10,
        bg="#111111",
        fg="#00e676",
        font=("Consolas", 10),
        bd=2,
        relief="sunken",
    )
    self.console.pack(fill="both", expand=True, padx=40, pady=(0, 20))

    self.log_console("[SYSTEM] Boot sequence initialized.")
    self.log_console("[SYSTEM] DMR Transceiver & SIM7600 ready.")
    self.update_lcd()

  def log_console(self, text):
    self.console.insert("end", text + "\n")
    self.console.see("end")

  def update_lcd(self, *args):
    v = self.volt_slider.get()
    status = "OK" if v > 11.5 else "LOW!"
    self.lcd_line1.config(text="SOLLINK NODE    ")
    self.lcd_line2.config(text=f"BATT: {v:.1f}V [{status}]  ")

  def on_rf_trigger(self):
    if self.is_transmitting:
      return
    threading.Thread(target=self.run_gateway_routine, daemon=True).start()

  def run_gateway_routine(self):
    self.is_transmitting = True
    self.btn_trigger.config(state="disabled")

    # 1. RF RX Event
    self.canvas_rf.itemconfig(self.led_rf, fill="#00e5ff")
    self.lcd_line2.config(text="RF RX -> ROUTING")
    self.log_console("\n------------------------------------------------")
    self.log_console("[VHF/UHF] Inbound packet decoded: DMR Voice Alert received.")
    time.sleep(1.0)

    # 2. GSM Relay Event
    self.canvas_gsm.itemconfig(self.led_gsm, fill="#ffea00")
    self.lcd_line2.config(text="GSM 4G RELAY... ")
    self.log_console("[GSM GW] Routing to SIM7600 4G Module...")
    time.sleep(0.4)
    self.log_console(">>> AT+CMGF=1")
    self.log_console("<<< OK")
    time.sleep(0.4)
    self.log_console('>>> AT+CMGS="+91XXXXXXXXXX"')
    self.log_console(
        ">>> [SOLLINK ALERT] Emergency remote relay forwarded via Gateway."
    )
    self.log_console(">>> <CTRL+Z>")
    self.log_console("<<< +CMGS: 128")
    self.log_console("<<< OK")
    self.log_console(
        "[GSM GW] Packet successfully relayed to Public Cellular Network."
    )
    self.log_console("------------------------------------------------\n")
    time.sleep(1.2)

    # Reset
    self.canvas_rf.itemconfig(self.led_rf, fill="#1c3b57")
    self.canvas_gsm.itemconfig(self.led_gsm, fill="#4a3f00")
    self.update_lcd()
    self.btn_trigger.config(state="normal")
    self.is_transmitting = False


if __name__ == "__main__":
  root = tk.Tk()
  app = SollinkHardwareSim(root)
  root.mainloop()