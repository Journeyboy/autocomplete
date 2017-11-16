import redis
import pysolr
from flask import Flask, Response
from flask_restful import reqparse, Resource, Api
#from flask.ext.cors import CORS


solr = pysolr.Solr('http://35.184.52.104:8983/solr/products', timeout=10)
r = redis.StrictRedis(host='redis-slave', port=6379, db=0)
w = redis.StrictRedis(host='redis-master', port=6379, db=0)

app = Flask(__name__)
#CORS(app)
api = Api(app)

parser = reqparse.RequestParser()


def redis(term):
    r.zadd('autocomplete',0,prefix)
    r.zadd('autocomplete',0,n+"%")


class Search(Resource):

    def get(self):
        #import pdb; pdb.set_trace()
        print("Call for GET /search")
        parser.add_argument('q')
        query_string = parser.parse_args()
        print(query_string)
        #search_elements = query_string['q'].replace(":"," ")
        elements = query_string['q'].split(':')
        search_elements = []
        for e in elements:
            search_elements.append('name:'+e)
        print(search_elements)
        results = solr.search(q=search_elements, fl='name', sort='score desc')
        products = [o['name'][0] for o in results]
        return products

api.add_resource(Search, '/v1/api/search')
app.run(debug=True)