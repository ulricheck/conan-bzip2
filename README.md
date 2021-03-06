# conan-BZip2

[Conan.io](https://conan.io) package for bzip2 library. 

The packages generated with this **conanfile** can be found in [conan.io](https://conan.io/source/bzip2/1.0.6/ulricheck/stable).

## Build packages

    $ pip install conan_package_tools
    $ python build.py
    
## Upload packages to server

    $ conan upload bzip2/1.0.6@ulricheck/stable --all
    
## Reuse the packages

### Basic setup

    $ conan install bzip2/1.0.6@ulricheck/stable
    
### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*
    
    [requires]
    bzip2/1.0.6@ulricheck/stable

    [options]
    bzip2:shared=true # false
    
    [generators]
    txt
    cmake

Complete the installation of requirements for your project running:</small></span>

    conan install . 

Project setup installs the library (and all his dependencies) and generates the files *conanbuildinfo.txt* and *conanbuildinfo.cmake* with all the paths and variables that you need to link with your dependencies.
