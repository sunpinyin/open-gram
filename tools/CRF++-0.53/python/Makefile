CXX = g++
CXXFLAGS = -std=gnu++11 -fPIC -shared -O2 -DHAVE_CONFIG_H -I../src
SRCS = libcrfpp.cpp lbfgs.cpp param.cpp encoder.cpp feature.cpp \
	feature_cache.cpp feature_index.cpp node.cpp path.cpp tagger.cpp

libcrfpp.so: $(addprefix ../src/,$(SRCS)) ../src/config.h
	$(CXX) $(CXXFLAGS) -o $@ $(addprefix ../src/,$(SRCS)) -lpthread -lm

.PHONY: clean
clean:
	rm -f libcrfpp.so
