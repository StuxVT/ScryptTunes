; ScryptTunesInstaller.nsi

!include "MUI2.nsh"

; General settings
Outfile "build\ScryptTunesInstaller.exe"
InstallDir $PROGRAMFILES\ScryptTunes

; UI settings
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_LANGUAGE "English"

; Default section
Section

; Output path for the installer
SetOutPath $INSTDIR

; Include all files from build/main.dist
File /r "build\main.dist\*.*"

; Create a shortcut on the desktop
CreateShortcut "$DESKTOP\ScryptTunes.lnk" "$INSTDIR\ScryptTunes.exe"

; Create a shortcut in the Start menu
CreateDirectory $SMPROGRAMS\ScryptTunes
CreateShortcut "$SMPROGRAMS\ScryptTunes\ScryptTunes.lnk" "$INSTDIR\ScryptTunes.exe"

; Write uninstall information
WriteUninstaller "$INSTDIR\Uninstall.exe"
WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\ScryptTunes" "DisplayName" "ScryptTunes"
WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\ScryptTunes" "UninstallString" "$\"$INSTDIR\Uninstall.exe$\""

SectionEnd

; Uninstaller section
Section "Uninstall"

; Remove all installed files
Delete "$INSTDIR\ScryptTunes.exe"
RMDir /r "$INSTDIR"

; Remove shortcuts
Delete "$DESKTOP\ScryptTunes.lnk"
Delete "$SMPROGRAMS\ScryptTunes\ScryptTunes.lnk"
RMDir "$SMPROGRAMS\ScryptTunes"

; Remove uninstall information
DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\ScryptTunes"

SectionEnd
