
import streamlit as st
import pandas as pd
from fpdf import FPDF
from fpdf.enums import XPos, YPos
import os.path
import base64
import mysql.connector

# Connect to MySQL



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
    data_manager_price_value = 100.0
    data_manager = "Yes"
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
#inverter list
# inverter_data = {'product_name': ['Fronius SYMO 6.0-3-M', 'Fronius SYMO 8.2-3-M', 'Fronius SYMO 10.0-3-M', 'Fronius SYMO 12.5-3-M', 'Fronius SYMO 15.5-3-M','Fronius SYMO 17.5-3-M'],
#         'power': [6, 8.2, 10, 12.5, 15.5, 17.5],
#         'connection': ['3P+N+PE', '3P+N+PE', '3P+N+PE', '3P+N+PE', '3P+N+PE', '3P+N+PE'],
#         }

#inverter_df = pd.DataFrame(inverter_data, columns = ['product_name', 'power', 'connection'])
#inverter_df.to_csv(filename1)
#pvpanel list
# pvpanel_data = {'product_name':['Regitec RMH54-415S1', 'Sharp NUJD540'],
#         'power': [415, 540]
#         }
# pvpanel_df = pd.DataFrame(pvpanel_data, columns = ['product_name', 'power'])
# pvpanel_df.to_csv(filename2) 
#smart meter list
# smeter_data = {'product_name':["Fronius TS 5KA-3", "Fronius TS 65A-3"],
#         'connection': ['indirect', 'direct']
#         }
# smeter_df = pd.DataFrame(smeter_data, columns = ['product_name', 'connection'])
# smeter_df.to_csv(filename3) 
#lists of equipment




panouri_stoc = pvpanel_df['product_name'].tolist()
inverter_stoc =inverter_df['product_name'].tolist()
meter_stoc = smeter_df['product_name'].tolist()

#streamlit form
#with st.form("form1"):
with st.expander("Project calculation parameters"):
    st.subheader("Project declaration")
    project = st.text_input("Enter project name", "Project name")
    beneficiary = st.text_input("Enter beneficiary name", "Beneficiary name")	
    address = st.text_input("Enter beneficiary address", "Beneficiary address")
    date = st.date_input("Enter date of calculation")
    st.subheader("Electric information")
    system = st.selectbox("Select system type", ("On-grid", "Off-grid"))
    connection_el = st.selectbox("Select connection type", ("Three phase", "Single phase"))
    st.subheader("Equipment selection")
    type_panels = st.selectbox("Choose panel type", (panouri_stoc))
    panels = st.number_input("Enter number of panels (pcs.)", value=20,step=1)
    type_inverter = st.selectbox("Choose inverter", (inverter_stoc))
    inverters = st.number_input("Enter number of inverters (pcs.)", value=1, step=1)
    strings = st.number_input("Enter number of strings (pcs.)", value=2, step=1)
    need_data_manager = st.checkbox("Do you need a data manager?")
    if need_data_manager:
        data_manager = st.selectbox("Choose data manager:", ("Internal board Data Manager","Electric panel Data Manager"))
    smart_meter = st.selectbox("Choose smart meter", (meter_stoc))
    pv_cable_connector = st.number_input("Enter number of solar cable connectors (set)", value=15, step=1)
    st.subheader("Electric materials")
    grounding = st.selectbox("New grounding system?", ("Yes", "No"))
    l_grounding= st.number_input("Length of cable to grounding system - from inverter to grounding (m)", value=15.0, step=1.0)
    l_inverter = st.number_input("Length of cable from panels to inverter - solar cable (m) ", value=25.0, step=1.0)
    l_meter = st.number_input("Length of cable from inverter to smart meter - FTP and power cables (m)", value=30.0, step=1.0)
    acpanel = st.selectbox("New AC panel mounted? -If NO, you will use an existing AC panel.", ("Yes", "No"))
    st.subheader("Other information")
    pv_panel_spacing= st.number_input("Enter spacing between solar panel mounts (m)", value=0.8, step=0.1)
    roofing_type = st.selectbox("What kind of roofing is it.", ("Metal", "Tiles"))
    distance_travel = st.number_input("Enter distance to transport (km)", value=600.0, step=10.0)
    # submit = st.form_submit_button("Submit")
    # if submit:
    #     st.write("Saved project as:", type_panels, " Date is:", date)



