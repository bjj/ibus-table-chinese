IF(ENABLE_TABLE_PREPROCESS)
SET(EXT out)
PREPROCESS_TABLE(${EXT}
    "${CMAKE_SOURCE_DIR}/tables/cangjie/cangjie3.txt"
    "${CMAKE_SOURCE_DIR}/tables/cangjie/cangjie5.txt"
    "${CMAKE_SOURCE_DIR}/tables/cangjie/cangjie-big.txt")
ELSE(ENABLE_TABLE_PREPROCESS)
SET(EXT txt)
ENDIF(ENABLE_TABLE_PREPROCESS)

CONVERT_DB(cangjie
    "${CMAKE_SOURCE_DIR}/tables/cangjie/cangjie3.${EXT}"
    "${CMAKE_SOURCE_DIR}/tables/cangjie/cangjie5.${EXT}"
    "${CMAKE_SOURCE_DIR}/tables/cangjie/cangjie-big.${EXT}")

