-------------------------------------------------------------
Functions returning ClimAF objects 
-------------------------------------------------------------

.. default-domain:: python


Except for the first three paragraphs, this section is for advanced use. As a first step, you should consider using
the built-in data definitions described at :py:mod:`~climaf.projects`. 
You may need to come back to this section for reference


cscalar : returns a scalar value (float) in python (using cMA)
------------------------------------------------------------------------------------------------

.. autofunction:: climaf.functions.cscalar


fadd : add two CliMAF objects or a CliMAF object and a constant 
------------------------------------------------------------------------------------------------

.. autofunction:: climaf.functions.fadd


fsub : subtract two CliMAF objects or a CliMAF object and a constant
------------------------------------------------------------------------------------------------

.. autofunction:: climaf.functions.fsub


fmul : multiply two CliMAF objects or a CliMAF object and a constant
------------------------------------------------------------------------------------------------

.. autofunction:: climaf.functions.fmul


fdiv : divide two CliMAF objects or a CliMAF object and a constant
------------------------------------------------------------------------------------------------

.. autofunction:: climaf.functions.fdiv


apply_scale_offset : Returns a CliMAF object after applying a scale and offset
------------------------------------------------------------------------------------------------

.. autofunction:: climaf.functions.apply_scale_offset


diff_regrid : Regrids dat1 on dat2 and returns the difference between dat1 and dat2
------------------------------------------------------------------------------------------------

.. autofunction:: climaf.functions.diff_regrid


diff_regridn : Regrids dat1 and dat2 on a chosen cdogrid (default is n90) and returns the difference between dat1 and dat2
-----------------------------------------------------------------------------------------------------------------------------

.. autofunction:: climaf.functions.diff_regridn


annual_cycle : Computes the annual cycle as the 12 climatological months of dat
------------------------------------------------------------------------------------------------

.. autofunction:: climaf.functions.annual_cycle


clim_average : Computes climatological averages on the annual cycle of a dataset
------------------------------------------------------------------------------------------------

.. autofunction:: climaf.functions.clim_average


lonlatvert_interpolation : Interpolates a lon/lat/pres field (two possible ways) 
----------------------------------------------------------------------------------------------------------

.. autofunction:: climaf.functions.lonlatvert_interpolation


zonmean : Return the zonal mean field of dat
------------------------------------------------------------------------------------------------

.. autofunction:: climaf.functions.zonmean


diff_zonmean : Returns the zonal mean bias of dat1 against dat2 (based on lonlatpres_interpolation)
-------------------------------------------------------------------------------------------------------

.. autofunction:: climaf.functions.diff_zonmean



