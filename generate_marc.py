import xml.etree.ElementTree as ET
from xml.dom import minidom

books = [
    {"id": "1001", "title": "Artificial Intelligence: A Modern Approach", "author": "Stuart Russell", "year": "2023", "subject": "Artificial Intelligence", "barcode": "B0001", "call": "AI-101"},
    {"id": "1002", "title": "Deep Learning for Beginners", "author": "Ian Goodfellow", "year": "2022", "subject": "Machine Learning", "barcode": "B0002", "call": "AI-102"},
    {"id": "1003", "title": "Introduction to Algorithms", "author": "Thomas H. Cormen", "year": "2021", "subject": "Algorithms", "barcode": "B0003", "call": "CS-201"},
    {"id": "1004", "title": "Clean Code: A Handbook of Agile Software Craftsmanship", "author": "Robert C. Martin", "year": "2019", "subject": "Software Engineering", "barcode": "B0004", "call": "SE-301"},
    {"id": "1005", "title": "Design Patterns: Elements of Reusable Object-Oriented Software", "author": "Erich Gamma", "year": "2020", "subject": "Software Engineering", "barcode": "B0005", "call": "SE-302"},
    {"id": "1006", "title": "Python Crash Course", "author": "Eric Matthes", "year": "2023", "subject": "Programming", "barcode": "B0006", "call": "PR-101"},
    {"id": "1007", "title": "Data Science from Scratch", "author": "Joel Grus", "year": "2021", "subject": "Data Science", "barcode": "B0007", "call": "DS-101"},
    {"id": "1008", "title": "Computer Networking: A Top-Down Approach", "author": "James Kurose", "year": "2022", "subject": "Networking", "barcode": "B0008", "call": "NT-201"},
    {"id": "1009", "title": "Operating System Concepts", "author": "Abraham Silberschatz", "year": "2020", "subject": "Operating Systems", "barcode": "B0009", "call": "OS-101"},
    {"id": "1010", "title": "Database System Concepts", "author": "Abraham Silberschatz", "year": "2021", "subject": "Databases", "barcode": "B0010", "call": "DB-101"},
    {"id": "1011", "title": "The Pragmatic Programmer", "author": "Andrew Hunt", "year": "2019", "subject": "Software Engineering", "barcode": "B0011", "call": "SE-303"},
    {"id": "1012", "title": "Head First Java", "author": "Kathy Sierra", "year": "2022", "subject": "Programming", "barcode": "B0012", "call": "PR-102"},
    {"id": "1013", "title": "Automate the Boring Stuff with Python", "author": "Al Sweigart", "year": "2020", "subject": "Programming", "barcode": "B0013", "call": "PR-103"},
    {"id": "1014", "title": "Cracking the Coding Interview", "author": "Gayle Laakmann McDowell", "year": "2023", "subject": "Career", "barcode": "B0014", "call": "CR-101"},
    {"id": "1015", "title": "Structure and Interpretation of Computer Programs", "author": "Harold Abelson", "year": "2021", "subject": "Computer Science", "barcode": "B0015", "call": "CS-101"}
]

root = ET.Element("collection", xmlns="http://www.loc.gov/MARC21/slim")

for book in books:
    record = ET.SubElement(root, "record")
    ET.SubElement(record, "leader").text = "00000nam a2200000 a 4500"
    
    c_001 = ET.SubElement(record, "controlfield", tag="001")
    c_001.text = book["id"]

    d_245 = ET.SubElement(record, "datafield", tag="245", ind1="1", ind2="0")
    ET.SubElement(d_245, "subfield", code="a").text = book["title"]
    
    d_100 = ET.SubElement(record, "datafield", tag="100", ind1="1", ind2=" ")
    ET.SubElement(d_100, "subfield", code="a").text = book["author"]
    
    d_260 = ET.SubElement(record, "datafield", tag="260", ind1=" ", ind2=" ")
    ET.SubElement(d_260, "subfield", code="a").text = "Islamabad"
    ET.SubElement(d_260, "subfield", code="b").text = "COMSATS University Press"
    ET.SubElement(d_260, "subfield", code="c").text = book["year"]

    d_650 = ET.SubElement(record, "datafield", tag="650", ind1=" ", ind2="0")
    ET.SubElement(d_650, "subfield", code="a").text = book["subject"]

    d_942 = ET.SubElement(record, "datafield", tag="942", ind1=" ", ind2=" ")
    ET.SubElement(d_942, "subfield", code="c").text = "BK"

    d_952 = ET.SubElement(record, "datafield", tag="952", ind1=" ", ind2=" ")
    ET.SubElement(d_952, "subfield", code="a").text = "CPL" # Branch code defaults to CPL (Centerville) or usually main
    ET.SubElement(d_952, "subfield", code="b").text = "CPL"
    ET.SubElement(d_952, "subfield", code="p").text = book["barcode"]
    ET.SubElement(d_952, "subfield", code="y").text = "BK"
    ET.SubElement(d_952, "subfield", code="o").text = book["call"]

xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")
with open("demo_books.xml", "w") as f:
    f.write(xmlstr)

print("Generated demo_books.xml successfully!")
