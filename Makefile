.SILENT:

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
help: # This is generated dynamically based on the previous line 
	awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# Composite target that triggers all other targets 
all: setup check test static_analysis offline run 

# Install any necessary dependencies for development and build
setup:
ifdef BUILD_REQ_PKGS
	brew install $(BUILD_REQ_PKGS)
else
	@echo "No dependencies to install or already installed"
endif

# For the install of dependencies 
deps:
	brew install $(BUILD_REQ_PKGS)
	brew install borkdude/brew/clj-kondo
	brew install git-lfs
	brew install ffmpeg
	brew install sox # brew install sox --with-lame --with-flac --with-libvorbis
	# brew install python3
	# pip3 install poetry
	# poetry install
	brew install portaudio

# Validate the project's structure and correctness
check:
	lein check

# Perform static code analysis
static_analysis:
	clj-kondo --lint $(SRC_DIR)

# Download dependencies and prepare the project for offline use
offline:
	lein offline

# Lint the code
lint: 
	echo "Linting the code"
	find . -name "*.clj" -exec clj-kondo --lint {} \;

# Run the project's tests
test: 
	echo "Running tests"
	clojure -M:test:runner


# Start the project 
run: 
	lein run -m $(PROJECT).core

# Interact with PostgreSQL through Babashka 
psql:
	$(BB) --classpath $(CLASSPATH) --main cljs.main -re psql -c "available-builds"

# Remove any build artifacts
clean:
	lein clean
	rm -rf audio.wav output.mp4 output.wav room.mp4 splash-2023.mp4 transcripts-test/ transcripts/

# Deploy the project to Clojars repository
deploy:
	lein deploy clojars

# Get all vidoes and summarize
summarize-videos:
	$(BB) --classpath $(CLASSPATH) --main cljs.main -re summarize-videos

# Room I
room-i:
	$(BB) --classpath $(CLASSPATH) --main cljs.main -re room-i

# Room II
room-ii:
	$(BB) --classpath $(CLASSPATH) --main cljs.main -re room-ii

# Room III
room-iii:
	$(BB) --classpath $(CLASSPATH) --main cljs.main -re room-iii

# Room IV
room-iv:
	$(BB) --classpath $(CLASSPATH) --main cljs.main -re room-iv

# Room XV
room-xv: 
	poetry run python summarize_video.py https://www.youtube.com/watch\?v\=e0V9-8unJbg

.PHONY: run-scripts
run-scripts:
	@echo "Running scripts..."
	clojure -M -m scripts.download-html
	clojure -M -m scripts.read-ics
	clojure -M -m scripts.gh-repo-create
	clojure -M -m scripts.clone-repos

# Output file
OUTFILE := splash-2023.mp4
STREAM_KEY := 2q9r-2q9r-2q9r-2q9r

record: # requires ffmpeg
	ffmpeg -f avfoundation -ac 2 -i :0 -c:a aac -ab 96k $(OUTFILE)

transcribe: # requires ffmpeg
	poetry run python transcribe.py $(OUTFILE)

whisper: # requires ffmpeg
	poetry run python transcribe.py $(OUTFILE) -w -m medium


test-transcribe:
	poetry run python transcribe.py

test-transcribe-model:
	poetry run python transcribe.py --whisper --model small

test-transcribe-duration:
	poetry run python transcribe.py --chunk-duration 60

test-transcribe-file:
	poetry run python transcribe.py --input file input/test.mp4

test-transcribe-phrase:
	poetry run python transcribe.py --phrase "test" 

test-transcribe-output:
	poetry run python transcribe.py --output-dir transcripts-test

test-transcribe-api-key:
	poetry run python transcribe.py --api-key $(ASSEMBLYAI_API_KEY)

record-with-ffmpeg:
	poetry run python record_with_ffmpeg.py
