import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
import base64

# Set page configuration
st.set_page_config(page_title="Control Room Notice Board Editor", layout="wide")

# Function to read data from JSON file or initialize with default values
def load_data():
    if os.path.exists("notice_board_data.json"):
        with open("notice_board_data.json", "r") as f:
            return json.load(f)
    else:
        # Initialize with default values from the HTML template
        return {
            "date": "16 March 2025",
            "transformer_data": [{
                "eb": "EB",
                "transformer_ckt": "1",
                "tap": "4",
                "date": "26-02-2025",
                "remarks": "GOOD"
            }],
            "username_data": [
                {"name": "CUE SHEET", "username": "crairchennai@gmail.com", "password": "crair@2021"},
                {"name": "QBIT", "username": "Q56XADMIN", "password": "QBIT"}
            ],
            "phone_data": [
                {"location": "AVADI 200 KW", "number": "26373995", "ext1": "", "ext2": ""}
            ],
            "computer_notes": [
                "HLBS Monitor DC Adaptor spare kept at server room rack.",
                "Network shortcut folder available in Backup-Protected folder. Copy & paste on the desktop to access network folder."
            ],
            "codec_notes": [],
            "acplant_data": [
                {"name": "STAGE-1", "time": "0630Hrs – 1830Hrs"},
                {"name": "STAGE-2", "time": ""},
                {"name": "PLANT1", "time": "2100 – 0600Hrs"},
                {"name": "PLANT2", "time": "0600 – 2100Hrs"},
                {"name": "BACK PANASONIC", "time": "NIGHT"},
                {"name": "FRONT PANASONIC", "time": "DAY"}
            ],
            "telephone_notes": [],
            "ups_notes": [
                "20KVA UPS-1 taken into circuit on 08-4-24.",
                "20 KVA UPS supply changed to ESS supply. So weekly twice discharging of batteries has to be carried out on Monday & Thursday for prolonging life of batteries."
            ],
            "transmission_notes": []
        }

# Function to save data to JSON file
def save_data(data):
    with open("notice_board_data.json", "w") as f:
        json.dump(data, f, indent=4)

