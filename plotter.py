from simulator import *
import matplotlib.pyplot as plt

import seaborn as sns
plt.style.use("bmh")
sns.color_palette("hls", 1)

import matplotlib
matplotlib.rc('xtick', labelsize=14)
matplotlib.rc('ytick', labelsize=14)
matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['font.family'] = 'STIXGeneral'

def intercept(A, B, center, angle):
    """ Calculates intercept with line of sight a
        and coast line  """
    Ax, Ay = A[0], A[1]
    Bx, By = B[0], B[1]
    m = (By - Ay)/(Bx - Ax)
    b = Ay - m*Ax
    x_inter = (-b + center[1] - np.tan(angle)*center[0])/(m - np.tan(angle))
    y_inter = m*x_inter + b
    return x_inter, y_inter

def coast_line(center, angle, length):
    """ Return coordinates for
        coast line end points """
    point1 = [length/2*np.cos(angle) + center[0], length/2*np.sin(angle) + center[1]]
    point2 = [-length/2*np.cos(angle) + center[0], -length/2*np.sin(angle) + center[1]]
    zip = np.array([[point1[0], point2[0]], [point1[1], point2[1]]])
    return zip

def deg_to_rad(angle):
    """ Convert from degrees
        to radians """
    return angle/360*2*np.pi

def color_cycle(num_color):
    """ get coloer from matplotlib
        color cycle """
    color = plt.rcParams['axes.prop_cycle'].by_key()['color']
    return color[num_color]

def plot_arrows(Pos, color):
    """ plot arrows on
        specified positions """
    arrow_length = 5
    head_width = 0.1
    head_length = arrow_length
    dir = np.array(Pos[1] - Pos[0])
    if np.linalg.norm(dir) < 0.1:
        dir = np.array([0,1])
    dir_norm = dir/np.linalg.norm(dir)
    dir_arrow = dir_norm*arrow_length
    for i in range(len(Pos[:,0])):
        plt.arrow(Pos[i,0] - dir_arrow[0]/2, Pos[i,1] - dir_arrow[1]/2, dir_arrow[0], dir_arrow[1], head_width = 7, head_length = arrow_length, length_includes_head = True, color = color)

