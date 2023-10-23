PROJECT := splash-2023

# Retrieve operating system type from host shell
OS_TYPE := $(shell uname)

# Required software packages for building the project
BUILD_REQ_PKGS := clojure babashka

# Source and test directories 
SRC_DIR := src
TEST_DIR := test

# Clojure dependencies
CLJ := clojure
BB := bb

# Conditional check for required software installations based on the OS type
ifeq ($(OS_TYPE), darwin)
	ifeq (,$(wildcard /usr/local/bin/$(CLJ)))
		$(error $(CLJ) is not installed on your system, please consider installing $(CLJ))
	endif
	ifeq (,$(wildcard /usr/local/bin/$(BB)))
		$(error $(BB) is not installed on your system, please consider installing $(BB))
	endif
endif

.PHONY: all setup check test static_analysis offline run 

# Show available targets with descriptions 
help:
	@echo "Usage: make [target]"
	@echo "Available Targets:"
	@echo "  all               - Perform all actions: setup, check, test, static_analysis, offline, run"
	@echo "  setup             - Install build dependencies"
	@echo "  check             - Verify the project's integrity"
	@echo "  test              - Execute project's tests"
	@echo "  static_analysis   - Run static analysis on source code"
	@echo "  offline           - Prepare application for offline use"
	@echo "  run               - Start the application"
	@echo "  psql              - Perform PostgreSQL operations"
	@echo "  clean             - Remove any build artifacts"
	@echo "  deploy            - Deploy application"
	@echo "  help              - Display this help message"

# Composite target that triggers all other targets 
all: setup check test static_analysis offline run 

# Install any necessary dependencies for development and build
setup:
ifdef BUILD_REQ_PKGS
	brew install $(BUILD_REQ_PKGS)
else
	@echo "No dependencies to install or already installed"
endif

# Validate the project's structure and correctness
check:
	lein check

# Execute the project's tests
test:
	lein test

# Perform static code analysis
static_analysis:
	clj-kondo --lint $(SRC_DIR)

# Download dependencies and prepare the project for offline use
offline:
	lein offline

# Start the project 
run: 
	lein run -m $(PROJECT).core

# Interact with PostgreSQL through Babashka 
psql:
	$(BB) --classpath $(CLASSPATH) --main cljs.main -re psql -c "available-builds"

# Remove any build artifacts
clean:
	lein clean

# Deploy the project to Clojars repository
deploy:
	lein deploy clojars
