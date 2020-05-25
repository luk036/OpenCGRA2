"""
==========================================================================
PseudoCGRA_test.py
==========================================================================
Test cases for CGRAs with pseudo data/config memory.

Author : Cheng Tan
  Date : Dec 28, 2019

"""

from pymtl3 import *
from pymtl3.stdlib.test           import TestSinkCL
from pymtl3.stdlib.test.test_srcs import TestSrcRTL

from ...lib.opt_type              import *
from ...lib.messages              import *
from ...lib.ctrl_helper           import *

from ...fu.flexible.FlexibleFu    import FlexibleFu
from ...fu.single.Alu             import Alu
from ...fu.single.MemUnit         import MemUnit
from ...fu.double.SeqMulAlu       import SeqMulAlu
from ..SystolicCL                 import SystolicCL

import os

#-------------------------------------------------------------------------
# Test harness
#-------------------------------------------------------------------------

class TestHarness( Component ):

  def construct( s, DUT, FunctionUnit, FuList, DataType, CtrlType,
                 width, height, ctrl_mem_size, data_mem_size,
                 src_opt, preload_data, preload_const ):

    s.num_tiles = width * height
    AddrType = mk_bits( clog2( ctrl_mem_size ) )

    s.dut = DUT( FunctionUnit, FuList, DataType, CtrlType, width, height,
                 ctrl_mem_size, data_mem_size, len( src_opt ), src_opt,
                 preload_data, preload_const )

#  def done( s ):
#    done = True
#    for i in range( s.num_tiles  ):
#      if not s.src_opt[i].done():
#        done = False
#        break
#    return done

  def line_trace( s ):
    return s.dut.line_trace()

def run_sim( test_harness, max_cycles=6 ):
  test_harness.elaborate()
  test_harness.apply( SimulationPass() )
  test_harness.sim_reset()

  # Run simulation

  ncycles = 0
  print()
  print( "{}:{}".format( ncycles, test_harness.line_trace() ))
  while ncycles < max_cycles:
    test_harness.tick()
    ncycles += 1
    print( "{}:{}".format( ncycles, test_harness.line_trace() ))

  # Check timeout

#  assert ncycles < max_cycles

  test_harness.tick()
  test_harness.tick()
  test_harness.tick()
