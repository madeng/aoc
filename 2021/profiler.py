import cProfile
import io
import pstats
from pstats import SortKey

pr = cProfile.Profile()
pr.enable()

import day21.main

pr.disable()
s = io.StringIO()
sortby = SortKey.CUMULATIVE
ps = pstats.Stats(pr, stream=s).sort_stats(sortby).reverse_order()
ps.print_stats()
print(s.getvalue())

