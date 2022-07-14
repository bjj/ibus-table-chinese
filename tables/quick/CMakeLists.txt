IF(ENABLE_TABLE_PREPROCESS)
SET(EXT out)
PREPROCESS_TABLE(${EXT}
    "${CMAKE_SOURCE_DIR}/tables/quick/quick3.txt"
    "${CMAKE_SOURCE_DIR}/tables/quick/quick5.txt"
    "${CMAKE_SOURCE_DIR}/tables/quick/quick-classic.txt")
ELSE(ENABLE_TABLE_PREPROCESS)
SET(EXT txt)
ENDIF(ENABLE_TABLE_PREPROCESS)

CONVERT_DB(quick
    "${CMAKE_SOURCE_DIR}/tables/quick/quick3.${EXT}"
    "${CMAKE_SOURCE_DIR}/tables/quick/quick5.${EXT}"
    "${CMAKE_SOURCE_DIR}/tables/quick/quick-classic.${EXT}")

