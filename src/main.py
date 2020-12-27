import svgwrite
import csv
from toolbox import *

# this function is made to preprocess the CSV file
def Formatting_csv(filename):
    #just opening the file
    with open(filename, newline='') as f:
        reader = csv.reader(f,delimiter=",")
        csv_list = list(reader)

    #pop the first line that contain information about the file
    csv_list.pop(0)

    #begining of modification
    for i in range(len(csv_list)):

        #spliting string for all connection station and the line connection
        for j in range(2,len(csv_list[0])):
            if csv_list[i][j]!='':
                csv_list[i][j]=list(csv_list[i][j].split(" "))
            else:
                csv_list[i][j]=[]
            csv_list[i][0]=int(csv_list[i][0])

        #processing connection to transform them into integer
        for k in range(len(csv_list[i][2])):
            csv_list[i][2][k]=list(csv_list[i][2][k].split("="))
            if csv_list[i][2][k][0]!='R':
                csv_list[i][2][k][0]=int(csv_list[i][2][k][0])
            csv_list[i][2][k][1]=int(csv_list[i][2][k][1])


    return csv_list
def Draw_circle(tool,cx,cy,index):
    tool.svg_file.add(svgwrite.text.Text(tool.csv_file[index][1], insert=None, x=[cx], y=[cy-2*tool.standard_station_radius],transform="rotate(-45 {} {})".format(cx,cy-2*tool.standard_station_radius,),font_family="Alata",font_size="20"))
    if(Has_connection(tool,index)):
        tool.svg_file.add(tool.svg_file.circle((cx, cy),
                           tool.standard_station_radius,
                           stroke_width=1,
                           fill=svgwrite.rgb(255,255,255),
                           stroke=svgwrite.rgb(0,0,0)))
    else:
        tool.svg_file.add(tool.svg_file.circle((cx, cy),
                           tool.standard_station_radius,
                           stroke_width=1,
                           fill=svgwrite.rgb(255,255,255),
                           stroke=svgwrite.rgb(tool.line_base_color[0], tool.line_base_color[1], tool.line_base_color[2])))
