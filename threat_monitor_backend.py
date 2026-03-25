#!/usr/bin/env python3
"""
AI Threat Monitor — Backend System Monitor v3.0
Provides real CPU, memory, temperature, process, and network data
to the AI Threat Monitor dashboard via REST API.

Features: Historical CSV logging, Windows toast notifications,
process kill, network traffic recording.

Based on: Ivan Barbato — "The Hidden Architecture of AI Platforms"
"""

import json
import time
import os
import csv
import threading
import subprocess
import signal
from datetime import datetime
import psutil
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

PORT = 8092
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'monitor_data')
os.makedirs(DATA_DIR, exist_ok=True)

# AI platform processes to watch for
AI_PROCESSES = [
    'chatgpt', 'claude', 'anthropic', 'deepseek', 'manus',
    'copilot', 'gemini', 'ollama', 'openai', 'bard',
    'electron',  # Many AI apps use Electron
    'node',      # Node.js backends
    'python',    # ML/AI Python processes
]

# Suspicious network domains
AI_DOMAINS = [
    'openai.com', 'anthropic.com', 'claude.ai', 'chatgpt.com',
    'deepseek.com', 'gemini.google.com', 'manus.im', 'api.openai.com',
    'cdn.oaistatic.com', 'browser.events.data.msn.com',
]


# ═══════════════════════════════════════════
# Historical CSV Logger
# ═══════════════════════════════════════════
class HistoryLogger:
    """Logs system metrics to CSV for forensic analysis."""

    def __init__(self):
        self.csv_path = os.path.join(DATA_DIR, f'metrics_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv')
        self.net_log_path = os.path.join(DATA_DIR, f'network_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv')
        self.sample_count = 0
        self._init_csv()
        self._init_net_csv()

    def _init_csv(self):
        with open(self.csv_path, 'w', newline='') as f:
            w = csv.writer(f)
            w.writerow(['timestamp', 'cpu_percent', 'cpu_level', 'mem_percent', 'mem_used_gb',
                        'mem_total_gb', 'battery_percent', 'battery_charging', 'drain_rate',
                        'thermal_estimate', 'ai_process_count', 'active_connections',
                        'fps_estimate', 'total_processes'])

    def _init_net_csv(self):
        with open(self.net_log_path, 'w', newline='') as f:
            w = csv.writer(f)
            w.writerow(['timestamp', 'local_addr', 'remote_addr', 'pid', 'process_name',
                        'ai_related', 'bytes_sent_mb', 'bytes_recv_mb'])

    def log_metrics(self, snapshot):
        """Append a row to the metrics CSV."""
        self.sample_count += 1
        try:
            cpu = snapshot.get('cpu', {})
            mem = snapshot.get('memory', {})
            batt = snapshot.get('battery', {})
            procs = snapshot.get('processes', {})
            net = snapshot.get('network', {})

            with open(self.csv_path, 'a', newline='') as f:
                w = csv.writer(f)
                w.writerow([
                    datetime.now().isoformat(),
                    cpu.get('overall', 0),
                    cpu.get('level', ''),
                    mem.get('percent', 0),
                    mem.get('used_gb', 0),
                    mem.get('total_gb', 0),
                    batt.get('percent', ''),
                    batt.get('charging', ''),
                    batt.get('drain_rate', ''),
                    batt.get('thermal_estimate', ''),
                    procs.get('ai_count', 0),
                    net.get('active_connections', 0),
                    '',
                    procs.get('total_processes', 0),
                ])
        except Exception:
            pass

    def log_network(self, connections, io_stats):
        """Append network connections to the network log."""
        try:
            ts = datetime.now().isoformat()
            with open(self.net_log_path, 'a', newline='') as f:
                w = csv.writer(f)
                for conn in connections:
                    proc_name = ''
                    if conn.get('pid'):
                        try:
                            proc_name = psutil.Process(conn['pid']).name()
                        except Exception:
                            pass
                    w.writerow([
                        ts, conn.get('local', ''), conn.get('remote', ''),
                        conn.get('pid', ''), proc_name,
                        conn.get('ai_related', False),
                        io_stats.get('bytes_sent_mb', 0),
                        io_stats.get('bytes_recv_mb', 0),
                    ])
        except Exception:
            pass

    def get_status(self):
        metrics_size = os.path.getsize(self.csv_path) if os.path.exists(self.csv_path) else 0
        net_size = os.path.getsize(self.net_log_path) if os.path.exists(self.net_log_path) else 0
        return {
            'metrics_file': self.csv_path,
            'network_file': self.net_log_path,
            'samples': self.sample_count,
            'metrics_size_kb': round(metrics_size / 1024, 1),
            'network_size_kb': round(net_size / 1024, 1),
        }


