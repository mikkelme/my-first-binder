from plotter import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.animation as animation
import matplotlib.gridspec as gridspec


def animator(MB_start, OB_start, MB_end, OB_end, coast_center, coast_angle, manual_limit, T = 10):

    #Positional data
    MB_pos, OB_pos = simulator(MB_start, OB_start, MB_end, OB_end, T, dt = 0.05)
    MB_pos_mark, OB_pos_mark = MB_pos - MB_pos, OB_pos - MB_pos

    #Hard coded settings
    intercept_points = True
    coast_length = 1e4
    coast_color = "darkorange"
    coast_color = color_cycle(4)

    def find_theta(MB_pos, i, x, y):
        #course_vector
        cv = np.array([MB_pos[-1,0] - MB_pos[0,0], MB_pos[-1,1] - MB_pos[0,1]])
        cv = cv/np.linalg.norm(cv)

        #eyeline vector
        ev = np.array([x - MB_pos[i,0], y - MB_pos[i,1]])
        if np.linalg.norm(ev) > 1e10:
            return np.nan
        ev = ev/np.linalg.norm(ev)

        theta = np.arccos(np.dot(cv, ev)) #[rad]
        return theta/(2*np.pi)*360 #[°]



    t = np.linspace(0, len(MB_pos)-1, len(MB_pos))
    x_inter = np.zeros(len(t))
    y_inter = np.zeros(len(t))

    for i in range(len(t)):
        x_inter[i],y_inter[i] = intercept((MB_pos[i,0], MB_pos[i,1]), (OB_pos[i,0], OB_pos[i,1]), coast_center, coast_angle)




    my_lines = [] ## array to keep track of the Line2D artists
    i = 0
    fig = plt.figure(num=0, figsize=(10, 7), facecolor='w', edgecolor='k')


    #--- Normal plot (x,y) ---#
    plt.subplot2grid((1,2), (0,0), colspan=1, rowspan=2)
    MB_point, = plt.plot(MB_pos[i,0], MB_pos[i,1], "o", color = color_cycle(3), label = "HB")
    OB_point, = plt.plot(OB_pos[i,0], OB_pos[i,1], "o", color = color_cycle(1), label = "KB")
    eye_line, = plt.plot((MB_pos[i,0], x_inter[i]), (MB_pos[i,1], y_inter[i]), linestyle = "--", marker = None, alpha = 0.5, color = 'black')
    intercept_point, = plt.plot(x_inter[i],y_inter[i], 'o', marker = "x", color = "black", label = "Skæringspunkt")
    my_lines += [MB_point, OB_point, eye_line, intercept_point]

    #Plot boat path
    plt.plot(MB_pos[:,0], MB_pos[:,1], linestyle = "--" , color = color_cycle(3))
    plt.plot(OB_pos[:,0], OB_pos[:,1], linestyle = "--" , color = color_cycle(1))

    #Plot background object
    plt.plot(x_inter[i], y_inter[i], 'o', marker = "s", color = color_cycle(3), label = "Fast objekt")

    #Plot coast
    zip = coast_line(coast_center, coast_angle, coast_length)
    plt.plot(zip[0], zip[1], color = color_cycle(4), alpha = 0.5,  label = "Kyst")


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


    #Limits auto
    plt.axis('equal')
    ylow = -200
    yhigh = 200

    xmin = -5
    xmax = coast_center[1] + 20
    ymin = np.max(np.array([ylow, np.min(np.array([ 0, np.min(MB_pos[:,1]), np.min(OB_pos[:,1]), np.min(y_inter)])) - 10]))
    ymax = np.min(np.array([yhigh, np.max(np.array([ 0, np.max(MB_pos[:,1]), np.max(OB_pos[:,1]), np.max(y_inter)])) + 10]))
    lim = [xmin, xmax, ymin, ymax]

    #Limits manual override
    for i in range(len(manual_limit[0])):
        if np.invert(np.isnan(manual_limit[0][i])):
            lim[i] = manual_limit[0][i]

    plt.xlim(lim[0], lim[1])
    plt.ylim(lim[2], lim[3])




    #Labels and Legend
    plt.legend(loc='lower center', bbox_to_anchor=(1.1, -0.15), ncol=6)
    plt.xlabel("$x$")
    plt.ylabel("$y$")


    #--- MB plot (x', y') ---#
    plt.subplot2grid((1,2), (0,1), colspan=1, rowspan=2)
    ax01 = plt.gca()
    x_inter_mark, y_inter_mark = x_inter-MB_pos[:,0] , y_inter-MB_pos[:,1]
    MB_point_mark, = plt.plot(MB_pos_mark[0,0], MB_pos_mark[0,1], "o", color = color_cycle(3), label = "HB")
    OB_point_mark, = plt.plot(OB_pos_mark[0,0], OB_pos_mark[0,1], "o", color = color_cycle(1), label = "KB")
    eye_line_mark, = plt.plot((MB_pos[i,0], x_inter_mark[i]), (MB_pos[i,1], y_inter_mark[i]), linestyle = "--", marker = None, alpha = 0.5, color = 'black')
    intercept_point_mark, = plt.plot(x_inter_mark[i],y_inter_mark[i], 'o', marker = "x", color = "black", label = "Skæringspunkt")
    background_object_mark, = plt.plot(x_inter_mark[0], y_inter_mark[0], 'o', marker = "s", color = color_cycle(3), label = "Fast objekt")

    #Plot coast
    zip_mark = coast_line(coast_center, coast_angle, coast_length)
    coast_line_mark, = plt.plot(zip_mark[0]- MB_pos[0,0], zip_mark[1] - MB_pos[0,1], color = color_cycle(4), alpha = 0.5,  label = "Kyst")

    #Fill coast
    big_number = 1000
    y1_mark = [zip_mark[1][1], zip_mark[1][1], zip_mark[1][0]]
    y2_mark = [zip_mark[1][0], zip_mark[1][0], zip_mark[1][0]]
    x1_mark = [zip_mark[0][1], zip_mark[0][1], zip_mark[0][0]]
    x2_mark = [zip_mark[0][0], zip_mark[0][0], zip_mark[0][0]]

    x_fill_mark_c = [big_number , zip_mark[0][1], zip_mark[0][0]]
    y_fill_mark_c = [big_number, zip_mark[1][1], zip_mark[1][0]]
    if np.abs(coast_angle -np.pi/2) < np.pi/4:
        coast_fill_mark = plt.fill_between(x_fill_mark_c, y1_mark, y2_mark, alpha = 0.25, color = coast_color)
    else:
        coast_fill_mark = plt.fill_betweenx(y_fill_mark_c, x1_mark, x2_mark, alpha = 0.25, color = coast_color)

    #Fill water
    x_fill_mark_w = [-big_number , zip_mark[0][1], zip_mark[0][0]]
    y_fill_mark_w = [-big_number, zip_mark[1][1], zip_mark[1][0]]
    if np.abs(coast_angle -np.pi/2) < np.pi/4:
        water_fil_mark = plt.fill_between(x_fill_mark_w, y1_mark, y2_mark, alpha = 0.1, color = color_cycle(9) )
    else:
        water_fil_mark = plt.fill_betweenx(y_fill_mark_w, x1_mark, x2_mark, alpha = 0.1, color = color_cycle(9) )

    my_lines += [MB_point_mark, OB_point_mark, eye_line_mark, intercept_point_mark, background_object_mark, coast_line_mark, coast_fill_mark, water_fil_mark]

    #Plot boat path
    plt.plot(OB_pos_mark[:,0], OB_pos_mark[:,1], linestyle = "--" , color = color_cycle(1))


    #Limits auto
    plt.axis('equal')
    ylow = -200
    yhigh = 200

    xmin = -5
    xmax = coast_center[1] + 20
    ymin = np.max(np.array([ylow, np.min(np.array([ 0, np.min(MB_pos_mark[:,1]), np.min(OB_pos_mark[:,1]), np.min(y_inter_mark)])) - 10]))
    ymax = np.min(np.array([yhigh, np.max(np.array([ 0, np.max(MB_pos_mark[:,1]), np.max(OB_pos_mark[:,1]), np.max(y_inter_mark)])) + 10]))


    lim = [xmin, xmax, ymin, ymax]

    #Limits manual override
    for i in range(len(manual_limit[1])):
        if np.invert(np.isnan(manual_limit[1][i])):
            lim[i] = manual_limit[1][i]

    plt.xlim(lim[0], lim[1])
    plt.ylim(lim[2], lim[3])



    #Labels and Legend
    plt.xlabel("$x'$")
    plt.ylabel("$y'$")



    def init():
        """ For practical reasons to
            avoid double i=0 in animate """
        pass
    def animate(i):
        #Plotter
        my_lines[0].set_data(MB_pos[i,0], MB_pos[i,1]) #MB
        my_lines[1].set_data(OB_pos[i,0], OB_pos[i,1]) #OB
        my_lines[2].set_data((MB_pos[i,0], x_inter[i]), (MB_pos[i,1], y_inter[i])) #eyeline
        my_lines[3].set_data(x_inter[i],y_inter[i]) #intercept point

        #MB_plotter
        my_lines[4].set_data(MB_pos_mark[i,0], MB_pos_mark[i,1]) #MB
        my_lines[5].set_data(OB_pos_mark[i,0], OB_pos_mark[i,1]) #OB
        my_lines[6].set_data((MB_pos_mark[i,0], x_inter_mark[i]), (MB_pos_mark[i,1], y_inter_mark[i])) #eyeline
        my_lines[7].set_data(x_inter_mark[i],y_inter_mark[i]) #intercept point
        my_lines[8].set_data(x_inter_mark[0]-MB_pos[i,0], y_inter_mark[0]-MB_pos[i,1]) #background object
        my_lines[9].set_data(zip_mark[0]-MB_pos[i,0], zip_mark[1]-MB_pos[i,1]) #coast line
        my_lines[10].remove() #fill coast
        if np.abs(coast_angle -np.pi/2) < np.pi/4:
            my_lines[10] = ax01.fill_between(x_fill_mark_c-MB_pos[i,0], y1_mark-MB_pos[i,1], y2_mark-MB_pos[i,1], alpha = 0.25, color = coast_color )
        else:
            my_lines[10] = ax01.fill_betweenx(y_fill_mark_c-MB_pos[i,1], x1_mark-MB_pos[i,0], x2_mark-MB_pos[i,0], alpha = 0.25, color = coast_color )
        my_lines[11].remove() #fill water
        if np.abs(coast_angle -np.pi/2) < np.pi/4:
            my_lines[11] = ax01.fill_between(x_fill_mark_w-MB_pos[i,0], y1_mark-MB_pos[i,1], y2_mark-MB_pos[i,1], alpha = 0.1, color = color_cycle(9) )
        else:
            my_lines[11] = ax01.fill_betweenx(y_fill_mark_w, x1_mark-MB_pos[i,0], x2_mark-MB_pos[i,0], alpha = 0.1, color = color_cycle(9) )


        return my_lines # return updated artists



    ani = animation.FuncAnimation(fig, animate, frames=len(MB_pos), init_func=init, interval=10, blit=False)
    plt.tight_layout(pad=1.1, w_pad=0.7, h_pad=0.2)
    plt.subplots_adjust(wspace=0.2, hspace = 0.65)
    return ani





if __name__ == "__main__":
    MB_start = (0,0)
    OB_start = (70,-20)
    MB_end = (0, 80)
    OB_end = (0, 50)
    coast_center = (200, 100)
    coast_angle = deg_to_rad(60)
    manual_limit = [(-5, 150, -100, 90), \
                    (-5, 150, np.nan, np.nan)]  #[Left: (xmin, xmax, ymin, ymax), Right:(xmin, xmax, ymin, ymax)]

    ani = animator(MB_start, OB_start, MB_end, OB_end, coast_center, coast_angle, manual_limit, T = 15)
    filename = "../article/figures/aniNC2.gif"
    writer = 'imagemagick'
    ani.save(filename, writer = writer, dpi = 200, fps=30)
    #plt.show()
