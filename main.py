import geopandas as gpd
import joblib
import pandas as pd
from flask import Flask
from flask import jsonify
from flask import request

from config import config


def create_app(arg_environment):
    local_app = Flask(__name__)
    local_app.config.from_object(arg_environment)
    return local_app


environment = config['development']
app = create_app(environment)
gdf = gpd.read_file('data/Catastro_gdb.geojson')

hurtos_groups = pd.read_csv('data/medellin_hurtos_groups.csv')
features = ['hurtos_peligrosos', 'hurtos_no_peligrosos', 'hurtos_a_mujeres', 'hurtos_a_hombres',
            'hurtos_en_transporte_publico', 'hurtos_en_transporte_particular', 'hurtos_en_via_publica', 'hurtos_niños',
            'hurtos_jovenes', 'hurtos_adultos', 'hurtos_adultos_mayores', 'hurtos']
X = hurtos_groups[features]


@app.route('/ping', methods=['GET'])
def get_ping():
    return 'pong'


@app.route('/predict', methods=['POST'])
def post_predict():
    args = request.args
    args = args.to_dict()
    clusters_quantity = args.get('clusters_quantity')

    model = joblib.load('models/km' + clusters_quantity + '.joblib')
    results = model.predict(X.values)
    results = pd.DataFrame([X.index, results]).T

    df_temp = hurtos_groups.join(results)
    clustered_df = pd.DataFrame()
    clustered_df['cluster'] = df_temp[1]
    clustered_df['codigo_barrio'] = df_temp['codigo_barrio']

    barrios = []
    for index, row in clustered_df.iterrows():
        barrios.append({
            'barrio': row['codigo_barrio'],
            'cluster': row['cluster']
        })

    return jsonify({'barrios': barrios})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
