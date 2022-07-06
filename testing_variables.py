posts = [{"id":1,"title":"Starting your project the right way","url":"/blog/starting"},{"id":2,"title":"bankruptcy made easy","url":"/blog/bankrupt"}]

posts_list_full_items = [
    {
        "id":1,
        "title":"Starting your project the right way",
        "url":"/blog/starting",
        "thumbnail":"\images\lake.jpg",
        "date":"12/4/2022",
        "summary":"how to start a good project",
        "body":"this is some highly important text about the above topic pretaining to this topic is really easy for me and you can clearly see this through the writing in this blog post"
    },
    {
        "id":2,
        "title":"Ending your project the right way",
        "url":"/blog/ending",
        "thumbnail":"\images\lake.jpg",
        "date":"15/5/2022",
        "summary":"how to finish your project and move to marketing",
        "body":"this is some highly important text about the above topic pretaining to this topic is really easy for me and you can clearly see this through the writing in this blog post"
    }
]

# INSERT INTO Login(ID,Username,Password) VALUES(1,'ADMIN','ADMIN1'); 
import sqlite3 as sql

if __name__ == "__main__":
  conn=sql.connect("TrimilEnterprises.db")
  cursor= conn.cursor()
  username="ADMIN"
  stuff = cursor.execute("SELECT * FROM Login WHERE Username = ?", (username,)).fetchall()
  if stuff[0][2] == "ADMIN1":
    print("good")
  conn.commit()
  conn.close()
  