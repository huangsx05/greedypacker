import matplotlib.pyplot as plt

def get_item_coordinates(res):
    item_dict = {}

    if len(res) > 1:
        # print(f"n_sheets = {len(res)}")
        # for i in range(len(res)):
        #     print(f"sheet {i}, n_items = {len(res[i].items)}")
        return False, item_dict
    
    for item in res[0].items:
        k = (round(item.height,1), round(item.width,1))
        if k not in item_dict.keys():
            item_dict[k] = []
        item_dict[k].append((round(item.y,1), round(item.x,1)))
    
    return True, item_dict

def plot_rectangle(x,y,w,h,color='blue'):
    """
    plot a rectangle
    x,y: origin
    w,h: width and height of rectangle
    """
    x1, x2, x3, x4, x5 = x, x+w, x+w, x, x
    y1, y2, y3, y4, y5 = y, y, y+h, y+h, y  
    plt.plot([x1,x2,x3,x4,x5], [y1,y2,y3,y4,y5], color)

def plot(sheet_width, sheet_height, item_dict):
    plot_rectangle(0,0,sheet_width,sheet_height,color='black')
    x_max = 0
    y_max = 0
    for k,v in item_dict.items():
        for i in v:
            plot_rectangle(i[0],i[1],k[0],k[1]) 
            if i[0]+k[0]>x_max:
                x_max = i[0]+k[0]
            if i[1]+k[1]>y_max:
                y_max = i[1]+k[1]
    print(f"unused = {sheet_width-x_max},{sheet_height-y_max}")
    plt.show()