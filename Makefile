lib.name = SOFAlizer~

.PHONY: all libmysofa 
all: libmysofa 

# Add a new target to build libsms
libmysofa:
	cd ./libmysofa && mkdir -p build && cd build && cmake -DCMAKE_BUILD_TYPE=Release .. && cmake --build . 

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