# Function to generate HTML
def generate_html(data):
    # Generate transformer rows
    transformer_rows = ""
    for row in data["transformer_data"]:
        transformer_rows += f"""<tr>
            <td rowspan="1" class="eb-cell">{row['eb']}</td>
            <td>{row['transformer_ckt']}</td>
            <td>{row['tap']}</td>
            <td>{row['date']}</td>
            <td>{row['remarks']}</td>
        </tr>"""
    
    # Generate username rows
    username_rows = ""
    for row in data["username_data"]:
        username_rows += f"""<tr>
            <td>{row['name']}</td>
            <td>{row['username']}</td>
            <td>{row['password']}</td>
        </tr>"""
    
    # Generate phone rows
    phone_rows = ""
    for row in data["phone_data"]:
        phone_rows += f"""<tr>
            <td>{row['location']}</td>
            <td>{row['number']}</td>
            <td>{row['ext1']}</td>
            <td>{row['ext2']}</td>
        </tr>"""
    
    # Generate computer content
    computer_content = ""
    for note in data["computer_notes"]:
        computer_content += f'<p class="bullet-point">{note}</p>'
    
    # Generate codec content
    codec_content = ""
    for note in data["codec_notes"]:
        codec_content += f'<p class="bullet-point">{note}</p>'
    
    # Generate AC Plant rows
    acplant_rows = ""
    ces_plant_rows = ""
    for i, row in enumerate(data["acplant_data"]):
        if i < 4:  # First 4 rows are for AC Plant
            acplant_rows += f"""<tr>
                <td>{row['name']}</td>
                <td>{row['time']}</td>
            </tr>"""
        else:  # The rest are for CES Plant
            ces_plant_rows += f"""<tr>
                <td>{row['name']}</td>
                <td>{row['time']}</td>
            </tr>"""
    
    # Generate telephone content
    telephone_content = ""
    for note in data["telephone_notes"]:
        telephone_content += f'<p class="bullet-point">{note}</p>'
    
    # Generate UPS content
    ups_content = ""
    for note in data["ups_notes"]:
        ups_content += f'<p class="bullet-point">{note}</p>'
    
    # Generate transmission content
    transmission_content = ""
    for note in data["transmission_notes"]:
        transmission_content += f'<p class="bullet-point">{note}</p>'
    
    # Create the HTML content with double curly braces for CSS
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CONTROL ROOM NOTICE</title>
    <style>
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}
        
        body {{
            font-family: Arial, sans-serif;
            background-color: #f3f3f3;
            padding: 20px;
            color: #333;
            line-height: 1.5;
        }}
        
        .notice-board {{
            width: 100%;
            max-width: 1200px;
            margin: 0 auto;
            background-color: #ffffff;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            overflow: hidden;
            padding: 0;
        }}
        
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: linear-gradient(135deg, #1a73e8, #0d47a1);
            color: white;
            padding: 15px 30px;
            border-bottom: 3px solid #0a3d91;
        }}
        
        .header h1 {{
            margin: 0;
            font-size: 32px;
            letter-spacing: 1px;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
        }}
        
        .date {{
            font-weight: bold;
            font-size: 18px;
            background-color: rgba(255,255,255,0.2);
            padding: 8px 15px;
            border-radius: 4px;
        }}
        
        .content-wrapper {{
            padding: 25px;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 25px;
            background-color: white;
            box-shadow: 0 2px 5px rgba(0,0,0,0.08);
            border-radius: 4px;
            overflow: hidden;
        }}
        
        table, th, td {{
            border: 1px solid #ddd;
        }}
        
        th, td {{
            padding: 12px 15px;
            text-align: left;
        }}
        
        th {{
            background-color: #f2f2f2;
            font-weight: bold;
            text-transform: uppercase;
            font-size: 14px;
            color: #555;
        }}
        
        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        
        tr:hover {{
            background-color: #f5f5f5;
        }}
        
        .eb-cell {{
            text-align: center;
            font-weight: bold;
            background-color: #ffeb3b;
            vertical-align: middle;
            color: #333;
        }}
        
        .two-column {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 25px;
            gap: 25px;
        }}
        
        .column {{
            flex: 1;
        }}
        
        .section-title {{
            font-weight: bold;
            background-color: #e0e0e0;
            padding: 10px 15px;
            border-radius: 4px 4px 0 0;
            border-bottom: 2px solid #ccc;
            color: #444;
            font-size: 16px;
        }}
        
        .section-content {{
            padding: 15px;
            background-color: white;
            border-radius: 0 0 4px 4px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.08);
        }}
        
        .postcards {{
            display: flex;
            flex-wrap: wrap;
            gap: 25px;
            margin-bottom: 25px;
        }}
        
        .postcard {{
            flex: 1;
            min-width: 300px;
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            overflow: hidden;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        
        .postcard:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 16px rgba(0,0,0,0.15);
        }}
        
        .postcard-top {{
            padding: 0;
            border-bottom: 1px solid #eee;
        }}
        
        .postcard-bottom {{
            padding: 0;
            background-color: #f8f8f8;
        }}
        
        .bullet-point {{
            margin: 8px 0 8px 25px;
            position: relative;
        }}
        
        .bullet-point:before {{
            content: "•";
            position: absolute;
            left: -15px;
            color: #1a73e8;
            font-weight: bold;
        }}
        
        /* Special styling for different tables */
        .transform-table {{
            background-color: #e3f2fd;
        }}
        
        .transform-table th {{
            background-color: #bbdefb;
        }}
        
        .username-table table {{
            background-color: #fff8e1;
        }}
        
        .username-table th {{
            background-color: #ffecb3;
        }}
        
        .phone-table table {{
            background-color: #e8f5e9;
        }}
        
        .phone-table th {{
            background-color: #c8e6c9;
        }}
        
        /* Responsive design */
        @media screen and (max-width: 992px) {{
            .two-column {{
                flex-direction: column;
            }}
            
            .postcards {{
                flex-direction: column;
            }}
            
            .postcard {{
                width: 100%;
            }}
        }}
        
        @media screen and (max-width: 768px) {{
            .header {{
                flex-direction: column;
                text-align: center;
                padding: 15px;
            }}
            
            .header h1 {{
                margin-bottom: 10px;
            }}
            
            .content-wrapper {{
                padding: 15px;
            }}
            
            th, td {{
                padding: 8px;
            }}
        }}
    </style>