# this function is used to draw the circule
#it should also be used to create other control point and therfore should be run first
def Trace_line_station(tool,cx=0,cy=0,index=0,side='right'):
    #--------------------------------------------------
    # We first check if this point is already treated so we can do anything
    #--------------------------------------------------
    if (tool.csv_file[index][0] in tool.already_drawn_station):
        return
    #--------------------------------------------------
    #Now We check the connection for the station
    #--------------------------------------------------
    connection=tool.csv_file[index][2]
    connection_type=Get_connection_type(connection)
    #-----------------------------------
    #find how to place the next station
    #-----------------------------------
    if (connection_type==1):##### end of line
        #-------------------------------------
        #First we draw the circule
        #-------------------------------------
        Draw_circle(tool,cx,cy,index)

        #-------------------------------------
        #Update position for connection
        #-------------------------------------
        if side=='right': new_cx=cx+tool.standard_station_space+2*tool.standard_station_radius
        if side=='left':  new_cx=cx-tool.standard_station_space+2*tool.standard_station_radius
        new_cy=cy
        new_index=Get_next_line(tool,index)

        Trace_line_station(tool,new_cx,new_cy,new_index,side)

    elif (connection_type==2):#### normal straight line
        #-------------------------------------
        #First we draw the circule
        #-------------------------------------
        Draw_circle(tool,cx,cy,index)

        #---------------------------------------
        # if this station is the begining
        # the left one in the databasse will be choosen as going left while the one on the right will be choosen to go right
        #---------------------------------------
        if side=='right':
            new_cx=cx+tool.standard_station_space+2*tool.standard_station_radius
        if side=='left':
            new_cx=cx-tool.standard_station_space+2*tool.standard_station_radius
        new_cy=cy
        new_index=Get_next_line(tool,index)

        Trace_line_station(tool,new_cx,new_cy,new_index[0],side)
        Trace_line_station(tool,new_cx,new_cy,new_index[1],side)
    elif (connection_type==3):#### bifurcation by two
        #----------------------
        #detect the tri point
        #---------------------
        if (connection[0][0]==connection[1][0] or connection[0][0]==connection[1][1]):
            tri=connection[0][0]
        else:
            tri=connection[0][1]


        if tri in tool.already_drawn_station: #we begin from the tri point

            print("lol")
            Draw_circle(tool,cx,cy,index)

            new_index=Get_next_line(tool,index)
            if side=='right':
                #----------------------------
                #upper point
                #----------------------------
                new_cx=cx+tool.standard_bifurcation_space+4*tool.standard_station_radius
                new_cy=cy+tool.standard_bifurcation_space

                Trace_line_station(tool,new_cx,new_cy,new_index[1],side='right')
                #----------------------------
                #lower point
                #----------------------------
                new_cx=cx+tool.standard_bifurcation_space+4*tool.standard_station_radius
                new_cy=cy-tool.standard_bifurcation_space

                Trace_line_station(tool,new_cx,new_cy,new_index[2],side='right')
            else: # side='left':
                new_cx=cx-tool.standard_bifurcation_space+4*tool.standard_station_radius
                new_cy=cy+tool.standard_bifurcation_space

                Trace_line_station(tool,new_cx,new_cy,new_index[1],side='left')

                new_cx=cx-tool.standard_bifurcation_space+4*tool.standard_station_radius
                new_cy=cy-tool.standard_bifurcation_space

                Trace_line_station(tool,new_cx,new_cy,new_index[2],side='left') ##### if the tripoint is the reference point

        elif connection[0][0] in tool.already_drawn_station or connection[0][1] in tool.already_drawn_station: #### we arrive from the bottom point
            new_index=Get_next_line(tool,index)
            if side=='right':
                cx=cx+tool.standard_bifurcation_space+2*tool.standard_station_radiuse
                cy=cy+tool.standard_bifurcation_space
                Draw_circle(tool,cx,cy,index)

                #----------------------------
                #upper point
                #----------------------------
                new_cx=cx-tool.standard_bifurcation_space-4*tool.standard_station_radius
                new_cy=cy+tool.standard_bifurcation_space


                Trace_line_station(tool,new_cx,new_cy,new_index[1],side='left')

                #----------------------------
                #straight point
                #----------------------------
                new_cx=cx+2*tool.standard_station_radius+tool.standard_station_space
                new_cy=cy

                Trace_line_station(tool,new_cx,new_cy,new_index[0],side='right')
            else: #ide='left':
                cx=cx-tool.standard_bifurcation_space-2*tool.standard_station_radiuse
                cy=cy+tool.standard_bifurcation_space
                Draw_circle(tool,cx,cy,index)

                #----------------------------
                #upper point
                #----------------------------
                new_cx=cx+tool.standard_bifurcation_space+4*tool.standard_station_radius
                new_cy=cy+tool.standard_bifurcation_space

                Trace_line_station(tool,new_cx,new_cy,new_index[1],side='right')

                #----------------------------
                #straight point
                #----------------------------
                new_cx=cx-2*tool.standard_station_radius-tool.standard_station_space
                new_cy=cy

                Trace_line_station(tool,new_cx,new_cy,new_index[0],side='left') ##### if the tripoint is the reference point
        elif connection[1][0] in tool.already_drawn_station or connection[1][1] in tool.already_drawn_station: #### we arrive from the top point
            new_index=Get_next_line(tool,index)
            if side=='right':
                cx=cx+tool.standard_bifurcation_space+2*tool.standard_station_radiuse
                cy=cy-tool.standard_bifurcation_space
                Draw_circle(tool,cx,cy,index)

                #----------------------------
                #lower point
                #----------------------------
                new_cx=cx-tool.standard_bifurcation_space-4*tool.standard_station_radius
                new_cy=cy-tool.standard_bifurcation_space

                Trace_line_station(tool,new_cx,new_cy,new_index[2],side='left')

                #----------------------------
                #Strainght point
                #----------------------------
                new_cx=cx+2*tool.standard_station_radius+tool.standard_station_space
                new_cy=cy

                Trace_line_station(tool,new_cx,new_cy,new_index[0],side='right')
            else: # side='left':
                cx=cx-tool.standard_bifurcation_space-4*tool.standard_station_radiuse
                cy=cy-tool.standard_bifurcation_space
                Draw_circle(tool,cx,cy,index)

                #----------------------------
                #lower point
                #----------------------------
                new_cx=cx+tool.standard_bifurcation_space+4*tool.standard_station_radius
                new_cy=cy-tool.standard_bifurcation_space

                Trace_line_station(tool,new_cx,new_cy,new_index[2],side='right')

                #----------------------------
                #Strainght point
                #----------------------------
                new_cx=cx+2*tool.standard_station_radius+tool.standard_station_space
                new_cy=cy

                Trace_line_station(tool,new_cx,new_cy,new_index[0],side='left') ##### if the tripoint is the reference point
        else: #this should never happend
            raise Exception('This bifurcation has a problem: {}'.format(connection))
    elif (connection_type==4): #crossing parallele four (right now working just like a 2 connection)
        #-------------------------------------
        #First we draw the circule
        #-------------------------------------
        Draw_circle(tool,cx,cy,index)

        #---------------------------------------
        # if this station is the begining
        # the left one in the databasse will be choosen as going left while the one on the right will be choosen to go right
        #---------------------------------------
        if side=='right':
            new_cx=cx+tool.standard_station_space+2*tool.standard_station_radius
        if side=='left':
            new_cx=cx-tool.standard_station_space+2*tool.standard_station_radius
        new_cy=cy
        new_index=Get_next_line(tool,index)

        Trace_line_station(tool,new_cx,new_cy,new_index[0],side)
    else:
        raise Exception('the type of connection is too big and unsuported: {}'.format(connection))