# ═══════════════════════════════════════════
# Windows Toast Notifications
# ═══════════════════════════════════════════
class NotificationEngine:
    """Sends Windows toast notifications for critical alerts."""

    def __init__(self):
        self.last_alerts = {}
        self.cooldown = 60  # seconds between repeated alerts
        self.history = []
        self.enabled = True

    def notify(self, title, message, level='warning'):
        if not self.enabled:
            return
        key = title
        now = time.time()
        if key in self.last_alerts and (now - self.last_alerts[key]) < self.cooldown:
            return
        self.last_alerts[key] = now
        self.history.append({'time': datetime.now().isoformat(), 'title': title, 'message': message, 'level': level})
        if len(self.history) > 50:
            self.history.pop(0)

        try:
            ps_cmd = f'''[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] > $null
$template = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent([Windows.UI.Notifications.ToastTemplateType]::ToastText02)
$text = $template.GetElementsByTagName("text")
$text.Item(0).AppendChild($template.CreateTextNode("{title}")) > $null
$text.Item(1).AppendChild($template.CreateTextNode("{message}")) > $null
$toast = [Windows.UI.Notifications.ToastNotification]::new($template)
[Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("AI Threat Monitor").Show($toast)'''
            subprocess.Popen(
                ['powershell', '-WindowStyle', 'Hidden', '-Command', ps_cmd],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0
            )
        except Exception:
            pass

    def get_history(self):
        return {'enabled': self.enabled, 'notifications': self.history[-20:], 'total': len(self.history)}


