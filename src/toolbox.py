import svgwrite

class toolbox(object):
    #this class is used to store important information (mostly constant)
    #used inside the project

    def __init__(self):
        self.csv_file=None
        self.svg_file=None
        self.line_base_color=None
        self.standard_station_space=None
        self.standard_station_radius=None
        self.standard_bifurcation_space=None
        self.already_drawn_station=[]
        self.line_path=None
    def Init_line_path(self):
        self.line_path=svgwrite.path.Path(d=None,
                                          fill="none",
                                          stroke=svgwrite.rgb(self.line_base_color[0],self.line_base_color[1], self.line_base_color[2]),
                                          stroke_width=2*self.standard_station_radius+1)
