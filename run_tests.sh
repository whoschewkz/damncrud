#!/bin/bash

# Script untuk menjalankan Pytest dengan berbagai konfigurasi
# DamnCRUD Functional Testing

echo "=========================================="
echo "DamnCRUD Functional Testing Script"
echo "=========================================="
echo ""

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo -e "${YELLOW}Pytest not found. Installing dependencies...${NC}"
    pip install -r requirements.txt
fi

# Parse arguments
case "${1}" in
    "all")
        echo -e "${GREEN}Running all tests...${NC}"
        pytest tests/ -v --tb=short -n auto
        ;;
    "parallel")
        echo -e "${GREEN}Running tests in parallel (auto-detected cores)...${NC}"
        pytest tests/ -v --tb=short -n auto
        ;;
    "serial")
        echo -e "${GREEN}Running tests serially...${NC}"
        pytest tests/ -v --tb=short
        ;;
    "create")
        echo -e "${GREEN}Running only CREATE tests...${NC}"
        pytest tests/ -v -k "create" -n auto
        ;;
    "read")
        echo -e "${GREEN}Running only READ tests...${NC}"
        pytest tests/ -v -k "read or view" -n auto
        ;;
    "update")
        echo -e "${GREEN}Running only UPDATE tests...${NC}"
        pytest tests/ -v -k "update" -n auto
        ;;
    "delete")
        echo -e "${GREEN}Running only DELETE tests...${NC}"
        pytest tests/ -v -k "delete" -n auto
        ;;
    "integration")
        echo -e "${GREEN}Running only integration tests...${NC}"
        pytest tests/ -v -m integration -n auto
        ;;
    "report")
        echo -e "${GREEN}Running tests and generating HTML report...${NC}"
        pytest tests/ -v --html=tests/reports/report.html --self-contained-html --tb=short -n auto
        echo -e "${GREEN}Report generated at: tests/reports/report.html${NC}"
        ;;
    "markers")
        echo -e "${GREEN}Available test markers:${NC}"
        pytest --markers
        ;;
    "collect")
        echo -e "${GREEN}Collecting test cases (no execution)...${NC}"
        pytest tests/ --collect-only
        ;;
    "help"|"")
        echo "Usage: $0 [COMMAND]"
        echo ""
        echo "Commands:"
        echo "  all          - Run all tests (parallel)"
        echo "  parallel     - Run tests in parallel (auto CPU cores)"
        echo "  serial       - Run tests serially"
        echo "  create       - Run CREATE operation tests"
        echo "  read         - Run READ operation tests"
        echo "  update       - Run UPDATE operation tests"
        echo "  delete       - Run DELETE operation tests"
        echo "  integration  - Run integration tests"
        echo "  report       - Run tests and generate HTML report"
        echo "  markers      - Show all available markers"
        echo "  collect      - Collect tests without execution"
        echo "  help         - Show this help message"
        echo ""
        echo "Examples:"
        echo "  ./run_tests.sh all"
        echo "  ./run_tests.sh parallel"
        echo "  ./run_tests.sh create"
        echo "  ./run_tests.sh report"
        ;;
    *)
        echo -e "${YELLOW}Unknown command: $1${NC}"
        echo "Use '$0 help' for usage information"
        exit 1
        ;;
esac

echo ""
echo "=========================================="