# ═══════════════════════════════════════════
# System Monitor
# ═══════════════════════════════════════════
class SystemMonitor:
    """Collects real system metrics using psutil."""

    def __init__(self):
        self.start_time = time.time()
        self.cpu_history = []
        self.battery_history = []
        self.logger = HistoryLogger()
        self.notifier = NotificationEngine()

    def get_cpu(self):
        """Real CPU usage per-core and overall."""
        overall = psutil.cpu_percent(interval=0.5)
        per_core = psutil.cpu_percent(interval=0, percpu=True)
        freq = psutil.cpu_freq()
        load_avg = None
        try:
            load_avg = [round(x, 2) for x in psutil.getloadavg()]
        except (AttributeError, OSError):
            pass

        self.cpu_history.append(overall)
        if len(self.cpu_history) > 120:
            self.cpu_history.pop(0)

        return {
            'overall': overall,
            'per_core': per_core,
            'core_count': psutil.cpu_count(logical=True),
            'physical_cores': psutil.cpu_count(logical=False),
            'freq_current': round(freq.current, 0) if freq else None,
            'freq_max': round(freq.max, 0) if freq else None,
            'load_avg': load_avg,
            'history': self.cpu_history[-30:],
            'alert': overall > 80,
            'level': 'CRITICAL' if overall > 90 else 'HIGH' if overall > 70 else 'FAIR' if overall > 40 else 'NOMINAL',
        }

    def get_memory(self):
        """Real memory usage."""
        vm = psutil.virtual_memory()
        swap = psutil.swap_memory()
        return {
            'total_gb': round(vm.total / (1024**3), 2),
            'used_gb': round(vm.used / (1024**3), 2),
            'available_gb': round(vm.available / (1024**3), 2),
            'percent': vm.percent,
            'swap_total_gb': round(swap.total / (1024**3), 2),
            'swap_used_gb': round(swap.used / (1024**3), 2),
            'swap_percent': swap.percent,
            'alert': vm.percent > 80,
            'level': 'CRITICAL' if vm.percent > 90 else 'HIGH' if vm.percent > 75 else 'FAIR' if vm.percent > 50 else 'NOMINAL',
        }

    def get_battery(self):
        """Battery status with drain rate calculation."""
        batt = psutil.sensors_battery()
        if not batt:
            return {'available': False}

        result = {
            'available': True,
            'percent': batt.percent,
            'charging': batt.power_plugged,
            'secs_left': batt.secsleft if batt.secsleft != psutil.POWER_TIME_UNLIMITED else None,
            'mins_left': round(batt.secsleft / 60, 1) if batt.secsleft not in (psutil.POWER_TIME_UNLIMITED, psutil.POWER_TIME_UNKNOWN) else None,
        }

        self.battery_history.append({'time': time.time(), 'level': batt.percent})
        if len(self.battery_history) > 120:
            self.battery_history.pop(0)

        if len(self.battery_history) >= 2 and not batt.power_plugged:
            first = self.battery_history[0]
            last = self.battery_history[-1]
            mins = (last['time'] - first['time']) / 60
            if mins > 0.5:
                drain = round((first['level'] - last['level']) / mins, 3)
                result['drain_rate'] = drain
                result['drain_alert'] = drain > 1.5
                if drain > 2.0:
                    result['thermal_estimate'] = 'THROTTLING'
                elif drain > 1.0:
                    result['thermal_estimate'] = 'HOT'
                elif drain > 0.5:
                    result['thermal_estimate'] = 'WARM'
                else:
                    result['thermal_estimate'] = 'COOL'

        return result

    def get_temperature(self):
        """System temperature sensors."""
        try:
            temps = psutil.sensors_temperatures()
            if not temps:
                return {'available': False, 'note': 'No temperature sensors found (common on Windows)'}
            result = {'available': True, 'sensors': {}}
            for name, entries in temps.items():
                result['sensors'][name] = [
                    {'label': e.label or 'Unknown', 'current': e.current, 'high': e.high, 'critical': e.critical}
                    for e in entries
                ]
            max_temp = max(e.current for entries in temps.values() for e in entries)
            result['max_temp'] = max_temp
            result['level'] = 'THROTTLING' if max_temp > 80 else 'HOT' if max_temp > 65 else 'WARM' if max_temp > 50 else 'COOL'
            return result
        except (AttributeError, Exception):
            return {'available': False, 'note': 'Temperature sensors not accessible'}

    def get_processes(self):
        """Detect AI-related processes and top CPU consumers."""
        ai_procs = []
        top_procs = []

        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
            try:
                info = proc.info
                name_lower = info['name'].lower() if info['name'] else ''

                # Collect top CPU processes
                if info['cpu_percent'] and info['cpu_percent'] > 1:
                    top_procs.append({
                        'pid': info['pid'],
                        'name': info['name'],
                        'cpu': round(info['cpu_percent'], 1),
                        'memory': round(info['memory_percent'], 1) if info['memory_percent'] else 0,
                    })

                # Check for AI-related processes
                for ai_name in AI_PROCESSES:
                    if ai_name in name_lower:
                        ai_procs.append({
                            'pid': info['pid'],
                            'name': info['name'],
                            'cpu': round(info['cpu_percent'], 1) if info['cpu_percent'] else 0,
                            'memory': round(info['memory_percent'], 1) if info['memory_percent'] else 0,
                            'matched': ai_name,
                        })
                        break
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        top_procs.sort(key=lambda x: x['cpu'], reverse=True)

        return {
            'ai_processes': ai_procs[:20],
            'top_cpu': top_procs[:10],
            'total_processes': len(list(psutil.process_iter())),
            'ai_count': len(ai_procs),
            'alert': len(ai_procs) > 0,
        }

    def get_network(self):
        """Network connections and traffic."""
        io = psutil.net_io_counters()
        conns = []
        ai_conns = []

        try:
            for conn in psutil.net_connections(kind='inet'):
                if conn.status == 'ESTABLISHED' and conn.raddr:
                    entry = {
                        'local': f"{conn.laddr.ip}:{conn.laddr.port}",
                        'remote': f"{conn.raddr.ip}:{conn.raddr.port}",
                        'status': conn.status,
                        'pid': conn.pid,
                    }
                    conns.append(entry)

                    # Check remote IP against AI domains (basic heuristic)
                    remote_ip = conn.raddr.ip
                    if conn.pid:
                        try:
                            proc = psutil.Process(conn.pid)
                            proc_name = proc.name().lower()
                            for ai_name in AI_PROCESSES:
                                if ai_name in proc_name:
                                    entry['ai_related'] = True
                                    ai_conns.append(entry)
                                    break
                        except (psutil.NoSuchProcess, psutil.AccessDenied):
                            pass
        except (psutil.AccessDenied, OSError):
            pass

        return {
            'bytes_sent': io.bytes_sent,
            'bytes_recv': io.bytes_recv,
            'bytes_sent_mb': round(io.bytes_sent / (1024**2), 1),
            'bytes_recv_mb': round(io.bytes_recv / (1024**2), 1),
            'packets_sent': io.packets_sent,
            'packets_recv': io.packets_recv,
            'active_connections': len(conns),
            'ai_connections': ai_conns[:10],
            'top_connections': conns[:15],
            'alert': len(ai_conns) > 0,
        }

    def get_disk(self):
        """Disk usage and I/O."""
        io = psutil.disk_io_counters()
        partitions = []
        for p in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(p.mountpoint)
                partitions.append({
                    'device': p.device,
                    'mountpoint': p.mountpoint,
                    'total_gb': round(usage.total / (1024**3), 1),
                    'used_gb': round(usage.used / (1024**3), 1),
                    'percent': usage.percent,
                })
            except (PermissionError, OSError):
                continue

        return {
            'read_mb': round(io.read_bytes / (1024**2), 1) if io else 0,
            'write_mb': round(io.write_bytes / (1024**2), 1) if io else 0,
            'partitions': partitions,
        }

    def kill_process(self, pid):
        """Kill a process by PID."""
        try:
            proc = psutil.Process(pid)
            name = proc.name()
            proc.terminate()
            proc.wait(timeout=3)
            self.notifier.notify('Process Killed', f'{name} (PID {pid}) terminated', 'info')
            return {'success': True, 'pid': pid, 'name': name, 'message': f'{name} terminated'}
        except psutil.NoSuchProcess:
            return {'success': False, 'error': f'Process {pid} not found'}
        except psutil.AccessDenied:
            return {'success': False, 'error': f'Access denied for PID {pid}'}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def get_all(self):
        """Complete system snapshot."""
        snapshot = {
            'timestamp': time.time(),
            'uptime_seconds': round(time.time() - self.start_time),
            'boot_time': psutil.boot_time(),
            'cpu': self.get_cpu(),
            'memory': self.get_memory(),
            'battery': self.get_battery(),
            'temperature': self.get_temperature(),
            'processes': self.get_processes(),
            'network': self.get_network(),
            'disk': self.get_disk(),
            'logging': self.logger.get_status(),
        }

        # Log to CSV
        self.logger.log_metrics(snapshot)

        # Log network connections
        net = snapshot['network']
        self.logger.log_network(net.get('top_connections', []), net)

        # Check alerts and send notifications
        cpu = snapshot['cpu']
        if cpu['overall'] > 90:
            self.notifier.notify('CPU CRITICAL', f'CPU at {cpu["overall"]}% - possible AI compute offload', 'critical')
        batt = snapshot.get('battery', {})
        drain = batt.get('drain_rate', 0)
        if drain and drain > 1.5:
            self.notifier.notify('Battery Drain Alert', f'Drain rate: {drain}%/min - catastrophic', 'critical')
        procs = snapshot['processes']
        if procs['ai_count'] > 5:
            self.notifier.notify('AI Processes', f'{procs["ai_count"]} AI processes running', 'warning')

        return snapshot


