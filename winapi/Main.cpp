#include "args.h"
#include "capture.h"

constexpr auto       help_options = make_array(L"-h", L"-?", L"--help");
constexpr auto screenshot_options = make_array(L"-s", L"--screenshot");
constexpr auto      click_options = make_array(L"-c", L"--click");
constexpr auto     window_options = make_array(L"-w", L"--window");
constexpr auto       name_options = make_array(L"-n", L"--name");
constexpr auto          x_options = make_array(L"-x");
constexpr auto          y_options = make_array(L"-y");

void screenshot(int argc, const wchar_t* argv[]) {
    args::wparser parser({ (size_t)argc, argv }, L"Windows API wrapper");

    std::wstring window_name = L"";
    std::wstring  image_name = L"screenshot.bmp";

    parser << args::woption  <void()      >(  help_options, L"Displays this help message",            [&]() { args::wparser::help(parser); exit(0); })
           << args::wargument<std::wstring>(window_options, L"Specify which window to look for",      L"name", window_name, false)
           << args::wargument<std::wstring>(  name_options, L"Specify the name to save the image as", L"name",  image_name,  true);

    parser();

    if (window_name.empty()) {
        std::wcerr << L"You have to specify a window name." << std::endl;
        exit(1);
    }
    
    HWND handle = FindWindowW(0, window_name.c_str());

    if (!handle) {
        std::wcerr << L"Could not find any window named \"" << window_name << L"\"." << std::endl;
        exit(1);
    }

    // Take screenshot.
    CaptureWindow(handle, image_name);
}

void click(int argc, const wchar_t* argv[]) {
    args::wparser parser({ (size_t)argc, argv }, L"Windows API wrapper");

    std::wstring window_name = L"";
    int x = -1;
    int y = -1;

    parser << args::woption  <void()      >(  help_options, L"Displays this help message",          [&]() { args::wparser::help(parser); exit(0); })
           << args::wargument<std::wstring>(window_options, L"Specify which window to look for",    L"name", window_name, false)
           << args::wargument<int         >(     x_options, L"Specify the X coordinate for the click", L"X",           x, false)
           << args::wargument<int         >(     y_options, L"Specify the Y coordinate for the click", L"Y",           y, false);

    parser();

    if (window_name.empty()) {
        std::cerr << "You have to specify a window name." << std::endl;
        exit(1);
    }

    if (x < 0 || y < 0) {
        std::cerr << "You have to specify a valid X and Y coordinate." << std::endl;
        exit(1);
    }
    
    HWND handle = FindWindowW(0, window_name.c_str());

    if (!handle) {
        std::wcerr << L"Could not find any window named \"" << window_name << L"\"." << std::endl;
        exit(1);
    }

    // Send click
    PostMessageW(handle, WM_LBUTTONDOWN, 1, MAKELPARAM(x, y));
    PostMessageW(handle, WM_LBUTTONUP,   0, MAKELPARAM(x, y));
}

int wmain(int argc, const wchar_t* argv[]) {
    args::wparser parser({ (size_t)argc, argv }, L"Windows API wrapper");

    parser << args::woption<void()>(screenshot_options, L"Take a screenshot of a window, even if it is in the background", [&]() { screenshot(argc, argv);      exit(0); })
           << args::woption<void()>(     click_options, L"Simulate a click in a window, even if it is in the background",  [&]() { click     (argc, argv);      exit(0); })
           << args::woption<void()>(      help_options, L"Displays this help message",                                     [&]() { args::wparser::help(parser); exit(0); });

    parser();

    return 0;
}
