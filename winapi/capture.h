#pragma once
#include <Windows.h>
#include <string>

extern void CaptureWindow(HWND hwndTarget, std::wstring lFilePath = L"ScreenShot.bmp");
