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