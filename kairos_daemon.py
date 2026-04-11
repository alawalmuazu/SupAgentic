#!/usr/bin/env python3
"""
KAIROS Daemon — Autonomous Background Agent for SupAgentic
Based on the leaked March 2026 Claude Code architecture.

Features:
- Proactive Heartbeat ("Anything worth doing right now?")
- autoDream (Memory consolidation when system is idle)
- Push Notifications (via Windows Toast API)
- Three-Layer Memory (Scratchpad -> MEMORY.md)
"""

import os
import sys
import time
import json
import threading
import subprocess
from datetime import datetime
from pathlib import Path
import ctypes

try:
    import psutil
except ImportError:
    psutil = None

# ═══ Configuration ═══
SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR / "monitor_data"
MEMORY_DIR = SCRIPT_DIR / "memory"

DATA_DIR.mkdir(exist_ok=True)
MEMORY_DIR.mkdir(exist_ok=True)

SCRATCHPAD_FILE = MEMORY_DIR / "scratchpad.log"
MEMORY_FILE = MEMORY_DIR / "MEMORY.md"

class PlatformIdleDetector:
    """Detects system idle time (Windows only for now)."""
    class LASTINPUTINFO(ctypes.Structure):
        _fields_ = [
            ("cbSize", ctypes.c_uint),
            ("dwTime", ctypes.c_int)
        ]

    @staticmethod
    def get_idle_duration_seconds():
        """Returns the number of seconds since last user input."""
        if sys.platform != 'win32':
            # Fallback for non-Windows (mock functionality)
            return 0
            
        lii = PlatformIdleDetector.LASTINPUTINFO()
        lii.cbSize = ctypes.sizeof(PlatformIdleDetector.LASTINPUTINFO)
        if ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii)):
            millis = ctypes.windll.kernel32.GetTickCount() - lii.dwTime
            return millis / 1000.0
        return 0

class PushNotifier:
    """Uses Windows UI Toast to send push notifications."""
    
    @staticmethod
    def notify(title, message):
        """Send a toast notification."""
        if sys.platform != 'win32':
            print(f"[NOTIFY] {title}: {message}")
            return

        try:
            ps_cmd = f'''[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] > $null
$template = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent([Windows.UI.Notifications.ToastTemplateType]::ToastText02)
$text = $template.GetElementsByTagName("text")
$text.Item(0).AppendChild($template.CreateTextNode("{title}")) > $null
$text.Item(1).AppendChild($template.CreateTextNode("{message}")) > $null
$toast = [Windows.UI.Notifications.ToastNotification]::new($template)
[Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("SupAgentic KAIROS").Show($toast)'''
            subprocess.Popen(
                ['powershell', '-WindowStyle', 'Hidden', '-Command', ps_cmd],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0
            )
        except Exception as e:
            print(f"[NOTIFY FAILED] {e}")