#conditionals |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
for i in range(len(inverter_df)):
    if inverter_df['product_name'][i] == type_inverter:
        inverter_power = inverter_df['power'][i]
inverter_power = inverter_power * inverters
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
if inverter_power > 30:
    other_mat_value = 600.0
else:
    other_mat_value = 300.0

if roofing_type == "Metal":
    mounts_price_value = 60.0
else:
    mounts_price_value = 70.0

if need_data_manager:
    if data_manager == "Internal board Data Manager":
        data_manager_price_value = 100.0
    else:
        data_manager_price_value = 150.0

#sidebar
navbar = st.sidebar
#navbar.image("logo.png", width=150)
navbar.title("Prices")
navbar.write("Set prices for equipment, transport, labor, materials and the app will calculate the costs for you")

#Design transport assembly commissioning prices
header1=navbar.subheader("Design, Transport, Assembly, Commisioning")
with navbar.expander("Expand to see Design, Transport, Assembly, Commisioning prices"):
    design_price = st.number_input("Design and engineering price. (€) ", value=design_price_value, step=10.0)
    transport_price = st.number_input("Transport price (€/km)", value=0.83, step=0.01)
    commissioning_price = st.number_input("Programming and commissioning price (€)", value=500.0, step=10.0)
    direct_pvpanel_labor = st.number_input("Enter direct PV panel labor including hotel (€/panel)", value=100.0, step=10.0)
    indirect_pvpanel_labor_percentage = st.number_input("Enter indirect PV panel labor percentage (%)", value=15.0, step=1.0)

#equipment prices
header2=navbar.subheader("Equipment prices")
with navbar.expander("Expand to see equipment prices"):
    pv_price = st.number_input("Enter PV panel price (€)", value=150.0, step=10.0)
    inverter_price = st.number_input("Enter inverter price (€/kW)", value=375.0, step=5.0)
    pv_panel_mounts_price = st.number_input("Enter panel mounts price (€)", value=mounts_price_value, step=1.0)
    data_manager_price = st.number_input("Enter data manager price (€)", value=data_manager_price_value, step=1.0)
    smart_meter_price = st.number_input("Enter smart meter price (€)", value = 300.0, step =0.5)
    smart_meter_ct_price = st.number_input("Enter smart meter current transformer price (€)", value = 20.0, step =0.5)
#material prices
header2=navbar.subheader("Materials prices")
with navbar.expander("Expand to see materials prices"):
    dcfuse_price= st.number_input("Enter DC fuse price (€)", value=5.0, step=0.5)
    dcfuse_slot_price= st.number_input("Enter DC fuse slot price (€)", value=7.5, step=0.5)
    acbreaker_price= st.number_input("Enter AC breaker price (€)", value=50.0,step=0.5)
    ac_sm_breaker_price= st.number_input("Enter smart meter breaker price (€)", value=6.0,step=0.5)
    vdc_power_supply_price= st.number_input("Enter 12VDC power supply price (€)", value=10.0,step=0.5)
    ftp_cable_price = st.number_input("Enter FTP cable price (€/m)", value=1.0, step=0.1)
    ground_cable_price = st.number_input("Enter grounding cable price (€/m)", value=3.0, step=0.1)
    solar_cable_price = st.number_input("Enter solar cable price (€/m)", value=2.0, step=0.1)
    power_cable_price = st.number_input("Enter power cable price (changes by power/distance) (€/m)", value=cable_price_value, step=0.1)
    connector_price = st.number_input("Enter solar cable connector price (€)", value=5.0, step=0.1)
    corrugated_tube_price = st.number_input("Enter corrugated tube price (€/m)", value=2.0, step=0.1)
    small_mat_price = st.number_input("Enter small material price (€)", value=50.0, step=1.0)
    discharger_price = st.number_input("Enter discharger price (€)", value=100.0, step=5.0)
    other_mat_price = st.number_input("Enter other materials price (€)", value=other_mat_value, step=10.0)

