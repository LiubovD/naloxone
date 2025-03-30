import arcpy

# Path to the File Geodatabase
output_gdb = r"C:\Users\l.dumarevskaya.ctr\ArcGIS projects\RISNER\data\CENSUS\Census_dataset\Census_dataset.gdb"

# Path to the feature class
output_feature_class = f"{output_gdb}\\Combined_All_Points"

# Create an update cursor to iterate through the feature class
with arcpy.da.UpdateCursor(output_feature_class, ['Address', 'City', 'Match_addr']) as cursor:
    for row in cursor:
        address, city, match_addr = row

        # If Match_addr is null or empty
        if not match_addr:
            # Populate Match_addr with Address + ', ' + City
            match_addr = f"{address}, {city}" if address and city else None
            row[2] = match_addr

        # If Address is empty
        if not address and match_addr and ',' in match_addr:
            # Split Match_addr into Address and City
            address_parts = match_addr.split(',')
            address = address_parts[0].strip()
            city = address_parts[1].strip() if len(address_parts) > 1 else None
            row[0], row[1] = address, city

        # Update the row
        cursor.updateRow(row)

# Rename the Match_addr field to Full address
arcpy.management.AlterField(output_feature_class, 'Match_addr', 'Full address')

print("Processing complete. Match_addr updated and renamed to Full address.")