# ------------------------------------------------------------------
# To emulate systolic array
# left bottom is 0, 0
# right top   is 1, 1
# 1: North, 2: South, 3: West, 4: East
# 5 - 8: registers
# ------------------------------------------------------------------
def test_systolic_2x2():
  num_tile_inports  = 4
  num_tile_outports = 4
  num_xbar_inports  = 6
  num_xbar_outports = 8
  ctrl_mem_size     = 8
  width  = 2
  height = 3
  RouteType     = mk_bits( clog2( num_xbar_inports + 1 ) )
  AddrType      = mk_bits( clog2( ctrl_mem_size ) )
  num_tiles     = width * height
  ctrl_mem_size = 3
  data_mem_size = 10
  DUT           = SystolicCL
  FunctionUnit  = FlexibleFu
  FuList        = [Alu, MemUnit, SeqMulAlu]
  DataType      = mk_data( 16, 1 )
  CtrlType      = mk_ctrl( num_xbar_inports, num_xbar_outports )
  src_opt       = [[CtrlType( OPT_LD_CONST, [ 
                    RouteType(5), RouteType(0), RouteType(0), RouteType(0),
                    RouteType(0), RouteType(0), RouteType(0), RouteType(0)] ),
                    CtrlType( OPT_LD_CONST, [
                    RouteType(5), RouteType(0), RouteType(0), RouteType(0),
                    RouteType(0), RouteType(0), RouteType(0), RouteType(0)] ),
                    CtrlType( OPT_LD_CONST, [
                    RouteType(5), RouteType(0), RouteType(0), RouteType(0),
                    RouteType(0), RouteType(0), RouteType(0), RouteType(0)] ),
                   ],
                   [CtrlType( OPT_LD_CONST, [ 
                    RouteType(5), RouteType(5), RouteType(5), RouteType(5),
                    RouteType(5), RouteType(5), RouteType(5), RouteType(5)] ),
                    CtrlType( OPT_LD_CONST, [
                    RouteType(5), RouteType(5), RouteType(5), RouteType(5),
                    RouteType(5), RouteType(5), RouteType(5), RouteType(5)] ),
                    CtrlType( OPT_LD_CONST, [
                    RouteType(5), RouteType(5), RouteType(5), RouteType(5),
                    RouteType(5), RouteType(5), RouteType(5), RouteType(5)] ),
                   ],
                   [CtrlType( OPT_NAH, [ 
                    RouteType(2), RouteType(2), RouteType(2), RouteType(2),
                    RouteType(2), RouteType(2), RouteType(2), RouteType(2)] ),
                    CtrlType( OPT_INC, [
                    RouteType(2), RouteType(2), RouteType(2), RouteType(2),
                    RouteType(2), RouteType(2), RouteType(2), RouteType(2)] ),
                    CtrlType( OPT_INC, [
                    RouteType(2), RouteType(2), RouteType(2), RouteType(2),
                    RouteType(2), RouteType(2), RouteType(2), RouteType(2)] ),
                   ],
                   [CtrlType( OPT_NAH, [ 
                    RouteType(3), RouteType(5), RouteType(1), RouteType(0),
                    RouteType(1), RouteType(4), RouteType(4), RouteType(4)] ),
                    CtrlType( OPT_NAH, [ 
                    RouteType(3), RouteType(5), RouteType(1), RouteType(0),
                    RouteType(1), RouteType(4), RouteType(4), RouteType(4)] ),
                    CtrlType( OPT_NAH, [ 
                    RouteType(3), RouteType(5), RouteType(1), RouteType(0),
                    RouteType(1), RouteType(4), RouteType(4), RouteType(4)] ),
                   ],
                   [CtrlType( OPT_NAH, [ 
                    RouteType(2), RouteType(2), RouteType(2), RouteType(2),
                    RouteType(2), RouteType(2), RouteType(2), RouteType(2)] ),
                    CtrlType( OPT_NAH, [ 
                    RouteType(2), RouteType(2), RouteType(2), RouteType(2),
                    RouteType(2), RouteType(2), RouteType(2), RouteType(2)] ),
                    CtrlType( OPT_INC, [ 
                    RouteType(2), RouteType(2), RouteType(2), RouteType(2),
                    RouteType(2), RouteType(2), RouteType(2), RouteType(2)] ),
                   ],
                   [CtrlType( OPT_NAH, [ 
                    RouteType(3), RouteType(5), RouteType(1), RouteType(0),
                    RouteType(1), RouteType(4), RouteType(4), RouteType(4)] ),
                    CtrlType( OPT_NAH, [ 
                    RouteType(3), RouteType(5), RouteType(1), RouteType(0),
                    RouteType(1), RouteType(4), RouteType(4), RouteType(4)] ),
                    CtrlType( OPT_NAH, [ 
                    RouteType(3), RouteType(5), RouteType(1), RouteType(0),
                    RouteType(1), RouteType(4), RouteType(4), RouteType(4)] ),
                   ]
                  ]

  preload_data  = [DataType(2, 1)]
  preload_const = [[DataType(0, 1)], [DataType(1, 1)],
                   [DataType(1, 1)], [DataType(2, 1)],
                   [DataType(3, 1)], [DataType(4, 1)]] 
  th = TestHarness( DUT, FunctionUnit, FuList, DataType, CtrlType,
                    width, height, ctrl_mem_size, data_mem_size,
                    src_opt, preload_data, preload_const )
  run_sim( th )

"""
def test_cgra_2x2_universal_fir():
  target_json = "config_fir.json"
  script_dir  = os.path.dirname(__file__)
  file_path   = os.path.join( script_dir, target_json )

  II                = 4
  num_tile_inports  = 4
  num_tile_outports = 4
  num_xbar_inports  = 6
  num_xbar_outports = 8
  ctrl_mem_size     = 8
  width             = 4
  height            = 4
  num_tiles         = width * height
  RouteType         = mk_bits( clog2( num_xbar_inports + 1 ) )
  AddrType          = mk_bits( clog2( ctrl_mem_size ) )
  num_tiles         = width * height
  ctrl_mem_size     = II
  data_mem_size     = 10
  DUT               = PseudoCGRA
  FunctionUnit      = FlexibleFu
  FuList            = [Alu, MemUnit]
  DataType          = mk_data( 16, 1 )
  CtrlType          = mk_ctrl( num_xbar_inports, num_xbar_outports )

  cgra_ctrl         = CGRACtrl( file_path, CtrlType, RouteType, width, height,
                                num_xbar_outports, II )
  src_opt           = cgra_ctrl.get_ctrl()
  print( src_opt )
  preload_data  = [ DataType( 1, 1 ) ] * data_mem_size
  preload_const = [ [ DataType( 1, 1 ) ] * II ] * num_tiles

  th = TestHarness( DUT, FunctionUnit, FuList, DataType, CtrlType,
                    width, height, ctrl_mem_size, data_mem_size,
                    src_opt, preload_data, preload_const )
  run_sim( th )
"""