#Electric panels
header3=navbar.subheader("Electric panels DC/AC")
with navbar.expander("Expand to see AC/DC panel prices"):
    ac_electric_panel_price = st.number_input("Enter AC electric panel price (€)", value=100.0, step=1.0)
    dc_electric_panel_price = st.number_input("Enter DC electric panel price (€)", value=120.0, step=1.0)
    panel_labor_price = st.number_input("Enter electric panel labor percentage (%)", value=30.0, step=1.0)

#Grounding system
header3=navbar.subheader("Grounding system prices")
with navbar.expander("Expand to see grounding system prices"):
    g_system = st.number_input("Enter grounding system total materials prices (€)", value=515.0, step=10.0)
    measure_g_system = st.number_input("Enter grounding system measurement price (€)", value=100.0, step=10.0)
    g_system_labor = st.number_input("Enter grounding system labor and equipment renting price (€)", value=1405.0, step=10.0)

#financial
discountheader=navbar.subheader("Financial")
with navbar.expander("Expand to see financial percentages"):
    resell_price = st.number_input("Enter resell price percentage (%)", value=20.0, step=1.0)
    discount = st.number_input("Discount for the whole project (%)", value=0.0, step=1.0)
    vat_price = st.number_input("Enter VAT (%)", value=19.0, step=1.0)

addequipmentheader=navbar.subheader("Add equipment to the database")
with navbar.expander("Exapand to add equipment to the database"):
    st.caption("Add inverter to the database")
    inverter_name = st.text_input("Enter inverter name")
    inverter_power_new = st.number_input("Enter inverter power (kW)", value=0.0, step=0.1)
    inverter_connection = st.selectbox("Choose connection type", ("3P+N+PE", "1P+N+PE", "3P+N", "1P+N"))
    inverter_add = st.button("Add inverter to the database")
    if inverter_add:
        inverter_new = pd.DataFrame({"product_name": [inverter_name], "power": [inverter_power_new], "connection": [inverter_connection]})
    # add inverter to inverter_df
        inverter_df.reset_index(drop=True, inplace=True)
        inverter_new.reset_index(drop=True, inplace=True)
        result_df = pd.concat([inverter_df,inverter_new], ignore_index=True)
        result_df = result_df.drop(columns=["Unnamed: 0"])
        result_df.to_csv(filename1)
    st.caption("Add PV panel to the database")
    panel_name = st.text_input("Enter panel name")
    panel_power = st.number_input("Enter panel power (W)", value=0.0, step=0.1)
    panel_add = st.button("Add panel to the database")
    if panel_add:
        panel_new = pd.DataFrame({"product_name": [panel_name], "power": [panel_power]})
        pvpanel_df.reset_index(drop=True, inplace=True)
        panel_new.reset_index(drop=True, inplace=True)
        result_df = pd.concat([pvpanel_df,panel_new], ignore_index=True)
        result_df = result_df.drop(columns=["Unnamed: 0"])
        result_df.to_csv(filename2)
    st.caption("Add smart meter to the database")
    meter_name = st.text_input("Enter smart meter name")
    meter_connection = st.selectbox("Choose connection type", ("indirect", "direct"))
    meter_add = st.button("Add smart meter to the database")
    if meter_add:
        meter_new = pd.DataFrame({"product_name": [meter_name], "connection": [meter_connection]})
        smeter_df.reset_index(drop=True, inplace=True)
        meter_new.reset_index(drop=True, inplace=True)
        result_df = pd.concat([smeter_df,meter_new], ignore_index=True)
        result_df = result_df.drop(columns=["Unnamed: 0"])
        result_df.to_csv(filename3)

#nav buttons
button1 = navbar.button("Save prices")


#calcualte panels power
if panels :
    totalkWp = (int(panels) * 415)/1000
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
col2.metric("Total PV power", str(totalkWp) + "kWp", str(round(inverter_power-totalkWp,2))+" kW")
col2.write(str(panels)+ " x "+type_panels)
#checkbox
checkbox = st.checkbox("Print to PDF when calculating!")

    
#calculate costs
calculate = st.button ("Calculate costs")
st_expander1=st.expander("Calculation results")

if button1:
    st.success("Prices saved")


