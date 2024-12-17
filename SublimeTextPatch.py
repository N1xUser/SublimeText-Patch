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
				raise ValueError("Original byte sequence not found in file.")

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
				self._print("Sublime Text not found.")
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
			
			sublime_backup_path.with_suffix('.exe').unlink()
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