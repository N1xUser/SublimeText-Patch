import os
import psutil
import shutil
import ctypes
import time
from pathlib import Path
from typing import Optional, List

class SublimeTextPatcher:
    def __init__(self):

       
        self.drives = self._get_available_drives()

    @staticmethod
    def _print(message: str, tag: Optional[str] = None) -> None:

        prefix = f" [{tag}] " if tag else " [+] "
        print(f"{prefix}{message}")

    @staticmethod
    def _clear_screen() -> None:

        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def _is_admin() -> bool:

        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except AttributeError:
            return False

    def _get_available_drives(self) -> List[str]:

        return [f"{chr(letter)}:\\" for letter in range(65, 91) if os.path.exists(f"{chr(letter)}:\\")]

    def _find_sublime_text(self, mode: str) -> Optional[Path]:

        filename = "sublime_text.exe" if mode == "p" else "sublime_text.bkp"
        
        for drive in self.drives:
            potential_paths = [
                Path(drive) / "Program Files" / "Sublime Text" / filename,
                Path(drive) / "Program Files (x86)" / "Sublime Text" / filename,
                Path(drive) / "Program Files" / "Sublime Text 3" / filename,
                Path(drive) / "Program Files (x86)" / "Sublime Text 3" / filename
            ]
            
            for path in potential_paths:
                if path.exists():
                    return path
        
        return None

    @staticmethod
    def _kill_sublime_processes() -> None:

        for proc in psutil.process_iter(['name']):
            if proc.info['name'] == "sublime_text.exe":
                proc.kill()
                time.sleep(1)

    def _backup_executable(self, file_path: Path) -> Path:

        backup_path = file_path.with_suffix('.bkp')
        shutil.copy2(file_path, backup_path)
        return backup_path

    def _patch_executable(self, file_path: Path) -> None:

        try:
            with open(file_path, 'rb') as f:
                content = f.read()

            original_bytes = b'\x80\x79\x05\x00\x0F\x94\xC2'
            patched_bytes = b'\xC6\x41\x05\x01\xB2\x00\x90'

            if original_bytes not in content:
                NOP = 0x90
                offsets_and_values = {
                    0x00030170: 0x00,
                    0x000A94D0: NOP, 0x000A94D1: NOP, 0x000A94D2: NOP, 0x000A94D3: NOP, 0x000A94D4: NOP, 0x000A94D5: NOP, 0x000A94D6: NOP, 0x000A94D7: NOP, 0x000A94D8: NOP, 0x000A94D9: NOP, 0x000A94DA: NOP, 0x000A94DB: NOP, 0x000A94DC: NOP, 0x000A94DD: NOP, 0x000A94DE: NOP, 0x000A94DF: NOP, 0x000A94E0: NOP, 0x000A94E1: NOP, 0x000A94E2: NOP, 0x000A94E3: NOP, 0x000A94E4: NOP, 0x000A94E5: NOP, 0x000A94E6: NOP, 0x000A94E7: NOP, 0x000A94E8: NOP, 0x000A94E9: NOP, 0x000A94EA: NOP, 0x000A94EB: NOP, 0x000A94EC: NOP, 0x000A94ED: NOP, 0x000A94EE: NOP, 0x000A94EF: NOP, 0x000A94F0: NOP, 0x000A94F1: NOP, 0x000A94F2: NOP, 0x000A94F3: NOP, 0x000A94F4: NOP, 0x000A94F5: NOP, 0x000A94F6: NOP, 0x000A94F7: NOP, 0x000A94F8: NOP, 0x000A94F9: NOP, 0x000A94FA: NOP, 0x000A94FB: NOP, 0x000A94FC: NOP, 0x000A94FD: NOP, 0x000A94FE: NOP, 0x000A94FF: NOP, 0x000A9500: NOP, 0x000A9501: NOP, 0x000A9502: NOP, 0x000A9503: NOP, 0x000A9504: NOP, 0x000A9505: NOP, 0x000A9506: NOP, 0x000A9507: NOP, 0x000A9508: NOP, 0x000A9509: NOP, 0x000A950A: NOP, 0x000A950B: NOP, 0x000A950C: NOP, 0x000A950D: NOP, 0x000A950E: NOP, 0x000A950F: NOP,
                    0x001C6CCD: 0x02,
                    0x001C6CE4: 0x00,
                    0x001C6CFB: 0x00,
                }
                patched_content = bytearray(content)
                for offset, value in offsets_and_values.items():
                    if offset < len(patched_content):
                        patched_content[offset] = value
            else:
                patched_content = content.replace(original_bytes, patched_bytes)

            with open(file_path, 'wb') as f:
                f.write(patched_content)

        except Exception as e:
            raise RuntimeError(f"Failed to patch the file: {e}")

    def _patch_hosts_file(self, mode: str) -> None:

        hosts_path = Path("C:\\Windows\\System32\\drivers\\etc\\hosts")
        hosts_backup_path = hosts_path.with_suffix('.bkp')

        if mode == "p":
            if not self._confirm_action("Do you want to block Sublime Text updates?"):
                return

            shutil.copy2(hosts_path, hosts_backup_path)

            with open(hosts_path, 'a') as f:
                f.write("\n127.0.0.1 www.sublimetext.com\n127.0.0.1 sublimetext.com\n")
            
            self._print("Hosts file patched successfully.")
        
        elif mode == "r":
            if hosts_backup_path.exists():
                hosts_path.unlink()
                hosts_backup_path.rename(hosts_path)
                self._print("Hosts file restored successfully.")
            else:
                self._print("Hosts file backup not found.")

    @staticmethod
    def _confirm_action(prompt: str) -> bool:

        return input(f" [+] {prompt} (yes/no): ").strip().lower() == 'yes'

    def patch(self) -> None:

        if not self._confirm_action("Are you sure you want to patch Sublime Text?"):
            self._print("Operation canceled.")
            return

        try:
            self._print("Searching for Sublime Text...")
            sublime_path = self._find_sublime_text("p")
            
            if not sublime_path:
                self._print("Sublime Text not found. or already restored")
                return

            self._print(f"Sublime Text found at: {sublime_path}")
            self._kill_sublime_processes()
            
            backup_path = self._backup_executable(sublime_path)
            self._print(f"Backup created at: {backup_path}")
            
            self._patch_executable(sublime_path)
            self._print("Patching completed successfully!")
            
            self._patch_hosts_file("p")

        except Exception as e:
            self._print(f"An error occurred: {e}")

    def restore(self) -> None:

        if not self._confirm_action("Are you sure you want to restore Sublime Text?"):
            self._print("Operation canceled.")
            return

        try:
            self._print("Searching for Sublime Text backup...")
            sublime_backup_path = self._find_sublime_text("r")
            
            if not sublime_backup_path:
                self._print("Sublime Text backup not found.")
                return

            self._print(f"Sublime Text backup found at: {sublime_backup_path}")
            self._kill_sublime_processes()
            
            try:
                sublime_backup_path.with_suffix('.exe').unlink()
            except:
                pass
            sublime_backup_path.with_suffix('.bkp').rename(sublime_backup_path.with_suffix('.exe'))
            
            self._patch_hosts_file("r")
            self._print("Restoration completed successfully!")

        except Exception as e:
            self._print(f"An error occurred: {e}")

def main():

    SublimeTextPatcher._clear_screen()

    if not SublimeTextPatcher._is_admin():
        SublimeTextPatcher._print("This script requires administrator privileges. Please run it as an administrator.")
        return

    SublimeTextPatcher._print("Welcome to Sublime Text patcher!")
    SublimeTextPatcher._print("Choose an option:", "-")
    SublimeTextPatcher._print("Patch Sublime Text", "1")
    SublimeTextPatcher._print("Restore Sublime Text", "2")

    option = input(" [!] Enter the option number: ").strip()
    patcher = SublimeTextPatcher()

    if option == '1':
        patcher.patch()
    elif option == '2':
        patcher.restore()
    else:
        SublimeTextPatcher._print("Invalid option. Please run the script again and choose a valid option.")

if __name__ == "__main__":
    
    main()