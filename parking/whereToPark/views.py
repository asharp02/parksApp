from django.http import HttpResponse
import pymongo


client = pymongo.MongoClient("mongodb://localhost:27017/admin")
# Define Db Name
dbname = client["admin"]
collection = dbname["bylaws"]
print(client)
print(collection)

# def get_db_handle(db_name, host, port, username, password):

#  client = MongoClient(host=host,
#                       port=int(port),
#                       username=username,
#                       password=password
#                      )
#  db_handle = client['db_name']
#  return db_handle, client


# Create your views here.
def index(request):
    return HttpResponse(
        "<h1>Hello and welcome to my first <u>Django App</u> project!</h1>"
    )