monitor = SystemMonitor()


class Handler(BaseHTTPRequestHandler):
    """HTTP handler with CORS for the frontend."""

    def do_OPTIONS(self):
        self.send_response(200)
        self._cors()
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        params = parse_qs(parsed.query)

        if path == '/api/health':
            self._json({'status': 'ok', 'version': '3.0', 'uptime': round(time.time() - monitor.start_time)})
        elif path == '/api/cpu':
            self._json(monitor.get_cpu())
        elif path == '/api/memory':
            self._json(monitor.get_memory())
        elif path == '/api/battery':
            self._json(monitor.get_battery())
        elif path == '/api/temperature':
            self._json(monitor.get_temperature())
        elif path == '/api/processes':
            self._json(monitor.get_processes())
        elif path == '/api/network':
            self._json(monitor.get_network())
        elif path == '/api/disk':
            self._json(monitor.get_disk())
        elif path == '/api/all':
            self._json(monitor.get_all())
        elif path == '/api/logging':
            self._json(monitor.logger.get_status())
        elif path == '/api/notifications':
            self._json(monitor.notifier.get_history())
        elif path == '/api/notifications/toggle':
            monitor.notifier.enabled = not monitor.notifier.enabled
            self._json({'enabled': monitor.notifier.enabled})
        elif path == '/api/kill':
            pid = params.get('pid', [None])[0]
            if pid:
                self._json(monitor.kill_process(int(pid)))
            else:
                self._json({'success': False, 'error': 'Missing pid parameter'})
        else:
            self.send_response(404)
            self._cors()
            self.end_headers()
            self.wfile.write(b'Not Found')

    def _json(self, data):
        self.send_response(200)
        self._cors()
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def _cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def log_message(self, format, *args):
        # Color-coded logging
        msg = format % args
        if '200' in msg:
            print(f"  \033[32m✓\033[0m {msg}")
        elif '404' in msg:
            print(f"  \033[33m⚠\033[0m {msg}")
        else:
            print(f"  \033[36m→\033[0m {msg}")


