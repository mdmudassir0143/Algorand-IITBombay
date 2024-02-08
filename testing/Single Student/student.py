# import hashlib
# import secrets
# import xml.etree.ElementTree as ET
# import json

# def calculate_merkle_root(final_hashes):
#     intermediate_hashes = final_hashes.copy()

#     while len(intermediate_hashes) > 1:
#         if len(intermediate_hashes) % 2 != 0:
#             intermediate_hashes.append(intermediate_hashes[-1])

#         new_hashes = []
#         for i in range(0, len(intermediate_hashes), 2):
#             combined_hash_data = intermediate_hashes[i] + intermediate_hashes[i+1]
#             combined_final_hash = hashlib.sha256(combined_hash_data.encode('utf-8')).hexdigest()  # noqa: E501
#             new_hashes.append(combined_final_hash)

#         intermediate_hashes = new_hashes

#     return intermediate_hashes[0]

# def append_nonce_to_hash(nonce,hash_object,data):
#     final_hashes = []
#     for d in data:
#         hash_object.update(d.encode('utf-8'))
#         init_hash = hash_object.hexdigest()
#         comb_data = init_hash + nonce
#         hash_object.update(comb_data.encode('utf-8'))
#         final_hash = hash_object.hexdigest()
#         final_hashes.append(final_hash)
#     return final_hashes

# def read_data_from_xml(file_path):
#     data = []
#     tree = ET.parse(file_path)
#     root = tree.getroot()
#     student_element = root.find("student")
#     name = student_element.find("name").text.strip()
#     rollno = student_element.find("rollno").text.strip()
#     university = student_element.find("university").text.strip()
#     program = student_element.find("program").text.strip()
#     year = student_element.find("year").text.strip()
#     gpa = student_element.find("gpa").text.strip()
#     data = [name,rollno,university,program,year,gpa]
#     return name, rollno, university, program, year, gpa, data

# # Specify the paths to your XML files for each student
# xml_file_paths = [
#     "./DegreeS1.xml",
#     "./DegreeS2.xml",
#     "./DegreeS3.xml",
#     "./DegreeS4.xml",
#     "./DegreeS5.xml"
# ]

# student_details = []
# verifications = []
# init_hashes = []
# merkle_roots = []
# nonces = []

# name, rollno, university, program, year, gpa, data = read_data_from_xml(xml_file_paths[0])
# nonce = secrets.token_hex(16)
# hash_object = hashlib.sha256()
# final_hashes = append_nonce_to_hash(nonce, hash_object, data)
# print("Check ",data)

# # Calculate the Merkle root
# nonces.append(nonce)
# merkle_root = calculate_merkle_root(final_hashes)
# merkle_roots.append(merkle_root)

# student_details.append((name, rollno, university, program, year, gpa, nonce))

# # Create Merkle openings for each data of student
# verification = {
#     'final_hashes': final_hashes,
#     'merkel_root': merkle_root
# }
# verifications.append(verification)

# print("\nStudent Details:")
# for i, detail in enumerate(student_details, start=1):
#     name, rollno, university, program, year, gpa, nonce = detail
#     print(f"\nStudent {i}:")
#     print("Name:", name)
#     print("Roll No:", rollno)
#     print("University:", university)
#     print("Program:", program)
#     print("Year:", year)
#     print("GPA:", gpa)
#     print("Nonce:", nonce)
#     print("Hash with Nonce:", final_hashes[i-1])

# # Write verifications to a JSON file
# with open('verifications.json', 'w') as file:
#     json.dump(verifications, file, indent=4)







import hashlib
import secrets
import xml.etree.ElementTree as ET
import json

def calculate_merkle_root(final_hashes):
    intermediate_hashes = final_hashes.copy()

    while len(intermediate_hashes) > 1:
        if len(intermediate_hashes) % 2 != 0:
            intermediate_hashes.append(intermediate_hashes[-1])

        new_hashes = []
        for i in range(0, len(intermediate_hashes), 2):
            combined_hash_data = intermediate_hashes[i] + intermediate_hashes[i+1]
            combined_final_hash = hashlib.sha256(combined_hash_data.encode('utf-8')).hexdigest()
            new_hashes.append(combined_final_hash)

        intermediate_hashes = new_hashes

    return intermediate_hashes[0]

def append_nonce_to_hash(nonce, hash_object, data):
    final_hashes = []
    for d in data:
        hash_object.update(d.encode('utf-8'))
        init_hash = hash_object.hexdigest()
        comb_data = init_hash + nonce
        hash_object.update(comb_data.encode('utf-8'))
        final_hash = hash_object.hexdigest()
        final_hashes.append(final_hash)
    return final_hashes

def read_data_from_xml(file_path):
    data = []
    tree = ET.parse(file_path)
    root = tree.getroot()
    student_element = root.find("student")
    name = student_element.find("name").text.strip()
    rollno = student_element.find("rollno").text.strip()
    university = student_element.find("university").text.strip()
    program = student_element.find("program").text.strip()
    year = student_element.find("year").text.strip()
    gpa = student_element.find("gpa").text.strip()
    data = [name, rollno, university, program, year, gpa]
    return name, rollno, university, program, year, gpa, data

# Specify the path to your XML file for one student
xml_file_path = "./DegreeS1.xml"

student_details = []
verifications = []
init_hashes = []
merkle_roots = []
nonces = {}

name, rollno, university, program, year, gpa, data = read_data_from_xml(xml_file_path)

# Initialize nonces for each field
nonces['name'] = secrets.token_hex(16)
nonces['rollno'] = secrets.token_hex(16)
nonces['university'] = secrets.token_hex(16)
nonces['program'] = secrets.token_hex(16)
nonces['year'] = secrets.token_hex(16)
nonces['gpa'] = secrets.token_hex(16)

# Append nonces to respective fields
nonce_name = nonces['name']
nonce_rollno = nonces['rollno']
nonce_university = nonces['university']
nonce_program = nonces['program']
nonce_year = nonces['year']
nonce_gpa = nonces['gpa']

hash_object = hashlib.sha256()
final_hashes = append_nonce_to_hash(nonce_name, hash_object, [name])
final_hashes += append_nonce_to_hash(nonce_rollno, hash_object, [rollno])
final_hashes += append_nonce_to_hash(nonce_university, hash_object, [university])
final_hashes += append_nonce_to_hash(nonce_program, hash_object, [program])
final_hashes += append_nonce_to_hash(nonce_year, hash_object, [year])
final_hashes += append_nonce_to_hash(nonce_gpa, hash_object, [gpa])

print("Check ", data)

# Calculate the Merkle root
merkle_root = calculate_merkle_root(final_hashes)
merkle_roots.append(merkle_root)

student_details.append((name, rollno, university, program, year, gpa, nonces))

# Create Merkle openings for each data of student
verification = {
    'final_hashes': final_hashes,
    'merkle_root': merkle_root
}
verifications.append(verification)

# Print student details
print("\nStudent Details:")
for i, detail in enumerate(student_details, start=1):
    name, rollno, university, program, year, gpa, nonces = detail
    print(f"\nStudent {i}:")
    print("Name:", name)
    print("Roll No:", rollno)
    print("University:", university)
    print("Program:", program)
    print("Year:", year)
    print("GPA:", gpa)
    print("Nonces:", nonces)

# Write verifications and nonces to a JSON file
output_data = {
    'verifications': verifications,
    'nonces': nonces
}
with open('verification_and_nonces_s1.json', 'w') as file:
    json.dump(output_data, file, indent=4)