#calculation results
if calculate:
    
    st_expander1.subheader("Project "+ project +" calculations")
    col1, col2 = st_expander1.columns(2)
    col1.write("Builder:")

    col1.subheader("M.A.R.S.A.T. S.A.")
    col1.write("Address: Termocentralei 2, Tg-Jiu, 210233, Romania")
    col1.write("Phone: +40 253 210 047")
    col1.write("Email: office@marsat.com.ro")
    col2.write("Beneficiary: ")
    col2.subheader(beneficiary)
    col2.write("Address:")
    col2.write(address)
    date_edit=("Date: "+ str(date))
    st_expander1.write(date_edit)
    connection_edit=("System type: "+connection_el+", "+ system)
    st_expander1.write(connection_edit)
    kwp=("Total kWp: "+ str(totalkWp))
    st_expander1.write(kwp)
    #st.write("Number of panels: ", str(panels) , "x", type_panels , "panels")
    #st.write("Number of inverters: ", str(inverters), "x", type_inverter)
    #st.write("Smart meter: ", smart_meter)
    #st.write("Number of strings: ", str(strings))

#calculate costs|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
    if calculate:
        #inverter costs:______________________________________________________________________________________________________________________
        
        if inverters:
            inverter_cost = inverters * inverter_price * inverter_power * (resell_price+100)/100
            inverter_cost=round(inverter_cost,2)
        else:
            inverter_cost = 0
        #st.write ("Inverter cost: ", str(inverter_cost), "EUR")

        #panels costs:________________________________________________________________________________________________________________________
        for i in range(len(pvpanel_df)):
            if pvpanel_df['product_name'][i] == type_panels:
                pvpanel_power = pvpanel_df['power'][i]

        if panels:
            pvpanel_cost = panels * pv_price * (resell_price+100)/100
        else:
            pvpanel_cost = 0

        #st.write ("PV panels cost: ", str(pvpanel_cost), "EUR")    
        
        #smart meter costs:___________________________________________________________________________________________________________________
        for i in range(len(smeter_df)):
            if smeter_df['product_name'][i] == smart_meter:
                if smeter_df['connection'][i] == "indirect":
                    if inverters:
                        smartmeter_cost =  smart_meter_price * (resell_price+100)/100
                        if connection_el == "Three phase":
                            smartmeter_cost = smartmeter_cost + (smart_meter_ct_price*3 * (resell_price+100)/100)
                        else:
                            smartmeter_cost = smartmeter_cost + (smart_meter_ct_price * (resell_price+100)/100)
                    else:
                        smartmeter_cost = 0
                else:
                    if inverters:
                        smartmeter_cost = smart_meter_price * (resell_price+100)/100
                    else:
                        smartmeter_cost = 0
        
        #st.write ("Smart meter cost: ", str(smartmeter_cost), "EUR")
        #data maanger cost
        if need_data_manager:
            data_manager_cost = data_manager_price * (resell_price+100)/100
            
            if data_manager == "Internal board Data Manager":
                vdc_ps_cost = 0
            else:
                vdc_ps_cost = vdc_power_supply_price * (resell_price+100)/100

        else:
            data_manager_cost = 0
            vdc_ps_cost = 0
        
        power_supply= "12VDC Power Supply"
    

        # PV panel mounts_______________________________________________________________________________________________________________________
        pvpanel_mounts_cost = pv_panel_mounts_price * panels * (resell_price+100)/100
        #st.write ("PV panel mounts cost: ", str(pvpanel_mounts_cost), "EUR")

        # assembly, design, commisioning costs:_________________________________________________________________________________________________
        design_cost=design_price * (resell_price+100)/100
        transport_cost= transport_price * (resell_price+100)/100*  distance_travel
        direct_pv_labor = direct_pvpanel_labor * (resell_price+100)/100 * panels
        indirect_pv_labor = indirect_pvpanel_labor_percentage/100 * direct_pvpanel_labor * panels * (resell_price+100)/100 
        commissioning_cost= commissioning_price * (resell_price+100)/100
        total_design_cost = design_cost + transport_cost + direct_pv_labor + indirect_pv_labor + commissioning_cost
        #st.write ("Assembly, Design, Commisioning cost: ", str(total_design_cost), "EUR")

        # AC electric panel costs:_________________________________________________________________________________________________________________
        if acpanel == "Yes":
            acpanel_cost = ac_electric_panel_price 
            small_mat_cost = small_mat_price 
            acpanel_qty = 1
        else:
            acpanel_cost = 0
            acpanel_qty = 0
            small_mat_cost = small_mat_price / 2
        acbreaker_cost = acbreaker_price
        mcb_smart_meter_cost = ac_sm_breaker_price 
        ac_panel_total_cost = (acpanel_cost + small_mat_cost + acbreaker_cost + mcb_smart_meter_cost)* (resell_price+100)/100 * (panel_labor_price+100)/100
        #st.write ("AC electric panel cost: ", str(ac_panel_total_cost), "EUR")

        # DC electric panel costs:_________________________________________________________________________________________________________________
        dc_panel_cost = dc_electric_panel_price
        dcbreaker_cost = dcfuse_price * strings * 2
        dc_fuse_slot_cost = strings * dcfuse_slot_price
        discharger_cost= discharger_price * strings
        dc_small_mat_cost = small_mat_price*3
        dc_panel_total_cost = (dc_panel_cost + dcbreaker_cost + dc_fuse_slot_cost + discharger_cost + dc_small_mat_cost)* (resell_price+100)/100 * (panel_labor_price+100)/100
        #st.write ("DC electric panel cost: ", str(dc_panel_total_cost), "EUR")

        # cavbles, connectors costs:______________________________________________________________________________________________________________
        pv_cable_cost = solar_cable_price * (l_inverter + 20)* (resell_price+100)/100
        power_cable_cost = power_cable_price * (l_meter)* (resell_price+100)/100
        ftp_cable_cost = ftp_cable_price * (l_meter)* (resell_price+100)/100
        pv_connector_cost = connector_price * pv_cable_connector * (resell_price+100)/100
        ground_cable_cost = ground_cable_price * (l_grounding)* (resell_price+100)/100
        corrugated_tube_length = l_grounding+(l_meter*2)+(l_inverter/2)+15
        corrugated_tube_cost = corrugated_tube_price * corrugated_tube_length* (resell_price+100)/100
        total_cables_cost = pv_cable_cost + power_cable_cost + ftp_cable_cost + pv_connector_cost + ground_cable_cost + corrugated_tube_cost
        #st.write ("Cables, connectors costs: ", str(total_cables_cost), "EUR")
        # other material costs:____________________________________________________________________________________________________________________
        
        other_material_cost = other_mat_price * (resell_price+100)/100
        #st.write ("Other material cost: ", str(other_material_cost), "EUR")

        aux_items_cost = vdc_ps_cost+ac_panel_total_cost+dc_panel_total_cost+total_cables_cost+other_material_cost
        aux_items_cost = round(aux_items_cost,2)
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
        total_cost = inverter_cost+pvpanel_cost + smartmeter_cost +data_manager_cost +pvpanel_mounts_cost + total_design_cost + ac_panel_total_cost + dc_panel_total_cost + total_cables_cost + other_material_cost + grounding_system_cost
        
        if discount>0.0:
            total_cost = total_cost - (total_cost * discount/100)
        total_cost = round(total_cost, 2)
        total_string = ("Total cost: "+ str(total_cost)+ " EUR")
        #st.subheader (total_string)
        vat_cost = total_cost * (vat_price/100)
        vat_cost = round(vat_cost, 2)
        vat_string = ("VAT: "+ str(vat_cost)+ " EUR")
        #st.subheader (vat_string)
        vat_total_cost = total_cost * (vat_price+100)/100
        vat_total_cost = round(vat_total_cost, 2)
        vat_total_string =("Total cost with VAT: "+ str(vat_total_cost)+ " EUR")
        #st.header(vat_total_string)

        calculation_data = {'Items': [type_panels, type_inverter, smart_meter,'PV panel mounts','Assembly, Design, Commisioning', 'Auxiliary items',grounding_item,data_manager],
            'Qty': [panels, inverters, 1,panels,1, 1, gr_qty,1 ],
            'Unit price (EUR)': [pv_price * (resell_price+100)/100, round(inverter_price * inverter_power * (resell_price+100)/100,2 ), smartmeter_cost, pv_panel_mounts_price*(resell_price+100)/100 , total_design_cost, aux_items_cost, grounding_system_cost, data_manager_cost],
            'Total price (EUR)': [pvpanel_cost, inverter_cost, smartmeter_cost, pvpanel_mounts_cost, total_design_cost, aux_items_cost, grounding_system_cost, data_manager_cost ],
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
        
        total_data = {'Items': ['Total cost', 'VAT', 'Total cost with VAT'],
            'Prices (EUR)': [total_cost, vat_cost, vat_total_cost],}
        total_df = pd.DataFrame(total_data, columns = ['Items','Prices (EUR)'])
        total_df.hide_columns= True
        st_expander1.table(calculation_df)
        st_expander1.table(total_df)
        create_table(table_data = total_data,title='PV System Total Costs',align_header='L', align_data='L', cell_width=[140,40,],  emphasize_data=['0','1000'], emphasize_style='BIU',emphasize_color=(255,0,0))    
        pdf.cell(200,30, txt="",new_x=XPos.LEFT, new_y=YPos.NEXT, align="L")
        pdf.cell(200, 6, txt="Signature ________________________", new_x=XPos.LEFT, new_y=YPos.NEXT, align="L")

        
       

        
#navbar button function
# EXTENDED CALCUALTION|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

        with st.expander("Equipment and materials calculated"):
            st.subheader("List of materials")
            #st.write("Prices contain "+ str(resell_price) +" %" +" resell price.")
            resell= (resell_price+100)/100
            materials_data = {'Items': [type_panels,type_inverter,smart_meter, 'PV panel mounts',"Solar cable", "Power Cable " + cable_type, "FTP cable", 'MYF 16','Corrugated tube', 'PV cable connectors', 'AC breaker', 'DC fuses', 'DC fuse slots', 'Discharger', 'AC panel', 'DC panel', 'MCB Smart meter 6A', data_manager, power_supply],
                    'Qty': [panels,inverters, 1, panels,l_inverter + 20, l_meter, l_meter, l_grounding,corrugated_tube_length, pv_cable_connector, inverters, strings*2, strings, strings, acpanel_qty, 1, 1,1,1],
                    'Unit': ['pcs.','pcs.','pcs.','set','m', 'm', 'm', 'm', 'm', 'set', 'pcs.', 'pcs.', 'pcs.', 'pcs.', 'pcs.', 'pcs.', 'pcs.', 'pcs.', 'pcs.'],
                    'Unit price (EUR)': [pv_price*resell, round(inverter_price * inverter_power * (resell_price+100)/100,2 ), smartmeter_cost, pv_panel_mounts_price*(resell_price+100)/100 , solar_cable_price*resell,power_cable_price*resell, ftp_cable_price*resell, round(ground_cable_price*resell,2), corrugated_tube_price*resell, connector_price*resell, acbreaker_price*resell, dcfuse_price*resell, dcfuse_slot_price*resell, discharger_price*resell, ac_electric_panel_price*resell, dc_electric_panel_price*resell, round(ac_sm_breaker_price*resell,2), data_manager_cost, vdc_ps_cost],
                    'Total price (EUR)': [pvpanel_cost, inverter_cost, smartmeter_cost, pvpanel_mounts_cost,pv_cable_cost,power_cable_cost,ftp_cable_cost,ground_cable_cost,corrugated_tube_cost,pv_connector_cost,acbreaker_cost*resell,dcbreaker_cost*resell,dc_fuse_slot_cost*resell,discharger_cost*resell,acpanel_cost*resell,dc_panel_cost*resell,round(mcb_smart_meter_cost*resell,2), data_manager_cost,vdc_ps_cost],
                    }
            if need_data_manager:
                if data_manager == "Internal board Data Manager":
                    materials_data['Items'].pop(-1)
                    materials_data['Qty'].pop(-1)
                    materials_data['Unit'].pop(-1)
                    materials_data['Unit price (EUR)'].pop(-1)
                    materials_data['Total price (EUR)'].pop(-1)
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


            materials_df = pd.DataFrame(materials_data, columns = ['Items','Unit', 'Qty', 'Unit price (EUR)', 'Total price (EUR)'])
            st.table(materials_df)
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



