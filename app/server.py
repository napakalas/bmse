import os
from sanic import Sanic
from sanic.response import json
from casbert import Searcher

# # for-development
# from utils.options import setup_options
# from utils.cors import add_cors_headers
# # end-development

SANIC_PREFIX = "SANIC_"

app = Sanic(name='Biosimulation_Model_IR')

"""Setting for searcher"""
searcher = Searcher()


@app.route("/searchPlots")
async def searchPlots(request):
    rs = searcher.searchPlots(request.args['query'][0], 100, 0.1)
    return json(rs)


@app.route("/search")
async def search(request):
    rs = searcher.searchVariables(request.args['query'][0], 100, 0.1)
    return json(rs)


@app.route("/dependencyMath")
async def dependencyMath(request):
    rs = searcher.getEntityDependencyMaths(request.args['varId'][0])
    return json(rs)


@app.route("/searchCellmls")
async def searchCellmls(request):
    rs = searcher.searchCellmls(request.args['query'][0], 100, 0.1)
    return json(rs)


@app.route("/searchSedmls")
async def searchSedmls(request):
    rs = searcher.searchSedmls(request.args['query'][0], 100, 0.1)
    return json(rs)


@app.route("/searchImages")
async def searchImages(request):
    rs = searcher.searchImages(request.args['query'][0], 200, 0.1)
    return json(rs)


@app.route("/searchComponents")
async def searchComponents(request):
    rs = searcher.searchComponents(request.args['query'][0], 100, 0.1)
    return json(rs)


@app.route("/getMaths")
async def getMaths(request):
    if 'varId' in request.args:
        rs = searcher.getEntityMaths(varIds=request.args['varId'][0])
    elif 'compId' in request.args:
        rs = searcher.getEntityMaths(compId=request.args['compId'][0])
    return json(rs)


@app.route("/getComponentCode")
async def getComponentCode(request):
    if 'varId' in request.args:
        rs = searcher.getComponentCode(varId=request.args['varId'][0])
    elif 'compId' in request.args:
        rs = searcher.getComponentCode(compId=request.args['compId'][0])
    return json(rs)


@app.route("/teaching")
async def teaching(request):
    return json({'a': 100})

if __name__ == "__main__":
    for k, v in os.environ.items():
        if k.startswith(SANIC_PREFIX):
            _, config_key = k.split(SANIC_PREFIX, 1)
            app.config[config_key] = v
    app.run(host="0.0.0.0", port=8000, debug=False, workers=4)
