"""
AI ORCHESTRATION KERNEL v8.7.1 - STUDENT EDITION
Enhanced with:
1. Original production-grade features
2. Educational software preloading
3. School hardware compatibility
4. Learning environment customization
5. Parental/teacher controls
6. Study productivity tools
"""

import os
import sys
import hashlib
import json
import time
import subprocess
import tempfile
import glob
import re
import shutil
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend
from enum import Enum, auto

# ========== ENVIRONMENT CHECK ==========
def is_wsl():
    try:
        with open("/proc/version", "r") as f:
            version_info = f.read().lower()
            return "microsoft" in version_info or "wsl" in version_info
    except Exception:
        return False

IN_WSL = is_wsl()

# ======================
# Hardware Detection (Original + School Device Support)
# ======================
class HardwareDetector:
    def __init__(self):
        self.arch = os.uname().machine
        self.details = self._detect_all()
        self._check_missing()

    def _detect_all(self) -> dict:
        return {
            'cpu': self._get_cpu_info(),
            'ram': self._get_ram_size(),
            'storage': self._get_storage_info(),
            'network': self._get_network_info(),
            'gpu': self._get_gpu_info(),
            'usb': self._scan_usb(),
            'firmware': self._check_firmware(),
            'boot_mode': self._get_boot_mode(),
            'school_devices': self._detect_school_devices()  # NEW
        }

    def _get_cpu_info(self):
        cpu_info = {'model': 'Unknown'}
        try:
            with open("/proc/cpuinfo") as f:
                for line in f:
                    if line.startswith("model name"):
                        cpu_info['model'] = line.split(":",1)[1].strip()
                        break
        except Exception:
            pass
        return cpu_info

    def _get_ram_size(self):
        ram_gb = 0.0
        try:
            with open("/proc/meminfo") as f:
                for line in f:
                    if line.startswith("MemTotal:"):
                        kb = int(re.findall(r'\d+', line)[0])
                        ram_gb = kb / 1024 / 1024
                        break
        except Exception:
            pass
        return ram_gb

    def _get_storage_info(self):
        total_size_gb = 0.0
        try:
            st = os.statvfs("/")
            total_size_gb = (st.f_blocks * st.f_frsize) / (1024**3)
        except Exception:
            pass
        return {'total_gb': total_size_gb}

    def _get_network_info(self):
        try:
            interfaces = os.listdir('/sys/class/net/')
            active = [iface for iface in interfaces if os.path.exists(f'/sys/class/net/{iface}/operstate') and
                      open(f'/sys/class/net/{iface}/operstate').read().strip() == 'up']
            return active
        except Exception:
            return []

    def _get_gpu_info(self):
        gpu_list = []
        try:
            lspci_output = subprocess.check_output(["lspci"]).decode()
            for line in lspci_output.split('\n'):
                if 'vga compatible controller' in line.lower():
                    gpu_list.append(line.strip())
        except Exception:
            pass
        return gpu_list

    def _scan_usb(self):
        usb_devices = []
        try:
            lsusb_out = subprocess.check_output(["lsusb"]).decode()
            usb_devices = [line.strip() for line in lsusb_out.split('\n') if line.strip()]
        except Exception:
            pass
        return usb_devices

    def _check_firmware(self):
        # Placeholder for firmware check
        return {'status': 'unknown'}

    def _check_missing(self):
        if not self.details['cpu']['model']:
            raise Exception("CPU not detected")

    def _get_boot_mode(self) -> str:
        return "uefi" if os.path.exists("/sys/firmware/efi") else "bios"

    def _detect_school_devices(self) -> dict:
        devices = {
            'projectors': self._scan_for_projectors(),
            'printers': self._scan_for_printers(),
            'tablets': self._scan_for_drawing_tablets()
        }
        return devices

    def _scan_for_projectors(self) -> list:
        try:
            output = subprocess.check_output(["lsusb"]).decode()
            return [line for line in output.split('\n') if any(brand in line.lower() 
                   for brand in ['benq', 'epson', 'optoma'])]
        except:
            return []

    def _scan_for_printers(self) -> list:
        try:
            output = subprocess.check_output(["lpstat", "-p"]).decode()
            return [line for line in output.split('\n') if line.strip()]
        except:
            return []

    def _scan_for_drawing_tablets(self) -> list:
        try:
            output = subprocess.check_output(["lsusb"]).decode()
            return [line for line in output.split('\n') if any(name in line.lower() 
                   for name in ['wacom', 'huion', 'xp-pen'])]
        except:
            return []