</head>
<body>
    <div class="notice-board">
        <!-- Header -->
        <div class="header">
            <h1>CONTROL ROOM NOTICE</h1>
            <div class="date">{data["date"]}</div>
        </div>
        
        <div class="content-wrapper">
            <!-- Transformer Table without heading -->
            <div class="transform-table">
                <table>
                    <tr>
                        <th>EB</th>
                        <th>TRANSFORMER IN CKT</th>
                        <th>TAP</th>
                        <th>DATE</th>
                        <th>REMARKS</th>
                    </tr>
                    {transformer_rows}
                </table>
            </div>

            <!-- Two Tables side by side -->
            <div class="two-column">
                <div class="column">
                    <div class="section-title">IMPORTANT USERNAME & PWD</div>
                    <div class="section-content username-table">
                        <table>
                            <tr>
                                <th></th>
                                <th>USERNAME</th>
                                <th>PASSWORD</th>
                            </tr>
                            {username_rows}
                        </table>
                    </div>
                </div>
                <div class="column">
                    <div class="section-title">IMPORTANT PHONE NOS</div>
                    <div class="section-content phone-table">
                        <table>
                            <tr>
                                <th>LOCATION</th>
                                <th>NUMBER</th>
                                <th></th>
                                <th></th>
                            </tr>
                            {phone_rows}
                        </table>
                    </div>
                </div>
            </div>

            <!-- Three Postcards -->
            <div class="postcards">
                <!-- First Postcard -->
                <div class="postcard">
                    <div class="postcard-top">
                        <div class="section-title">COMPUTER</div>
                        <div class="section-content">
                            {computer_content}
                        </div>
                    </div>
                    <div class="postcard-bottom">
                        <div class="section-title">CODEC</div>
                        <div class="section-content">
                            {codec_content}
                        </div>
                    </div>
                </div>

                <!-- Second Postcard -->
                <div class="postcard">
                    <div class="postcard-top">
                        <div class="section-title">ACPLANT</div>
                        <div class="section-content">
                            <table>
                                {acplant_rows}
                                <tr>
                                    <td colspan="2" class="section-title">CES PLANT</td>
                                </tr>
                                {ces_plant_rows}
                            </table>
                        </div>
                    </div>
                    <div class="postcard-bottom">
                        <div class="section-title">TELEPHONE</div>
                        <div class="section-content">
                            {telephone_content}
                        </div>
                    </div>
                </div>

                <!-- Third Postcard -->
                <div class="postcard">
                    <div class="postcard-top">
                        <div class="section-title">UPS</div>
                        <div class="section-content">
                            {ups_content}
                        </div>
                    </div>
                    <div class="postcard-bottom">
                        <div class="section-title">TRANSMISSION</div>
                        <div class="section-content">
                            {transmission_content}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Add some interactivity
        document.addEventListener("DOMContentLoaded", function() {{
            // Highlight rows on hover
            const tables = document.querySelectorAll('table');
            tables.forEach(table => {{
                const rows = table.querySelectorAll('tr');
                rows.forEach(row => {{
                    row.addEventListener('mouseover', function() {{
                        this.style.backgroundColor = '#e3f2fd';
                    }});
                    row.addEventListener('mouseout', function() {{
                        this.style.backgroundColor = '';
                    }});
                }});
            }});
        }});
    </script>
