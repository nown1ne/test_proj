cmake_minimum_required(VERSION 2.8.11)

include(CheckIncludeFileCXX)

if(DEFINED COOLPROP_INSTALL_PREFIX)
  #set(COOLPROP_INSTALL_PREFIX ${CMAKE_CURRENT_SOURCE_DIR}/install_root)
  message(STATUS "COOLPROP_INSTALL_PREFIX=${COOLPROP_INSTALL_PREFIX}")
else()
  set(COOLPROP_INSTALL_PREFIX ${CMAKE_CURRENT_SOURCE_DIR}/install_root)
  message(STATUS "COOLPROP_INSTALL_PREFIX=${COOLPROP_INSTALL_PREFIX}")
endif()

set(CMAKE_INSTALL_PREFIX
    ${COOLPROP_INSTALL_PREFIX}
    CACHE PATH "default install path" FORCE)

#######################################
#           BUILD OPTIONS             #
#-------------------------------------#
# These options are available to be   #
# modified in the build process.      #
# packages may want to modify these   #
# to suit, or just leave as defaults. #
#######################################

option(COOLPROP_STATIC_LIBRARY "Build CoolProp as a static library (.lib, .a)"
       OFF)

option(COOLPROP_SHARED_LIBRARY "Build CoolProp as a shared library (.dll, .so)"
       OFF)

option(COOLPROP_OBJECT_LIBRARY
       "Build CoolProp objects, but do not link them (.obj, .o)" OFF)

option(COOLPROP_EES_MODULE "Build the EES module" OFF)

option(COOLPROP_WINDOWS_PACKAGE "Build the Windows installer" OFF)

option(BUILD_TESTING "Enable testing for this given builder" OFF)

option(FORCE_BITNESS_32 "Force a 32bit build regardless of the host" OFF)

option(FORCE_BITNESS_64 "Force a 64bit build regardless of the host" OFF)

option(FORCE_BITNESS_NATIVE
       "Force a native bitness build regardless of the host" OFF)

option(COOLPROP_RELEASE "Optimize the builds with the release specs" OFF)

option(COOLPROP_DEBUG "Make a debug build" OFF)

option(COOLPROP_SMATH_WORK_INPLACE "Build SMath wrapper in source directory"
       OFF)

option(
  COOLPROP_MSVC_STATIC
  "Statically link Microsoft Standard library removes dependency on MSVCRXXX.dll."
  OFF)

option(
  COOLPROP_MSVC_DYNAMIC
  "Dynamically link Microsoft Standard library to integrate with other builds."
  OFF)

option(
  COOLPROP_MSVC_DEBUG
  "Link the debug version of Microsoft Standard library to the debug builds."
  ON)

option(COOLPROP_NO_EXAMPLES
       "Do not generate example code, does only apply to some wrappers." OFF)

#option (DARWIN_USE_LIBCPP
#        "On Darwin systems, compile and link with -std=libc++ instead of the default -std=libstdc++"
#        ON)

# Force C++11 since lambdas are used in CPStrings.h
set(CMAKE_CXX_STANDARD 11)

