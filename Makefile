lib.name = SOFAlizer~

uname := $(shell uname -s)

.PHONY: all libmysofa 
all: libmysofa 

# Add a new target to build libsms
libmysofa:
	cd ./libmysofa && mkdir -p build && cd build && cmake -DBUILD_TESTS=OFF -DBUILD_STATIC_LIBS=OFF -DCODE_COVERAGE=OFF -DCMAKE_BUILD_TYPE=Release .. && cmake --build .

ifeq (MINGW,$(findstring MINGW,$(uname)))
	cp ./libmysofa/build/src/libmysofa.dll .
endif

class.sources = src/SOFAlizer~.c
cflags += -Wno-cast-function-type
ldlibs = -Llibmysofa/build/src -lmysofa
PDLIBBUILDER_DIR=./pd-lib-builder
include $(PDLIBBUILDER_DIR)/Makefile.pdlibbuilder

localdep_linux: 
	resources/localdeps/localdeps.linux.sh "./SOFAlizer~.${extension}"

localdep_windows: 
	resources/localdeps/localdeps.win.sh "./SOFAlizer~.${extension}"

localdep_macos: 
	resources/localdeps/localdeps.macos.sh "./SOFAlizer~.${extension}"