</body>
</html>'''
    
    return html_content

# Function to create downloadable HTML file
def get_download_link(html_content, filename="notice_board.html"):
    b64 = base64.b64encode(html_content.encode()).decode()
    return f'<a href="data:text/html;base64,{b64}" download="{filename}" target="_blank">Download HTML file</a>'

# Load data
data = load_data()

# Create Streamlit App
st.title("Control Room Notice Board Editor")

# Create tabs for different sections
tabs = st.tabs([
    "Preview", 
    "Date", 
    "Transformer", 
    "Usernames", 
    "Phone Numbers", 
    "Computer Notes", 
    "Codec Notes", 
    "AC Plant", 
    "Telephone Notes", 
    "UPS Notes", 
    "Transmission Notes"
])

# Preview Tab
with tabs[0]:
    st.header("Notice Board Preview")
    
    html_content = generate_html(data)
    
    # Display HTML preview
    st.components.v1.html(html_content, height=800, scrolling=True)
    
    # Download button
    st.markdown(get_download_link(html_content), unsafe_allow_html=True)
    
    if st.button("Save All Changes"):
        save_data(data)
        st.success("All changes saved successfully!")

# Date Tab
with tabs[1]:
    st.header("Update Date")
    new_date = st.text_input("Notice Board Date", data["date"])
    
    if st.button("Update Date"):
        data["date"] = new_date
        save_data(data)
        st.success("Date updated successfully!")

# Transformer Tab
with tabs[2]:
    st.header("Update Transformer Data")
    transformer_df = pd.DataFrame(data["transformer_data"])
    
    edited_transformer_df = st.data_editor(
        transformer_df, 
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "eb": st.column_config.TextColumn("EB"),
            "transformer_ckt": st.column_config.TextColumn("Transformer In CKT"),
            "tap": st.column_config.TextColumn("Tap"),
            "date": st.column_config.TextColumn("Date"),
            "remarks": st.column_config.TextColumn("Remarks")
        }
    )
    
    if st.button("Update Transformer Data"):
        data["transformer_data"] = edited_transformer_df.to_dict('records')
        save_data(data)
        st.success("Transformer data updated successfully!")

# Usernames Tab
with tabs[3]:
    st.header("Update Username & Password Data")
    username_df = pd.DataFrame(data["username_data"])
    
    # For older versions of Streamlit, use regular TextColumn without password parameter
    edited_username_df = st.data_editor(
        username_df,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "name": st.column_config.TextColumn("Name"),
            "username": st.column_config.TextColumn("Username"),
            "password": st.column_config.TextColumn("Password")
        }
    )
    
    if st.button("Update Username Data"):
        data["username_data"] = edited_username_df.to_dict('records')
        save_data(data)
        st.success("Username data updated successfully!")

# Phone Numbers Tab
with tabs[4]:
    st.header("Update Phone Numbers")
    phone_df = pd.DataFrame(data["phone_data"])
    
    edited_phone_df = st.data_editor(
        phone_df,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "location": st.column_config.TextColumn("Location"),
            "number": st.column_config.TextColumn("Number"),
            "ext1": st.column_config.TextColumn("Ext 1"),
            "ext2": st.column_config.TextColumn("Ext 2")
        }
    )
    
    if st.button("Update Phone Data"):
        data["phone_data"] = edited_phone_df.to_dict('records')
        save_data(data)
        st.success("Phone data updated successfully!")

# Computer Notes Tab
with tabs[5]:
    st.header("Update Computer Notes")
    
    computer_notes = st.text_area("Computer Notes (One note per line)", "\n".join(data["computer_notes"]), height=200)
    
    if st.button("Update Computer Notes"):
        data["computer_notes"] = [note for note in computer_notes.split("\n") if note.strip()]
        save_data(data)
        st.success("Computer notes updated successfully!")

# Codec Notes Tab
with tabs[6]:
    st.header("Update Codec Notes")
    
    codec_notes = st.text_area("Codec Notes (One note per line)", "\n".join(data["codec_notes"]), height=200)
    
    if st.button("Update Codec Notes"):
        data["codec_notes"] = [note for note in codec_notes.split("\n") if note.strip()]
        save_data(data)
        st.success("Codec notes updated successfully!")

# AC Plant Tab
with tabs[7]:
    st.header("Update AC Plant Data")
    
    st.subheader("AC Plant")
    acplant_df = pd.DataFrame(data["acplant_data"][:4])  # First 4 rows
    
    edited_acplant_df = st.data_editor(
        acplant_df,
        use_container_width=True,
        column_config={
            "name": st.column_config.TextColumn("Name"),
            "time": st.column_config.TextColumn("Time")
        }
    )
    
    st.subheader("CES Plant")
    ces_plant_df = pd.DataFrame(data["acplant_data"][4:])  # Remaining rows
    
    edited_ces_plant_df = st.data_editor(
        ces_plant_df,
        use_container_width=True,
        column_config={
            "name": st.column_config.TextColumn("Name"),
            "time": st.column_config.TextColumn("Time")
        }
    )
    
    if st.button("Update AC Plant Data"):
        data["acplant_data"] = edited_acplant_df.to_dict('records') + edited_ces_plant_df.to_dict('records')
        save_data(data)
        st.success("AC Plant data updated successfully!")

# Telephone Notes Tab
with tabs[8]:
    st.header("Update Telephone Notes")
    
    telephone_notes = st.text_area("Telephone Notes (One note per line)", "\n".join(data["telephone_notes"]), height=200)
    
    if st.button("Update Telephone Notes"):
        data["telephone_notes"] = [note for note in telephone_notes.split("\n") if note.strip()]
        save_data(data)
        st.success("Telephone notes updated successfully!")

# UPS Notes Tab
with tabs[9]:
    st.header("Update UPS Notes")
    
    ups_notes = st.text_area("UPS Notes (One note per line)", "\n".join(data["ups_notes"]), height=200)
    
    if st.button("Update UPS Notes"):
        data["ups_notes"] = [note for note in ups_notes.split("\n") if note.strip()]
        save_data(data)
        st.success("UPS notes updated successfully!")

# Transmission Notes Tab
with tabs[10]:
    st.header("Update Transmission Notes")
    
    transmission_notes = st.text_area("Transmission Notes (One note per line)", "\n".join(data["transmission_notes"]), height=200)
    
    if st.button("Update Transmission Notes"):
        data["transmission_notes"] = [note for note in transmission_notes.split("\n") if note.strip()]
        save_data(data)
        st.success("Transmission notes updated successfully!")

# Footer
st.markdown("---")
st.info("Note: Changes are saved in each tab independently. The preview will reflect all saved changes.")