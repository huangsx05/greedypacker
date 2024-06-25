import pandas as pd
from utils.tools import plot
from utils.solver import iterate_to_optimize_ups

###### optimize ups
sheet_width = 678
sheet_height = 528

inp = pd.DataFrame({"dg_name":             ["DG03", "DG05", "DG01", "DG06", "DG04", "DG02"],
                    "overall_label_width": [  63.5,   46.8,   70.6,   46.0,   27.0,  57.0 ],
                    "overall_label_length":[  43.0,   34.0,   51.0,   20.0,   76.0,  21.0 ],
                    "n_ups":               [    84,     15,     10,     11,      6,     9 ],
                    "qty":                 [  7866,    400,    400,    300,    450,   450 ],
                    "rotation":            [ False,  False,  False,   True,   True,  True ]
                    })

item_dict = iterate_to_optimize_ups(sheet_width, sheet_height, inp)
# for k,v in item_dict.items():
#     print(k,v)
# print(item_dict)
plot(sheet_width, sheet_height, item_dict)


###### optimize layout



# res = pd.DataFrame({"dg_name":             ["DG03", "DG05", "DG01", "DG06", "DG04", "DG02"],
#                     "overall_label_width": [  63.5,   46.8,   70.6,   46.0,   27.0,  57.0 ],
#                     "overall_label_length":[  43.0,   34.0,   51.0,   20.0,   76.0,  21.0 ],
#                     "n_ups":               [  96,     10,      7,      9,      6,     8   ]})


# can_layout, item_dict = solve(sheet_width, sheet_height, res)
# plot(item_dict)