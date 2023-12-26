# From https://github.com/scverse/scanpy/blob/d7e13025b931ad4afd03b4344ef5ff4a46f78b2b/scanpy/_settings.py
# Under BSD 3-Clause License
# Copyright (c) 2017 F. Alexander Wolf, P. Angerer, Theis Lab
import builtins

is_run_from_ipython = getattr(builtins, "__IPYTHON__", False)
