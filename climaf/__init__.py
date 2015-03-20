"""
Climaf python modules are :
 - api       : the user interface, or Application Program Interface
 - classes   : define basic classes
 - dataloc   : handling data location and data access
 - operators : handling external scripts and binaries
 - driver    : gluing all that together, and interpreting commands

CliMAF user's are interested only by module ``api``, while CliMAF developpers may wish to
know more about the other modules, but ``driver``, which is rather for CliMAF wizzard's use

"""

# Created : S.Senesi - 2014

# The CliMAF software is an environment for Climate Model Assessment. It
# has been developped mainly by CNRM-GAME (Meteo-France and CNRS), and
# by IPSL, in the context of the `CONVERGENCE project
# <http://convergence.ipsl.fr/>`_, funded by The
# French 'Agence Nationale de la Recherche' under grant #
# ANR-13-MONU-0008-01
# 
# This software is governed by the CeCILL-C license under French law and
# biding by the rules of distribution of free software. The CeCILL-C
# licence is a free software license,explicitly compatible with the GNU
# GPL (see http://www.gnu.org/licenses/license-list.en.html#CeCILL)


__all__=[ "api", "classes", "operators", "cache" , "driver" , "dataloc" ]
import posixpath
