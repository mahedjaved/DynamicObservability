# DynObsPersonal - Dynamic Observability Personal Project

## Ollama Setup Instructions

To use Ollama with this project, follow these steps:

### 1. Set up Ollama in your environment

#### Option 1: Permanent PATH Setup (Windows)
1. Open System Properties → Advanced → Environment Variables
2. In User variables, select PATH and click Edit
3. Add `C:\Users\ksfma\AppData\Local\Programs\Ollama` to the list
4. Restart your terminal/command prompt

#### Option 2: Use provided scripts
Run either:
- `run_with_ollama.bat` (for Command Prompt)
- `run_with_ollama.ps1` (for PowerShell)

These scripts temporarily add Ollama to your PATH and run the test.

### 2. Verify Ollama installation
```bash
ollama --version
```

### 3. Run the tests
```bash
python test_run.py
```
or use the provided scripts:
```bash
# Command Prompt
run_with_ollama.bat

# PowerShell
.\run_with_ollama.ps1
```

## Project Structure
- `src/`: Main source code
- `src/crew.py`: Main crew implementation
- `src/test_run.py`: Test script with Ollama environment checking
- `src/run_with_ollama.bat`: Windows batch script
- `src/run_with_ollama.ps1`: PowerShell script