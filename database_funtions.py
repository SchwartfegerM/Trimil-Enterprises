import sqlite3 as sql

def get_database_connection():
  #create the connection to the database
  conn = sql.connect('TrimilEnterprises.db')
  conn.row_factory = sql.Row
  return conn

def convert_to_binary_data(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData

def insert_image_to_database(image):
    #inserts binary data about a file into the sqlite3 database
    try:
        conn = get_database_connection()
        image_insert_query = """INSERT INTO BlogPosts (thumbnail) VALUES (?)""" #fix items in the {}
        thumbnail = convert_to_binary_data(image)
        conn.execute(image_insert_query,(thumbnail,))
        conn.commit()
        conn.close()
    except sql.Error as error:
        print("Failed to write blob data to sqlite table", error)
        #relay this to flask to display to user

def write_to_file(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)
    print("Stored blob data into: ", filename, "\n")

def read_images_from_database(id):
    #pulls binary data on files from the sqlite3 database
    try:
        conn = get_database_connection()
        sql_fetch_blob_query = """SELECT * from BlogPosts where id = ?""" 
        conn.execute(sql_fetch_blob_query, (id,))
        posts = conn.fetchall()
        for row in posts:
          #store the image name in the database upon conversion
          filename = row[9] # change to whatever row this ends up being
          image = row[3]

          imagepath = "\static\images\\" + filename + ".jpg"
          write_to_file(image, imagepath)
            

        conn.close()

    except sql.Error as error:
        print("Failed to read blob data from sqlite table", error)