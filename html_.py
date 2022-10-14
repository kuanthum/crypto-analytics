
def card(i,backround=(94,156,118)):
        sline = ''
        wch_colour_box = backround
        wch_colour_font = (66,103,178)
        fontsize_upper = 40
        fontsize_bottom = 18
        valign = "middle"
        iconname = "fas fa-asterisk"
        lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.12.1/css/all.css" crossorigin="anonymous">'

        htmlstr = f"""<p style='width:110px;
                                height:70px;
                                valign:{valign};
                                background-color: rgb({wch_colour_box[0]}, 
                                                        {wch_colour_box[1]}, 
                                                        {wch_colour_box[2]}, 0.75); 
                                color: rgb({wch_colour_font[0]}, 
                                        {wch_colour_font[1]}, 
                                        {wch_colour_font[2]}, 0.75); 
                                font-size: {fontsize_upper}px; 
                                border-radius: 7px; 
                                padding-left: 17px; 
                                padding-top: 17px; 
                                padding-bottom: 18px; 
                                <i class={iconname} fa-xs'></i> {i}
                                </style><BR><span style='font-size: {fontsize_bottom}px; 
                                margin-top: 0;>{sline}</style></span></p>"""

        return lnk+htmlstr

def card_2(i,backround=(94,156,118)):
        sline = ''
        wch_colour_box = backround
        wch_colour_font = (66,103,178)
        fontsize_upper = 15
        fontsize_bottom = 18
        valign = "middle"
        iconname = "fas fa-asterisk"
        lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.12.1/css/all.css" crossorigin="anonymous">'

        htmlstr = f"""<p style='width:110px;
                                height:70px;
                                valign:{valign};
                                background-color: rgb({wch_colour_box[0]}, 
                                                        {wch_colour_box[1]}, 
                                                        {wch_colour_box[2]}, 0.75); 
                                color: rgb({wch_colour_font[0]}, 
                                        {wch_colour_font[1]}, 
                                        {wch_colour_font[2]}, 0.75); 
                                font-size: {fontsize_upper}px; 
                                border-radius: 7px; 
                                padding-left: 17px; 
                                padding-top: 17px; 
                                padding-bottom: 18px; 
                                <i class={iconname} fa-xs'></i> {i}
                                </style><BR><span style='font-size: {fontsize_bottom}px; 
                                margin-top: 0;>{sline}</style></span></p>"""

        return lnk+htmlstr