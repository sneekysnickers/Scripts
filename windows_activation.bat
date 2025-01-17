@echo off
cls
echo ========================================
echo Windows 11 Activation Script
echo ========================================
echo 1. Windows 11 Pro
echo 2. Windows 11 Home
echo ========================================
set /p choice="Please choose the edition to activate (1 for Pro, 2 for Home): "

if "%choice%"=="1" (
    echo You selected Windows 11 Pro.
    call :ActivateWindows "Pro"
) else if "%choice%"=="2" (
    echo You selected Windows 11 Home.
    call :ActivateWindows "Home"
) else (
    echo Invalid selection. Exiting...
    exit /b
)

exit /b

:ActivateWindows
set edition=%1

if "%edition%"=="Pro" (
    echo Activating Windows 11 Pro...
    cscript slmgr.vbs /upk
    cscript slmgr.vbs /cpky
    cscript slmgr.vbs /ckms
    cscript slmgr.vbs /ipk W269N-WFGWX-YVC9B-4J6C9-T83GX
    cscript slmgr.vbs /skms kms8.msguides.com
    cscript slmgr.vbs /ato
) else if "%edition%"=="Home" (
    echo Activating Windows 11 Home...
    cscript slmgr.vbs /upk
    cscript slmgr.vbs /cpky
    cscript slmgr.vbs /ckms
    cscript slmgr.vbs /ipk 33PXH-7Y6Y6-9QMXP-K3P4P-3P6Y4
    cscript slmgr.vbs /skms kms8.msguides.com
    cscript slmgr.vbs /ato
) else (
    echo Invalid edition selected. Exiting...
    exit /b
)

exit /b
