from PyKbd.layout import Layout


def generate_inf_file(layout: Layout):
    # TODO add version to name
    layout_id = "19360409"  # TODO "{variant}{codepage}"
    size = 32  # TODO size in kB

    return f"""
; https://learn.microsoft.com/en-us/windows-hardware/drivers/install/summary-of-inf-sections

[Version]
Signature = "$Windows NT$"

[SourceDisksNames]
1 = "{layout.name}" 

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

[DefaultUninstall.NTAMD64]
LegacyUninstall = 1

[Files_Inf]
{layout.dll_name[:-4]}.inf,,,0x00010002

[Files_System32_NTx86]
{layout.dll_name},{layout.dll_name[:-4]}32.dll,,0x00014002

[Files_System32_NTAMD64]
{layout.dll_name},{layout.dll_name[:-4]}64.dll,,0x00014002

[Files_SysWOW64_NTAMD64]
{layout.dll_name},{layout.dll_name[:-4]}WW.dll,,0x00014002

[Reg_Layout]
HKLM,"SYSTEM\\CurrentControlSet\\Control\\Keyboard Layouts\\{layout_id}","Layout Text",,"{layout.name}"
HKLM,"SYSTEM\\CurrentControlSet\\Control\\Keyboard Layouts\\{layout_id}","Layout File",,"{layout.dll_name}"
HKLM,"SYSTEM\\CurrentControlSet\\Control\\Keyboard Layouts\\{layout_id}","Layout Id",,"001C" ; TODO ???

[Reg_Uninstall]
HKLM,"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{layout.dll_name}",DisplayName,,"{layout.name}"
HKLM,"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{layout.dll_name}",Publisher,,"{layout.author}"
HKLM,"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{layout.dll_name}",UninstallString,,"rundll32.exe setupapi,InstallHinfSection DefaultUninstall 132 %17%\\{layout.dll_name[:-4]}.inf"
HKLM,"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{layout.dll_name}",EstimatedSize,0x00010001,{size}
HKLM,"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{layout.dll_name}",NoModify,0x00010001,1
HKLM,"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{layout.dll_name}",NoRepair,0x00010001,1

[Reg_Delete]
HKLM,"SYSTEM\\CurrentControlSet\\Control\\Keyboard Layouts\\{layout_id}"
HKLM,"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{layout.dll_name}"
"""