def main():
    import sys, io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

    print()
    print("  +===================================================+")
    print("  |   AI THREAT MONITOR - Backend System Monitor       |")
    print("  |   Based on: Ivan Barbato's Hidden Architecture     |")
    print("  +===================================================+")
    print()
    print(f"  [*] Real-time system metrics server")
    print(f"  [*] API endpoint: http://127.0.0.1:{PORT}/api/all")
    print(f"  [*] CPU Cores: {psutil.cpu_count(logical=True)} logical / {psutil.cpu_count(logical=False)} physical")
    print(f"  [*] RAM: {round(psutil.virtual_memory().total / (1024**3), 1)} GB")

    batt = psutil.sensors_battery()
    if batt:
        print(f"  [*] Battery: {batt.percent}% {'(charging)' if batt.power_plugged else '(on battery)'}")
    else:
        print(f"  [*] Battery: Not available")

    print(f"  [*] Data dir: {DATA_DIR}")
    print(f"  [*] CSV log: {monitor.logger.csv_path}")
    print(f"  [*] Net log: {monitor.logger.net_log_path}")
    print()
    print(f"  API Routes:")
    print(f"    GET /api/all              - Complete system snapshot")
    print(f"    GET /api/cpu              - CPU pressure & per-core usage")
    print(f"    GET /api/memory           - RAM & swap usage")
    print(f"    GET /api/battery          - Battery drain & thermal")
    print(f"    GET /api/temperature      - System temperature sensors")
    print(f"    GET /api/processes        - AI process detection")
    print(f"    GET /api/network          - Connections & traffic")
    print(f"    GET /api/disk             - Disk I/O & partitions")
    print(f"    GET /api/kill?pid=1234    - Kill process by PID")
    print(f"    GET /api/logging          - CSV logging status")
    print(f"    GET /api/notifications    - Toast notification history")
    print(f"    GET /api/health           - Health check")
    print()
    print(f"  Press Ctrl+C to stop")
    print()

    server = HTTPServer(('127.0.0.1', PORT), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Server stopped.")
        server.server_close()


if __name__ == '__main__':
    main()