# see
# https://stackoverflow.com/questions/52509602/cant-compile-c-program-on-a-mac-after-upgrade-to-mojave
# https://support.enthought.com/hc/en-us/articles/204469410-OS-X-GCC-Clang-and-Cython-in-10-9-Mavericks
# https://github.com/pandas-dev/pandas/pull/24274/files
# https://github.com/explosion/thinc/pull/84/files
# https://github.com/jlfaucher/builder/commit/d144d3a695949f90c5e2acff4dfd94fdcf8dcdfa
# https://github.com/CoolProp/CoolProp/issues/1778
# https://gitlab.kitware.com/cmake/cmake/issues/18396
if(DEFINED DARWIN_USE_LIBCPP)
  if(DARWIN_USE_LIBCPP)
    set(CMAKE_OSX_DEPLOYMENT_TARGET
        "10.9"
        CACHE STRING "Minimum OS X deployment version")
    set(OSX_COMPILE_FLAGS "${OSX_COMPILE_FLAGS} -stdlib=libc++")
    set(OSX_COMPILE_FLAGS "${OSX_COMPILE_FLAGS} -mmacosx-version-min=10.9")
    set(OSX_COMPILE_FLAGS "${OSX_COMPILE_FLAGS} -std=c++11")
    set(OSX_LINK_FLAGS "${OSX_LINK_FLAGS} -lc++")
    set(OSX_LINK_FLAGS "${OSX_LINK_FLAGS} -nodefaultlibs")
    set(CMAKE_XCODE_ATTRIBUTE_CLANG_CXX_LIBRARY "libc++")
  else(DARWIN_USE_LIBCPP)
    set(CMAKE_OSX_DEPLOYMENT_TARGET
        "10.5"
        CACHE STRING "Minimum OS X deployment version") # Default is 10.7
    set(OSX_COMPILE_FLAGS "${OSX_COMPILE_FLAGS} -stdlib=libstdc++")
    set(OSX_COMPILE_FLAGS "${OSX_COMPILE_FLAGS} -mmacosx-version-min=10.5")
    set(OSX_LINK_FLAGS "${OSX_LINK_FLAGS} -lstdc++")
    set(CMAKE_XCODE_ATTRIBUTE_CLANG_CXX_LIBRARY "libstdc++")
  endif(DARWIN_USE_LIBCPP)
  message(STATUS "DARWIN_USE_LIBCPP was set added some flags:")
  message(STATUS "  OSX_COMPILE_FLAGS: ${OSX_COMPILE_FLAGS}")
  message(STATUS "     OSX_LINK_FLAGS: ${OSX_LINK_FLAGS}")
else(DEFINED DARWIN_USE_LIBCPP)
  if("${CMAKE_SYSTEM_NAME}" MATCHES "Darwin")
    message(STATUS "OSX build detected:")
    message(
      STATUS "  You might want to pass the -DDARWIN_USE_LIBCPP=ON/OFF parameter"
    )
    message(STATUS "  to enable or disable different C++ standard libraries.")
    message(
      STATUS
        "  You can also specify the environment variable MACOSX_DEPLOYMENT_TARGET=10.9 to force clang builds."
    )
  endif("${CMAKE_SYSTEM_NAME}" MATCHES "Darwin")
endif(DEFINED DARWIN_USE_LIBCPP)

#if("${CMAKE_SYSTEM_NAME}" MATCHES "Darwin")
#  set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS}${OSX_COMPILE_FLAGS}")
#  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS}${OSX_COMPILE_FLAGS}")
#endif()
# Alternatively you could use
# set_target_properties(TARGET_NAME PROPERTIES APPEND_STRING PROPERTY COMPILE_FLAGS "-mmacosx-version-min=10.5")
# set_target_properties(TARGET_NAME PROPERTIES APPEND_STRING PROPERTY LINK_FLAGS "-mmacosx-version-min=10.5")

#######################################
#         PROJECT INFORMATION         #
#-------------------------------------#
# This CMakeLists.txt file is for the #
# CoolProp thermodynamic library      #
# written by Ian Bell. The following  #
# section contains project and        #
# version information.                #
#######################################

# Project name
set(project_name "CoolProp")
set(app_name ${project_name})
project(${project_name})

# Project version
set(COOLPROP_VERSION_MAJOR 6)
set(COOLPROP_VERSION_MINOR 4)
set(COOLPROP_VERSION_PATCH 2)
set(COOLPROP_VERSION_REVISION dev)
set(COOLPROP_VERSION
    "${COOLPROP_VERSION_MAJOR}.${COOLPROP_VERSION_MINOR}.${COOLPROP_VERSION_PATCH}${COOLPROP_VERSION_REVISION}"
)
message(STATUS "CoolProp version: ${COOLPROP_VERSION}")