def Trace_line_path(tool,cx=0,cy=0,index=0,side='right'):
    #--------------------------------------------------
    # We first check if this point is already treated so we can do anything
    #--------------------------------------------------
    if (tool.csv_file[index][0] in tool.already_drawn_station):
        return
    #--------------------------------------------------
    #Now We check the connection for the station
    #--------------------------------------------------
    connection=tool.csv_file[index][2]
    connection_type=Get_connection_type(connection)
    #-----------------------------------
    #find how to place the next station
    #-----------------------------------
    if (connection_type==1):##### end of line
        if cx==0 and cy==0:
            tool.line_path.push("M 0 0")
        else:
            tool.line_path.push("L {} {}".format(cx,cy))
        #-------------------------------------
        #First we draw the circule
        #-------------------------------------
        Draw_circle(tool,cx,cy,index)

        #-------------------------------------
        #Update position for connection
        #-------------------------------------
        if side=='right': new_cx=cx+tool.standard_station_space+2*tool.standard_station_radius
        if side=='left':  new_cx=cx-tool.standard_station_space+2*tool.standard_station_radius
        new_cy=cy
        new_index=Get_next_line(tool,index)

        Trace_line_path(tool,new_cx,new_cy,new_index,side)

    elif (connection_type==2):#### normal straight line
        #-------------------------------------
        #First we draw the circule
        #-------------------------------------
        Draw_circle(tool,cx,cy,index)

        #---------------------------------------
        # if this station is the begining
        # the left one in the databasse will be choosen as going left while the one on the right will be choosen to go right
        #---------------------------------------
        if side=='right':
            new_cx=cx+tool.standard_station_space+2*tool.standard_station_radius
        if side=='left':
            new_cx=cx-tool.standard_station_space+2*tool.standard_station_radius
        new_cy=cy
        new_index=Get_next_line(tool,index)

        Trace_line_path(tool,new_cx,new_cy,new_index[0],side)
        Trace_line_path(tool,new_cx,new_cy,new_index[1],side)
    elif (connection_type==3):#### bifurcation by two
        #----------------------
        #detect the tri point
        #---------------------
        if (connection[0][0]==connection[1][0] or connection[0][0]==connection[1][1]):
            tri=connection[0][0]
        else:
            tri=connection[0][1]


        if tri in tool.already_drawn_station: #we begin from the tri point

            new_index=Get_next_line(tool,index)
            if side=='right':
                tool.line_path.push("L {} {}".format(cx+tool.standard_station_radius,cy))
                #----------------------------
                #upper point
                #----------------------------
                new_cx=cx+tool.standard_bifurcation_space+4*tool.standard_station_radius
                new_cy=cy+tool.standard_bifurcation_space

                tool.line_path.push("L {} {}".format(cx+tool.standard_bifurcation_space+3*tool.standard_station_radius,cy+tool.standard_bifurcation_space))
                Trace_line_path(tool,new_cx,new_cy,new_index[1],side='right')
                #----------------------------
                #lower point
                #----------------------------
                new_cx=cx+tool.standard_bifurcation_space+4*tool.standard_station_radius
                new_cy=cy-tool.standard_bifurcation_space

                tool.line_path.push("M {} {}".format(cx+tool.standard_station_radius,cy))
                tool.line_path.push("L {} {}".format(cx+tool.standard_bifurcation_space+3*tool.standard_station_radius,cy-tool.standard_bifurcation_space))
                Trace_line_path(tool,new_cx,new_cy,new_index[2],side='right')
            else: # side='left':
                tool.line_path.push("L {} {}".format(cx-tool.standard_station_radius,cy))
                new_cx=cx-tool.standard_bifurcation_space+4*tool.standard_station_radius
                new_cy=cy+tool.standard_bifurcation_space

                tool.line_path.push("L {} {}".format(cx-tool.standard_bifurcation_space-3*tool.standard_station_radius,cy+tool.standard_bifurcation_space))
                Trace_line_path(tool,new_cx,new_cy,new_index[1],side='left')

                new_cx=cx-tool.standard_bifurcation_space+4*tool.standard_station_radius
                new_cy=cy-tool.standard_bifurcation_space

                tool.line_path.push("M {} {}".format(cx-tool.standard_station_radius,cy))
                tool.line_path.push("L {} {}".format(cx-tool.standard_bifurcation_space-3*tool.standard_station_radius,cy-tool.standard_bifurcation_space))
                Trace_line_path(tool,new_cx,new_cy,new_index[2],side='left') ##### if the tripoint is the reference point

        elif connection[0][0] in tool.already_drawn_station or connection[0][1] in tool.already_drawn_station: #### we arrive from the bottom point
            new_index=Get_next_line(tool,index)
            if side=='right':
                cx=cx+tool.standard_bifurcation_space+2*tool.standard_station_radiuse
                cy=cy+tool.standard_bifurcation_space
                Draw_circle(tool,cx,cy,index)

                #----------------------------
                #upper point
                #----------------------------
                new_cx=cx-tool.standard_bifurcation_space-4*tool.standard_station_radius
                new_cy=cy+tool.standard_bifurcation_space


                Trace_line_path(tool,new_cx,new_cy,new_index[1],side='left')

                #----------------------------
                #straight point
                #----------------------------
                new_cx=cx+2*tool.standard_station_radius+tool.standard_station_space
                new_cy=cy

                Trace_line_path(tool,new_cx,new_cy,new_index[0],side='right')
            else: #ide='left':
                cx=cx-tool.standard_bifurcation_space-2*tool.standard_station_radiuse
                cy=cy+tool.standard_bifurcation_space
                Draw_circle(tool,cx,cy,index)

                #----------------------------
                #upper point
                #----------------------------
                new_cx=cx+tool.standard_bifurcation_space+4*tool.standard_station_radius
                new_cy=cy+tool.standard_bifurcation_space

                Trace_line_path(tool,new_cx,new_cy,new_index[1],side='right')

                #----------------------------
                #straight point
                #----------------------------
                new_cx=cx-2*tool.standard_station_radius-tool.standard_station_space
                new_cy=cy

                Trace_line_path(tool,new_cx,new_cy,new_index[0],side='left') ##### if the tripoint is the reference point
        elif connection[1][0] in tool.already_drawn_station or connection[1][1] in tool.already_drawn_station: #### we arrive from the top point
            new_index=Get_next_line(tool,index)
            if side=='right':
                cx=cx+tool.standard_bifurcation_space+2*tool.standard_station_radiuse
                cy=cy-tool.standard_bifurcation_space
                Draw_circle(tool,cx,cy,index)

                #----------------------------
                #lower point
                #----------------------------
                new_cx=cx-tool.standard_bifurcation_space-4*tool.standard_station_radius
                new_cy=cy-tool.standard_bifurcation_space

                Trace_line_path(tool,new_cx,new_cy,new_index[2],side='left')

                #----------------------------
                #Strainght point
                #----------------------------
                new_cx=cx+2*tool.standard_station_radius+tool.standard_station_space
                new_cy=cy

                Trace_line_path(tool,new_cx,new_cy,new_index[0],side='right')
            else: # side='left':
                cx=cx-tool.standard_bifurcation_space-4*tool.standard_station_radiuse
                cy=cy-tool.standard_bifurcation_space
                Draw_circle(tool,cx,cy,index)

                #----------------------------
                #lower point
                #----------------------------
                new_cx=cx+tool.standard_bifurcation_space+4*tool.standard_station_radius
                new_cy=cy-tool.standard_bifurcation_space

                Trace_line_path(tool,new_cx,new_cy,new_index[2],side='right')

                #----------------------------
                #Strainght point
                #----------------------------
                new_cx=cx+2*tool.standard_station_radius+tool.standard_station_space
                new_cy=cy

                Trace_line_path(tool,new_cx,new_cy,new_index[0],side='left') ##### if the tripoint is the reference point
        else: #this should never happend
            raise Exception('This bifurcation has a problem: {}'.format(connection))
    elif (connection_type==4): #crossing parallele four (right now working just like a 2 connection)
        #-------------------------------------
        #First we draw the circule
        #-------------------------------------
        Draw_circle(tool,cx,cy,index)

        #---------------------------------------
        # if this station is the begining
        # the left one in the databasse will be choosen as going left while the one on the right will be choosen to go right
        #---------------------------------------
        if side=='right':
            new_cx=cx+tool.standard_station_space+2*tool.standard_station_radius
        if side=='left':
            new_cx=cx-tool.standard_station_space+2*tool.standard_station_radius
        new_cy=cy
        new_index=Get_next_line(tool,index)

        Trace_line_path(tool,new_cx,new_cy,new_index[0],side)
        Trace_line_path(tool,new_cx,new_cy,new_index[1],side)
    else:
        raise Exception('the type of connection is too big and unsuported: {}'.format(connection))

