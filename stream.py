
from re import X
import streamlit as st
import pandas as pd
from fpdf import FPDF
from fpdf.enums import XPos, YPos
import os.path
import base64
import itertools
style1 = st.markdown("""
    <title>PV Calculator</title>""", unsafe_allow_html=True)

#read css file
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    design_price_value = 400.0
    cable_price_value = 5.0
    corrugated_tube_length = 0.0
    cable_type = "CYABY-F 5x6"
    calculation_df = pd.DataFrame(columns=['Items', 'Qty', 'Unit price (€)', 'Total price (€)'])
    calculation_data = {}
    mounts_price_value = 60.0
    data_manager_price_value = 150.0
    ac_electric_panel_uprice=0.0
    data_manager = "Yes"
    acpanel="No"
    vdc_power_supply_type = "none"
    inverter_power_resell = 0.0
    q_data_manager = 0
    smart_meter_ct_price = 0.0
    sm_tc_tp = 0.0
    t_data_manager_price = 0.0
    o_data_manager_price = 0.0
    vdc_power_supply_tp=0.0
    acpanel_tp = 0.0
    AC_panel_labor_price = 0.0
    vdc_power_supply_total_price = 0.0
    vdc_power_socket_total_price = 0.0
    g_system_labor=0.0
    g_system=0.0
    gr_cable_lines=1
    sl_cable_lines=1
    sm_tc_qty=0

    total_grnew = [0.0,0.0,0.0]
    unit_grnew = [0.0,0.0,0.0]
    total_slnew = [0.0,0.0,0.0]
    unit_slnew = [0.0,0.0,0.0]
    total_pwnew = [0.0,0.0,0.0]
    unit_pwnew = [0.0,0.0,0.0]
    total_ctnew = [0.0,0.0,0.0]
    unit_ctnew = [0.0,0.0,0.0]
    total_acnew = [0.0,0.0,0.0]
    unit_acnew = [0.0,0.0,0.0]
    total_dcnew = [0.0,0.0,0.0]
    unit_dcnew = [0.0,0.0,0.0]
    total_acmcbnew = [0.0,0.0,0.0]
    unit_acmcbnew = [0.0,0.0,0.0]
if 'gr_count' not in st.session_state:
	st.session_state.gr_count = 1
if 'sl_count' not in st.session_state:
	st.session_state.sl_count = 1
if 'pw_count' not in st.session_state:
	st.session_state.pw_count = 1
if 'ct_count' not in st.session_state:
	st.session_state.ct_count = 1
if 'ac_count' not in st.session_state:
	st.session_state.ac_count = 1
if 'dc_count' not in st.session_state:
	st.session_state.dc_count = 1
if 'acmcb_count' not in st.session_state:
	st.session_state.acmcb_count = 1
if 'panels_count' not in st.session_state:
	st.session_state.panels_count = 20
if 'panels_count2' not in st.session_state:
	st.session_state.panels_count2 = 20
if 'total_costs' not in st.session_state:
	st.session_state.total_costs = 0
def create_table(table_data, title='', data_size = 10, title_size=12, align_data='L', align_header='L', cell_width='even', x_start='x_default',emphasize_data=[], emphasize_style=None, emphasize_color=(0,0,0)):
    """
    table_data: 
                list of lists with first element being list of headers
    title: 
                (Optional) title of table (optional)
    data_size: 
                the font size of table data
    title_size: 
                the font size fo the title of the table
    align_data: 
                align table data
                L = left align
                C = center align
                R = right align
    align_header: 
                align table data
                L = left align
                C = center align
                R = right align
    cell_width: 
                even: evenly distribute cell/column width
                uneven: base cell size on lenght of cell/column items
                int: int value for width of each cell/column
                list of ints: list equal to number of columns with the widht of each cell / column
    x_start: 
                where the left edge of table should start
    emphasize_data:  
                which data elements are to be emphasized - pass as list 
                emphasize_style: the font style you want emphaized data to take
                emphasize_color: emphasize color (if other than black) 
    
    """
    default_style = pdf.font_style
    if emphasize_style == None:
        emphasize_style = default_style
    # default_font = pdf.font_family
    # default_size = pdf.font_size_pt
    # default_style = pdf.font_style
    # default_color = pdf.color # This does not work

    # Get Width of Columns
    def get_col_widths():
        col_width = cell_width
        if col_width == 'even':
            col_width = pdf.epw / len(data[0]) - 1  # distribute content evenly   # epw = effective page width (width of page not including margins)
        elif col_width == 'uneven':
            col_widths = []

            # searching through columns for largest sized cell (not rows but cols)
            for col in range(len(table_data[0])): # for every row
                longest = 0 
                for row in range(len(table_data)):
                    cell_value = str(table_data[row][col])
                    value_length = pdf.get_string_width(cell_value)
                    if value_length > longest:
                        longest = value_length
                col_widths.append(longest + 4) # add 4 for padding
            col_width = col_widths



                    ### compare columns 

        elif isinstance(cell_width, list):
            col_width = cell_width  # TODO: convert all items in list to int        
        else:
            # TODO: Add try catch
            col_width = int(col_width)
        return col_width

    # Convert dict to lol
    # Why? because i built it with lol first and added dict func after
    # Is there performance differences?
    if isinstance(table_data, dict):
        header = [key for key in table_data]
        data = []
        for key in table_data:
            value = table_data[key]
            data.append(value)
        # need to zip so data is in correct format (first, second, third --> not first, first, first)
        data = [list(a) for a in zip(*data)]

    else:
        header = table_data[0]
        data = table_data[1:]

    line_height = pdf.font_size * 2.5

    col_width = get_col_widths()
    pdf.set_font('Times',size=title_size)

    # Get starting position of x
    # Determin width of table to get x starting point for centred table
    if x_start == 'C':
        table_width = 0
        if isinstance(col_width, list):
            for width in col_width:
                table_width += width
        else: # need to multiply cell width by number of cells to get table width 
            table_width = col_width * len(table_data[0])
        # Get x start by subtracting table width from pdf width and divide by 2 (margins)
        margin_width = pdf.w - table_width
        # TODO: Check if table_width is larger than pdf width

        center_table = margin_width / 2 # only want width of left margin not both
        x_start = center_table
        pdf.set_x(x_start)
    elif isinstance(x_start, int):
        pdf.set_x(x_start)
    elif x_start == 'x_default':
        x_start = pdf.set_x(pdf.l_margin)


    # TABLE CREATION #

    # add title
    if title != '':
        pdf.multi_cell(0, line_height, title, border=0, align='j', new_x=XPos.LEFT, new_y=YPos.TOP, max_line_height=pdf.font_size)
        pdf.ln(line_height) # move cursor back to the left margin

    pdf.set_font(size=data_size)
    # add header
    y1 = pdf.get_y()
    if x_start:
        x_left = x_start
    else:
        x_left = pdf.get_x()
    x_right = pdf.epw + x_left
    if  not isinstance(col_width, list):
        if x_start:
            pdf.set_x(x_start)
        for datum in header:
            pdf.multi_cell(col_width, line_height, datum, border=0, align=align_header,  new_x=XPos.LEFT, new_y=YPos.TOP, max_line_height=pdf.font_size)
            x_right = pdf.get_x()
        pdf.ln(line_height) # move cursor back to the left margin
        y2 = pdf.get_y()
        pdf.line(x_left,y1,x_right,y1)
        pdf.line(x_left,y2,x_right,y2)

        for row in data:
            if x_start: # not sure if I need this
                pdf.set_x(x_start)
            for datum in row:
                if datum in emphasize_data:
                    pdf.set_text_color(*emphasize_color)
                    pdf.set_font(style=emphasize_style)
                    pdf.multi_cell(col_width, line_height, datum, border=0, align=align_data,  new_x=XPos.LEFT, new_y=YPos.TOP, max_line_height=pdf.font_size)
                    pdf.set_text_color(0,0,0)
                    pdf.set_font(style=default_style)
                else:
                    pdf.multi_cell(col_width, line_height, datum, border=0, align=align_data,  new_x=XPos.LEFT, new_y=YPos.TOP, max_line_height=pdf.font_size) # ln = 3 - move cursor to right with same vertical offset # this uses an object named pdf
            pdf.ln(line_height) # move cursor back to the left margin
    
    else:
        if x_start:
            pdf.set_x(x_start)
        for i in range(len(header)):
            datum = header[i]
            pdf.multi_cell(col_width[i], line_height, datum, border=0, align=align_header,  new_x=XPos.RIGHT, new_y=YPos.LAST, max_line_height=pdf.font_size)
            x_right = pdf.get_x()
        pdf.ln(line_height) # move cursor back to the left margin
        y2 = pdf.get_y()
        pdf.line(x_left,y1,x_right,y1)
        pdf.line(x_left,y2,x_right,y2)


        for i in range(len(data)):
            if x_start:
                pdf.set_x(x_start)
            row = data[i]
            for i in range(len(row)):
                datum = row[i]
                if not isinstance(datum, str):
                    datum = str(datum)
                adjusted_col_width = col_width[i]
                if datum in emphasize_data:
                    pdf.set_text_color(*emphasize_color)
                    pdf.set_font(style=emphasize_style)
                    pdf.multi_cell(adjusted_col_width, line_height, datum, border=0, align=align_data,  new_x=XPos.LEFT, new_y=YPos.TOP, max_line_height=pdf.font_size)
                    pdf.set_text_color(0,0,0)
                    pdf.set_font(style=default_style)
                else:
                    pdf.multi_cell(adjusted_col_width, line_height, datum, border=0, align=align_data,  new_x=XPos.RIGHT, new_y=YPos.LAST, max_line_height=pdf.font_size) # ln = 3 - move cursor to right with same vertical offset # this uses an object named pdf
            pdf.ln(line_height) # move cursor back to the left margin
    y3 = pdf.get_y()
    pdf.line(x_left,y3,x_right,y3)

#logo
#st.image("logo.png", width=150)

#title page
st.title("PV cost calculator")	
st.write("Use this app to calculate costs to build a PV system")

# equipment lists
#inverter list
try:
    filename1 = 'inverter_list.csv'

    if os.path.isfile(filename1): 
        inverter_df = pd.read_csv(filename1)
    else: 
        inverter_df = pd.DataFrame()
except:
    print ('error accesing file')
#pvpanel list
try:
    filename2 = 'panels_list.csv'

    if os.path.isfile(filename2): 
        pvpanel_df = pd.read_csv(filename2)
    else: 
        pvpanel_df = pd.DataFrame()
except:
    print ('error accesing file')
#smart meter list
try:
    filename3 = 'meters_list.csv'

    if os.path.isfile(filename3): 
        smeter_df = pd.read_csv(filename3)
    else: 
        smeter_df = pd.DataFrame()
except:
    print ('error accesing file')

panouri_stoc = pvpanel_df['product_name'].tolist()
inverter_stoc =inverter_df['product_name'].tolist()
meter_stoc = smeter_df['product_name'].tolist()

#_______________________________________________________________________________________________________________________________________________________
with st.expander("Project calculation parameters"):
    tab1, tab0,tab2, tab3, tab4,tab5, tab6, tab7,tab8 = st.tabs(["Information","DTAC", "Equipment", "Cables","AC Panel", "DC Panel","Grounding system", "PV Mounts","Other"])
    with tab1:
        st.subheader("Project declaration")
        dl1,dl2,dl3 = st.columns(3)
        with dl1:
            project = st.text_input("Enter project name", "Project name")
            beneficiary = st.text_input("Enter beneficiary name", "Beneficiary name")	
            address = st.text_input("Enter beneficiary address", "Beneficiary address")
        with dl2:
            date = st.date_input("Enter date of calculation")
            system = st.selectbox("Select system type", ("On-grid", "Off-grid"))
            connection_el = st.selectbox("Select connection type", ("Three phase", "Single phase"))
        with dl3:    
            resell_price = st.number_input("Resell percentage (%)", value=20.0, step=1.0)
            disgr_count = st.number_input("Discount (%)", value=0.0, step=1.0)
            vat_price = st.number_input("VAT (%)", value=19.0, step=1.0)
        resell= (resell_price+100)/100