string(TIMESTAMP COOLPROP_YEAR 2010-%Y)
#set ( COOLPROP_YEAR "2010-2016" )
set(COOLPROP_PUBLISHER "The CoolProp developers")

# Add definitions to silence warnings in MSVC2017 related to shared ptr code.
#if (MSVC_VERSION GREATER_EQUAL 1910 AND MSVC_VERSION LESS_EQUAL 1919) # OR MSVC_TOOLSET_VERSION EQUAL 141) # This requuires CMake >= 3.7
#  add_definitions(-D_SILENCE_TR1_NAMESPACE_DEPRECATION_WARNING)
#endif (MSVC_VERSION GREATER_EQUAL 1910 AND MSVC_VERSION LESS_EQUAL 1919)

if(MSVC
   AND NOT (MSVC_VERSION LESS 1910)
   AND NOT (MSVC_VERSION GREATER 1919))
  add_definitions(-D_SILENCE_TR1_NAMESPACE_DEPRECATION_WARNING)
endif()

if(COOLPROP_RELEASE AND COOLPROP_DEBUG)
  message(FATAL_ERROR "You can only make a release OR and debug build.")
endif()
if(COOLPROP_RELEASE)
  set(CMAKE_BUILD_TYPE Release)
elseif(COOLPROP_DEBUG)
  set(CMAKE_BUILD_TYPE Debug)
  #ELSEIF ("${CMAKE_BUILD_TYPE}" STREQUAL "")
  #  IF("${COOLPROP_VERSION_REVISION}" STREQUAL "dev")
  #    SET(CMAKE_BUILD_TYPE Debug)
  #  ELSE ()
  #    SET(CMAKE_BUILD_TYPE Release)
  #  ENDIF()
endif()

if(COOLPROP_MSVC_STATIC)
  set(COOLPROP_MSVC_REL "/MT")
  if(COOLPROP_MSVC_DEBUG)
    set(COOLPROP_MSVC_DBG "/MTd")
  else()
    set(COOLPROP_MSVC_DBG "/MT")
  endif()
elseif(COOLPROP_MSVC_DYNAMIC)
  set(COOLPROP_MSVC_REL "/MD")
  if(COOLPROP_MSVC_DEBUG)
    set(COOLPROP_MSVC_DBG "/MDd")
  else()
    set(COOLPROP_MSVC_DBG "/MD")
  endif()
else(COOLPROP_MSVC_DYNAMIC)
  set(COOLPROP_MSVC_REL "IGNORE")
  set(COOLPROP_MSVC_DBG "IGNORE")
endif()

set(COOLPROP_MSVC_ALL "/MTd" "/MT" "/MDd" "/MD"
)# order matters "/MXd" before "/MX"

#######################################
#         FIND ALL SOURCES            #
#-------------------------------------#
# The project is organised with       #
# split includes and source folders   #
# this makes it easier for developers #
# to quickly find relevant includes.  #
# This section finds all sources,     #
# headers and corresponding dirs.     #
#######################################

# These backends will be compiled in
set(COOLPROP_ENABLED_BACKENDS
    Cubics
    IF97
    Helmholtz
    REFPROP
    Incompressible
    Tabular
    PCSAFT)

# Get everything in the src/ directory (always), but not recursive
file(GLOB APP_SOURCES "${CMAKE_CURRENT_SOURCE_DIR}/src/*.cpp")

# For each enabled backend, grab its files
foreach(backend ${COOLPROP_ENABLED_BACKENDS})
  file(GLOB_RECURSE BACKEND_SOURCES
       "${CMAKE_CURRENT_SOURCE_DIR}/src/Backends/${backend}/*.cpp")
  list(APPEND APP_SOURCES ${BACKEND_SOURCES})
endforeach()

