SWIG_SOURCES = crfpp.i
pkgpython_PYTHON = crfpp.py
pkgpython_LTLIBRARIES = _crfpp.la
_crfpp_la_SOURCES = $(srcdir)/crfpp_wrap.cxx $(SWIG_SOURCES)
_crfpp_la_CPPFLAGS = $(SWIG_PYTHON_CPPFLAGS) -I$(top_srcdir)/src -shared
_crfpp_la_LDFLAGS = -module -avoid-version
_crfpp_la_LIBADD = $(top_srcdir)/src/libcrfpp.la

$(srcdir)/crfpp_wrap.cxx: $(SWIG_SOURCES)
	swig -python -shadow -c++ -I$(top_srcdir)/src -o $@ $<
