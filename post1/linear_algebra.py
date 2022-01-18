#%%
from julia import Main
import numpy as np
%load_ext julia.magic

#%%
Main.eval('A = rand(3, 3)')
Main.b = Main.eval('A * ones(3)')
%julia x = A \ b

#%%
np.linalg.norm(np.matmul(Main.A, Main.x) - Main.b)
# %%
Main.eval('A = rand(1000, 1000)')
Main.eval('b = A * ones(1000)')
#%%
%%timeit
Main.eval('x = A \ b')
# %%
%%timeit
np.linalg.solve(Main.A, Main.b)