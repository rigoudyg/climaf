tableau : generates a table as used by cpage with n_lin rows and n_col columns.
---------------------------------------------------------------------------------------

Generates a table as used by cpage with n_lin rows and n_col columns.
Useful to generate a table and fill it with plots created in a loop.
The table is filled with None.

**Provider / contact** : climaf at meteo dot fr

**Input** : n_lin and n_col (integers)

**Mandatory argument**: 

None

**Output** : an array with n_lin lines and n_col columns (typically used for fig_lines in cpage)

**Climaf call example** ::
 
  >>> my_table = tableau(2,3)

**Side effects** : none