## You can exclude this file, in case you want to run your own tests or use Catch
list(REMOVE_ITEM APP_SOURCES "${CMAKE_CURRENT_SOURCE_DIR}/src/Tests/Tests.cpp")
list(REMOVE_ITEM APP_SOURCES
     "${CMAKE_CURRENT_SOURCE_DIR}/src/Tests/CoolProp-Tests.cpp")

## This file is only needed for the library, normal builds do not need it.
list(REMOVE_ITEM APP_SOURCES "${CMAKE_CURRENT_SOURCE_DIR}/src/CoolPropLib.cpp")

set(APP_INCLUDE_DIRS "${CMAKE_CURRENT_SOURCE_DIR}")
list(APPEND APP_INCLUDE_DIRS "${CMAKE_CURRENT_SOURCE_DIR}/externals/Eigen")
list(APPEND APP_INCLUDE_DIRS
     "${CMAKE_CURRENT_SOURCE_DIR}/externals/msgpack-c/include")
list(APPEND APP_INCLUDE_DIRS
     "${CMAKE_CURRENT_SOURCE_DIR}/externals/fmtlib/include")
list(APPEND APP_INCLUDE_DIRS "${CMAKE_CURRENT_SOURCE_DIR}/externals/fmtlib"
)# should be deprecated
list(APPEND APP_INCLUDE_DIRS "${CMAKE_CURRENT_SOURCE_DIR}/include")
list(APPEND APP_INCLUDE_DIRS "${CMAKE_CURRENT_SOURCE_DIR}/src")

include_directories(${APP_INCLUDE_DIRS})

set(SWIG_DEPENDENCIES
    ${CMAKE_CURRENT_SOURCE_DIR}/include/DataStructures.h
    ${CMAKE_CURRENT_SOURCE_DIR}/include/CoolProp.h
    ${CMAKE_CURRENT_SOURCE_DIR}/include/AbstractState.h
    ${CMAKE_CURRENT_SOURCE_DIR}/include/Configuration.h
    ${CMAKE_CURRENT_SOURCE_DIR}/include/PhaseEnvelope.h)

set(COOLPROP_APP_SOURCES
    ${APP_SOURCES}
    CACHE LIST "List of CPP sources needed for CoolProp")
set(COOLPROP_INCLUDE_DIRECTORIES
    ${APP_INCLUDE_DIRS}
    CACHE LIST "List of include directories needed for CoolProp")

#######################################
#         REQUIRED MODULES            #
#-------------------------------------#
# CoolProp requires some standard OS  #
# features, these include:            #
# DL (CMAKE_DL_LIBS) for REFPROP      #
#######################################
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH}
                      "${CMAKE_CURRENT_SOURCE_DIR}/dev/cmake/Modules/")

set(Python_ADDITIONAL_VERSIONS 2.7 2.6 2.5 2.4)
find_package(PythonInterp 2.7)
if(NOT PYTHON_EXECUTABLE)
  message(STATUS "Looking for Python")
  find_package(Python COMPONENTS Interpreter)
endif()
if(NOT PYTHON_EXECUTABLE)
  message(STATUS "Looking for Python2")
  find_package(Python2 COMPONENTS Interpreter)
  if(Python2_Interpreter_FOUND)
    set(PYTHON_EXECUTABLE ${Python2_EXECUTABLE})
  endif()
endif()
if(NOT PYTHON_EXECUTABLE)
  message(STATUS "Looking for Python3")
  find_package(Python3 COMPONENTS Interpreter)
  if(Python3_Interpreter_FOUND)
    set(PYTHON_EXECUTABLE ${Python3_EXECUTABLE})
  endif()
endif()
if(NOT PYTHON_EXECUTABLE)
  message(WARNING "Could not find Python, be prepared for errors.")
endif()


