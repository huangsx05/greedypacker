import numpy as np
import greedypacker
from utils.tools import get_item_coordinates


def iterate_to_optimize_ups(sheet_width, sheet_height, df):
    """
    iterate to optimize ups until the best solution is obtained
    """
    df["pds"] = (df["qty"]/df["n_ups"])  # use float in purpose
    df = df.sort_values("pds").reset_index(drop=True)
    best_pds = df["pds"].values[-1]  # max pds
    _, best_item_dict = solve(sheet_width, sheet_height, df)  # solve 2D layout problem

    i = 0  # only for logs
    ADD_UPS = True  # whether continue to +1 ups
    updated_df = df.copy()  # only updated for each better solution found
    while True:
        i += 1
        print(f"\niteration {i}, best_pds = {best_pds}, n_ups = {df['n_ups'].sum()}")
        df["pds"] = (df["qty"]/df["n_ups"])  # use float in purpose
        df = df.sort_values("pds").reset_index(drop=True)  # tentitative df for each iteration

        if ADD_UPS:
            max_pds_dg = df["dg_name"].values[-1]
            print(f"+1 ups for {max_pds_dg}")
            df.loc[df["dg_name"]==max_pds_dg,"n_ups"] += 1

        res = df.copy().drop(columns=["pds"])  # calculated df for each iteration, but not necessarily a better solution
        can_layout, item_dict = solve(sheet_width, sheet_height, res)
        print(f"can_layout = {can_layout}")

        if can_layout:  # +1 pds for next iteration
            ADD_UPS = True
            res["pds"] = (res["qty"]/res["n_ups"])  # use float in purpose
            res = res.sort_values("pds").reset_index(drop=True)
            temp_pds = res["pds"].values[-1]
            if temp_pds<=best_pds:
                print(f"better pds is found = {temp_pds}")
                best_pds = temp_pds
                best_item_dict = item_dict
                df = res.copy()
                updated_df = res.copy()
                # for k,v in best_item_dict.items():
                #     print(k,len(v))
            else:
                print(f"break - can layout but worse pds")
                break
        else:  # -1 ups for min_pds for next iteration
            ADD_UPS = False
            min_pds_dg = df["dg_name"].values[0]
            df.loc[df["dg_name"]==min_pds_dg,"n_ups"] -= 1
            print(f"-1 ups for {min_pds_dg}")
            df["temp_pds"] = (df["qty"]/df["n_ups"])
            temp_pds = df["temp_pds"].values.max()
            if temp_pds>best_pds:
                print(f"break - further reduction causes worse pds")
                break
            else:
                df = df.drop(columns=["temp_pds"])          

    print(f"best_pds = {best_pds}")
    print(updated_df)

    return best_item_dict


def solve(sheet_width, sheet_height, res):
    """
    solve a 2D layout problem
    """
    M = greedypacker.BinManager(sheet_height, 
                                sheet_width, 
                                bin_algo = 'bin_best_fit',
                                pack_algo='shelf', 
                                heuristic ='best_width_fit',
                                rotation=False,  # 用于sheet rotation
                                rectangle_merge=False,  # ???
                                wastemap=False,  # ???
                                sorting=True,
                                sorting_heuristic='MAXCOUNT_DESCWIDTHI')

    items = []
    for i, row in res.iterrows():
        # dg_name = row["dg_name"]
        label_y = row["overall_label_width"]
        label_x = row["overall_label_length"]
        rotation = row["rotation"]
        n_ups = row["n_ups"]
        for i in range(n_ups):
            item = greedypacker.Item(width=label_x, 
                                     height=label_y,
                                     rotation=rotation)
            items.append(item)

    M.add_items(*items)

    M.execute()

    res = M.bins
    print(res)
    # print(f"len(items) = {len(items)}, {len(res[0].items)}")

    if len(items)!=len(res[0].items):
        can_layout = False
        item_dict = {}
    else:
        can_layout, item_dict = get_item_coordinates(res)

    return can_layout, item_dict


# def optimize_ups(df):
#     df["pds"] = (df["qty"]/df["ups"])#.astype(int)
#     df = df.sort_values("pds").reset_index(drop=True)

#     # get dgs to update ups and pds
#     max_pds_dg = df["dg_name"].values[-1]
#     min_pds_dg = df["dg_name"].values[0]   

#     # calculate ups change amount
#     max_rotation = df[df["dg_name"]==max_pds_dg]["rotation"].values[0]
#     max_dg_width = df[df["dg_name"]==max_pds_dg]["overall_label_width"].values[0]
#     max_dg_length = df[df["dg_name"]==max_pds_dg]["overall_label_length"].values[0]
#     min_dg_width = df[df["dg_name"]==min_pds_dg]["overall_label_width"].values[0]
#     min_dg_length = df[df["dg_name"]==min_pds_dg]["overall_label_length"].values[0]

#     dec_ups_1 = np.ceil(max_dg_width/min_dg_width)*np.ceil(max_dg_length/min_dg_length)
#     dec_ups_2= np.ceil(max_dg_width/min_dg_length)*np.ceil(max_dg_length/min_dg_width)
#     if max_rotation==0:
#         dec_ups = np.max([dec_ups_1, 1])
#     else:
#         dec_ups = np.max([np.min([dec_ups_1, dec_ups_2]), 1])
#     print(f"dec_ups = {dec_ups}")

#     inc_ups_1 = int(dec_ups*min_dg_width/max_dg_width)*int(dec_ups*min_dg_length/max_dg_length)
#     inc_ups_2= int(dec_ups*min_dg_width/max_dg_length)*int(dec_ups*min_dg_length/max_dg_width)
#     if max_rotation==0:
#         inc_ups = inc_ups_1
#     else:
#         inc_ups = np.max([inc_ups_1,inc_ups_2])

#     # update ups and pds
#     df["temp_ups"] = df["ups"]
#     df.loc[df["dg_name"]==min_pds_dg,"temp_ups"] -= int(dec_ups)
#     df.loc[df["dg_name"]==max_pds_dg,"temp_ups"] += inc_ups
#     df["temp_pds"] = (df["qty"]/df["temp_ups"])#.astype(int)

#     print(df)
#     return df