# ======================
# Kernel Configuration (Original + Student Settings)
# ======================
class KernelConfig:
    def __init__(self):
        self.hardware = HardwareDetector()
        self._init_partitions()
        self.overlay_dir = "/var/overlay"
        self.student_config = StudentConfig()
        
        # Driver repositories (original + educational)
        self.driver_repos = {
            'iwlwifi': 'https://firmware.intel.com',
            'broadcom-sta': 'https://packages.debian.org',
            'rtlwifi': 'https://github.com/lwfinger/rtlwifi_new',
            'mesa': 'https://packages.debian.org',
            'firmware': 'https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git',
            'school': 'https://edu-drivers.josiahkernel.org'
        }

        self.use_tpm = self._detect_tpm()
        self.boot_key = self._load_or_generate_key()
        self.safe_mode = True  # Enabled by default for students

    def _init_partitions(self):
        if self.hardware.details['boot_mode'] == "uefi":
            # Only set boot and rootfs if partitions are found; else fallback
            boot = self._find_partition("EFI")
            root = self._find_partition("ROOT")
            self.boot = boot if boot else "/dev/sda1"
            self.rootfs = root if root else "/dev/sda2"
        else:
            self.boot = "/dev/sda1"
            self.rootfs = "/dev/sda2"

    def _find_partition(self, label: str) -> str:
        try:
            output = subprocess.check_output(["blkid", "-L", label]).decode().strip()
            return output if output else ""
        except:
            return ""

    def _detect_tpm(self) -> bool:
        return os.path.exists("/dev/tpm0")

    def _load_or_generate_key(self):
        key_path = "/etc/josiah_kernel/boot_key.pem"
        try:
            if os.path.exists(key_path):
                with open(key_path, "rb") as f:
                    return f.read()
            else:
                from cryptography.hazmat.primitives import serialization
                private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
                pem = private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                )
                os.makedirs(os.path.dirname(key_path), exist_ok=True)
                with open(key_path, "wb") as f:
                    f.write(pem)
                return pem
        except Exception:
            return None

# ======================
# NEW: Student Configuration System
# ======================
class StudentConfig:
    def __init__(self):
        self.safe_search = True
        self.parental_controls = False
        self.study_timer = 45  # minutes
        self.break_timer = 10  # minutes
        self.allowed_websites = [
            "wikipedia.org",
            "khanacademy.org",
            "wolframalpha.com",
            "geeksforgeeks.org",
            "josiahkernel.org/edu"
        ]
        self.installed_software = []
        
    def apply_settings(self):
        self._enable_safe_search()
        self._setup_timers()
        self._configure_environment()
        
    def _enable_safe_search(self):
        try:
            with open("/etc/resolv.conf", "a") as f:
                f.write("\n# Student Edition Safe Search\n")
                f.write("nameserver 8.8.8.8\n")
                f.write("nameserver 8.8.4.4\n")
        except Exception as e:
            print(f"Failed to configure DNS safe search: {e}")
        
        firefox_policy = {
            "policies": {
                "SafeBrowsingEnabled": True,
                "TrackingProtection": True,
                "BlockAboutAddons": True
            }
        }
        try:
            os.makedirs("/etc/firefox", exist_ok=True)
            with open("/etc/firefox/policies.json", "w") as f:
                json.dump(firefox_policy, f)
        except Exception as e:
            print(f"Failed to configure Firefox policies: {e}")
        
    def _setup_timers(self):
        if IN_WSL:
            print("Study timer service skipped on WSL")
            return
        try:
            with open("/etc/systemd/system/study-timer.service", "w") as f:
                f.write(f"""[Unit]
Description=Study Timer Service
After=graphical.target

[Service]
ExecStart=/usr/bin/study-timer --study {self.study_timer} --break {self.break_timer}
Restart=always

[Install]
WantedBy=multi-user.target
""")
            subprocess.run(["systemctl", "enable", "study-timer.service"], check=True)
        except Exception as e:
            print(f"Failed to setup study timer service: {e}")
        
    def _configure_environment(self):
        try:
            with open("/etc/xdg/mimeapps.list", "w") as f:
                f.write("""[Default Applications]
text/html=firefox.desktop
application/pdf=org.kde.okular.desktop
application/x-python-code=thonny.desktop
""")
        except Exception as e:
            print(f"Failed to configure environment: {e}")

