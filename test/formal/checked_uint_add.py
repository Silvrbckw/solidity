from opcodes import GT, ADD
from rule import Rule
from util import BVUnsignedMax, BVUnsignedUpCast
from z3 import BitVec, BVAddNoOverflow, Not

"""
Overflow checked unsigned integer addition.
"""

n_bits = 256
for type_bits in range(8, n_bits + 1, 8):

	rule = Rule()

	# Input vars
	X_short = BitVec('X', type_bits)
	Y_short = BitVec('Y', type_bits)

	# Z3's overflow condition
	actual_overflow = Not(BVAddNoOverflow(X_short, Y_short, False))

	# cast to full n_bits values
	X = BVUnsignedUpCast(X_short, n_bits)
	Y = BVUnsignedUpCast(Y_short, n_bits)
	sum_ = ADD(X, Y)

	# Constants
	maxValue = BVUnsignedMax(type_bits, n_bits)

	# Overflow check in YulUtilFunction::overflowCheckedIntAddFunction
	overflow_check = GT(X, sum_) if type_bits == 256 else GT(sum_, maxValue)
	rule.check(overflow_check != 0, actual_overflow)
