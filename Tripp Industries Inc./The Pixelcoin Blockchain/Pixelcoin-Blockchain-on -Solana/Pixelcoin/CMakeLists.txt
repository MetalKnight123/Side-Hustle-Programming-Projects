cmake_minimum_required(VERSION 3.16)
project(Pixelcoin)

set(CMAKE_CXX_STANDARD 17)

add_library(Pixelcoin STATIC
    src/Blockchain.cpp
    src/Block.cpp
    src/Transaction.cpp
    src/MergeSort.cpp
)

target_include_directories(Pixelcoin PUBLIC include)