#_____________________________________________________________________________________________________________________________________________________   
    with tab0:
        st.subheader("Design, Transport, Assembly, Commissioning")

        dtac1,dtac2,dtac3,dtac4,dtac5 = st.columns([2.5,1,1,1,1])
        
        with dtac1:
            st.text_input("#","Transport from warehouse to beneficiary", disabled = True, label_visibility='hidden')
            st.text_input("#","Labor costs for PV Panels including hotel", disabled = True, label_visibility='hidden')
            st.text_input("#","Design and Engineering costs", disabled = True, label_visibility='hidden')
            st.text_input("#","Programming and Commissioning costs", disabled = True, label_visibility='hidden')
        with dtac2:
            distance_travel = st.number_input("Distance (km)", value=600.0, step=10.0)
            direct_pvpanel_labor = st.number_input("Direct PV labor (€/panel)", value=100.0, step=10.0)
        with dtac3:
            transport_price = st.number_input("Transport price (€/km)", value=0.83, step=0.01)
            indirect_pvpanel_labor_percentage = st.number_input("Indirect PV labor (%)", value=15.0, step=1.0)
            design_price = st.number_input("Price. (€) ", value=design_price_value, step=10.0)
            commissioning_price = st.number_input("Price (€)", value=500.0, step=10.0)
        with dtac4:
            transport_up = st.text_input("Unit Price (€/km)", round(transport_price*resell,2), disabled = True, key="transport_up")
            direct_pv_labor_u = direct_pvpanel_labor * resell
            indirect_pv_labor_u = indirect_pvpanel_labor_percentage/100 * direct_pvpanel_labor  * resell
            pv_labor_u = direct_pv_labor_u + indirect_pv_labor_u
            pv_labor_u = st.text_input("Unit Price (€/panel)",round(pv_labor_u,2), disabled=True, key="pv_labor_u")
            design_u = st.text_input("Unit Price (€)", round(design_price*resell,2), disabled=True, key="design_u")
            commissioning_u = st.text_input("Unit Price (€)", round(commissioning_price*resell,2), disabled=True, key="commissioning_u")
        with dtac5:
            if 'panels' not in st.session_state: 
                number_of_panels =  st.session_state.panels_count
            else:
                number_of_panels =  st.session_state["panels"]

            direct_pv_labor = direct_pvpanel_labor * resell * number_of_panels
            indirect_pv_labor = indirect_pvpanel_labor_percentage/100 * direct_pvpanel_labor * number_of_panels * resell
            pv_labor = direct_pv_labor + indirect_pv_labor
            transport_tp = st.text_input("Total Price (€)", round(float(transport_up) *distance_travel,2), disabled = True, key="transport_tp")
            pv_labor_tcost = st.text_input("Total cost (€)", pv_labor, disabled=True)
            design_t = st.text_input("Total price (€)", round(design_price*resell,2), disabled=True, key="design_t")
            commissioning_t = st.text_input("Total price (€)", round(commissioning_price*resell,2), disabled=True, key="commissioning_t")
        dtacs1, = st.columns(1)
        total_cost_design_value = design_price*resell + commissioning_price*resell + pv_labor + float(transport_tp)
        with dtacs1:
            st.text_input("empty", value="", key="total_cost_design",label_visibility="hidden", disabled=True)
            total_costs_eq = st.write(f'<p style=" margin-top: -58px; padding-top:4px; padding-bottom:4px;font-size:22px;border-radius:4px; text-align:right; padding-right:60px;">{"Costs: " + str(total_cost_design_value) + " EUR"}</p>', unsafe_allow_html=True)
    
#_______________________________________________________________________________________________________________________________
    with tab2:
         
        st.subheader("Equipment selection")
        need_data_manager = st.checkbox("Do you need a data manager?")
        c1,c2,c3,c4,c5 = st.columns([2.5,1,1,1,1])
        with c1:
            type_panels = st.selectbox("Choose panel type", (panouri_stoc))
            type_inverter = st.selectbox("Choose inverter", (inverter_stoc))
            smart_meter = st.selectbox("Choose smart meter", (meter_stoc))
            for i in range(len(smeter_df)):
                if smeter_df['product_name'][i] == smart_meter:
                    sm_connetion = smeter_df['connection'][i]  
            if sm_connetion=="indirect":
                sm_tc = st.selectbox("TC type for smart meter.", ("30A", "50A", "100A", "200A"))
            if need_data_manager:
                data_manager = st.selectbox("Choose data manager:", ("Internal board - Data Manager","Panel Mounted Data Manager"))
           
            
        with c2:
            panels = st.number_input("Panels Qty.", value=st.session_state.panels_count,step=1, key="panels")	
            
            inverters = st.number_input("Inverters Qty.", value=1, step=1)
            q_smart_meter = st.number_input("Meter Qty.", value=1, step=1)
            if sm_connetion=="indirect":
                if connection_el == "Three phase":	
                    q_sm_tc_qty = 3
                else:
                    q_sm_tc_qty = 1
                sm_tc_qty = st.number_input("CT Qty.", value=q_sm_tc_qty,step=1)
            if need_data_manager:
                q_data_manager = st.number_input("Data Manager Qty.", value=1, step=1)

        with c3:
            o_pv_price = st.number_input("Panels Sell Price €/pc.", value=150.0, step=10.0)
            o_inverter_price = st.number_input("Inverter Sell Price €/kW", value=375.0, step=5.0)
            o_smart_meter_price = st.number_input("Mater Sell Price €/pc.", value = 300.0, step =0.5)
            if sm_connetion=="indirect":
                smart_meter_ct_price = st.number_input("CT Sell Price €/pc. ", value = 20.0, step =0.5)
            if need_data_manager:
                o_data_manager_price = st.number_input("D. Manager Sell Price €/pc.", value=data_manager_price_value, step=1.0)    
        for i in range(len(inverter_df)):
            if inverter_df['product_name'][i] == type_inverter:
                inverter_power_resell = inverter_df['power'][i]  
            
        with c4:
            pv_price_resell = o_pv_price * resell
            pv_price = st.text_input("Panels Unit Price", str(pv_price_resell),disabled= True)
            inverter_price_resell = round(o_inverter_price * resell * inverter_power_resell, 2)
            inverter_price = st.text_input("Inverter Unit Price", inverter_price_resell,disabled= True)
            smart_meter_price_resell = round(o_smart_meter_price * resell, 2)
            smart_meter_price = st.text_input("Meter Unit Price", smart_meter_price_resell,disabled= True) 
            if sm_connetion=="indirect":
                sm_tc_price_resell = round(smart_meter_ct_price * resell, 2)
                sm_tc_up = st.text_input("CT Unit Price", value=sm_tc_price_resell,disabled= True)
            data_manager_price_value_resell = round(o_data_manager_price * resell, 2)
            if need_data_manager:
                data_manager_price = st.text_input("Data Manager Unit Price", data_manager_price_value_resell,disabled= True)
        with c5:
            t_pv_total_value_resell = pv_price_resell * panels 
            t_pv_price = st.text_input("Panels Total Price", t_pv_total_value_resell,disabled= True)
            t_inverter_price_resell = round(inverter_price_resell * inverters,2)
            t_inverter_price = st.text_input("Inverters Total Price", t_inverter_price_resell,disabled= True)
            t_smart_meter_price_resell = round(smart_meter_price_resell * q_smart_meter,2)
            t_smart_meter_price = st.text_input("Meter Total Price", t_smart_meter_price_resell,disabled= True)
            t_sm_tc_price_resell = round(smart_meter_ct_price * resell * sm_tc_qty , 2)
            if sm_connetion=="indirect":
                sm_tc_tp = st.text_input("CT Total Price", value=t_sm_tc_price_resell,disabled= True)
            t_data_manager_price_value_resell = data_manager_price_value_resell * q_data_manager
            if need_data_manager:
                t_data_manager_price = st.text_input("Data Manager Total Price", t_data_manager_price_value_resell,disabled= True)
        s1, = st.columns(1)
        total_cost_eq_value = float(t_data_manager_price) + float(t_inverter_price) + float(t_pv_price) + float(t_smart_meter_price) + t_sm_tc_price_resell
        with s1:
            st.text_input("empty", value="", key="total_cost_eq",label_visibility="hidden", disabled=True)
            total_costs_eq = st.write(f'<p style=" margin-top: -58px; padding-top:4px; padding-bottom:4px;font-size:22px;border-radius:4px; text-align:right; padding-right:60px;">{"Costs: " + str(total_cost_eq_value) + " EUR"}</p>', unsafe_allow_html=True)
    
    #function to insert new grounding cables
    
    def insert_gr_line( key):
        ex1.selectbox("Choose extra grounding cable type", ("MYF 6","MYF 10", "MYF 16"), key = str("GCT"+str(key)))
        ex2.number_input("Grounding cable (m)", value=15.0, step=1.0,key = "GCL"+str(key))
        ex3.number_input("Gr. cbl. Sell Price", value=3.0, step=0.1,key = "GCP"+str(key))
        
        if st.session_state.gr_count >1:
            for x in range(1, st.session_state.gr_count):
                total_grnew[x]= float(st.session_state["GCP"+str(x)]) * st.session_state["GCL"+str(x)] * resell
                unit_grnew[x] = round(float(st.session_state["GCP"+str(x)]) * resell, 2)
        ex4.text_input("Gr. cbl. Unit Price", value=round(unit_grnew[key],2), key = "GCU"+str(key), disabled=True)
        ex5.text_input("Gr. cbl. Total Price", value=round(total_grnew[key],2), key = "GCTP"+str(key), disabled=True)

    def insert_sl_line( key):
        ex1.selectbox("Choose extra solar cable type", ("Solar 4mm2", "Solar 6mm2", "Solar 10mm2"), key = str("SCT"+str(key)))
        ex2.number_input("Solar cable (m)", value=30.0, step=1.0,key = "SCL"+str(key))
        ex3.number_input("Solar Cable Sell Price", value=2.0, step=0.1,key = "SCP"+str(key))
        
        if st.session_state.sl_count >1:
            for x in range(1, st.session_state.sl_count):
                total_slnew[x]= float(st.session_state["SCP"+str(x)]) * st.session_state["SCL"+str(x)] * resell
                unit_slnew[x] = round(float(st.session_state["SCP"+str(x)]) * resell, 2)
        ex4.text_input("Solar Cable Unit Price", value=round(unit_slnew[key],2), key = "SCU"+str(key), disabled=True)
        ex5.text_input("Solar Cable Total Price", value=round(total_slnew[key],2), key = "SCTP"+str(key), disabled=True)    

    def insert_pw_line( key):
        ex1.selectbox("Choose extra power cable type", ("CYABY-F 5x4", "CYABY-F 5x6", "CYABY-F 5x16"), key = str("PWT"+str(key)))
        ex2.number_input("Power cable (m)", value=30.0, step=1.0,key = "PWL"+str(key))
        ex3.number_input("Power Cable Sell Price", value=2.0, step=0.1,key = "PWP"+str(key))
        
        if st.session_state.pw_count >1:
            for x in range(1, st.session_state.pw_count):
                total_pwnew[x]= float(st.session_state["PWP"+str(x)]) * st.session_state["PWL"+str(x)] * resell
                unit_pwnew[x] = round(float(st.session_state["PWP"+str(x)]) * resell, 2)
        ex4.text_input("Power Cable Unit Price", value=round(unit_pwnew[key],2), key = "PWU"+str(key), disabled=True)
        ex5.text_input("Power Cable Total Price", value=round(total_pwnew[key],2), key = "PWTP"+str(key), disabled=True)  

    def insert_ct_line( key):
        ex1.selectbox("Choose extra corrugated tube dimmension", ("16", "25", "32", "40"), key = str("CTT"+str(key)))
        ex2.number_input("Corrugated tube (m)", value=30.0, step=1.0,key = "CTL"+str(key))
        ex3.number_input("Corrugated Tube Sell Price", value=2.0, step=0.1,key = "CTP"+str(key))
        
        if st.session_state.ct_count >1:
            for x in range(1, st.session_state.ct_count):
                total_ctnew[x]= float(st.session_state["CTP"+str(x)]) * st.session_state["CTL"+str(x)] * resell
                unit_ctnew[x] = round(float(st.session_state["CTP"+str(x)]) * resell, 2)
        ex4.text_input("Corrugated Tube Unit Price", value=round(unit_ctnew[key],2), key = "CTU"+str(key), disabled=True)
        ex5.text_input("Corrugated Tube Total Price", value=round(total_ctnew[key],2), key = "CTTP"+str(key), disabled=True)  

    def insert_ac_line( key):
        eac1.selectbox("Choose extra AC Panel", ("50x40x20", "60x60x20"), key = str("ACT"+str(key)))
        eac2.number_input("Qty.", value=1.0, step=1.0,key = "ACL"+str(key))
        eac3.number_input("AC Panel Sell Price", value=100.0, step=1.0,key = "ACP"+str(key))
        
        if st.session_state.ac_count >1:
            for x in range(1, st.session_state.ac_count):
                total_acnew[x]= float(st.session_state["ACP"+str(x)]) * st.session_state["ACL"+str(x)] * resell
                unit_acnew[x] = round(float(st.session_state["ACP"+str(x)]) * resell, 2)
        eac4.text_input("AC Panel Unit Price", value=round(unit_acnew[key],2), key = "ACU"+str(key), disabled=True)
        eac5.text_input("AC Panel Total Price", value=round(total_acnew[key],2), key = "ACTP"+str(key), disabled=True)  

    def insert_dc_line( key):
        edc1.selectbox("Choose extra DC Panel", ("50x40x20", "60x60x20"), key = str("DCT"+str(key)))
        edc2.number_input("Qty.", value=1.0, step=1.0,key = "DCL"+str(key))
        edc3.number_input("DC Panel Sell Price", value=100.0, step=1.0,key = "DCP"+str(key))
        
        if st.session_state.dc_count >1:
            for x in range(1, st.session_state.dc_count):
                total_dcnew[x]= float(st.session_state["DCP"+str(x)]) * st.session_state["DCL"+str(x)] * resell
                unit_dcnew[x] = round(float(st.session_state["DCP"+str(x)]) * resell, 2)
        edc4.text_input("DC Panel Unit Price", value=round(unit_dcnew[key],2), key = "DCU"+str(key), disabled=True)
        edc5.text_input("DC Panel Total Price", value=round(total_dcnew[key],2), key = "DCTP"+str(key), disabled=True)

    def insert_acmcb_line( key):
        eac1.selectbox("Choose extra AC MCB", ("20A", "25A", "32A", "40A", "50A", "63A", "80A", "100A"), key = str("ACMCBT"+str(key)))
        eac2.number_input("Qty.", value=1.0, step=1.0,key = "ACMCBL"+str(key))
        eac3.number_input("AC MCB Sell Price", value=50.0, step=1.0,key = "ACMCBP"+str(key))
        
        if st.session_state.acmcb_count >1:
            for x in range(1, st.session_state.acmcb_count):
                total_acmcbnew[x]= float(st.session_state["ACMCBP"+str(x)]) * st.session_state["ACMCBL"+str(x)] * resell
                unit_acmcbnew[x] = round(float(st.session_state["ACMCBP"+str(x)]) * resell, 2)
        eac4.text_input("AC MCB Unit Price", value=round(unit_acmcbnew[key],2), key = "ACMCBU"+str(key), disabled=True)
        eac5.text_input("AC MCB Total Price", value=round(total_acmcbnew[key],2), key = "ACMCBTP"+str(key), disabled=True)  