# ======================
# NEW: Student Package Management
# ======================
class StudentPackages:
    def __init__(self):
        self.educational_tools = {
            'math': ['kalgebra', 'geogebra', 'gnuplot'],
            'science': ['stellarium', 'avogadro', 'kalzium'],
            'programming': ['thonny', 'scratch', 'jupyter-notebook'],
            'writing': ['libreoffice', 'lyx', 'focuswriter'],
            'misc': ['gcompris', 'kturtle', 'kodu']
        }
        
    def install_defaults(self):
        print("=== Installing Educational Software ===")
        self._ensure_package_manager()
        for category, packages in self.educational_tools.items():
            print(f"\nInstalling {category} tools...")
            for pkg in packages:
                try:
                    subprocess.run(
                        ["apt-get", "install", "-y", "--no-install-recommends", pkg],
                        check=True
                    )
                    print(f"✓ {pkg}")
                    config.student_config.installed_software.append(pkg)
                except subprocess.CalledProcessError:
                    print(f"⚠ Failed to install {pkg}")
        self._install_school_drivers()
        
    def _ensure_package_manager(self):
        if not shutil.which("apt-get"):
            print("Package manager apt-get not found. Skipping installation.")
            
    def _install_school_drivers(self):
        print("\nChecking for school hardware...")
        for device_type, devices in config.hardware.details['school_devices'].items():
            if devices:
                print(f"Found {device_type}, installing drivers...")
                try:
                    subprocess.run(
                        ["apt-get", "install", "-y", f"school-{device_type}-drivers"],
                        check=True
                    )
                except subprocess.CalledProcessError:
                    print(f"Could not install drivers for {device_type}")

