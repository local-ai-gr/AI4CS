from flask import Flask, jsonify, request, make_response, redirect
from flask_cors import CORS
import psycopg2
from flask.json.provider import DefaultJSONProvider
from datetime import datetime, date
import flexpolyline
from werkzeug.routing import Rule
import json
import os

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['JSON_AS_ASCII'] = False
app.config['JSON_SORT_KEYS'] = False

app.url_rule_class = lambda path, **options: Rule('/api/' + path, **options)

class UpdatedJSONProvider(DefaultJSONProvider):
    def default(self, o):
        if isinstance(o, date) or isinstance(o, datetime):
            return o.strftime("%Y-%m-%d %H:%M:%S")
        return super().default(o)
app.json = UpdatedJSONProvider(app)
CORS(app)



@app.route("/")
def hello_world():
    return jsonify(status="ok!")


#AI4CS

@app.route("/getRecommendation", methods = ["POST","GET"])
def getRecommendation():
    data = request.get_json()
    postGISpoly=data.get('postGISpoly','')
    desiredHour=data.get('hour','') 

    connection = psycopg2.connect(
    host="db",
    database=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD")
    )
    cursor = connection.cursor()
    qry="""
    with asked_time as (select """+desiredHour+""" as t0)
    select 
    *,
    (case risk_evaluation when 'increase' then 2 when 'decrease' then 0.5 else 1 end)/((abs(ds_hour-t0)+1)*(forecasted_utilization+0.01)) score
    from
    (
    select 
    a.*,
    extract(hour from ds) ds_hour
    from
    (
        select 
        a.location_id,
        a.ds,
        case when forecasted_utilization<0 then 0 else forecasted_utilization end forecasted_utilization,
        b.location_friendlyname,
        b.geocode_string,
        b.lat,
        b.lon,
        rank() over (partition by a.location_id order by ds desc) rnk
        from 
        utilization_forecast a, 
        ht_cpn_station_locations b
        where a.location_id = b.location_id 
        and b.lat is not null
    ) a
    where rnk<25) forecast
    left outer join 
    ( select location_id,string_agg(recommender_color,',') donut_data from (
 select 
 u.location_id,
 u.ds_hour,
 u.forecasted_utilization,
 r.risk_evaluation,
 case 
 when risk_evaluation = 'increase' and forecasted_utilization<=5 then '0'
 when risk_evaluation = 'increase' and forecasted_utilization>5 then '1'
 else '2' end recommender_color
 from
 (select 
    a.*,
    extract(hour from ds) ds_hour
    from
    (
        select 
        a.location_id,
        a.ds,
        case when forecasted_utilization<0 then 0 else forecasted_utilization end forecasted_utilization,
        b.location_friendlyname,
        b.geocode_string,
        b.lat,
        b.lon,
        rank() over (partition by a.location_id order by ds desc) rnk
        from 
        utilization_forecast a, 
        ht_cpn_station_locations b
        where a.location_id = b.location_id 
        and b.lat is not null
    ) a
    where rnk<25) u,
    (select
    datetime,
    case when risk_evaluation = 'not_available' then 'increase' else risk_evaluation end risk_evaluation,
    extract(hour from datetime) datetime_hour
    from
    (
        select 
        datetime::timestamp,
        risk_evaluation,
        rank() over (order by datetime::timestamp desc) rnk
        from (select * from 
                (select datetime,risk_evaluation,rank() over (partition by datetime order by created_at::timestamp desc) rnk from energy_app_recommender
                where created_by = 'interoperable-recommender-inesctec') e where rnk = 1) e
    ) a
    where rnk<25) r
    where u.ds_hour = datetime_hour order by location_id,ds_hour) a
    group by location_id) d
    on (forecast.location_id = d.location_id)
    join
    (
    select
    datetime,
    case when risk_evaluation = 'not_available' then 'increase' else risk_evaluation end risk_evaluation,
    extract(hour from datetime) datetime_hour
    from
    (
        select 
        datetime::timestamp,
        risk_evaluation,
        rank() over (order by datetime::timestamp desc) rnk
        from (select * from 
                (select datetime,risk_evaluation,rank() over (partition by datetime order by created_at::timestamp desc) rnk from energy_app_recommender
                where created_by = 'interoperable-recommender-inesctec') e where rnk = 1) e
    ) a
    where rnk<25
    ) recommender on (forecast.ds_hour=recommender.datetime_hour)
    cross join
    asked_time
    where (
       forecast.ds_hour = (t0 - 2 + 24) % 24
    or forecast.ds_hour = (t0 - 1 + 24) % 24
    or forecast.ds_hour = t0
    or forecast.ds_hour = (t0 + 1) % 24
    or forecast.ds_hour = (t0 + 2) % 24
    )
    and st_intersects(st_setsrid(st_makepoint(lon,lat),4326),st_geomfromgeojson('
    """+postGISpoly+"""     
    '
    ) )
    order by score desc limit 5
    """
    cursor.execute(qry)

    row_headers = [x[0] for x in cursor.description]
    results = cursor.fetchall()
    cursor.close()
    connection.close()

    json_data = []
    for result in results:
        json_data.append(dict(zip(row_headers, result)))
        
    return jsonify(json_data), 200