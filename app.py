# Import the Flask framework
from pydoc import pager
from flask import Flask, render_template, jsonify, request, url_for
import graphs_advanced
import graphs
import time
import threading
#from flask_mysqldb import MySQL

app = Flask(__name__)
name = "Joe"
age = 23
jobs = ["PA", "DS", "SF"]
lock = threading.Lock()

@app.route("/")
def home():
    return render_template("index.html")  # Renders the HTML file , age=age,name=name,jobs=jobs

@app.route("/g_a_r")
def gar():
    # year = request.args.get('year')
    # gas = request.args.get('gas')
    # data = graphs_advanced.create_table(2023, 'co2e_100yr')
    # countries = data[0]
    # capita = data[1]
    # emissions = data[2]
    # combined_list = list(zip(countries, emissions, capita))
    return render_template("g_a_r.html" )#, combined_list=combined_list)  # Renders the HTML file

# @app.route("/g_a_r1")
# def gar1():
#     time.sleep(3)
#     with lock:
#         year = request.args.get('year')
#         gas = request.args.get('gas')
#         data = graphs_advanced.create_table(year, gas)
#         countries = data[0]
#         capita = data[1]
#         emissions = data[2]
#         combined_list = list(zip(countries, emissions, capita))
    
#     return jsonify(combined_list)
    #return jsonify({"result": combined_list})  
@app.route("/g_a_r1")
def gar1():
    time.sleep(3)
    with lock:
        year = request.args.get('year')
        gas = request.args.get('gas')
        sort_key = request.args.get('sort_key', 'emissions')
        data = graphs_advanced.create_table(year, gas, sort_key)
        countries = data[0]
        capita = data[1]
        emissions = data[2]
        combined_list = list(zip(countries, emissions, capita))
    return jsonify(combined_list)


@app.route("/data")
def data():
    return render_template("data_analysis.html")  # Renders the HTML file

@app.route("/conc")
def conc():
    # c = request.args.get('c')
    # target = graphs_advanced.generate_targets(c)
    return render_template("conc.html") # Renders the HTML file , cut = cut, sector = sector

@app.route("/conc1")
def conc1():
    time.sleep(3)
    with lock:
        c = request.args.get('c')
        target = request.args.get('year')
        target = int(target)
        cut = graphs_advanced.calculate_cut(c, target)
    return jsonify({"result": f"You need to cut your emisions by {cut} every year"})

@app.route("/calculate_sector")
def calc_sector():
    time.sleep(3)
    with lock:
        c = request.args.get('c')
        sector = graphs_advanced.calculate_sector(c)
    return jsonify({"result": f"Your highest sector is {sector} we reccommend you try reduce your emissions in this sector"})

@app.route("/useless", methods=["POST", "GET"])
def useless():
    # if request.method == "POST":
    #     user = request.form["nm"]
    #     print(user)
    #     return user
    # else:
    return render_template("useless.html")
    #return render_template("useless.html")  

@app.route("/bar_chart.html")
def growth_rate_chart():
    return render_template("bar_chart.html")

@app.route("/emissions.html")
def emissions():
    return render_template("emissions.html")

@app.route("/animation.html")
def animation():
    return render_template("animation.html")

@app.route("/pie_chart.html")
def pie_chart():
    return render_template("pie_chart.html")

@app.route("/emissions_projected.html")
def emissions_projected():
    return render_template("emissions_projected.html")

@app.route('/calculate_result')
def calculate_result():
  with lock:
    c = request.args.get('c')
    filename = graphs_advanced.generate_bar(c)
  return jsonify({"result":filename})

@app.route('/generate_pie')
def generate_pie():
  with lock:
    gas = (request.args.get('gas'))
    year = (request.args.get('year'))
    filename = graphs_advanced.generate_pie_chart(gas, year)
  return jsonify({"result":filename})

@app.route('/generate_graph')
def generate_graph():
  with lock:
    # generate html page
    c = request.args.get('c')
    year = request.args.get('year')
    filename = graphs_advanced.generate_projections(c, year)
  return jsonify({"result":filename})

@app.route('/pick_country')
def pick_country():
  # generate html page
  c = request.args.get('c')
  filename = graphs_advanced.generate_graph(c)
  return jsonify({"result":filename})

@app.route('/generate_animation')
def generate_animation():
  # generate html page
  filename = graphs_advanced.generate_animation()
  return jsonify({"result":filename})

if __name__ == "__main__":
    app.run(debug=True)
    #app.run(host='127.0.0.1', port=6009, debug=False)
