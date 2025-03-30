import pandas
import arcpy
import geopandas


field_aliases = {
    'Is_this_service_device_publicly': 'Is_this_se',
    'Please_tell_us_when_the_service': 'Please_tel',
    'Other___Please_tell_us_when_the': 'Other___Pl',
    'General_comments_about_this_ser': 'General_co',
    'Please_select_the_type_of_devic': 'Please_sel',
    'Does_the_NaloxBox_have_a_rapid_': 'Does_the_N',
    'Is_the_rapid_response_kit_intac': 'Is_the_rap',
    'Is_the_NaloxBox_in_date_': 'Is_the_Nal',
    'Is_this_NaloxBox_easily_accessi': 'Is_this_Na',
    'If_the_NaloxBox_is_not_easily_a': 'If_the_Nal',
    'Is_there_a_sign_that_indicates_': 'Is_there_a',
    'Is_this_service_device_publicly_available_': 'Is_this__1',
    'Please_tell_us_when_the_service_is_publicly_available_': 'Please_t_1',
    'Other___Please_tell_us_when_the_service_is_publicly_available_': 'Other____1',
    'General_comments_about_this_service_': 'General__1',
    'Please_select_the_type_of_device': 'Please_s_1',
    'Does_the_NaloxBox_have_a_rapid_response_kit_': 'Does_the_1',
    'Is_the_rapid_response_kit_intact_': 'Is_the_r_1',
    'Is_this_NaloxBox_easily_accessible_': 'Is_this__2',
    'If_the_NaloxBox_is_not_easily_accessible__please_give_detailed_i': 'If_the_N_1',
    'Is_there_a_sign_that_indicates_the_location_of_the_NaloxBox_': 'Is_there_1',
    'Name_of_Location_Org__B1_E29A36': 'Name_of_Lo',
    'Naloxone_Supplier': 'Naloxone_S',
    'Address_of_NaloxBox': 'Address_of',
    'Naloxone_Supplier1': 'Naloxone_1',
    'Org_Facility': 'Org_Facili'
}

# Path to the File Geodatabase
output_gdb = r"C:\Users\l.dumarevskaya.ctr\ArcGIS projects\RISNER\data\CENSUS\Census_dataset\Census_dataset.gdb"


# Path to the output feature class
output_feature_class = f"{output_gdb}\\Combined_All_Points"

# Check if the feature class exists
if not arcpy.Exists(output_feature_class):
    print(f"❌ Error: The feature class '{output_feature_class}' does not exist.")
    exit()

# Get the field names in the feature class
field_names = [field.name for field in arcpy.ListFields(output_feature_class)]

# Print field names for debugging
print("Field names in the feature class:", field_names)

# Check if any fields in the feature class match the keys in the dictionary
for field in field_names:
    if field in field_aliases:  # Check if the field name matches a key in the alias dictionary
        alias = field_aliases[field]  # Get the corresponding alias
        try:
            # Apply the alias to the field
            arcpy.management.AlterField(output_feature_class, field, new_field_name=field, new_field_alias=alias)
            print(f"✅ Alias applied: {field} → {alias}")
        except Exception as e:
            print(f"❌ Failed to apply alias to '{field}': {e}")
    else:
        print(f"⚠️ No alias found for field '{field}', skipping.")

print("🎉 Aliases successfully updated in the feature class!")