#_______________________________________________________________________________________________________________________________________________
    with tab3:
        st.subheader("Cables selection")
        

            
        dl1, dl2, dl3, dl4, dl5,dl6,dl7,dl8,dl9,dl10,dl11,dl12 = st.columns([0.45,0.12,0.12,0.45,0.12,0.12,0.45,0.12,0.12,0.45,0.12,0.12])

        with dl1:
            st.write(f'<p style="text-align:center;padding-top:4px; padding-bottom:4px;">{"Grounding cable ⏵"}</p>', unsafe_allow_html=True)
        with dl2:
            gr_btnup=st.button("+", key="gr_btnup")
            if gr_btnup:
                if st.session_state.gr_count < 3:
                    st.session_state.gr_count = st.session_state.gr_count + 1
        with dl3:
            gr_btndown=st.button("-", key="gr_btndown")
            if gr_btndown:
                if st.session_state.gr_count > 1:
                    st.session_state.gr_count = st.session_state.gr_count - 1
                    
        #_______________________________________________________________________________________________________________________________
        with dl4:
            st.write(f'<p style="text-align:center;padding-top:4px; padding-bottom:4px;">{"Solar cable ⏵"}</p>', unsafe_allow_html=True)
        with dl5:
            sl_btnup=st.button("+", key="sl_btnup")
            if sl_btnup:
                if st.session_state.sl_count < 3:
                    st.session_state.sl_count = st.session_state.sl_count + 1 
        with dl6:
            sl_btndown=st.button("-", key="sl_btndown")
            if sl_btndown:
                if st.session_state.sl_count > 1:
                    st.session_state.sl_count = st.session_state.sl_count - 1
        #_______________________________________________________________________________________________________________________________
        with dl7:
            st.write(f'<p style="text-align:center;padding-top:4px; padding-bottom:4px;">{"Power cable  ⏵"}</p>', unsafe_allow_html=True)     
        with dl8:
            pw_btnup=st.button("+", key="pw_btnup")
            if pw_btnup:
                if st.session_state.pw_count < 3:
                    st.session_state.pw_count = st.session_state.pw_count + 1 
        with dl9:
            pw_btndown=st.button("-", key="pw_btndown") 
            if pw_btndown:
                if st.session_state.pw_count > 1:
                    st.session_state.pw_count = st.session_state.pw_count - 1
        #_______________________________________________________________________________________________________________________________
        with dl10:
            st.write(f'<p style="text-align:center;padding-top:4px; padding-bottom:4px;">{"Corrugated tube ⏵"}</p>', unsafe_allow_html=True)     
        with dl11:
            ct_btnup=st.button("+", key="ct_btnup")
            if ct_btnup:
                if st.session_state.ct_count < 3:
                    st.session_state.ct_count = st.session_state.ct_count + 1 
        with dl12:
            ct_btndown=st.button("-", key="ct_btndown") 
            if ct_btndown:
                if st.session_state.ct_count > 1:
                    st.session_state.ct_count = st.session_state.ct_count - 1
        
        #extra cable table
        if st.session_state.gr_count >1 or st.session_state.sl_count >1 or st.session_state.pw_count >1 or st.session_state.ct_count >1:
            st.write(f'<p style="text-align:left;padding-top:4px; padding-left:4px;padding-bottom:4px; border-radius:2px; background-color:rgba(180,35,35,0.2);">{" Extra Cables"}</p>', unsafe_allow_html=True) 
            
        ex1,ex2,ex3,ex4,ex5 = st.columns([2.5,1,1,1,1]) 
        with ex1:
            if str(st.session_state.gr_count) =="2":
                gr_cable_lines = 1
                insert_gr_line(gr_cable_lines)
            if str(st.session_state.gr_count) =="3":
                gr_cable_lines = 2
                insert_gr_line(gr_cable_lines)
                gr_cable_lines = 1
                insert_gr_line(gr_cable_lines)

            if str(st.session_state.sl_count) =="2":
                sl_cable_lines = 1
                insert_sl_line(sl_cable_lines)
            if str(st.session_state.sl_count) =="3":
                sl_cable_lines = 2
                insert_sl_line(sl_cable_lines)
                sl_cable_lines = 1
                insert_sl_line(sl_cable_lines)

            if str(st.session_state.pw_count) =="2":
                pw_cable_lines = 1
                insert_pw_line(pw_cable_lines)
            if str(st.session_state.pw_count) =="3":
                pw_cable_lines = 2
                insert_pw_line(pw_cable_lines)
                pw_cable_lines = 1
                insert_pw_line(pw_cable_lines)

            if str(st.session_state.ct_count) =="2":
                ct_cable_lines = 1
                insert_ct_line(ct_cable_lines)
            if str(st.session_state.ct_count) =="3":
                ct_cable_lines = 2
                insert_ct_line(ct_cable_lines)
                ct_cable_lines = 1
                insert_ct_line(ct_cable_lines)

        #add st.markdown with horizontal separator style

        if st.session_state.gr_count >1 or st.session_state.sl_count >1 or st.session_state.pw_count >1 or st.session_state.ct_count >1:
            st.markdown("---")
            st.write(f'<p style="text-align:left;padding-top:4px; padding-left:4px;padding-bottom:4px; border-radius:2px; background-color:rgba(85,180,85,0.2);">{"Cables"}</p>', unsafe_allow_html=True) 

        # normal table
        d1,d2,d3,d4,d5 = st.columns([2.5,1,1,1,1])
        with d1:
            grounding_cable_type = st.selectbox("Choose grounding cable type", ("MYF 6","MYF 10", "MYF 16"))
            solar_cable_type = st.selectbox("Choose solar cable type", ("Solar 4mm2", "Solar 6mm2", "Solar 10mm2"))
            power_cable_type = st.selectbox("Choose power cable type", ("CYABY-F 5x4", "CYABY-F 5x6", "CYABY-F 5x16"))
            FTP_cable_type = st.selectbox("Choose FTP cable type", ("FTP 4x2x0.5", "FTP 4x2x0.85"))
            corrugated_tube_type = st.selectbox("Choose corrugated tube dimmension", ("16", "25", "32", "40"))
        with d2:
            l_grounding= st.number_input("Grounding cable (m)", value=15.0, step=1.0)
            l_inverter = st.number_input("Solar cable (m) ", value=25.0, step=1.0)
            l_meter = st.number_input("Power cable (m)", value=30.0, step=1.0)
            l_ftp_meter = st.number_input("FTP cable (m)", value=30.0, step=1.0)
            l_corrugated_tube = st.number_input("Corrugated tube (m)", value=l_ftp_meter+l_meter+l_grounding + (l_inverter/2), step=0.1)
        with d3:
            ground_cable_price = st.number_input("Gr. cbl. Sell Price", value=3.0, step=0.1, key="ground_cable_price")
            solar_cable_price = st.number_input("Solar Cable Sell Price", value=2.0, step=0.1)
            power_cable_price = st.number_input("Power Cable Sell Price", value=cable_price_value, step=0.1)
            ftp_cable_price = st.number_input("FTP Sell Price", value=1.0, step=0.1)
            corrugated_tube_price = st.number_input("Corrugated Tube Sell Price", value=2.0, step=0.1)
        with d4:
            gr_price_unit = round(ground_cable_price* resell,2)
            solar_price_unit = solar_cable_price* resell
            power_price_unit = power_cable_price* resell
            ftp_price_unit = ftp_cable_price* resell
            corrugated_tube_price_unit = corrugated_tube_price* resell
            gr_price = st.text_input("Gr. Cbl. Unit Price", gr_price_unit,disabled= True, key="gr_price")
            solar_price = st.text_input("Solar Cable Unit Price", solar_price_unit,disabled= True)
            power_price = st.text_input("Power Cable Unit Price", power_price_unit,disabled= True)
            ftp_price = st.text_input("FTP Sell Price", ftp_price_unit,disabled= True)
            cor_tube_price = st.text_input("Corrugated Tube Unit Price", corrugated_tube_price_unit,disabled= True)
        with d5:
            t_gr_price_unit = round(ground_cable_price* resell*l_grounding,2)
            t_solar_price_unit = solar_cable_price* resell*l_inverter
            t_power_price_unit = power_cable_price* resell*l_meter
            t_ftp_price_unit = ftp_cable_price* resell*l_ftp_meter
            t_corrugated_tube_price_unit = corrugated_tube_price* resell*l_corrugated_tube
            t_gr_price = st.text_input("Gr. Cbl. Total Price", t_gr_price_unit,disabled= True, key="t_gr_price")
            t_solar_price = st.text_input("Solar Cable Total Price", t_solar_price_unit,disabled= True)
            t_power_meter_price = st.text_input("Power Cable Total Price", t_power_price_unit,disabled= True)
            t_ftp_price = st.text_input("FTP Total Price", t_ftp_price_unit,disabled= True)
            t_corrugated_tube_price = st.text_input("Corrugated Tube Total Price", round(t_corrugated_tube_price_unit,2),disabled= True)
        r1, = st.columns(1)
        total_cost_cables_value = float(t_gr_price) + float(t_solar_price) + float(t_power_meter_price) + float(t_ftp_price) + float(t_corrugated_tube_price)
        # add extra cables costs
        for x in range(1, st.session_state.gr_count):
            total_cost_cables_value = total_cost_cables_value + total_grnew[x]
        for x in range(1, st.session_state.sl_count):
            total_cost_cables_value = total_cost_cables_value + total_slnew[x]
        for x in range(1, st.session_state.pw_count):
            total_cost_cables_value = total_cost_cables_value + total_pwnew[x]
        for x in range(1, st.session_state.ct_count):
            total_cost_cables_value = total_cost_cables_value + total_ctnew[x]
        #show total cable costs
        with r1:
            st.text_input("empty", value="", key="total_cost_cables",label_visibility="hidden", disabled=True)
            total_costs_cables = st.write(f'<p style=" margin-top: -58px; padding-top:4px; padding-bottom:4px;font-size:22px;border-radius:4px; text-align:right; padding-right:60px;">{"Costs: " + str(round(total_cost_cables_value,2)) + " EUR"}</p>', unsafe_allow_html=True)
    