def plotter(MB_pos, OB_pos, coast_center, coast_angle, subplot = False):
    """ Plots boats, coast, line of sight with coasts intercepts
        and crash point if possible """

    #Hard coded settings
    intercept_points = True
    coast_length = 500
    coast_color = "darkorange"
    coast_color = color_cycle(4) # 4, 8
    num_points = 4
    idx = np.linspace(0, len(MB_pos) - 1, num_points).astype('int')

    #Make figure
    if subplot == False:
        plt.figure(num=0, dpi=80, facecolor='w', edgecolor='k')

    #Plot boat path
    plt.plot(MB_pos[idx,0], MB_pos[idx,1], linestyle = "--" , color = color_cycle(3), label = "HB")
    plt.plot(OB_pos[idx,0], OB_pos[idx,1], linestyle = "--" , color = color_cycle(1), label = "KB")

    #Plot coast
    zip = coast_line(coast_center, coast_angle, coast_length)
    plt.plot(zip[0], zip[1], color = color_cycle(4), alpha = 0.5,  label = "Kyst")

    #Plot boath arrows
    if np.linalg.norm(MB_pos[idx[-1]] - OB_pos[idx[-1]]) < 0.1:
        plot_arrows(MB_pos[idx[:-1]], color_cycle(3))
        plot_arrows(OB_pos[idx[:-1]], color_cycle(1))
        plt.plot(MB_pos[idx[-1],0], MB_pos[idx[-1],1], "o", marker = "X", markersize = 8, color = color_cycle(4), label = "Kollisionspunkt")
    else:
        plot_arrows(MB_pos[idx], color_cycle(3))
        plot_arrows(OB_pos[idx], color_cycle(1))


    #Plot intercept
    intercepts = []
    if intercept_points:
        label = "Skæringspunkt"
        label2 = "Fast objekt (tidsnr.)"
        for i in range(num_points):
            diff = np.min(np.linalg.norm(MB_pos[idx[i]] - OB_pos[idx[i]]))
            tol = 0.01
            if diff > tol:
                if i == 1:
                    label = "_" + label
                    label2 = "_" + label2
                x,y = intercept((MB_pos[idx[i],0], MB_pos[idx[i],1]), (OB_pos[idx[i],0], OB_pos[idx[i],1]), coast_center, coast_angle)
                if i == 0:
                    x_coast, y_coast = x, y
                    plt.plot(x_coast, y_coast, 'o', marker = "s", color = color_cycle(3), label = label2)
                plt.plot(x,y, 'o', marker = "x", color = "black", label = label)
                plt.plot((MB_pos[idx[i],0], x), (MB_pos[idx[i],1], y), linestyle = "--", marker = None, alpha = 0.5, color = 'black')
                intercepts.append([x,y])
    intercepts = np.array(intercepts)

    #Fill coast
    big_number = 1000
    y1 = [zip[1][1], zip[1][1], zip[1][0]]
    y2 = [zip[1][0], zip[1][0], zip[1][0]]
    x1 = [zip[0][1], zip[0][1], zip[0][0]]
    x2 = [zip[0][0], zip[0][0], zip[0][0]]

    x_fill = [big_number , zip[0][1], zip[0][0]]
    y_fill = [big_number, zip[1][1], zip[1][0]]
    if np.abs(coast_angle -np.pi/2) < np.pi/4:
        plt.fill_between(x_fill, y1, y2, alpha = 0.25, color = coast_color )
    else:
        plt.fill_betweenx(y_fill, x1, x2, alpha = 0.25, color = coast_color )


    #Fill water
    x_fill = [-big_number , zip[0][1], zip[0][0]]
    y_fill = [-big_number, zip[1][1], zip[1][0]]
    if np.abs(coast_angle -np.pi/2) < np.pi/4:
        plt.fill_between(x_fill, y1, y2, alpha = 0.1, color = color_cycle(9) )
    else:
        plt.fill_betweenx(y_fill, x1, x2, alpha = 0.1, color = color_cycle(9) )


    #Limits
    plt.axis('equal')
    ylow = -200
    yhigh = 200
    if np.linalg.norm(MB_pos[idx[-1]] - OB_pos[idx[-1]]) < 0.1: #If crash:
        ymin = np.min(np.array([-5, np.min(intercepts[:,1]) -10]))
        ymax = np.max(np.array([ 5, np.max(intercepts[:,1]) +10]))
        xmin = - 5
        xmax = 120
    else:
        xmin = -5
        xmax = 120
        ymin = np.min(np.array([ 0, np.min(MB_pos[idx,1]), np.min(OB_pos[idx,1]), np.min(intercepts[:,1])])) - 10
        ymax = np.max(np.array([ 0, np.max(MB_pos[idx,1]), np.max(OB_pos[idx,1]), np.max(intercepts[:,1])])) + 10

        ymin = np.max(np.array([ylow, ymin]))
        ymax = np.min(np.array([yhigh, ymax]))
    plt.ylim(ymin, ymax)
    plt.xlim(xmin, xmax)

    #Axis labels and legend
    plt.xlabel("x [m]", fontsize = 14)
    plt.ylabel("y [m]", fontsize = 14)
    if subplot == False:
        plt.legend(loc = "best", fontsize = 13)


