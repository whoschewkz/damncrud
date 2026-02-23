# Run DamnCRUD Tests - Windows PowerShell Script
# Usage: .\run_tests.ps1 [command]

param(
    [string]$Command = "help"
)

# Color codes
$Green = "Green"
$Yellow = "Yellow"
$Red = "Red"

function Show-Help {
    Write-Host "DamnCRUD Functional Testing Script (PowerShell)" -ForegroundColor $Green
    Write-Host "Usage: .\run_tests.ps1 [COMMAND]" -ForegroundColor $Green
    Write-Host ""
    Write-Host "Commands:" -ForegroundColor $Green
    Write-Host "  all          - Run all tests (parallel)" -ForegroundColor $Green
    Write-Host "  parallel     - Run tests in parallel (auto CPU cores)" -ForegroundColor $Green
    Write-Host "  serial       - Run tests serially" -ForegroundColor $Green
    Write-Host "  create       - Run CREATE operation tests" -ForegroundColor $Green
    Write-Host "  read         - Run READ operation tests" -ForegroundColor $Green
    Write-Host "  update       - Run UPDATE operation tests" -ForegroundColor $Green
    Write-Host "  delete       - Run DELETE operation tests" -ForegroundColor $Green
    Write-Host "  integration  - Run integration tests" -ForegroundColor $Green
    Write-Host "  report       - Run tests and generate HTML report" -ForegroundColor $Green
    Write-Host "  markers      - Show all available markers" -ForegroundColor $Green
    Write-Host "  collect      - Collect tests without execution" -ForegroundColor $Green
    Write-Host "  help         - Show this help message" -ForegroundColor $Green
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor $Green
    Write-Host "  .\run_tests.ps1 all" -ForegroundColor $Green
    Write-Host "  .\run_tests.ps1 parallel" -ForegroundColor $Green
    Write-Host "  .\run_tests.ps1 create" -ForegroundColor $Green
    Write-Host "  .\run_tests.ps1 report" -ForegroundColor $Green
}

function Check-Pytest {
    $pytestInstalled = pip show pytest 2>$null
    if (-not $pytestInstalled) {
        Write-Host "Pytest not found. Installing dependencies..." -ForegroundColor $Yellow
        pip install -r requirements.txt
    }
}

function Run-Tests {
    param(
        [string]$Command
    )
    
    Check-Pytest
    
    $separator = "==========================================" 
    Write-Host $separator -ForegroundColor $Green
    Write-Host "DamnCRUD Functional Testing" -ForegroundColor $Green
    Write-Host $separator -ForegroundColor $Green
    Write-Host ""
    
    switch ($Command.ToLower()) {
        "all" {
            Write-Host "Running all tests..." -ForegroundColor $Green
            pytest tests/ -v --tb=short -n auto
        }
        "parallel" {
            Write-Host "Running tests in parallel (auto-detected cores)..." -ForegroundColor $Green
            pytest tests/ -v --tb=short -n auto
        }
        "serial" {
            Write-Host "Running tests serially..." -ForegroundColor $Green
            pytest tests/ -v --tb=short
        }
        "create" {
            Write-Host "Running only CREATE tests..." -ForegroundColor $Green
            pytest tests/ -v -k "create" -n auto
        }
        "read" {
            Write-Host "Running only READ tests..." -ForegroundColor $Green
            pytest tests/ -v -k "read or view" -n auto
        }
        "update" {
            Write-Host "Running only UPDATE tests..." -ForegroundColor $Green
            pytest tests/ -v -k "update" -n auto
        }
        "delete" {
            Write-Host "Running only DELETE tests..." -ForegroundColor $Green
            pytest tests/ -v -k "delete" -n auto
        }
        "integration" {
            Write-Host "Running only integration tests..." -ForegroundColor $Green
            pytest tests/ -v -m integration -n auto
        }
        "report" {
            Write-Host "Running tests and generating HTML report..." -ForegroundColor $Green
            pytest tests/ -v --html=tests/reports/report.html --self-contained-html --tb=short -n auto
            Write-Host "Report generated at: tests/reports/report.html" -ForegroundColor $Green
        }
        "markers" {
            Write-Host "Available test markers:" -ForegroundColor $Green
            pytest --markers
        }
        "collect" {
            Write-Host "Collecting test cases (no execution)..." -ForegroundColor $Green
            pytest tests/ --collect-only
        }
        "help" {
            Show-Help
        }
        default {
            Write-Host "Unknown command: $Command" -ForegroundColor $Yellow
            Write-Host "Use 'help' for usage information" -ForegroundColor $Yellow
            exit 1
        }
    }
    
    Write-Host ""
    Write-Host $separator -ForegroundColor $Green
}

# Main execution
Run-Tests -Command $Command