#_________________________________________________________________________________________________________________________________________________    
    with tab4:
        st.subheader("AC panel")
        acl1, acl2, acl3, acl4, acl5,acl6,acl7,acl8,acl9,acl10 = st.columns([0.8,0.13,0.13,0.4,0.45,0.13,0.13,0.45,0.13,0.13])
            
        with acl1:
            need_AC_panel = st.checkbox("Do you need an AC panel?")
        with acl8:
            if need_AC_panel == False:

                st.write(f'<p style="text-align:center;padding-top:4px; padding-bottom:4px;">{"AC MCB ⏵"}</p>', unsafe_allow_html=True)
        with acl9:
            if need_AC_panel == False:

                acmcb_btnup=st.button("+", key="acmcb_btnup")
                if acmcb_btnup:
                    if st.session_state.acmcb_count < 3:
                        st.session_state.acmcb_count = st.session_state.acmcb_count + 1 
        with acl10:
            if need_AC_panel == False:

                acmcb_btndown=st.button("-", key="acmcb_btndown")
                if acmcb_btndown:
                    if st.session_state.acmcb_count > 1:
                        st.session_state.acmcb_count = st.session_state.acmcb_count - 1
        
        if need_AC_panel:
            acpanel="Yes"
            

            acl1, acl2, acl3, acl4, acl5,acl6,acl7,acl8,acl9,acl10 = st.columns([0.8,0.45,0.13,0.13,0.45,0.13,0.13,0.45,0.13,0.13])
            with acl1:
                AC_panel_labor_price = st.number_input("AC electric panel labor percentage (%)", value=30.0, step=1.0)

            with acl5:
                st.write("##")
                st.write(f'<p style="text-align:center;padding-top:4px; padding-bottom:4px;">{"AC MCB ⏵"}</p>', unsafe_allow_html=True)
            with acl6:
                st.write("##")
                acmcb_btnup=st.button("+", key="acmcb_btnup")
                if acmcb_btnup:
                    if st.session_state.acmcb_count < 3:
                        st.session_state.acmcb_count = st.session_state.acmcb_count + 1 
            with acl7:
                st.write("##")
                acmcb_btndown=st.button("-", key="acmcb_btndown")
                if acmcb_btndown:
                    if st.session_state.acmcb_count > 1:
                        st.session_state.acmcb_count = st.session_state.acmcb_count - 1

            with acl8:
                st.write("##")
                st.write(f'<p style="text-align:center;padding-top:4px; padding-bottom:4px;">{"AC panel ⏵"}</p>', unsafe_allow_html=True)
            with acl9:
                st.write("##")
                ac_btnup=st.button("+", key="ac_btnup")
                if ac_btnup:
                    if st.session_state.ac_count < 3:
                        st.session_state.ac_count = st.session_state.ac_count + 1 
            with acl10:
                st.write("##")
                ac_btndown=st.button("-", key="ac_btndown")
                if ac_btndown:
                    if st.session_state.ac_count > 1:
                        st.session_state.ac_count = st.session_state.ac_count - 1
                
        else:
            acpanel="No"


        if st.session_state.ac_count >1 or st.session_state.acmcb_count >1:
            st.write(f'<p style="text-align:left;padding-top:4px; padding-left:4px;padding-bottom:4px; border-radius:2px; background-color:rgba(180,35,35,0.2);">{" Extra AC Panel Equipment"}</p>', unsafe_allow_html=True) 

        eac1,eac2,eac3,eac4,eac5 = st.columns([2.5,1,1,1,1])
        with eac1:

            if str(st.session_state.ac_count) =="2":
                ac_cable_lines = 1
                insert_ac_line(ac_cable_lines)
            if str(st.session_state.ac_count) =="3":
                ac_cable_lines = 2
                insert_ac_line(ac_cable_lines)
                ac_cable_lines = 1
                insert_ac_line(ac_cable_lines)

            if str(st.session_state.acmcb_count) =="2":
                acmcb_cable_lines = 1
                insert_acmcb_line(acmcb_cable_lines)
            if str(st.session_state.acmcb_count) =="3":
                acmcb_cable_lines = 2
                insert_acmcb_line(acmcb_cable_lines)
                acmcb_cable_lines = 1
                insert_acmcb_line(acmcb_cable_lines)

        if st.session_state.ac_count >1 or st.session_state.acmcb_count >1:
            st.markdown("---")
            st.write(f'<p style="text-align:left;padding-top:4px; padding-left:4px;padding-bottom:4px; border-radius:2px; background-color:rgba(85,180,85,0.2);">{"AC Panel Equipment"}</p>', unsafe_allow_html=True) 


        e1,e2,e3,e4,e5 = st.columns([2.5,1,1,1,1])
        with e1:
            acbreaker_type= st.selectbox("AC MCB", ("20A", "25A", "32A", "40A", "50A", "63A", "80A", "100A"))
            ac_sm_breaker_type= st.selectbox("Smart meter MCB", ("6A", "10A" ))
            if data_manager=="Panel Mounted Data Manager":
                vdc_power_supply_type= st.selectbox("220 VAC Data Manager Charger", ("Data Manager - charger", ))
                vdc_power_socket_type= st.selectbox("220 VAC socket for Data Manager", ("Panel power socket 220 VAC", ))
            if need_AC_panel:
                acpanel = st.selectbox("AC panel type", ("50x40x20", "60x60x20"))
            AC_small_mat_type = st.text_input("Extra materials (€)", "Small material",  key= "AC_small_mat_type",disabled=True)
            
        with e2:
            acbreaker_qty = st.number_input("Quantity", value=1,step=1)
            ac_sm_breaker_qty = st.number_input("SMMCB qty(€)",value=1,step=1,label_visibility="hidden")
            if data_manager=="Panel Mounted Data Manager":
                vdc_power_supply_qty = st.number_input("Charger sty (€)", value=1,step=1,label_visibility="hidden")
                vdc_power_socket_qty = st.number_input("Socket qty (€)", value=1,step=1,label_visibility="hidden")
            if need_AC_panel:
                acpanel_qty = st.number_input("AC panel price (€)", value=1,step=1,label_visibility="hidden")
            AC_small_mat_qty = st.number_input("Small material price (€)", value=1.0, step=1.0, key= "AC_small_mat_qty",  label_visibility="hidden")
        with e3:
            
            acbreaker_price= st.number_input("Sell price", value=50.0,step=0.5, key="acbreaker_price")
            ac_sm_breaker_price= st.number_input("ac_sm price (€)", value=6.0,step=0.5,label_visibility="hidden")
            if data_manager=="Panel Mounted Data Manager":
                vdc_power_supply_price= st.number_input("ps (€)", value=25.0,step=0.5,label_visibility="hidden")
                vdc_power_socket_price= st.number_input("pso (€)", value=10.0,step=0.5,label_visibility="hidden")
            if need_AC_panel:
                ac_electric_panel_price = st.number_input("AC panel price (€)", value=100.0, step=1.0,label_visibility="hidden")    
                AC_small_mat_price = st.number_input("Small  (€)", value=50.0, step=1.0, key= "AC_small_mat_price", label_visibility="hidden")
            else:
                AC_small_mat_price = st.number_input("Small  (€)", value=25.0, step=1.0, key= "AC_small_mat_price", label_visibility="hidden")
        with e4:
            acbreaker_uprice = round(acbreaker_price* resell,2)
            ac_sm_breaker_uprice = round(ac_sm_breaker_price* resell,2)
            ac_mcb_price = st.text_input("Unit Price", acbreaker_uprice,disabled= True, key="ac_mcb_up")
            ac_sm_mcb_price = st.text_input("S up (€/kW)", ac_sm_breaker_uprice,label_visibility="hidden",disabled= True, key="ac_sm_mcb_up")
            if data_manager=="Panel Mounted Data Manager":
                vdc_power_supply_uprice = round(vdc_power_supply_price* resell,2)
                vdc_power_supply_up= st.text_input("ps up (€)", vdc_power_supply_uprice,disabled= True,label_visibility="hidden")
                vdc_power_socket_uprice = round(vdc_power_socket_price* resell,2)
                vdc_power_socket_up= st.text_input("pso up (€)", vdc_power_socket_uprice,disabled= True,label_visibility="hidden")
            if need_AC_panel:
                ac_electric_panel_uprice = round(ac_electric_panel_price* resell,2)
                acpanel_up = st.text_input("AC panel up (€)", ac_electric_panel_uprice,disabled= True,label_visibility="hidden")
            AC_small_mat_uprice = st.text_input("Extra materials (€)", value = round(AC_small_mat_price*resell,2),  key= "AC_small_mat_uprice",disabled=True, label_visibility="hidden")
            
        with e5:
            acbreaker_total_price = acbreaker_uprice*acbreaker_qty
            ac_sm_breaker_total_price = ac_sm_breaker_uprice * ac_sm_breaker_qty
            ac_mcb_tp = st.text_input("Total Price", acbreaker_total_price,disabled= True, key="ac_mcb_tp")
            ac_sm_mcb_tp = st.text_input("S up (€/kW)", ac_sm_breaker_total_price,label_visibility="hidden",disabled= True, key="ac_sm_mcb_tp")
            if data_manager=="Panel Mounted Data Manager":
                vdc_power_supply_total_price = vdc_power_supply_uprice*vdc_power_supply_qty
                vdc_power_supply_tp= st.text_input("pstp up (€)", vdc_power_supply_total_price,disabled= True,label_visibility="hidden")
                vdc_power_socket_total_price = vdc_power_socket_uprice*vdc_power_socket_qty
                vdc_power_socket_tp= st.text_input("pstpo up (€)", vdc_power_socket_total_price,disabled= True,label_visibility="hidden")
            if need_AC_panel:
                ac_electric_panel_total_price = ac_electric_panel_uprice*acpanel_qty
                acpanel_tp = st.text_input("AC panel tp (€)", ac_electric_panel_total_price,disabled= True,label_visibility="hidden")
            labor_total_price = (float(ac_mcb_tp)+float(ac_sm_mcb_tp)+float(vdc_power_supply_tp)+float(acpanel_tp) +vdc_power_supply_total_price+vdc_power_socket_total_price)*(AC_panel_labor_price/100)
            AC_small_mat_tprice = st.text_input("Extra materials (€)", value = round(AC_small_mat_price*resell*AC_small_mat_qty,2),  key= "AC_small_mat_tprice",disabled=True, label_visibility="hidden")
        
            
        q1, = st.columns(1)
        total_cost_AC_value = round(float(ac_mcb_tp)+float(ac_sm_mcb_tp)+float(vdc_power_supply_tp)+float(acpanel_tp) + labor_total_price +vdc_power_supply_total_price+vdc_power_socket_total_price+float(AC_small_mat_tprice),2)
        # add extra cables costs
        for x in range(1, st.session_state.ac_count):
            total_cost_AC_value = total_cost_AC_value + (total_acnew[x]*(AC_panel_labor_price/100+1))
        for x in range(1, st.session_state.acmcb_count):
            if need_AC_panel:
                total_cost_AC_value = total_cost_AC_value + (total_acmcbnew[x]*(AC_panel_labor_price/100+1))
            else:
                total_cost_AC_value = total_cost_AC_value + total_acmcbnew[x]
        with q1:
            total_cost_AC_value= round(total_cost_AC_value,2)
            st.text_input("empty", value="", key="total_cost_ac",label_visibility="hidden", disabled=True)
            total_costs_AC = st.write(f'<p style=" margin-top: -58px; padding-top:4px; padding-bottom:4px;font-size:22px;border-radius:4px; text-align:right; padding-right:60px;">{"Costs: " + str(total_cost_AC_value) + " EUR"}</p>', unsafe_allow_html=True)
#_______________________________________________________________________________________________________________________________________________        
    with tab5:
        st.subheader("DC panel")
        cl1,cl2,cl3,cl4,cl5,cl6,cl7 = st.columns([1,1,0.6,0.13,0.45,0.16,0.16])
        with cl1:
            strings = st.number_input("DC strings", value=2, step=1)
        with cl2:
            panel_labor_price = st.number_input("DC electric panel labor percentage (%)", value=30.0, step=1.0)
        with cl5:
            st.write("##")
            st.write(f'<p style="text-align:center;padding-top:4px; padding-bottom:4px;">{"DC panel ⏵"}</p>', unsafe_allow_html=True)
        with cl6:
            st.write("##")
            dc_btnup=st.button("+", key="dc_btnup")
            if dc_btnup:
                    if st.session_state.dc_count < 3:
                        st.session_state.dc_count = st.session_state.dc_count + 1 
        with cl7:
            st.write("##")
            dc_btndown=st.button("-", key="dc_btndown")
            if dc_btndown:
                if st.session_state.dc_count > 1:
                    st.session_state.dc_count = st.session_state.dc_count - 1

        if st.session_state.dc_count >1 :
            st.write(f'<p style="text-align:left;padding-top:4px; padding-left:4px;padding-bottom:4px; border-radius:2px; background-color:rgba(180,35,35,0.2);">{" Extra DC Panel Equipment"}</p>', unsafe_allow_html=True) 

        edc1,edc2,edc3,edc4,edc5 = st.columns([2.5,1,1,1,1])
        with edc1:

            if str(st.session_state.dc_count) =="2":
                dc_cable_lines = 1
                insert_dc_line(dc_cable_lines)
            if str(st.session_state.dc_count) =="3":
                dc_cable_lines = 2
                insert_dc_line(dc_cable_lines)
                dc_cable_lines = 1
                insert_dc_line(dc_cable_lines)

        if st.session_state.dc_count >1 :
            st.markdown("---")
            st.write(f'<p style="text-align:left;padding-top:4px; padding-left:4px;padding-bottom:4px; border-radius:2px; background-color:rgba(85,180,85,0.2);">{"DC Panel Equipment"}</p>', unsafe_allow_html=True) 

        f1,f2,f3,f4,f5 = st.columns([2.5,1,1,1,1])
        with f1:
            
            dcfuse_type= st.selectbox("DC fuse", ("16A", "20A", "25A", "32A", "40A", "50A", "63A"))
            dcfuse_slot_type= st.selectbox("DC Fuse Slot", ("ETI", "Noark"))
            discharger_type = st.selectbox("Discharger selector", ("Schneider", "Noark"))
            pv_cable_connector = st.text_input("Solar cable connectors", "PV cable connector set", disabled=True)
            dc_electric_panel_type = st.selectbox("DC electric panel type", ("50x40x20", "60x60x20")) 
            small_material_type = st.text_input("Extra materials", "Small Material", disabled=True)
        with f2:
            dcfuse_qty= st.number_input("Quantity", value=2*strings, step=1, key = "dcfuse_qty", disabled=True)
            dcfuse_slot_qty= st.number_input(" slotd price (€)", value=strings, step=1,label_visibility="hidden",disabled=True)
            discharger_qty = st.number_input("dischdarger price (€)", value=strings, step=1,label_visibility="hidden",disabled=True)
            connector_qty = st.number_input(" connedctor price (€)", value=15, step=1,label_visibility="hidden")
            dc_electric_panel_qty = st.number_input("DC eledctric panel(€)", value=1, step=1,label_visibility="hidden")
            small_mat_qty = st.number_input("Small material price (€)", value=1.0, step=1.0,label_visibility="hidden", key="small_mat_qty")
        with f3:
            dcfuse_price= st.number_input("Sell price", value=5.0, step=0.5, key = "dcfuse_price")
            dcfuse_slot_price= st.number_input(" slot price (€)", value=7.5, step=0.5,label_visibility="hidden")
            discharger_price = st.number_input("discharger price (€)", value=100.0, step=5.0,label_visibility="hidden")
            connector_price = st.number_input(" connector price (€)", value=5.0, step=0.1,label_visibility="hidden")
            dc_electric_panel_price = st.number_input("DC electric panel(€)", value=120.0, step=1.0,label_visibility="hidden")    
            small_mat_price = st.number_input("Small material price (€)", value=150.0, step=1.0,label_visibility="hidden")
        with f4:
            dcfuse_uuprice= dcfuse_price*resell
            dcfuse_slot_uuprice= dcfuse_slot_price*resell
            discharger_uuprice = discharger_price*resell
            connector_uuprice = connector_price*resell
            dc_electric_panel_uuprice = dc_electric_panel_price*resell
            dcfuse_uprice= st.text_input("Unit price", dcfuse_uuprice,  key = "dcfuse_uprice",disabled=True)
            dcfuse_slot_uprice= st.text_input(" slot uprice (€)", dcfuse_slot_uuprice, label_visibility="hidden",disabled=True)
            discharger_uprice = st.text_input("discharger uprice (€)", discharger_uuprice, label_visibility="hidden",disabled=True)
            connector_uprice = st.text_input("connector uprice (€)", connector_uuprice, label_visibility="hidden",disabled=True)
            dc_electric_panel_uprice = st.text_input("DC electric uprice(€)", dc_electric_panel_uuprice, label_visibility="hidden",disabled=True)
            small_mat_uprice = st.text_input("Small material price (€)", value=round(small_mat_price*resell,2), disabled=True, label_visibility="hidden",key="small_mat_uprice")
        with f5:

            dcfuse_total_price = float(dcfuse_uprice) * float(dcfuse_qty)
            dcfuse_slot_total_price= float(dcfuse_slot_uprice) * dcfuse_slot_qty
            discharger_total_price = float(discharger_uprice) * discharger_qty
            connector_total_price = float(connector_uprice) * connector_qty
            dc_electric_panel_total_price = float(dc_electric_panel_uprice)*dc_electric_panel_qty
            dcfuse_tprice= st.text_input("Total price", dcfuse_total_price,  key = "dcfuse_tprice",disabled=True)
            dcfuse_slot_tprice= st.text_input(" slot tprice (€)", dcfuse_slot_total_price, label_visibility="hidden",disabled=True)
            discharger_tprice = st.text_input("discharger tprice (€)",  discharger_total_price, label_visibility="hidden",disabled=True)
            connector_tprice = st.text_input(" connector tprice (€)", connector_total_price, label_visibility="hidden",disabled=True)
            dc_electric_panel_tprice = st.text_input("DC electric tprice(€)", dc_electric_panel_total_price, label_visibility="hidden",disabled=True)
            laborDC_total_price = (dcfuse_total_price + dcfuse_slot_total_price + discharger_total_price + connector_total_price+dc_electric_panel_total_price)*(panel_labor_price/100)
            small_mat_tprice = st.text_input("Small material price (€)", value=round(small_mat_price*resell*small_mat_qty,2), disabled=True, label_visibility="hidden",key="small_mat_tprice")

        
            
        g1, = st.columns(1)
        total_cost_DC_value = round(dcfuse_total_price + dcfuse_slot_total_price + discharger_total_price + connector_total_price+dc_electric_panel_total_price+laborDC_total_price + float(small_mat_tprice),2)
        for x in range(1, st.session_state.dc_count):
            total_cost_DC_value = round(total_cost_DC_value + (total_dcnew[x]*(panel_labor_price/100+1)),2)
        
        with g1:
            st.text_input("empty", value="", key="total_cost_dc",label_visibility="hidden", disabled=True)
            total_costs_DC = st.write(f'<p style=" margin-top: -58px; padding-top:4px; padding-bottom:4px;font-size:22px;border-radius:4px; text-align:right; padding-right:60px;">{"Costs: " + str(total_cost_DC_value) + " EUR"}</p>', unsafe_allow_html=True)
