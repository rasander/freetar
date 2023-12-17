from flask import Flask, render_template, request, jsonify

from ug import ug_search, ug_tab
import waitress

app = Flask(__name__)

favs_data_file = "/app/data/favs.json"

@app.route("/")
def index():
    return app.redirect("/favs",code=302)
#    return render_template("index.html")


@app.route("/search")
def search():
    search_term = request.args.get("search_term")
    if search_term:
        search_results = ug_search(search_term)
    else:
        search_results = []
    return render_template("index.html",
                           search_term=search_term,
                           title=f"Freetar - Search: {search_term}",
                           search_results=search_results,)


@app.route("/tab/<artist>/<song>")
def show_tab(artist: str, song: str):
    tab = ug_tab(f"{artist}/{song}")
    return render_template("index.html",
                           tab=tab,
                           title=f"{tab.artist_name} - {tab.song_name}")


@app.route("/tab/<tabid>")
def show_tab2(tabid: int):
    tab = ug_tab(tabid)
    return render_template("index.html",
                           tab=tab,
                           title=f"{tab.artist_name} - {tab.song_name}")


@app.route("/")
@app.route("/favs")
def show_favs():
    return render_template("index.html",
                           title="Freetar - Favorites",
                           favs=True)


@app.route("/api/favs", methods=['GET'])
def api_get_favs():
    app.logger.debug("api_get_favs: start")
    try:
        with open(favs_data_file) as f:
            content = f.read()
            #app.logger.debug("api_get_favs: ", str(content))
            return content, 200
    except Exception as e:
        app.logger.error("api_get_favs: Exception occurred", e)
        return "", 500



@app.route("/api/favs", methods=['POST'])
def api_store_favs():
    try:
        
        #json_data = json.loads(request.data)
        content = request.data.decode("utf-8")

        f = open(favs_data_file, "w")
        f.write(content)
        f.close()
        return "", 204
    except:
        app.logger.error("api_store_favs: Exception occurred", e)
        return "", 500



def main():
    host = "0.0.0.0"
    port = 8080
    if __name__ == '__main__':
        app.run(debug=True,
                host=host,
                port=port)
    else:
        print(f"Running backend on {host}:{port}")
        waitress.serve(app, listen=f"{host}:{port}")


if __name__ == '__main__':
    main()
