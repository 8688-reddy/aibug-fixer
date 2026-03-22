# AI Bug Fixer

This is a graphical desktop application that uses Google's Gemini AI to automatically fix bugs in any source code file you provide. 

## Setup
You need a Google Gemini API Key to use this software.
Get one for free at: [Google AI Studio](https://aistudio.google.com/app/apikey)

## Features
- **Dark Mode UI**: Clean, premium dark mode interface using `customtkinter`.
- **Side-by-side view**: Review the original and fixed code adjacent to one another.
- **Save**: With one click, save the newly fixed code to a file ending in `_fixed.ext`.
- **Any language**: AI bug fixer supports all major programming languages.

## Build the Executable
You can run the provided PowerShell script to build it into a `.exe` file that can be sent to friends or used as a standalone tool.

1. Open PowerShell in this folder.
2. Run `.\build_exe.ps1`
3. The `.exe` will be located in the `dist/` folder.