#_______________________________________________________________________________________________________________________________    
    with tab6:
        st.subheader("Grounding system")
        need_grounding_system = st.checkbox("Do you need a grounding system?")
        if need_grounding_system:
            grounding = "Yes"
            g_system = st.number_input("Enter grounding system total materials prices (€)", value=515.0, step=10.0)
            g_system_labor = st.number_input("Enter grounding system labor and equipment renting price (€)", value=1405.0, step=10.0)
        else:
            grounding = "No"
        
        measure_g_system = st.number_input("Enter grounding system measurement price (€)", value=100.0, step=10.0)

        t1, = st.columns(1)
        total_cost_gr_value = measure_g_system*resell + g_system_labor +g_system
        with t1:
            st.text_input("empty", value="", key="total_cost_gr",label_visibility="hidden", disabled=True)
            total_costs_gr = st.write(f'<p style=" margin-top: -58px; padding-top:4px; padding-bottom:4px;font-size:22px;border-radius:4px; text-align:right; padding-right:60px;">{"Costs: " + str(total_cost_gr_value) + " EUR"}</p>', unsafe_allow_html=True)
 #_______________________________________________________________________________________________________________________________   
    
    with tab7:
        st.subheader("PV panel mounting system")

        plm1,plm2,plm3,plm4,plm5 = st.columns(5)
        with plm1:
            roofing_type = st.selectbox("What kind of roofing is it?", ("Metal sandwich", "Metal sheet","Tiles", "Flat"))
            if roofing_type == "Metal sandwich":
                mounts_price_value = 60.0
            else:
                mounts_price_value = 70.0
            if roofing_type == "Flat":
                mounts_price_value = 300.0
            #pv_panel_mounts_price = st.number_input("Enter panel mounts price (€)", value=mounts_price_value, step=1.0)

        with plm2:  
            pv_panel_spacing = 0.0 
            if roofing_type != "Flat":
                pv_panel_spacing= st.number_input("Spacing between mounts (m)", value=0.8, step=0.1)
                if pv_panel_spacing <= 0.4 and roofing_type == "Metal sandwich":
                    panel_mount_type = "Mini-rail "
                    mounts_qty_calc = panels*4
                    mounts_price_value = 15.0
                elif pv_panel_spacing > 0.4 and roofing_type == "Metal sandwich":
                    panel_mount_type = "Micro-rail "
                    mounts_qty_calc = panels*4
                    mounts_price_value = 15.0
                elif roofing_type != "Flat":
                    panel_mount_type = "3.3 m rail  "
                    mounts_qty_calc = panels
                    mounts_price_value = 70.0
            if roofing_type == "Flat":
                panel_mount_type = "15° - Flat roof mounting system "
                mounts_qty_calc = panels
                mounts_price_value = 300.0

        with plm3:
        
            groups = st.number_input("Number of groups", value=0, step=1)

        with plm4:
            orientation=st.selectbox("Mounts direction", ("Horizontal", "Vertical" ), key="orientation_mounts", help="Direction determines the setup of the mounts.")
        with plm5:
            prespace = st.number_input("Rail before/after group (cm) ", value=30, step=1, help= "Lenght of rail before and after the group of panels.")
       
        rotation=st.checkbox("Rotate panels", value=False, key="rotate_panels")
        image_rotation=st.checkbox("Rotate roof", value=False, key="rotate_roof" , help="Rotate roof image to match the real roof. Doesn't change calculations.")
        #create arays of solar panels

        # background image for panels layout
        if image_rotation:
            if roofing_type =="Tiles":
                style = st.markdown(f'<p style=" padding-top:34px; font-size:22px; text-align:center; display:none; ">{"x"}</p>'"""
                <style>
                .css-1e38a0u.e1tzin5v2{
                    background-image: url("https://i.postimg.cc/52XmXdsm/roof-tiles-r.png");
                    background-size: 80px;
                    border-radius: 5px;
                }
                </style>""", unsafe_allow_html=True)
            elif roofing_type =="Metal sheet":
                style = st.markdown(f'<p style=" padding-top:34px; font-size:22px; text-align:center; display:none; ">{"x"}</p>'"""
                <style>
                .css-1e38a0u.e1tzin5v2{
                    background-image: url("https://i.postimg.cc/cCYrphhw/sheet-r.jpg");
                    background-size: 250px;
                    border-radius: 5px;
                }
                </style>""", unsafe_allow_html=True)
            elif roofing_type =="Metal sandwich":
                style = st.markdown(f'<p style=" padding-top:34px; font-size:22px; text-align:center; display:none; ">{"x"}</p>'"""
                <style>
                .css-1e38a0u.e1tzin5v2{
                    background-image: url("https://i.postimg.cc/nLvSLfLP/sandwich-r.jpg");
                    background-size: 70px;
                    border-radius: 5px;
                }
                </style>""", unsafe_allow_html=True)
            elif roofing_type =="Flat":
                style = st.markdown(f'<p style=" padding-top:34px; font-size:22px; text-align:center; display:none; ">{"x"}</p>'"""
                <style>
                .css-1e38a0u.e1tzin5v2{
                    background-image: url("https://thumbs.dreamstime.com/b/texture-grey-flat-roofing-slate-close-up-140963645.jpg");
                    background-size: 160px;
                    border-radius: 5px;
                }
                </style>""", unsafe_allow_html=True)
        else:
            if roofing_type =="Tiles":
                style = st.markdown(f'<p style=" padding-top:34px; font-size:22px; text-align:center; display:none; ">{"x"}</p>'"""
                <style>
                .css-1e38a0u.e1tzin5v2{
                    background-image: url("	https://www.the3rdsequence.com/texturedb/thumbnail/161/512/roof+tiles.jpg");
                    background-size: 80px;
                    border-radius: 5px;
                }
                </style>""", unsafe_allow_html=True)
            elif roofing_type =="Metal sheet":
                style = st.markdown(f'<p style=" padding-top:34px; font-size:22px; text-align:center; display:none; ">{"x"}</p>'"""
                <style>
                .css-1e38a0u.e1tzin5v2{
                    background-image: url("https://s3.amazonaws.com/texturemax_th/metal/corrugated-metal/corrugated-metal_0001_01_thr.jpg");
                    background-size: 250px;
                    border-radius: 5px;
                }
                </style>""", unsafe_allow_html=True)
            elif roofing_type =="Metal sandwich":
                style = st.markdown(f'<p style=" padding-top:34px; font-size:22px; text-align:center; display:none; ">{"x"}</p>'"""
                <style>
                .css-1e38a0u.e1tzin5v2{
                    background-image: url("https://i.pinimg.com/originals/60/26/d0/6026d00ed91fa4dd73d0922de954e485.jpg");
                    background-size: 70px;
                    border-radius: 5px;
                }
                </style>""", unsafe_allow_html=True)
            elif roofing_type =="Flat":
                style = st.markdown(f'<p style=" padding-top:34px; font-size:22px; text-align:center; display:none; ">{"x"}</p>'"""
                <style>
                .css-1e38a0u.e1tzin5v2{
                    background-image: url("https://thumbs.dreamstime.com/b/texture-grey-flat-roofing-slate-close-up-140963645.jpg");
                    background-size: 160px;
                    border-radius: 5px;
                }
                </style>""", unsafe_allow_html=True)



        
        if rotation:
            style = st.markdown(f'<p style=" padding-top:34px; font-size:22px; text-align:center; display:none; ">{"x"}</p>'"""
            <style>
            
            [data-testid="stImage"]{
                margin-top:-16px;
            }
            [data-testid="stVerticalBlock"]{
                padding-top:0px;
            }
            </style>""", unsafe_allow_html=True)
            if orientation == "Horizontal":
                solar_img = ["solar_rotated-h.png",]
            else:
                solar_img = ["solar_rotated-v.png",]
                                
            width_value=70
        else:
            style = st.markdown(f'<p style=" padding-top:34px; font-size:22px; text-align:center; display:none; ">{"x"}</p>'"""
            <style>
            
            [data-testid="stImage"]{
                margin-top:-16px;
                
            }
            [data-testid="stVerticalBlock"]{
                padding-top:0px;
            }

            </style>""", unsafe_allow_html=True)
            width_value=40
            if orientation == "Horizontal":
                solar_img = ["solar-h.png",] 
            else:
                solar_img = ["solar-v.png",]
           
        solar_images = solar_img*panels*2   

        for i in range(groups):
            if i!=0:
                st.write("#")
                
            test1,test2,test3,test4 = st.columns([0.8,0.3,0.8,12.1])
            with test1:
                columns=st.text_input("Columns", value=1, key="columns"+str(i))
            with test2:
                st.write(f'<p style=" padding-top:34px; font-size:22px; text-align:center; ">{"x"}</p>', unsafe_allow_html=True)
            with test3:
                rows=st.text_input("Rows", value=1, key="rows"+str(i))

              
            for x in range(int(st.session_state["rows"+str(i)])):
                
                image_iterator=itertools.islice(enumerate(solar_images), 0, int(st.session_state["columns"+str(i)]))
                indices_on_page, images_on_page = map(list, zip(*image_iterator))
                if int(st.session_state["rows"+str(i)]) == 1 and rotation:
                    test4.write(f'<p style=" font-size:10px; text-align:center;visibility: hidden; ">{"##"}</p>', unsafe_allow_html=True)
                    test4.image(images_on_page, width=width_value)
                elif int(st.session_state["rows"+str(i)]) == 1:
                    test4.write(f'<p style=" font-size:2px; text-align:center; visibility: hidden; ">{"##"}</p>', unsafe_allow_html=True)
                    test4.image(images_on_page, width=width_value)
                else:
                    test4.image(images_on_page, width=width_value)
        total_end_clamp_qty = 0      
        total_mid_clamp_qty = 0   
        rail_length_total = 0  
        railholder_total = 0

        if rotation and orientation == "Horizontal":
            width_panel=1722
        elif rotation and orientation == "Vertical":
            width_panel=1134
        elif orientation == "Horizontal":
            width_panel=1134
        elif orientation == "Vertical":
            width_panel=1722

        for i in range(groups):
            rows_c=int(st.session_state["rows"+str(i)]) 
            columns_c=int(st.session_state["columns"+str(i)])
            if orientation == "Vertical":
                intermediary = rows_c
                rows_c = columns_c
                columns_c = intermediary
            end_clamps_no = rows_c*2*2
            mid_clamps_no = (columns_c-1)*2*rows_c
            total_end_clamp_qty += end_clamps_no
            total_mid_clamp_qty += mid_clamps_no
            rail_length = columns_c * width_panel * 2 * rows_c + columns_c * 20 + prespace * 40 * rows_c
            if roofing_type != "Flat":
                railholder = (rail_length)/(pv_panel_spacing * 1000) + 2
                railholder_total += railholder  
            rail_length_total += rail_length
        
        #st.write("Rail length: "+str(rail_length_total/1000)+" m")
      

        total_mounts = total_mid_clamp_qty+total_end_clamp_qty
        if roofing_type == "Flat":
            total_mounts = panels
        elif panel_mount_type == "3.3 m rail  ":
            total_mounts = int(round(rail_length_total/3300,0))
            mounts_price_value = 18.5
        gf1,gf2,gf3,gf4,gf5 = st.columns([2.5,1,1,1,1])
        with gf1:
            mounts_type= st.text_input("Type of mounts", panel_mount_type,disabled=True)
            if roofing_type != "Flat":
                end_clamp_type= st.text_input("End Clamps", "Aluminium clamp",disabled=True)
                mid_clamp_type= st.text_input("Mid Clamps", "Aluminium clamp",disabled=True)
                if roofing_type != "Metal sandwich" :
                    if roofing_type == "Tiles":
                        screw_type= st.text_input("Tiles mount: ", "Tile hook", key="tile_hook", disabled= True)
                    else:
                        screw_type= st.selectbox("Screw type", ("M8 X 200", "M8 X 100", "M8 X 150", "M8 X 250",), key="screw_type")
        with gf2:
            mounts_qty= st.number_input("Qty.", value=total_mounts, step=1)
            if roofing_type != "Flat":
                end_clamp_qty= st.number_input("Qty.", value=total_end_clamp_qty, step=1, key="end_clamp_qty",label_visibility="hidden")
                mid_clamp_qty= st.number_input("Qty.", value=total_mid_clamp_qty, step=1, key="mid_clamp_qty", label_visibility="hidden")
                if roofing_type != "Metal sandwich" :
                    screw_qty= st.number_input("Qty.", value=int(round(railholder_total,0)), step=1, key="screw_qty", label_visibility="hidden")
        with gf3:
            pv_panel_mounts_price= st.number_input("Buy price (€)", value=mounts_price_value, step=1.0, key="pv_panel_mounts_price" )
            if roofing_type != "Flat":
                end_clamp_price= st.number_input("Buy price (€)", value=2.0, step=0.5, key="end_clamp_price", label_visibility="hidden")
                mid_clamp_price= st.number_input("Buy price (€)", value=2.0, step=0.5, key="mid_clamp_price" , label_visibility="hidden")
                if roofing_type != "Metal sandwich" :
                    if roofing_type == "Tiles":
                        screw_price= st.number_input("Buy price (€)", value=7.5, step=0.1, key="screw_price", label_visibility="hidden")
                    else:
                        screw_price= st.number_input("Buy price (€)", value=0.5, step=0.1, key="screw_price", label_visibility="hidden")
        with gf4:
            mounts_uprice= st.text_input("Unit price (€)", value=pv_panel_mounts_price*resell, disabled=True, key = "mounts_uprice")
            if roofing_type != "Flat":
                end_clamp_uprice= st.text_input("Unit price (€)", value=end_clamp_price*resell, disabled=True, key = "end_clamp_uprice", label_visibility="hidden")
                mid_clamp_uprice= st.text_input("Unit price (€)", value=mid_clamp_price*resell, disabled=True, key = "mid_clamp_uprice", label_visibility="hidden")
                if roofing_type != "Metal sandwich" :
                    screw_uprice= st.text_input("Unit price (€)", value=screw_price*resell, disabled=True, key = "screw_uprice", label_visibility="hidden")
        with gf5:
            mounts_tprice= st.text_input("Total price", total_mounts * pv_panel_mounts_price *resell,  key = "mounts_tprice",disabled=True)
            if roofing_type != "Flat":
                end_clamp_tprice= st.text_input("Total price", round(end_clamp_qty * end_clamp_price *resell,2),  key = "end_clamp_tprice",disabled=True, label_visibility="hidden")
                mid_clamp_tprice= st.text_input("Total price", round(mid_clamp_qty * mid_clamp_price *resell,2),  key = "mid_clamp_tprice",disabled=True, label_visibility="hidden")
                if roofing_type != "Metal sandwich" :
                    screw_tprice= st.text_input("Total price", round(screw_qty * screw_price *resell,2),  key = "screw_tprice",disabled=True, label_visibility="hidden")
        tt1, = st.columns(1)
        total_cost_mounts_value = total_mounts * pv_panel_mounts_price *resell
        with tt1:
            st.text_input("empty", value="", key="total_cost_mounts",label_visibility="hidden", disabled=True)
            total_costs_mounts = st.write(f'<p style=" margin-top: -58px; padding-top:4px; padding-bottom:4px;font-size:22px;border-radius:4px; text-align:right; padding-right:60px;">{"Costs: " + str(total_cost_mounts_value) + " EUR"}</p>', unsafe_allow_html=True)