def MB_plotter(MB_pos, OB_pos, coast_center, coast_angle, subplot = False):
    """ Analog to plotter function, but plots with respect to
        transformed initial system where MB is in rest """

    #Transform to MB's initial frame of reference
    MB_pos_mark, OB_pos_mark = MB_pos - MB_pos, OB_pos - MB_pos

    #Settings
    intercept_points = True
    coast_length = 500
    coast_color = "darkorange"
    coast_color = color_cycle(4) # 4, 8
    num_points = 4
    idx = np.linspace(0, len(MB_pos) - 1, num_points).astype('int')

    #Make figure
    if subplot == False:
        plt.figure(num=0, dpi=80, facecolor='w', edgecolor='k')

    #Plot intercept
    intercepts = []
    if intercept_points:
        if np.linalg.norm(MB_pos[idx[-1]] - OB_pos[idx[-1]]) < 0.1: #If crash:
            #Crash point
            plt.plot(0, 0, "o", marker = "X", markersize = 8, color = color_cycle(4), label = "Kollisionspunkt")

            #Intercept
            x,y = intercept((MB_pos[idx[0],0], MB_pos[idx[0],1]), (OB_pos[idx[0],0], OB_pos[idx[0],1]), coast_center, coast_angle)
            label = "Skæringspunkt"
            label2 = "Fast objekt (tidsnr.)"
            for i in range(num_points):
                if i == 1:
                    label = "_" + label
                    label2 = "_" + label2
                x_new = x - MB_pos[idx[i],0]
                y_new = y - MB_pos[idx[i],1]
                x_coast, y_coast = x_new, y_new
                if i == 0:
                    plt.plot((MB_pos_mark[idx[i],0], x_new), (MB_pos_mark[idx[i],1], y_new), linestyle = "--", marker = None, alpha = 0.5, color = 'black')
                plt.plot(x_coast, y_coast, 'o', marker = "s", color = color_cycle(3), label = label2)
                plt.text(x_coast + 6, y_coast - 1,  f"{i}", horizontalalignment='center', verticalalignment='center', color= color_cycle(3), fontsize=13)
                intercepts.append([x_new,y_new])
            plt.plot(x, y, 'o', marker = "x", color = "black", label = label)
            intercepts = np.array(intercepts)

            #Plot boat path
            plt.plot(OB_pos_mark[idx,0], OB_pos_mark[idx,1], linestyle = "--" , color = color_cycle(1), label = "KB")

            #Plot arrows
            plot_arrows(OB_pos_mark[idx[:-1]], color_cycle(1))

        else: #If non crash
            label = "Skæringspunkt"
            label2 = "Fast objekt (tidsnr.)"
            x0,y0 = intercept((MB_pos[idx[0],0], MB_pos[idx[0],1]), (OB_pos[idx[0],0], OB_pos[idx[0],1]), coast_center, coast_angle)
            for i in range(num_points):
                if i == 1:
                    label = "_" + label
                    label2 = "_" + label2
                x,y = intercept((MB_pos[idx[i],0], MB_pos[idx[i],1]), (OB_pos[idx[i],0], OB_pos[idx[i],1]), coast_center, coast_angle)
                x = x - MB_pos[idx[i],0]
                y = y - MB_pos[idx[i],1]
                x_coast = x0 - MB_pos[idx[i],0]
                y_coast = y0 - MB_pos[idx[i],1]
                plt.plot(x, y, 'o', marker = "x", color = "black", label = label)
                plt.plot(x_coast, y_coast, 'o', marker = "s", color = color_cycle(3), label = label2)
                plt.text(x_coast + 6, y_coast - 1,  f"{i}", horizontalalignment='center', verticalalignment='center', color= color_cycle(3), fontsize=13)
                plt.plot((MB_pos_mark[idx[i],0], x), (MB_pos_mark[idx[i],1], y), linestyle = "--", marker = None, alpha = 0.5, color = 'black')
                intercepts.append([x,y])
            intercepts = np.array(intercepts)

            #Plot boat path
            plt.plot(MB_pos_mark[idx,0], MB_pos_mark[idx,1], linestyle = "--" , color = color_cycle(3), label = "HB")
            plt.plot(OB_pos_mark[idx,0], OB_pos_mark[idx,1], linestyle = "--" , color = color_cycle(1), label = "KB")

            #Plot arrows
            plot_arrows(MB_pos_mark[idx], color_cycle(3))
            plot_arrows(OB_pos_mark[idx], color_cycle(1))


    #Plot coast
    zip = coast_line(coast_center, coast_angle, coast_length)
    plt.plot(zip[0], zip[1], color = color_cycle(4), alpha = 0.5,  label = "Kyst")
    for i in range(num_points):
        plt.plot(np.array(zip[0]) - [MB_pos[idx[i],0]], np.array(zip[1])- MB_pos[idx[i],1], color = color_cycle(4), alpha = 0.2)


    #Fill coast
    big_number = 1000
    y1 = [zip[1][1], zip[1][1], zip[1][0]]
    y2 = [zip[1][0], zip[1][0], zip[1][0]]
    x1 = [zip[0][1], zip[0][1], zip[0][0]]
    x2 = [zip[0][0], zip[0][0], zip[0][0]]

    x_fill = [big_number , zip[0][1], zip[0][0]]
    y_fill = [big_number, zip[1][1], zip[1][0]]
    if np.abs(coast_angle -np.pi/2) < np.pi/4:
        plt.fill_between(x_fill, y1, y2, alpha = 0.25, color = coast_color )
    else:
        plt.fill_betweenx(y_fill, x1, x2, alpha = 0.25, color = coast_color )


    #Fill water
    x_fill = [-big_number , zip[0][1], zip[0][0]]
    y_fill = [-big_number, zip[1][1], zip[1][0]]
    if np.abs(coast_angle -np.pi/2) < np.pi/4:
        plt.fill_between(x_fill, y1, y2, alpha = 0.1, color = color_cycle(9) )
    else:
        plt.fill_betweenx(y_fill, x1, x2, alpha = 0.1, color = color_cycle(9) )


    #Limits
    plt.axis('equal')
    ymin = np.min(np.array([-5, np.min(intercepts[:,1]) -10]))
    ymax = np.max(np.array([ 5, np.max(intercepts[:,1]) +10]))
    xmin = - 20
    xmax = 120
    plt.ylim(ymin, ymax)
    plt.xlim(xmin, xmax)

    plt.xlabel("x' [m]", fontsize = 14)
    plt.ylabel("y' [m]", fontsize = 14)
    if subplot == False:
        plt.legend(loc = "best", fontsize = 13)



