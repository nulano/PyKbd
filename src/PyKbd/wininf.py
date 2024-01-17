from PyKbd.crc16 import crc16xmodem
from PyKbd.layout import Layout


def get_name(layout: Layout):
    # keep in sync with compile_windll, TODO refactor this
    revision = crc16xmodem(layout.to_json())
    return f"{layout.name} {layout.version[0]}.{layout.version[1]} ({revision})"


def generate_inf_file(layout: Layout):
    # TODO add version to name
    layout_id = "19360409"  # TODO "{variant}{codepage}"
    size = 32  # TODO size in kB

    name = get_name(layout)

    return f"""
; https://learn.microsoft.com/en-us/windows-hardware/drivers/install/summary-of-inf-sections

[Version]
Signature = "$Windows NT$"

[SourceDisksNames]
1 = "{name}" 

[SourceDisksFiles]
{layout.dll_name[:-4]}.inf = 1
{layout.dll_name[:-4]}32.dll = 1
{layout.dll_name[:-4]}WW.dll = 1
{layout.dll_name[:-4]}64.dll = 1

[DestinationDirs]
DefaultDestDir         =    11 ; %SystemRoot%\\system32
Files_SysWOW64_NTAMD64 = 16425 ; %SystemRoot%\\SysWOW64
Files_Inf              =    17 ; INF file directory

[DefaultInstall.NTx86]
AddReg = Reg_Layout, Reg_Uninstall
CopyFiles = Files_Inf, Files_System32_NTx86

[DefaultInstall.NTAMD64]
AddReg = Reg_Layout, Reg_Uninstall
CopyFiles = Files_Inf, Files_System32_NTAMD64, Files_SysWOW64_NTAMD64

[DefaultUninstall.NTx86]
DelReg = Reg_Delete
DelFiles = Files_Inf, Files_System32_NTx86

[DefaultUninstall.NTAMD64]
DelReg = Reg_Delete
DelFiles = Files_Inf, Files_System32_NTAMD64, Files_SysWOW64_NTAMD64

[Files_Inf]
{layout.dll_name[:-4]}.inf,,,0x00010000

[Files_System32_NTx86]
{layout.dll_name},{layout.dll_name[:-4]}32.dll,,0x00014000

[Files_System32_NTAMD64]
{layout.dll_name},{layout.dll_name[:-4]}64.dll,,0x00014000

[Files_SysWOW64_NTAMD64]
{layout.dll_name},{layout.dll_name[:-4]}WW.dll,,0x00014000

[Reg_Layout]
HKLM,"SYSTEM\\CurrentControlSet\\Control\\Keyboard Layouts\\{layout_id}","Layout Text",,"{name}"
HKLM,"SYSTEM\\CurrentControlSet\\Control\\Keyboard Layouts\\{layout_id}","Layout File",,"{layout.dll_name}"
HKLM,"SYSTEM\\CurrentControlSet\\Control\\Keyboard Layouts\\{layout_id}","Layout Id",,"001C" ; TODO ???

[Reg_Uninstall]
HKLM,"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{layout.dll_name}",DisplayName,,"{name}"
HKLM,"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{layout.dll_name}",Publisher,,"{layout.author}"
HKLM,"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{layout.dll_name}",UninstallString,,"rundll32.exe setupapi,InstallHinfSection DefaultUninstall 132 %17%\\{layout.dll_name[:-4]}.inf"
HKLM,"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{layout.dll_name}",EstimatedSize,0x00010001,{size}
HKLM,"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{layout.dll_name}",NoModify,0x00010001,1
HKLM,"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{layout.dll_name}",NoRepair,0x00010001,1

[Reg_Delete]
HKLM,"SYSTEM\\CurrentControlSet\\Control\\Keyboard Layouts\\{layout_id}"
HKLM,"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{layout.dll_name}"
"""


def generate_inf_launcher(layout: Layout, inffile, uninstall=False):
    name = get_name(layout)
    verb = "Uninstall" if uninstall else "Install"
    action = "DefaultUninstall" if uninstall else "DefaultInstall"
    # TODO the Sysnative indirection below requires Vista or newer (that may be OK, 64-bit XP was uncommon)
    return f"""
@choice /M "{verb} {name}"
@if errorlevel 2 goto end
@if errorlevel 1 (echo Running {inffile}) else goto end
set "SystemPath=%SystemRoot%\\System32"
if not "%ProgramFiles(x86)%" == "" if exist %SystemRoot%\\Sysnative\\cmd.exe set "SystemPath=%SystemRoot%\\Sysnative"
%SystemPath%\\rundll32.exe setupapi,InstallHinfSection {action} 132 %~dp0{inffile}
@echo.
@pause
:end
"""