def Has_connection(tool,index):
    #check for connection
    for i in range(3,len(tool.csv_file[index])):
        if tool.csv_file[index][i]!=[]:
            return True
    return False


def Get_next_line(tool,index):
    tool.already_drawn_station.append(tool.csv_file[index][0])
    connection=tool.csv_file[index][2]
    connection_type=Get_connection_type(connection)
    if connection_type==1:
        return [tool.csv_file[i][0] for i in range(len(tool.csv_file))].index(connection[0][1])
    elif connection_type==2:
        return [[tool.csv_file[i][0] for i in range(len(tool.csv_file))].index(connection[0][0]),[tool.csv_file[i][0] for i in range(len(tool.csv_file))].index(connection[0][1])]
    elif connection_type==3:
        temp=[]
        #-----------------------------------
        # First we need to find the three connection pussible [tri, bottom, top]
        #-----------------------------------
        if (connection[0][0]==connection[1][0] or connection[0][0]==connection[1][1]):
            tri=connection[0][0]
            temp=[[tool.csv_file[i][0] for i in range(len(tool.csv_file))].index(tri),[tool.csv_file[i][0] for i in range(len(tool.csv_file))].index(connection[0][1])]
        else:
            tri=connection[0][1]
            temp=[[tool.csv_file[i][0] for i in range(len(tool.csv_file))].index(tri),[tool.csv_file[i][0] for i in range(len(tool.csv_file))].index(connection[0][0])]
        if tri==connection[1][0]:
            temp.append([tool.csv_file[i][0] for i in range(len(tool.csv_file))].index(connection[1][1]))
        else:
            temp.append([tool.csv_file[i][0] for i in range(len(tool.csv_file))].index(connection[1][0]))

        return temp
    elif connection_type==4:
        tool.already_drawn_station.pop(tool.already_drawn_station.index(tool.csv_file[index][0]))
        print(tool.already_drawn_station)
        print(connection)
        if connection[0][0] in tool.already_drawn_station and not (connection[0][1] in tool.already_drawn_station):# [x]=[] []=[]
            return [[tool.csv_file[i][0] for i in range(len(tool.csv_file))].index(connection[0][1])]
        elif connection[0][1] in tool.already_drawn_station and not (connection[0][0] in tool.already_drawn_station):# []=[x] []=[]
            return [[tool.csv_file[i][0] for i in range(len(tool.csv_file))].index(connection[0][0])]
        elif connection[1][0] in tool.already_drawn_station and not (connection[1][1] in tool.already_drawn_station):# []=[] [x]=[]
            return [[tool.csv_file[i][0] for i in range(len(tool.csv_file))].index(connection[1][1])]
        elif connection[1][1] in tool.already_drawn_station and not (connection[1][0] in tool.already_drawn_station):# []=[] []=[x]
            return [[tool.csv_file[i][0] for i in range(len(tool.csv_file))].index(connection[1][0])]
        else: #we conventionaly begining toward the right
            raise Exception("we cannot guess the next connection for connection type 4")
    else:
        raise Exception('the type of connection is too big and unsuported: {}'.format(connection))