def subplotter(MB_start, OB_start, MB_end, OB_end,  coast_center, coast_angle):
    """ Calls plotter and MB_plotter and creates
        a subfigure display for the article """

    n = len(MB_start)
    plt.figure(num=0, figsize = (10,11), facecolor='w', edgecolor='k')
    for i in range(n):
        plt.subplot(4,2,2*i+1)
        MB_pos, OB_pos = simulator(MB_start[i], OB_start[i], MB_end[i], OB_end[i])
        MB_pos_mark, OB_pos_mark = MB_pos - MB_pos, OB_pos - MB_pos
        plotter(MB_pos, OB_pos, coast_center[i], coast_angle[i], subplot = True)
        if i == 3:
            plt.legend(loc='lower center', bbox_to_anchor=(1.1, -0.5), ncol=6)
        plt.subplot(4,2,2*i+2)
        MB_plotter(MB_pos, OB_pos, coast_center[i], coast_angle[i], subplot = True)

    plt.tight_layout(pad=1.1, w_pad=0.7, h_pad=0.2)
    plt.subplots_adjust(wspace = 0.2)


if __name__ == "__main__":

    if False: #plotter
        MB_start = (0,0)
        OB_start = (50,40)
        MB_end = (0, 40)
        OB_end = (10, 40)
        MB_pos, OB_pos = simulator(MB_start, OB_start, MB_end, OB_end)
        coast_center = (100, 100)
        coast_angle = deg_to_rad(90)
        plotter(MB_pos, OB_pos, coast_center, coast_angle)
        plt.show()

    if False: #MB_plotter
        MB_start = (0,0)
        OB_start = (50,40)
        MB_end = (0, 40)
        OB_end = (0, 40)
        MB_pos, OB_pos = simulator(MB_start, OB_start, MB_end, OB_end)
        coast_center = (100, 100)
        coast_angle = deg_to_rad(90)
        MB_plotter(MB_pos, OB_pos, coast_center, coast_angle)
        plt.show()

    if True: #subplotter
        # Crash 1
        MB_start = [(0,0), (0,0), (0,0), (0,0)]
        OB_start = [(20,0), (40,20), (50,40), (50,60)]
        MB_end = [(0, 40), (0, 40), (0, 40), (0, 40)]
        OB_end = [(0, 40), (0, 40), (0, 40), (0, 40)]
        coast_center = [(100,100), (100,100), (100,100), (100,100)]
        coast_angle = deg_to_rad(np.array([90, 90, 90, 90]))
        subplotter(MB_start, OB_start, MB_end, OB_end, coast_center, coast_angle)
        #plt.savefig("../article/figures/subplot_C1.pdf", bbox_inches="tight")
        plt.show()

        # Crash 2
        MB_start = [(0,0), (0,0), (0,0), (0,0)]
        OB_start = [(50,40), (50,70), (30,80), (0.1,80)]
        MB_end = [(0, 40), (0, 40), (0, 40), (0, 40)]
        OB_end = [(0, 40), (0, 40), (0, 40), (0, 40)]
        coast_center = [(100,110), (100,110), (100,110), (100,150)]
        coast_angle = deg_to_rad(np.array([180, 180, 180, 180]))
        subplotter(MB_start, OB_start, MB_end, OB_end, coast_center, coast_angle)
        #plt.savefig("../article/figures/subplot_C2.pdf", bbox_inches="tight")
        plt.show()

        # Non Crash 1
        MB_start = [(0,0), (0,0), (0,0), (0,0)]
        OB_start = [(30,0), (40,40), (30,60), (10,80)]
        MB_end = [(0, 40), (0, 40), (0, 40), (0, 40)]
        OB_end = [(10, 30), (10, 40), (10, 45), (10, 45)]
        coast_center = [(100,100), (100,100), (100,120), (100,120)]
        coast_angle = deg_to_rad(np.array([90, 90, 180, 180]))
        subplotter(MB_start, OB_start, MB_end, OB_end, coast_center, coast_angle)
        #plt.savefig("../article/figures/subplot_NC1.pdf", bbox_inches="tight")
        plt.show()
