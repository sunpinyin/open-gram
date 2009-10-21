bin_PROGRAMS = crf_learn crf_test crf_seg

AUTOMAKE_OPTIONS = no-dependencies
lib_LTLIBRARIES = libcrfpp.la
libcrfpp_la_SOURCES = crfpp.h thread.h libcrfpp.cpp lbfgs.cpp scoped_ptr.h param.cpp param.h encoder.cpp feature.cpp stream_wrapper.h \
                      feature_cache.cpp feature_index.cpp node.cpp path.cpp tagger.cpp \
		      common.h darts.h encoder.h feature_cache.h feature_index.h \
                      freelist.h lbfgs.h mmap.h node.h path.h tagger.h timer.h
include_HEADERS = crfpp.h

crf_learn_SOURCES = crf_learn.cpp 
crf_learn_LDADD = libcrfpp.la

crf_test_SOURCES = crf_test.cpp 
crf_test_LDADD = libcrfpp.la 

crf_seg_SOURCES = crf_seg.cpp
crf_seg_LDADD = libcrfpp.la