def Get_connection_type(connection):
    if len(connection)==1:
        if connection[0][0]=='R':
            return 1
        else:
            return 2
    elif len(connection)==2:
        if connection[0][0]==connection[1][0] or connection[0][0]==connection[1][1] or connection[0][1]==connection[1][0] or connection[0][1]==connection[1][1]:
            #if we get here this is a triangle connection
            return 3
        else:
            return 4
    else:
        raise Exception('the length of connection is too big and unsuported: {}'.format(connection))


if __name__=="__main__":
    csv_file="REA_D_data.csv"
    svg_file="REA_D.svg"
    tool=toolbox()
    #color definition
    #tool.line_base_color=[255,142,17] #jaune
    #tool.line_base_color=[5,124,9] #vert
    tool.line_base_color=[0,37,144] #bleu
    #standard metric definition
    tool.standard_station_space=25#px
    tool.standard_station_radius=6.5#px

    tool.standard_bifurcation_space=90#px

    #csv loading
    tool.csv_file=Formatting_csv(csv_file)
    tool.Init_line_path()
    #for i in range(len(tool.csv_file)):
    #    print(tool.csv_file[i])

    #svg file definition
    tool.svg_file = svgwrite.Drawing(svg_file)
    Trace_line_path(tool)
    tool.already_drawn_station=[]
    tool.svg_file.add(tool.line_path)
    Trace_line_station(tool,0,0,0)
    tool.svg_file.save()