if(COOLPROP_LIBREOFFICE_MODULE)

  if("${LO_PROGRAM_PATH}" STREQUAL "")
    message(
      FATAL_ERROR
        "You must provide the path to LibreOffice programs, something like -DLO_PROGRAM_PATH=/usr/lib/libreoffice/program"
    )
  else()
    message(STATUS "LO_PROGRAM_PATH: ${LO_PROGRAM_PATH}")
  endif()

  if("${LO_SDK_PATH}" STREQUAL "")
    message(
      FATAL_ERROR
        "You must provide the path to LibreOffice SDK, something like -DLO_SDK_PATH=/usr/lib/libreoffice/sdk"
    )
  else()
    message(STATUS "LO_SDK_PATH: ${LO_SDK_PATH}")
  endif()

  add_custom_target(CoolPropLibreOfficeAddin)

  # set paths for LibreOffice tools
  set(LO_IDLC "${LO_SDK_PATH}/bin/idlc")
  set(LO_REGMERGE "${LO_PROGRAM_PATH}/regmerge")
  set(COOLPROP_LIBREOFFICE_TMP_DIR "${CMAKE_CURRENT_BINARY_DIR}/LibreOffice")

  # set version strings for LibreOffice extension
  configure_file(
    "${CMAKE_CURRENT_SOURCE_DIR}/wrappers/LibreOffice/src/description.xml.in"
    "${COOLPROP_LIBREOFFICE_TMP_DIR}/src/description.xml")
  configure_file(
    "${CMAKE_CURRENT_SOURCE_DIR}/wrappers/LibreOffice/src/scripts/scripts.py.in"
    "${COOLPROP_LIBREOFFICE_TMP_DIR}/src/scripts/scripts.py")

  add_custom_command(
    TARGET CoolPropLibreOfficeAddin
    # copy source files to build directory
    COMMAND
      ${CMAKE_COMMAND} ARGS "-E" "copy_directory"
      "${CMAKE_CURRENT_SOURCE_DIR}/wrappers/LibreOffice/src"
      "${COOLPROP_LIBREOFFICE_TMP_DIR}/src"
    COMMAND
      ${CMAKE_COMMAND} ARGS "-E" "remove"
      "${COOLPROP_LIBREOFFICE_TMP_DIR}/src/description.xml.in"
      "${COOLPROP_LIBREOFFICE_TMP_DIR}/src/scripts/scripts.py.in"
    # rebuild the registry database file (rdb)
    COMMAND ${LO_IDLC} XCoolProp.idl -I. -I${LO_SDK_PATH}/idl -O. XCoolProp.idl
    COMMAND ${LO_REGMERGE} XCoolProp.rdb /UCR XCoolProp.urd
    COMMAND ${CMAKE_COMMAND} ARGS "-E" "remove" XCoolProp.urd
    # download and bundle latest Python pip package (py2.py3, platform independent)
    COMMAND pip download pip -d pythonpath
    COMMAND 7z x "./pythonpath/pip-*.whl" -y -opythonpath
    # download and bundle latest Python certifi package (py2.py3, platform independent)
    COMMAND pip download certifi -d pythonpath
    COMMAND 7z x "./pythonpath/certifi-*.whl" -y -opythonpath
    # add license file
    COMMAND ${CMAKE_COMMAND} ARGS "-E" "make_directory"
            "${COOLPROP_LIBREOFFICE_TMP_DIR}/src/license"
    COMMAND
      ${CMAKE_COMMAND} ARGS "-E" "copy" "${CMAKE_CURRENT_SOURCE_DIR}/LICENSE"
      "${COOLPROP_LIBREOFFICE_TMP_DIR}/src/license/."
    # package complete folder to extension
    COMMAND 7z a -tzip "../CoolProp.oxt"
    # copy example spreadsheet file
    COMMAND
      ${CMAKE_COMMAND} ARGS "-E" "copy"
      "${CMAKE_CURRENT_SOURCE_DIR}/wrappers/LibreOffice/Test.ods"
      "${COOLPROP_LIBREOFFICE_TMP_DIR}/."
    WORKING_DIRECTORY ${COOLPROP_LIBREOFFICE_TMP_DIR}/src
    COMMENT "Building LibreOffice wrapper"
    VERBATIM)
endif()