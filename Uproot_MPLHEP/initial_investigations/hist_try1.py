from hist import Hist

# Quick construction, no other imports needed:
h = (
  Hist.new
  .Reg(10, 0 ,1, name="x", label="x-axis")
  .Var(range(10), name="y", label="y-axis")
  .Int64()
)

# Filling by names is allowed:
h.fill(y=[1, 4, 6], x=[3, 5, 2])

# Names can be used to manipulate the histogram:
h.project("x")
h[{"y": 0.5j + 3, "x": 5j}]

# You can access data coordinates or rebin with a `j` suffix:
h[.3j:, ::2j] # x from .3 to the end, y is rebinned by 2

# Elegant plotting functions:
h.plot()
input()
h.plot2d_full()
# h.plot_pull(Callable)