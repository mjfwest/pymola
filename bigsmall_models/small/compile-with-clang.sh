clang -shared -fPIC -O0 SmallModel_variable_metadata.c -o SmallModel_variable_metadata.so
clang -shared -fPIC -O0 SmallModel_initial_residual.c -o SmallModel_initial_residual.so
clang -shared -fPIC -O0 SmallModel_dae_residual.c -o SmallModel_dae_residual.so