#_______________________________________________________________________________________________________________________________        
    with tab8:

        for i in range(len(inverter_df)):
            if inverter_df['product_name'][i] == type_inverter:
                inverter_power = inverter_df['power'][i]
        inverter_power = inverter_power * inverters

        if inverter_power > 30:
            other_mat_value = 600.0
        else:
            other_mat_value = 300.0

        st.subheader("Other information")
        
        odc1,odc2,odc3,odc4,odc5 = st.columns([2.5,1,1,1,1])
        with odc1:
            other_material_type = st.text_input("Extra materials", "Other Materials", disabled=True)
        with odc2:
            other_material_qty = st.number_input("Qty.", value=1, step=1, key="other_material_qty")
        with odc3:    
            other_mat_price = st.number_input("Other materials costs (€)", value=other_mat_value, step=10.0, help="300 EUR for 30kWp or less, 600 EUR for more than 30kWp")
        with odc4:
            other_mat_uprice = st.text_input("Unit price (€)", value=other_mat_price*resell, disabled=True,   key = "other_mat_uprice")
        with odc5:
            other_mat_tprice = st.text_input("Total price", other_material_qty * other_mat_price *resell,   key = "other_mat_tprice",disabled=True)
        
        u1, = st.columns(1)
        total_cost_oth_value = other_mat_price*resell*other_material_qty
        with u1:
            st.text_input("empty", value="", key="total_cost_oth",label_visibility="hidden", disabled=True)
            total_costs_gr = st.write(f'<p style="margin-top: -58px; padding-top:4px; padding-bottom:4px;font-size:22px;border-radius:4px; text-align:right; padding-right:60px;">{"Costs: " + str(total_cost_oth_value) + " EUR"}</p>', unsafe_allow_html=True)

tt1, = st.columns(1)
        
with tt1:
    tt_value = total_cost_eq_value+ total_cost_oth_value+total_cost_mounts_value+total_cost_gr_value+total_cost_DC_value+total_cost_AC_value + total_cost_design_value + total_cost_cables_value       
    st.text_input("empty", value="", key="total_cost_tt",label_visibility="hidden", disabled=True)
    total_costs_gr = st.write(f'<p style="color:rgb(9, 171, 59);  margin-top: -58px; padding-top:4px; padding-bottom:4px;font-size:22px;border-radius:4px; text-align:right; padding-right:60px;">{"Project Total: " + str(tt_value) + " EUR"}</p>', unsafe_allow_html=True)
if grounding == "Yes":
    gr_qty=1
    grounding_item = "Grounding System"
    #st.write ("Grounding system cost: ", str(grounding_system_cost), "EUR")
else:
    gr_qty = 1
    grounding_item = "Grounding measurement"

for i in range(len(smeter_df)):
    if smeter_df['product_name'][i] == smart_meter:
        if smeter_df['connection'][i] == "indirect":
            if inverters:
                smartmeter_cost =  smart_meter_price_resell
                if connection_el == "Three phase":
                    smartmeter_cost = smartmeter_cost + (smart_meter_ct_price*3 * resell)
                else:
                    smartmeter_cost = smartmeter_cost + (smart_meter_ct_price * resell)
            else:
                smartmeter_cost = 0
        else:
            if inverters:
                smartmeter_cost = smart_meter_price_resell
            else:
                smartmeter_cost = 0
if need_data_manager:
    data_manager_cost = float(data_manager_price) * resell
    
    if data_manager == "Internal board - Data Manager":
        vdc_ps_cost = 0
    else:
        vdc_ps_cost = vdc_power_supply_price * resell

else:
    data_manager_cost = 0
    vdc_ps_cost = 0
other_material_cost = other_mat_price*resell*other_material_qty        
aux_items_cost = vdc_ps_cost+total_cost_AC_value+total_cost_DC_value+total_cost_cables_value+other_material_cost
aux_items_cost = round(aux_items_cost,2)
calculation_data2 = {'Items': [type_panels, type_inverter, smart_meter,panel_mount_type +' PV panel mounts','Assembly, Design, Commisioning', 'Auxiliary items',grounding_item,data_manager],
    'Qty': [panels, inverters, 1,mounts_qty,1, 1, gr_qty,1 ],
    'Seller Price': [o_pv_price, o_inverter_price, o_smart_meter_price, pv_panel_mounts_price, total_cost_design_value/resell, aux_items_cost/resell, round(total_cost_gr_value/resell,2), data_manager_cost],
    'Unit price (EUR)': [pv_price_resell, inverter_price_resell, smartmeter_cost, pv_panel_mounts_price*resell, total_cost_design_value, aux_items_cost,total_cost_gr_value, data_manager_cost],
    'Total price (EUR)': [t_pv_total_value_resell, t_inverter_price_resell, smartmeter_cost, total_cost_mounts_value, total_cost_design_value, aux_items_cost, total_cost_gr_value, data_manager_cost ],
    }

#drop last entry from dictionary
if need_data_manager:
    calculation_data2=calculation_data2
else:
    
    calculation_data2['Items'].pop(-1)
    calculation_data2['Qty'].pop(-1)
    calculation_data2['Seller Price'].pop(-1)
    calculation_data2['Unit price (EUR)'].pop(-1)
    calculation_data2['Total price (EUR)'].pop(-1)

calculation_df2 = pd.DataFrame(calculation_data2, columns = ['Items', 'Qty','Seller Price','Unit price (EUR)', 'Total price (EUR)'])

st.table (calculation_df2)

#conditionals |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

if inverter_power<9.0:
    design_price_value=400.0
    cable_price_value = 5.0
    cable_type = "CYABY-F 5x6"
elif inverter_power<15.6:
    design_price_value=500.0
    if inverter_power > 12.5:
        cable_price_value = 8.0
        cable_type = "CYABY-F 5x16"
else:
    design_price_value=700.0
    cable_price_value = 8.0
    cable_type = "CYABY-F 5x16"



if need_data_manager:
    if data_manager == "Internal board - Data Manager":
        data_manager_price_value = 150.0
    else:
        data_manager_price_value = 200.0

#sidebar
navbar = st.sidebar
navbar.image("logo.png", width=150)
navbar.title("Add Equipment")
navbar.write("Add equipment to your design to better fit your project needs.")

# add equipment 

with navbar:
        
    equipment_type = st.selectbox("Enter equipment type :", ("Inverter", "PV Panel","Smart Meter"))	
    equipment_name = st.text_input("Enter equipment name")
    if equipment_type == "Inverter":
        inverter_power_new = st.number_input("Enter inverter power (kW)", value=0.0, step=0.1)
        inverter_connection = st.selectbox("Choose connection type", ("3P+N+PE", "1P+N+PE", "3P+N", "1P+N"))
        equipment_add = st.button("Add inverter to the database")
    elif equipment_type == "PV Panel":
        panel_power = st.number_input("Enter panel power (W)", value=0.0, step=0.1)
        equipment_add = st.button("Add PV Panel to the database")
    elif equipment_type == "Smart Meter":
        meter_connection = st.selectbox("Choose connection type", ("indirect", "direct"))
        equipment_add = st.button("Add Meter to the database")
    
    if equipment_name != "":
        if equipment_add and equipment_type == "Inverter":
            inverter_new = pd.DataFrame({"product_name": [equipment_name], "power": [inverter_power_new], "connection": [inverter_connection]})
            inverter_df.reset_index(drop=True, inplace=True)
            inverter_new.reset_index(drop=True, inplace=True)
            result_df = pd.concat([inverter_df,inverter_new], ignore_index=True)
            result_df = result_df.drop(columns=["Unnamed: 0"])
            result_df.to_csv(filename1)
            st.success("Inverter added to the database")
        
        elif equipment_add and equipment_type == "PV Panel":
            panel_new = pd.DataFrame({"product_name": [equipment_name], "power": [panel_power]})
            pvpanel_df.reset_index(drop=True, inplace=True)
            panel_new.reset_index(drop=True, inplace=True)
            result_df = pd.concat([pvpanel_df,panel_new], ignore_index=True)
            result_df = result_df.drop(columns=["Unnamed: 0"])
            result_df.to_csv(filename2)
            st.success("PV Panel added to the database")
        
        if equipment_add and equipment_type == "Smart Meter":
            meter_new = pd.DataFrame({"product_name": [equipment_name], "connection": [meter_connection]})
            smeter_df.reset_index(drop=True, inplace=True)
            meter_new.reset_index(drop=True, inplace=True)
            result_df = pd.concat([smeter_df,meter_new], ignore_index=True)
            result_df = result_df.drop(columns=["Unnamed: 0"])
            result_df.to_csv(filename3)
            st.success("Smart Meter added to the database")
    else:
        st.warning("Please enter equipment name!")
    st.caption ("*Equipment name must be unique and should reflect the characteristics of the equipment. For example: 'ABB 3P+N+PE 5kW'")

for i in range(len(pvpanel_df)):
    if pvpanel_df['product_name'][i] == type_panels:
        pvpanel_power = pvpanel_df['power'][i] 

#calcualte panels power
if panels :
    totalkWp = (int(panels) * pvpanel_power)/1000
else:
    totalkWp = 0

#calculate inverter power
if inverters:
    totalkWp_inverter = int(inverters) * 8.2
else:
    totalkWp_inverter = 0

