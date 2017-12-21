from conans import ConanFile, CMake, tools
import os, shutil

class Bzip2Conan(ConanFile):
    name = "bzip2"
    version = "1.0.6"
    description = 'bzip2 is a freely available, patent free (see below), high-quality data compressor.'
    license = "BSD-style license"
    url = "https://github.com/ulricheck/conan-bzip2"
    settings = "os", "compiler", "arch", "build_type"
    generators = []

    def source(self):
        tools.download('http://www.bzip.org/%s/bzip2-%s.tar.gz' % (self.version, self.version), 'bzip2.tar.gz')
        tools.unzip('bzip2.tar.gz')
        os.unlink('bzip2.tar.gz')
        os.rename('bzip2-%s' % self.version, self.name)
        
        if self.settings.os == "Windows":
            tools.replace_in_file('bzip2/makefile.msc', 'CFLAGS= -DWIN32 -MD -Ox -D_FILE_OFFSET_BITS=64 -nologo', '''
!IF "$(CFG)" == "debug"
CFG_CFLAGS=-nologo -DWIN32 -D_FILE_OFFSET_BITS=64 -fp:fast -arch:AVX -Zi -Fdlibbz2.pdb -MDd -Od 
CFG_LDFLAGS=
!ELSE
CFG_CFLAGS=-nologo -DWIN32 -D_FILE_OFFSET_BITS=64 -fp:fast -arch:AVX -Zi -Fdlibbz2.pdb -MD -Ox -Oi -Ot -GT -GL
CFG_LDFLAGS=-LTCG
!ENDIF''')
            tools.replace_in_file('bzip2/makefile.msc', '$(CFLAGS)', '$(CFG_CFLAGS)')
            tools.replace_in_file('bzip2/makefile.msc', 'lib /out:libbz2.lib $(OBJS)', 'lib $(CFG_LDFLAGS) /out:libbz2.lib $(OBJS)')
            tools.replace_in_file('bzip2/makefile.msc', 'del *.obj', 'del *.obj\n\tdel *.pdb')

    def configure(self):
        del self.settings.compiler.libcxx

    def build(self):
        config = str(self.settings.build_type).lower()
        with tools.chdir('bzip2'):
            if self.settings.os == "Windows":
                self.run('nmake -f makefile.msc CFG=%s' % config)
            else:
                self.run('make -f Makefile CFG=%s' % config)

    def package(self):
        self.copy("bzlib.h", dst="include", src="bzip2", keep_path=False)
        self.copy("libbz2.lib", dst="lib", src='bzip2', keep_path=False)
        self.copy("libbz2.pdb", dst="lib", src='bzip2', keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["libbz2"]
