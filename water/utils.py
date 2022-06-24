import frappe,json
import mysql.connector
from mysql.connector import Error
import pandas as pd
from decouple import config

class QGIS:
    def __init__(self,doc,geo_field):
        '''
        Initialize QGIS intergration class
        '''
        self.doc = doc
        self.geo_field = geo_field

    def extract_gis_data(self):
        '''
        Extract GIS data from QGIS
        '''
        pass
        geo_data_dict = json.loads(self.doc.__dict__.get(self.geo_field))
        #get features
        self.lat_long = geo_data_dict.get('features')[0].get('geometry').get('coordinates')

    def save_lat_long(self):
        '''
        Save the lat long data from frappe doctype to
        spatial table
        '''
        #add a try except block to enusure saving always work
        try:
            #now commit to the database
            doctype_name = "tab{}".format(self.doc.__dict__.get('doctype'))
            sql_str = """UPDATE `{}` SET geometry_field = ST_GeomFromText('POINT({} {})') WHERE name = '{}'""".format(doctype_name,self.lat_long[1],self.lat_long[0],self.doc.name)
            #create a database connection and sql query
            conn = create_db_connection()
            run_queries(conn,sql_str)
            frappe.db.sql(sql_str)
            frappe.db.commit()
        except Exception as e:
            print("An Error was encoutered:",e)

    def main(self):
        '''
        Function that calls both of the method in this class
        '''
        try:
            self.extract_gis_data()
            self.save_lat_long()
        except Exception as e:
            print("Error occured saving location to customer spatial table",e)

def run_queries(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
    except Error as err:
        print(f"Error: '{err}'")

def create_db_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host=config('database_host'),
            user=config('user_name'),
            passwd=config('database_password'),
            database=config('database_name')
        )
    except Error as err:
        print(f"Error: '{err}'")
    return connection

@frappe.whitelist(allow_guest = True)
def add_spatial_field_to_doctype(target_doctype,geometry_field,geolocation_value):
    '''
    Function that adds geometry field to a given doctype
    '''
    try:
        # convert the geojson field to a python dictionary and get lat,long
        geolocation_value = json.loads(geolocation_value)
        lat = geolocation_value.get('features')[0].get('geometry').get('coordinates')[1]
        lon = geolocation_value.get('features')[0].get('geometry').get('coordinates')[0]
        #generate sql query to add column and run the query
        sql_str = """ALTER TABLE `tab{}` ADD COLUMN {} GEOMETRY NOT NULL""".format(target_doctype,geometry_field)
        conn = create_db_connection()
        run_queries(conn, sql_str)
        #update the added column with a spatial index
        sql_str = """ALTER TABLE  `tab{}` ADD SPATIAL INDEX({})""".format(target_doctype,geometry_field)
        conn = create_db_connection()
        run_queries(conn, sql_str)
        #now set a default value for the column
        sql_str = """ALTER TABLE `tab{}` ALTER COLUMN {} SET DEFAULT ST_GeomFromText('POINT({} {})')"""\
            .format(target_doctype,geometry_field,lon,lat)
        conn = create_db_connection()
        run_queries(conn, sql_str)
        #return success message
        return {'status':True}
    except Exception as e:
        return {
            'status':False,
            'message':e
        }

def update_geometry_field(doc,geo_field):
    '''
    Function that be used on any doctype to update
    the geometry field using the values on the geolocation
    field on the same doctype
    input:
        doc - class instance of doctype
        geo_field - str
    '''
    instance = QGIS(doc,geo_field)
    instance.main()

def update_geometry_field_main(doc,geolocation_field):
	if doc.get(geolocation_field):
		qgis_instance = QGIS(doc,geolocation_field)
		#now extract gis data then save to database
		qgis_instance.main()

def enqueue_update_geometry_field(doc,geolocation_field):
    frappe.enqueue('water.utils.update_geometry_field_main',doc=doc,geolocation_field=geolocation_field)

def enqueue_long_job(doc,geo_field):
    frappe.enqueue('water.utils.update_geometry_field',doc=doc,geo_field=geo_field)



