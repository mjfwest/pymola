clang -shared -fPIC -O0 BigModel_variable_metadata.c -o BigModel_variable_metadata.so
clang -shared -fPIC -O0 BigModel_initial_residual.c -o BigModel_initial_residual.so
clang -shared -fPIC -O0 BigModel_dae_residual.c -o BigModel_dae_residual.so
