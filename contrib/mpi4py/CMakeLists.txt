set(MPI4PY_DIR mpi4py-1.3) 
set(MPI4PY_SOURCES ${MPI4PY_DIR}/src/MPI.c)
set(DL_SOURCES ${MPI4PY_DIR}/src/dynload.c)

include_directories(${CMAKE_CURRENT_SOURCE_DIR}/${MPI4PY_DIR}/src)

add_library(MPI ${MPI4PY_SOURCES})
target_link_libraries(MPI ${PYTHON_LIBRARIES} ${VAMPIRTRACE_LIBRARIES} ${MPI_LIBRARIES})
set_target_properties(MPI PROPERTIES PREFIX "" SUFFIX ".so")

add_library(dl ${DL_SOURCES})
target_link_libraries(dl ${PYTHON_LIBRARIES} ${VAMPIRTRACE_LIBRARIES} ${MPI_LIBRARIES})
set_target_properties(dl PROPERTIES PREFIX "" SUFFIX ".so")

install(TARGETS MPI LIBRARY DESTINATION ${PYTHON_INSTDIR}/mpi4py ARCHIVE DESTINATION ${LIB})
install(FILES __init__.py DESTINATION ${PYTHON_INSTDIR}/mpi4py)
