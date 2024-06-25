import greedypacker

M = greedypacker.BinManager(8, 4, pack_algo='shelf', heuristic='best_width_fit', wastemap=False, rotation=True)

ITEM = greedypacker.Item(4, 2)

ITEM2 = greedypacker.Item(5, 2)

ITEM3 = greedypacker.Item(2, 2)


M.add_items(ITEM, ITEM2, ITEM3)

M.execute()

res = M.bins
print(res)

item_dict = get_item_coordinates(res)
print(item_dict)
plot(item_dict)
    
