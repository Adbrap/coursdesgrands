import ftplib
from bs4 import BeautifulSoup
from datetime import datetime
import io
import locale

# Set locale to French
locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

# FTP Configuration
FTP_HOST = "server133.web-hosting.com"
FTP_USER = "abtrqawg"
FTP_PASS = "Km8V2Q67pUbL"
remote_html_file = "public_html/index.html"
remote_text_file = "public_html/pourcent.txt"

# Connect to FTP server
ftp = ftplib.FTP(FTP_HOST, FTP_USER, FTP_PASS)

# Download HTML file
html_content = io.BytesIO()
ftp.retrbinary(f'RETR {remote_html_file}', html_content.write)
html_content.seek(0)
soup = BeautifulSoup(html_content, "lxml")  # Using lxml as the parser

# Find the specific table by ID
table = soup.find("table", id="tableau_99")

# Download the text file containing the gain
gain_content = io.BytesIO()
ftp.retrbinary(f'RETR {remote_text_file}', gain_content.write)
gain_content.seek(0)
gain = gain_content.getvalue().decode().strip()
gain = float(gain)
gain = (gain * 1000)/100

# Create a new row in the table
new_row = soup.new_tag("tr")
cells = [soup.new_tag("td"), soup.new_tag("td")]
cells[0].string = datetime.now().strftime("%A %d %B")
cells[1].string = f"{gain}€"
for cell in cells:
    new_row.append(cell)
table.append(new_row)

# Save the modifications to the HTML file
html_content.seek(0)
html_content.truncate(0)
html_content.write(str(soup).encode('utf-8'))
html_content.seek(0)
ftp.storbinary(f'STOR {remote_html_file}', html_content)

# Close FTP connection
ftp.quit()

