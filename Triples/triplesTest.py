import matplotlib.pyplot as plt
import numpy as np
import triples as pit

l = [[],[],[],[],[]]
for i in range(1, 101):
    l[0].append(pit.brute(i)[-1])
    l[1].append(pit.brute_vol2(i)[-1])
    l[2].append(pit.one_factor_elimination(i)[-1])
    l[3].append(pit.pythagorean_from_imagine(i)[-1])
    l[4].append(pit.euclid_formula(i)[-1])

plt.style.use("ggplot")
fig, ax = plt.subplots()

t = range(1, 101)
plots = ax.plot(t, l[0], "o",
t, l[1], "o",
t, l[2], "go",
t, l[3], "co",
t, l[4], "yo",
alpha = 0.5)
ax.set_xlim(0, 100)
ax.set_ylim(0, 2 *10e3)
ax.set_title("Algorithms efficient comparison")
ax.set_xlabel("n")
ax.set_ylabel("Operations")
plt.legend(iter(plots), ("brute",
"brute_vol2",
"one_factor_elimination",
"pythagorean_from_imagine",
"euclid_formula"))

t = range(1, 21)

axins = ax.inset_axes([0.35, 0.35 + 0.2, 0.40, 0.40])
axins.plot(t, l[0][1:21], "o",
t, l[1][1:21], "o",
t, l[2][1:21], "go",
t, l[3][1:21], "co",
t, l[4][1:21], "yo",
alpha = 0.5)


x1, x2, y1, y2 = 0, 20, 0, 2500
axins.set_xlim(x1, x2)
axins.set_ylim(y1, y2)

ax.indicate_inset_zoom(axins, edgecolor="black")


mng = plt.get_current_fig_manager()
mng.full_screen_toggle()

plt.show()