#calculate inverter load
if inverters and panels:
    total_load = (totalkWp / inverter_power)*100
else:
    total_load = 0

if total_load > 100:
    overload = 100 - total_load
    load = 100
else:
    overload= 100 - total_load
    load  = total_load

# round values
totalkWp = round(totalkWp, 2)
totalkWp_inverter = round(totalkWp_inverter, 2)
total_load = round(total_load, 2)
overload = round(overload, 2)
load = round(load, 2)



# power metrics
col1, col2 = st.columns(2)
col1.metric("Inverter", str(inverter_power) + "kW", str(overload)+"%")
col1.write(str(inverters)+ " x "+type_inverter)
col2.metric("Total PV power", str(totalkWp) + "kWp", str(round(inverter_power-totalkWp,2))+" kW "  + " or " +str(round((inverter_power-totalkWp)*1000/pvpanel_power,2))+" panels")
col2.write(str(panels)+ " x "+type_panels)
#checkbox
checkbox = st.checkbox("Print to PDF when calculating!")

    
#calculate costs
calculate = st.button ("Calculate costs")
st_expander1=st.expander("Calculation results")



#calculation results
if calculate:
    
    st_expander1.subheader("Project "+ project +" calculations")
   
    beneficiary_txt=("Beneficiary: "+ beneficiary)
    ben_address=("Address: " + address)
    st_expander1.write( beneficiary_txt)
    st_expander1.write(ben_address)
    date_edit=("Date: "+ str(date))
    st_expander1.write(date_edit)
    connection_edit=("System type: "+connection_el+", "+ system)

    st_expander1.write(connection_edit)
    kwp=("Total power: "+ str(totalkWp) + "kWp")
    st_expander1.write(kwp)
    #st.write("Number of panels: ", str(panels) , "x", type_panels , "panels")
    #st.write("Number of inverters: ", str(inverters), "x", type_inverter)
    #st.write("Smart meter: ", smart_meter)
    #st.write("Number of strings: ", str(strings))

#calculate costs|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
    if calculate:
        #inverter costs:______________________________________________________________________________________________________________________
        
        if inverters:
            inverter_cost = inverters * inverter_price_resell
            inverter_cost=round(inverter_cost,2)
        else:
            inverter_cost = 0
        #st.write ("Inverter cost: ", str(inverter_cost), "EUR")

        #panels costs:________________________________________________________________________________________________________________________
        

        if panels:
            pvpanel_cost = panels * pv_price_resell
        else:
            pvpanel_cost = 0

        #st.write ("PV panels cost: ", str(pvpanel_cost), "EUR")    
        
        #smart meter costs:___________________________________________________________________________________________________________________
        
        
        #st.write ("Smart meter cost: ", str(smartmeter_cost), "EUR")
        #data maanger cost
        
        power_supply= "12VDC Power Supply"
   
        # AC electric panel costs:_________________________________________________________________________________________________________________
        if acpanel == "Yes":
            acpanel_cost = ac_electric_panel_price 
            small_mat_cost = small_mat_price 
        else:
            acpanel_cost = 0
            small_mat_cost = small_mat_price / 2
        acbreaker_cost = acbreaker_price
        mcb_smart_meter_cost = ac_sm_breaker_price 
        
        #st.write ("AC electric panel cost: ", str(ac_panel_total_cost), "EUR")

        # DC electric panel costs:_________________________________________________________________________________________________________________
        dc_panel_cost = dc_electric_panel_price
        dcbreaker_cost = dcfuse_price * strings * 2
        dc_fuse_slot_cost = strings * dcfuse_slot_price
        discharger_cost= discharger_price * strings
        
        
        #st.write ("DC electric panel cost: ", str(dc_panel_total_cost), "EUR")

        # cavbles, connectors costs:______________________________________________________________________________________________________________
        pv_cable_cost = solar_cable_price * (l_inverter )* (resell_price+100)/100
        power_cable_cost = power_cable_price * (l_meter)* (resell_price+100)/100
        ftp_cable_cost = ftp_cable_price * (l_meter)* (resell_price+100)/100
        pv_connector_cost = connector_uuprice * connector_qty
        ground_cable_cost = ground_cable_price * (l_grounding)* (resell_price+100)/100
        
        corrugated_tube_cost = corrugated_tube_price * l_corrugated_tube* (resell_price+100)/100
        total_cables_cost = pv_cable_cost + power_cable_cost + ftp_cable_cost + pv_connector_cost + ground_cable_cost + corrugated_tube_cost
        #st.write ("Cables, connectors costs: ", str(total_cables_cost), "EUR")
        # other material costs:____________________________________________________________________________________________________________________
        
        
        #st.write ("Other material cost: ", str(other_material_cost), "EUR")

        
        #st.write ("Auxiliary items cost: ", str(aux_items_cost), "EUR")

        #grounding system costs:__________________________________________________________________________________________________________________
        if grounding == "Yes":
            grounding_system_cost = (g_system + measure_g_system + g_system_labor) * (resell_price+100)/100
            gr_qty=1
            grounding_item = "Grounding System"
            #st.write ("Grounding system cost: ", str(grounding_system_cost), "EUR")
        else:
            grounding_system_cost = measure_g_system * (resell_price+100)/100
            gr_qty = 1
            grounding_item = "Grounding measurement"
        #total costs:_____________________________________________________________________________________________________________________________
        total_cost = inverter_cost + pvpanel_cost + smartmeter_cost + data_manager_cost +total_cost_mounts_value + total_cost_design_value + total_cost_DC_value + total_cost_cables_value+total_cost_AC_value+ other_material_cost + grounding_system_cost
  
        
        total_string = ("Total cost: "+ str(total_cost)+ " EUR")
        #st.subheader (total_string)
        vat_cost = total_cost * (vat_price/100)
        vat_cost = round(vat_cost, 2)
        vat_string = ("VAT: "+ str(vat_cost)+ " EUR")
        #st.subheader (vat_string)
        vat_total_cost = round(total_cost * (vat_price+100)/100,2)
        
        vat_total_string =("Total cost with VAT: "+ str(vat_total_cost)+ " EUR")
        #st.header(vat_total_string)

        calculation_data = {'Items': [type_panels, type_inverter, smart_meter,panel_mount_type +' PV panel mounts','Assembly, Design, Commisioning', 'Auxiliary items',grounding_item,data_manager],
            'Qty': [panels, inverters, 1,mounts_qty,1, 1, gr_qty,1 ],
            'Unit price (EUR)': [pv_price_resell, inverter_price_resell, smartmeter_cost, pv_panel_mounts_price*resell, total_cost_design_value, aux_items_cost, grounding_system_cost, data_manager_cost],
            'Total price (EUR)': [pvpanel_cost, inverter_cost, smartmeter_cost, total_cost_mounts_value, total_cost_design_value, aux_items_cost, grounding_system_cost, data_manager_cost ],
            }
        #drop last entry from dictionary
        if need_data_manager:
            calculation_data=calculation_data
        else:
          
            calculation_data['Items'].pop(-1)
            calculation_data['Qty'].pop(-1)
            calculation_data['Unit price (EUR)'].pop(-1)
            calculation_data['Total price (EUR)'].pop(-1)

        calculation_df = pd.DataFrame(calculation_data, columns = ['Items', 'Qty', 'Unit price (EUR)', 'Total price (EUR)'])

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Times", size=10)
        pdf.image('logo.png', 10, 14, 40)
        pdf.cell(200, 16, txt="", new_x=XPos.LEFT, new_y=YPos.NEXT, align="L")
        pdf.cell(200, 6, txt="M.A.R.S.T. S.A.", new_x=XPos.LEFT, new_y=YPos.NEXT, align="L")
        pdf.cell(200, 6, txt="Tg-Jiu, 210233, Romania", new_x=XPos.LEFT, new_y=YPos.NEXT, align="L")
        pdf.cell(200, 6, txt="Str. Termocentralei 2", new_x=XPos.LEFT, new_y=YPos.NEXT, align="L")
        pdf.set_font("Times", size=16)
        pdf.cell(200, 6, txt="Quotation for " + str(totalkWp) + " kWp PV system", new_x=XPos.LEFT, new_y=YPos.NEXT, align="C")
        pdf.set_font("Times", size=10)
        pdf.cell(200, 6, txt="", new_x=XPos.LEFT, new_y=YPos.NEXT, align="L")
        pdf.cell(200, 6, txt="Date: "+ str(date), new_x=XPos.LEFT, new_y=YPos.NEXT, align="L")
        pdf.cell(200, 6, txt="Beneficiary: "+ beneficiary, new_x=XPos.LEFT, new_y=YPos.NEXT, align="L")
        pdf.cell(200, 6, txt="Address: "+ address,new_x=XPos.LEFT, new_y=YPos.NEXT, align="L")
        pdf.cell(200, 6, txt=connection_edit, new_x=XPos.LEFT, new_y=YPos.NEXT, align="L")
        pdf.cell(200, 6, txt="Available for 30 days", new_x=XPos.LEFT, new_y=YPos.NEXT, align="L")

        pdf.cell(200, 6, txt="", new_x=XPos.LEFT, new_y=YPos.NEXT, align="L")
        create_table(table_data = calculation_data,title='PV System Items',align_header='L', align_data='L', cell_width=[85,15,40,40,],  emphasize_data=['0'], emphasize_style='BIU',emphasize_color=(255,0,0))
        
        total_data = {'Items': ['Total cost',],
            'Prices (EUR)': [total_cost,],}
        if disgr_count>0.0:
            total_cost= total_cost - (total_cost * disgr_count/100)
            total_data['Items'].append("Discount % ")
            total_data['Prices (EUR)'].append(disgr_count)
            total_data['Items'].append("Total cost with discount ")
            total_data['Prices (EUR)'].append(total_cost)
        vat_cost = round(total_cost * (vat_price/100),2)
        vat_total_cost = round(total_cost * (vat_price+100)/100,2)
        total_data['Items'].append("VAT")
        total_data['Prices (EUR)'].append(vat_cost)       
        total_data['Items'].append("Total cost with VAT")
        total_data['Prices (EUR)'].append(vat_total_cost)    

        total_df = pd.DataFrame(total_data, columns = ['Items','Prices (EUR)'])
        total_df.hide_columns= True
        st_expander1.table(calculation_df.style.format({"Qty": "{:.2f}","Unit price (EUR)": "{:.2f}","Total price (EUR)": "{:.2f}" }))
        st_expander1.table(total_df.style.format({"Prices (EUR)": "{:.2f}" }))
        create_table(table_data = total_data,title='PV System Total Costs',align_header='L', align_data='L', cell_width=[140,40,],  emphasize_data=['0','1000'], emphasize_style='BIU',emphasize_color=(255,0,0))    
        pdf.cell(200,30, txt="",new_x=XPos.LEFT, new_y=YPos.NEXT, align="L")
        pdf.cell(200, 6, txt="Signature ________________________", new_x=XPos.LEFT, new_y=YPos.NEXT, align="L")

        
       

        