class MemoryManager:
    """Handles the 'Three-Layer Memory Architecture'."""

    @staticmethod
    def log_observation(text):
        """Append to the raw transcript/scratchpad."""
        entry = f"[{datetime.now().isoformat()}] {text}\n"
        with open(SCRATCHPAD_FILE, "a", encoding="utf-8") as f:
            f.write(entry)

    @staticmethod
    def auto_dream_consolidation():
        """
        The autoDream process. 
        Simulates: Merging disparate observations, removing contradictions, 
        and maintaining the MEMORY.md file strictly indexed by pointers.
        """
        if not SCRATCHPAD_FILE.exists() or os.path.getsize(SCRATCHPAD_FILE) < 50:
            return False # Nothing to consolidate

        print(f"[{datetime.now().strftime('%H:%M:%S')}] 🧠 [autoDream] Initiating Memory Consolidation Phase...")
        
        # 1. Read scratchpad
        with open(SCRATCHPAD_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        if not lines:
            return False
            
        # Simulate LLM processing
        print("    -> Merging disparate observations...")
        time.sleep(1)
        print("    -> Removing logical contradictions...")
        time.sleep(1)
        print("    -> Rewriting memory indexes (Strict Write Discipline)...")
        
        # 2. Extract facts (Simulated)
        events = len(lines)
        latest_event = lines[-1].strip()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 3. Write to MEMORY.md
        memory_content = ""
        if MEMORY_FILE.exists():
            memory_content = MEMORY_FILE.read_text(encoding="utf-8")
            
        new_fact = f"- **{timestamp}**: Encapsulated {events} granular events. Latest state: *{latest_event.split(']')[-1].strip()}*\n"
        
        if "# SupAgentic Perpetual Context (KAIROS)" not in memory_content:
            memory_content = "# SupAgentic Perpetual Context (KAIROS)\n\n" + new_fact
        else:
            memory_content += new_fact
            
        MEMORY_FILE.write_text(memory_content, encoding="utf-8")
        
        # 4. Clear scratchpad maintaining strict write discipline
        open(SCRATCHPAD_FILE, 'w').close()
        
        return True

class KairosDaemon:
    """
    KAIROS background orchestrator. 
    Maintains a heartbeat and sleeps until actionable context demands attention.
    """
    
    def __init__(self, interval=5.0):
        self.interval = interval
        self.running = False
        self.idle_threshold_seconds = 180 # Consider system idle after 3 mins
        self.last_action_time = time.time()
        
    def start(self):
        self.running = True
        print(f"\n[KAIROS DAEMON STAGE: ONLINE]")
        print("==================================================")
        print(f"[*] Heartbeat initialized (interval: {self.interval}s)")
        print(f"[*] autoDream idle threshold: {self.idle_threshold_seconds}s")
        print("==================================================\n")
        
        PushNotifier.notify("KAIROS Online", "Autonomous background process initialized.")
        MemoryManager.log_observation("KAIROS Daemon started.")
        
        self._loop()

    def stop(self):
        self.running = False
        PushNotifier.notify("KAIROS Offline", "Daemon shutting down.")
        MemoryManager.log_observation("KAIROS Daemon stopped.")

    def _loop(self):
        heartbeat_counter = 0
        
        while self.running:
            try:
                idle_time = PlatformIdleDetector.get_idle_duration_seconds()
                heartbeat_counter += 1
                
                # Proactive Heartbeat Check
                is_idle = idle_time > self.idle_threshold_seconds
                self._evaluate_context(heartbeat_counter, idle_time, is_idle)
                
                # autoDream Memory Consolidation Check
                if is_idle and (time.time() - self.last_action_time > 60):
                    # We have been idle over the threshold and haven't dreamed in 60s
                    dream_success = MemoryManager.auto_dream_consolidation()
                    if dream_success:
                        self.last_action_time = time.time()
                        PushNotifier.notify("autoDream", "Memory consolidation completed while system idle.")

                time.sleep(self.interval)
                
            except KeyboardInterrupt:
                self.stop()
                break
            except Exception as e:
                print(f"[!] Error in KAIROS loop: {e}")
                time.sleep(self.interval)

    def _evaluate_context(self, counter, idle_time, is_idle):
        """
        The core "Anything worth doing right now?" evaluation prompt.
        """
        now_str = datetime.now().strftime("%H:%M:%S")
        
        # Periodically log system state for demonstration purposes
        if counter % 12 == 0:  # Every ~60 seconds
            cpu = psutil.cpu_percent(interval=None) if psutil else "Unknown"
            status = "IDLE (Dream Mode Enabled)" if is_idle else "ACTIVE (Listening)"
            
            MemoryManager.log_observation(f"Heartbeat context check - CPU: {cpu}%, User State: {status}")
            print(f"[{now_str}] ♥ Heartbeat: Anything worth doing? [Context = {status}] -> Decided: Stay quiet.")

        # Simulate detecting a notable event occasionally
        if counter % 50 == 0 and not is_idle:
            PushNotifier.notify("KAIROS Proactive Insight", "Notice: CPU workload shifted. Contextualizing current task.")
            MemoryManager.log_observation("Detected notable load shift, proactively alerting user.")
            print(f"[{now_str}] ♥ Heartbeat: Anything worth doing? -> Decided: ACT (Send Notification).")
            self.last_action_time = time.time()

if __name__ == "__main__":
    import signal
    daemon = KairosDaemon(interval=5.0)
    
    def signal_handler(sig, frame):
        print('\n[KAIROS] Graceful shutdown triggered...')
        daemon.stop()
        sys.exit(0)
        
    signal.signal(signal.SIGINT, signal_handler)
    daemon.start()
