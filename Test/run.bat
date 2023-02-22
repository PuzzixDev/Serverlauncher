@ECHO OFF
SET BINDIR=%~dp0
CD /D "%BINDIR%"
"C:\Program Files\java\jdk-19\bin\java.exe" -Xmx1024M -Xms1024M -jar 1.19.3.jar nogui
PAUSE