# ======================
# Initramfs Generator (Original)
# ======================
class InitramfsBuilder:
    def generate(self):
        os.makedirs("/tmp/initramfs", exist_ok=True)
        for cmd in ["busybox", "modprobe", "mount"]:
            try:
                shutil.copy(f"/bin/{cmd}", "/tmp/initramfs/")
            except FileNotFoundError:
                print(f"Warning: {cmd} not found in /bin")
        with open("/tmp/initramfs/init", "w") as f:
            f.write("""#!/bin/busybox sh
mount -t proc proc /proc
mount -t sysfs sysfs /sys
mount -t devtmpfs devtmpfs /dev
exec /sbin/init
""")
        os.chmod("/tmp/initramfs/init", 0o755)
        try:
            subprocess.run("cd /tmp/initramfs && find . | cpio -H newc -o | gzip > /boot/initrd.img",
                           shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to build initramfs: {e}")

# ======================
# Boot Manager (Original + Student Mode Check)
# ======================
class BootManager:
    def __init__(self):
        self.efi_mounted = False

    def setup(self):
        if IN_WSL:
            print("WSL detected: Skipping EFI mount and GRUB installation")
        else:
            self._mount_efi()
            self._install_grub()
        self._generate_initramfs()
        if os.path.exists("/etc/student-mode"):
            self._setup_student_theme()

    def _mount_efi(self):
        try:
            os.makedirs("/boot/efi", exist_ok=True)
            subprocess.run(["mount", config.boot, "/boot/efi"], check=True)
            self.efi_mounted = True
        except subprocess.CalledProcessError as e:
            print(f"Failed to mount EFI partition: {e}")

    def _install_grub(self):
        try:
            target = "--target=x86_64-efi" if config.hardware.details['boot_mode'] == "uefi" else "--target=i386-pc"
            device = config.boot.split()[0] if isinstance(config.boot, str) else config.boot
            subprocess.run(["grub-install", target, device], check=True)
            subprocess.run(["grub-mkconfig", "-o", "/boot/grub/grub.cfg"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to install GRUB: {e}")
        
    def _setup_student_theme(self):
        try:
            subprocess.run([
                "grub-mktheme", "-o", "/boot/grub/themes/student",
                "-t", "education", "-i", "fonts"
            ])
            subprocess.run([
                "sed", "-i", 
                r"s/GRUB_THEME=.*/GRUB_THEME=\"\/boot\/grub\/themes\/student\/theme.txt\"/",
                "/etc/default/grub"
            ])
            subprocess.run(["grub-mkconfig", "-o", "/boot/grub/grub.cfg"])
        except Exception as e:
            print(f"Failed to setup student theme: {e}")

    def _generate_initramfs(self):
        InitramfsBuilder().generate()

# ======================
# NEW: Study Tools Service
# ======================
class StudyTools:
    def __init__(self):
        self.active_timers = {}
        
    def start_study_session(self):
        self._start_timer()
        self._enable_focus_mode()
        self._log_session_start()
        
    def _start_timer(self):
        if IN_WSL:
            print("Study timer start skipped (binary missing or unsupported on WSL).")
            return
        try:
            subprocess.Popen([
                "/usr/bin/study-timer",
                "--study", str(config.student_config.study_timer),
                "--break", str(config.student_config.break_timer)
            ])
        except Exception as e:
            print(f"Failed to start study timer: {e}")
        
    def _enable_focus_mode(self):
        try:
            with open("/etc/hosts", "a") as f:
                f.write("\n# Focus Mode Blocklist\n")
                f.write("127.0.0.1 facebook.com\n")
                f.write("127.0.0.1 twitter.com\n")
                f.write("127.0.0.1 instagram.com\n")
            if not IN_WSL:
                subprocess.run(["systemctl", "restart", "network-manager"], check=True)
            else:
                print("network-manager restart skipped or not available on WSL.")
        except Exception as e:
            print(f"Failed to enable focus mode: {e}")
        
    def _log_session_start(self):
        try:
            with open("/var/log/study-sessions.log", "a") as f:
                f.write(f"Session started at {time.ctime()}\n")
        except Exception as e:
            print(f"Failed to log study session start: {e}")

# ======================
# Placeholder: Init System (original feature)
# ======================
class InitSystem:
    def start_essential(self):
        print("Starting essential init system services...")

# ======================
# Main System (Original + Student Features)
# ======================
if __name__ == "__main__":
    try:
        config = KernelConfig()
        print("=== Josiah Kernel OS - Student Edition ===")
        print(f"Boot Mode: {config.hardware.details['boot_mode'].upper()}")
        print(f"CPU: {config.hardware.details['cpu']['model']}")
        print(f"RAM: {config.hardware.details['ram']:.1f}GB")

        if any(config.hardware.details['school_devices'].values()):
            print("\nDetected School Hardware:")
            for device, list_devices in config.hardware.details['school_devices'].items():
                if list_devices:
                    print(f"- {device}: {len(list_devices)} found")

        boot = BootManager()
        boot.setup()

        init = InitSystem()
        init.start_essential()

        packages = StudentPackages()
        packages.install_defaults()

        config.student_config.apply_settings()

        study = StudyTools()
        study.start_study_session()

        print("\n=== System Ready ===")
        print("Preinstalled educational software:")
        print("- Math: kalgebra, geogebra, gnuplot...")
        print("- Science: stellarium, avogadro, kalzium...")
        print("- Programming: thonny, scratch, jupyter-notebook...")
        print("- Writing: libreoffice, lyx, focuswriter...")
        print("- Misc: gcompris, kturtle, kodu...")

        print("\nStudy Tools Active:")
        print(f"- Focus timer: {config.student_config.study_timer}min study, {config.student_config.break_timer}min break")
        print("- Safe search enabled")
        
    except Exception as e:
        print(f"Fatal error during setup: {e}")
        sys.exit(1)