#navbar button function
# EXTENDED CALCUALTION|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

        with st.expander("Equipment and materials calculated"):
            st.subheader("List of materials")
            #st.write("Prices contain "+ str(resell_price) +" %" +" resell price.")
            
            if connection_el == "Three phase":
                AC_breacker_text = 'AC breaker '+ acbreaker_type + " 4-pole"
            else:
                AC_breacker_text = 'AC breaker '+ acbreaker_type + " 2-pole"
            
            materials_data = {'Items': [type_panels,type_inverter,smart_meter, panel_mount_type +' PV panel mounts',solar_cable_type, power_cable_type, FTP_cable_type, grounding_cable_type,"Corrugated tube "+corrugated_tube_type, 'PV cable connectors', AC_breacker_text, 'DC fuses ' + dcfuse_type , 'DC fuse slots ' + dcfuse_slot_type, 'Discharger '+ discharger_type, 'DC panel ' + dc_electric_panel_type, 'MCB Smart meter '+ ac_sm_breaker_type, data_manager, vdc_power_supply_type],
                    'Qty': [panels,inverters, 1, mounts_qty,l_inverter + 20, l_meter, l_meter, l_grounding,l_corrugated_tube, connector_qty, inverters, strings*2, strings, strings, 1, 1,1,1],
                    'Unit': ['pcs.','pcs.','pcs.','set','m', 'm', 'm', 'm', 'm', 'set', 'pcs.', 'pcs.', 'pcs.', 'pcs.', 'pcs.', 'pcs.', 'pcs.', 'pcs.'],
                    'Unit price (EUR)': [pv_price_resell, inverter_price_resell, smartmeter_cost, pv_panel_mounts_price*(resell_price+100)/100 , solar_cable_price*resell,power_cable_price*resell, ftp_cable_price*resell, round(ground_cable_price*resell,2), corrugated_tube_price*resell, connector_price*resell, acbreaker_price*resell, dcfuse_price*resell, dcfuse_slot_price*resell, discharger_price*resell, dc_electric_panel_price*resell, round(ac_sm_breaker_price*resell,2), data_manager_cost, vdc_ps_cost],
                    'Total price (EUR)': [pvpanel_cost, inverter_cost, smartmeter_cost, total_cost_mounts_value,pv_cable_cost,power_cable_cost,ftp_cable_cost,ground_cable_cost,corrugated_tube_cost,pv_connector_cost,acbreaker_cost*resell,dcbreaker_cost*resell,dc_fuse_slot_cost*resell,discharger_cost*resell,dc_panel_cost*resell,round(mcb_smart_meter_cost*resell,2), data_manager_cost,vdc_ps_cost],
                    }

            if need_data_manager:
                if data_manager == "Internal board - Data Manager":
                    materials_data['Items'].pop(-1)
                    materials_data['Qty'].pop(-1)
                    materials_data['Unit'].pop(-1)
                    materials_data['Unit price (EUR)'].pop(-1)
                    materials_data['Total price (EUR)'].pop(-1)
                else:
                    materials_data['Items'].append(vdc_power_socket_type)
                    materials_data['Qty'].append(1)
                    materials_data['Unit'].append('pcs.')
                    materials_data['Unit price (EUR)'].append(vdc_power_socket_uprice)
                    materials_data['Total price (EUR)'].append(vdc_power_socket_total_price)
            else:
                materials_data['Items'].pop(-2)
                materials_data['Qty'].pop(-2)
                materials_data['Unit'].pop(-2)
                materials_data['Unit price (EUR)'].pop(-2)
                materials_data['Total price (EUR)'].pop(-2)
                materials_data['Items'].pop(-1)
                materials_data['Qty'].pop(-1)
                materials_data['Unit'].pop(-1)
                materials_data['Unit price (EUR)'].pop(-1)
                materials_data['Total price (EUR)'].pop(-1)
            # add extra cables to material list
            cables_data = {'Items': [], 'Qty': [],'Unit':[], 'Unit price (EUR)': [], 'Total price (EUR)': []}
            if st.session_state.gr_count>1:
                for x in range(1, st.session_state.gr_count):
                    total_cost_cables_value = total_cost_cables_value + total_grnew[x]

                    cabless_data = {'Items': [ st.session_state["GCT"+str(x)],],
                        'Qty': [float(st.session_state["GCL"+str(x)])],
                        'Unit': ["m"],
                        'Unit price (EUR)': [float( st.session_state["GCU"+str(x)])],
                        'Total price (EUR)': [float( st.session_state["GCTP"+str(x)])],
                        }
                    materials_data['Items'].append(cabless_data['Items'][0])
                    materials_data['Qty'].append(cabless_data['Qty'][0])
                    materials_data['Unit'].append(cabless_data['Unit'][0])
                    materials_data['Unit price (EUR)'].append(cabless_data['Unit price (EUR)'][0])
                    materials_data['Total price (EUR)'].append(cabless_data['Total price (EUR)'][0])
            if st.session_state.sl_count>1:
                for x in range(1, st.session_state.sl_count):
                    total_cost_cables_value = total_cost_cables_value + total_slnew[x]

                    cabless_data = {'Items': [ st.session_state["SCT"+str(x)],],
                        'Qty': [float(st.session_state["SCL"+str(x)])],
                        'Unit': ["m"],
                        'Unit price (EUR)': [float( st.session_state["SCU"+str(x)])],
                        'Total price (EUR)': [float( st.session_state["SCTP"+str(x)])],
                        }
                    materials_data['Items'].append(cabless_data['Items'][0])
                    materials_data['Qty'].append(cabless_data['Qty'][0])
                    materials_data['Unit'].append(cabless_data['Unit'][0])
                    materials_data['Unit price (EUR)'].append(cabless_data['Unit price (EUR)'][0])
                    materials_data['Total price (EUR)'].append(cabless_data['Total price (EUR)'][0])
            if st.session_state.pw_count>1:
                for x in range(1, st.session_state.pw_count):
                    total_cost_cables_value = total_cost_cables_value + total_pwnew[x]

                    cabless_data = {'Items': [ st.session_state["PWT"+str(x)],],
                        'Qty': [float(st.session_state["PWL"+str(x)])],
                        'Unit': ["m"],
                        'Unit price (EUR)': [float( st.session_state["PWU"+str(x)])],
                        'Total price (EUR)': [float( st.session_state["PWTP"+str(x)])],
                        }
                    materials_data['Items'].append(cabless_data['Items'][0])
                    materials_data['Qty'].append(cabless_data['Qty'][0])
                    materials_data['Unit'].append(cabless_data['Unit'][0])
                    materials_data['Unit price (EUR)'].append(cabless_data['Unit price (EUR)'][0])
                    materials_data['Total price (EUR)'].append(cabless_data['Total price (EUR)'][0])
            if st.session_state.ct_count>1:
                for x in range(1, st.session_state.ct_count):
                    total_cost_cables_value = total_cost_cables_value + total_ctnew[x]

                    cabless_data = {'Items': [ st.session_state["CTT"+str(x)],],
                        'Qty': [float(st.session_state["CTL"+str(x)])],
                        'Unit': ["m"],
                        'Unit price (EUR)': [float( st.session_state["CTU"+str(x)])],
                        'Total price (EUR)': [float( st.session_state["CTTP"+str(x)])],
                        }
                    materials_data['Items'].append("Corrugated tube " + cabless_data['Items'][0])
                    materials_data['Qty'].append(cabless_data['Qty'][0])
                    materials_data['Unit'].append(cabless_data['Unit'][0])
                    materials_data['Unit price (EUR)'].append(cabless_data['Unit price (EUR)'][0])
                    materials_data['Total price (EUR)'].append(cabless_data['Total price (EUR)'][0])

            if sm_connetion=="indirect":
                materials_data['Items'].append("Smart Meter TC " + sm_tc)
                materials_data['Qty'].append( sm_tc_qty)
                materials_data['Unit'].append("pcs.")
                materials_data['Unit price (EUR)'].append(sm_tc_price_resell)
                materials_data['Total price (EUR)'].append(t_sm_tc_price_resell)
            # add ac panel to material list
            if need_AC_panel:
                materials_data['Items'].append("AC panel " + acpanel)
                materials_data['Qty'].append(acpanel_qty)
                materials_data['Unit'].append("pcs.")
                materials_data['Unit price (EUR)'].append(ac_electric_panel_uprice)
                materials_data['Total price (EUR)'].append(ac_electric_panel_total_price)

            if st.session_state.ac_count>1:
                for x in range(1, st.session_state.ac_count):
                    acpanel_data = {'Items': [ st.session_state["ACT"+str(x)],],
                        'Qty': [float(st.session_state["ACL"+str(x)])],
                        'Unit': ["m"],
                        'Unit price (EUR)': [float( st.session_state["ACU"+str(x)])],
                        'Total price (EUR)': [float( st.session_state["ACTP"+str(x)])],
                        }
                    materials_data['Items'].append("AC Panel " + acpanel_data['Items'][0])
                    materials_data['Qty'].append(acpanel_data['Qty'][0])
                    materials_data['Unit'].append(acpanel_data['Unit'][0])
                    materials_data['Unit price (EUR)'].append(acpanel_data['Unit price (EUR)'][0])
                    materials_data['Total price (EUR)'].append(acpanel_data['Total price (EUR)'][0])

            if st.session_state.dc_count>1:
                for x in range(1, st.session_state.dc_count):
                    dcpanel_data = {'Items': [ st.session_state["DCT"+str(x)],],
                        'Qty': [float(st.session_state["DCL"+str(x)])],
                        'Unit': ["m"],
                        'Unit price (EUR)': [float( st.session_state["DCU"+str(x)])],
                        'Total price (EUR)': [float( st.session_state["DCTP"+str(x)])],
                        }
                    materials_data['Items'].append("DC Panel " + dcpanel_data['Items'][0])
                    materials_data['Qty'].append(dcpanel_data['Qty'][0])
                    materials_data['Unit'].append(dcpanel_data['Unit'][0])
                    materials_data['Unit price (EUR)'].append(dcpanel_data['Unit price (EUR)'][0])
                    materials_data['Total price (EUR)'].append(dcpanel_data['Total price (EUR)'][0])

            if st.session_state.acmcb_count>1:
                for x in range(1, st.session_state.acmcb_count):
                    acpanel_data = {'Items': [ st.session_state["ACMCBT"+str(x)],],
                        'Qty': [float(st.session_state["ACMCBL"+str(x)])],
                        'Unit': ["m"],
                        'Unit price (EUR)': [float( st.session_state["ACMCBU"+str(x)])],
                        'Total price (EUR)': [float( st.session_state["ACMCBTP"+str(x)])],
                        }
                    if connection_el == "Three phase":
                        AC_breacker_text1 =" 4-pole"
                    else:
                        AC_breacker_text1 =" 2-pole"
                    materials_data['Items'].append("AC MCB " + acpanel_data['Items'][0] + AC_breacker_text1)
                    materials_data['Qty'].append(acpanel_data['Qty'][0])
                    materials_data['Unit'].append(acpanel_data['Unit'][0])
                    materials_data['Unit price (EUR)'].append(acpanel_data['Unit price (EUR)'][0])
                    materials_data['Total price (EUR)'].append(acpanel_data['Total price (EUR)'][0])

            materials_df = pd.DataFrame(materials_data, columns = ['Items','Unit', 'Qty', 'Unit price (EUR)', 'Total price (EUR)'])
            
            
            st.table(materials_df.style.format({"Qty": "{:.2f}","Unit price (EUR)": "{:.2f}","Total price (EUR)": "{:.2f}" }))
            
            st.write("*Note: Small material costs are not presented here.")

        pdf.add_page()
        pdf.set_font("Times", size=10)
        pdf.image('logo.png', 10, 14, 40)
        pdf.cell(200, 16, txt="", new_x=XPos.LEFT, new_y=YPos.NEXT, align="L")
        pdf.cell(200, 6, txt="M.A.R.S.T. S.A.", new_x=XPos.LEFT, new_y=YPos.NEXT, align="L")
        pdf.cell(200, 6, txt="Tg-Jiu, 210233, Romania", new_x=XPos.LEFT, new_y=YPos.NEXT, align="L")
        pdf.cell(200, 6, txt="Str. Termocentralei 2", new_x=XPos.LEFT, new_y=YPos.NEXT, align="L")
        
        pdf.cell(200, 6, txt="", new_x=XPos.LEFT, new_y=YPos.NEXT, align="L")
        pdf.cell(200, 6, txt="Date: "+ str(date), new_x=XPos.LEFT, new_y=YPos.NEXT, align="L")
        pdf.cell(200, 6, txt="Beneficiary: "+ beneficiary, new_x=XPos.LEFT, new_y=YPos.NEXT, align="L")
        pdf.cell(200, 6, txt="Address: "+ address, new_x=XPos.LEFT, new_y=YPos.NEXT, align="L")
        pdf.cell(200, 6, txt=connection_edit, new_x=XPos.LEFT, new_y=YPos.NEXT, align="L")
        pdf.cell(200, 6, txt="Available for 30 days", new_x=XPos.LEFT, new_y=YPos.NEXT, align="L")
        pdf.set_font("Times", size=16)
        pdf.cell(200, 6, txt="Equipment and materials  for a " + str(totalkWp) + " kWp PV system", new_x=XPos.LEFT, new_y=YPos.NEXT, align="C")
        pdf.set_font("Times", size=10)
        pdf.cell(200, 6, txt="", new_x=XPos.LEFT, new_y=YPos.NEXT, align="L")
        #pdf.cell(200, 6, txt="Resell percentage added: "+str(resell_price)+ ' %', new_x=XPos.LEFT, new_y=YPos.NEXT, align="L")
        create_table(table_data = materials_data,title='PV System Items',align_header='L', align_data='L', cell_width=[85,15,20,30,30],  emphasize_data=['0'], emphasize_style='BIU',emphasize_color=(255,0,0))
        pdf.cell(200, 6, txt="*Note: Small material costs are not presented here.", new_x=XPos.LEFT, new_y=YPos.NEXT, align="L")
        if checkbox:
            #pdf.output('Quotation for '+beneficiary+' - '+str(totalkWp)+'kWp.pdf')

            def create_download_link(val, filename):
                b64 = base64.b64encode(val)  # val looks like b'...'
                return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf">Download file</a>'
            html = create_download_link(pdf.output(), 'Quotation for '+beneficiary+' - '+str(totalkWp)+'kWp')
            st.markdown(html, unsafe_allow_html=True)





# #button
# button = st.button("Click me")
# if button:
#     st.write("You clicked me")

# #checkbox
# checkbox = st.checkbox("Check me")
# if checkbox:
#     st.write("You checked me")

# #radio button
# radio = st.radio("Choose one", ("Option 1", "Option 2"))
# if radio == "Option 1":
#     st.write("You chose option 1")
# elif radio == "Option 2":
#     st.write("You chose option 2")

# #select box
# select = st.selectbox("Choose one", ("Option 1", "Option 2"))
# if select == "Option 1":
#     st.write("You chose option 1")
# elif select == "Option 2":
#     st.write("You chose option 2")

# #multiselect
# multiselect = st.multiselect("Choose one", ("Option 1", "Option 2"))
# if multiselect == "Option 1":
#     st.write("You chose option 1")
# elif multiselect == "Option 2":
#     st.write("You chose option 2")

# #slider
# slider = st.slider("Choose a number", 0, 10)
# st.write("You chose", slider)

# #text input
# text = st.text_input("Enter your name")
# st.write("Hello", text)

# #text area
# text_area = st.text_area("Enter your name")
# st.write("Hello", text_area)

# #date input
# date = st.date_input("Enter a date")
# st.write("You entered", date)

# #time input
# time = st.time_input("Enter a time")
# st.write("You entered", time)

# #file uploader
# file = st.file_uploader("Choose a file")
# if file is not None:
#     st.write("You chose", file.name)

# #color picker
# color = st.color_picker("Choose a color")
# st.write("You chose", color)

# #dataframe
# df = pd.DataFrame(np.random.randn(10, 5), columns=list("ABCDE"))
# st.dataframe(df)

# #table
# st.table(df)

# #plot with matplotlib
# fig, ax = plt.subplots()
# ax.plot([1, 2, 3, 4], [1, 4, 9, 16])
# st.pyplot(fig)


