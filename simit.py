#!/usr/bin/python2
"""Simit: A web frontend for SimulationCraft"""
import subprocess
import os
import time
import multiprocessing
from flask import Flask, render_template, request

SIMC_BINARY = "/home/sim/simc-release-710-01/engine/simc" #path to simc binary
CACHE_TIME = 60 #time to cache results in seconds

SIMIT = Flask(__name__)

@SIMIT.route("/")
def home():
    return render_template("index.html")

@SIMIT.route("/submit", methods=['POST'])
def submit():
    if (len(request.form['character']) != 0) and (len(request.form['realm']) != 0):
        return sim(request.form['realm'], request.form['character'])
    return "meep"

@SIMIT.route("/<realm>/<character>")
def sim(realm, character):
    """Simulate combat for character on realm"""
    output_file = "report/{}-{}.html".format(realm, character)
    output_json = "report/{}-{}.json".format(realm, character)
    try:
        result_mtime = os.path.getmtime(output_file)
        if time.time() - result_mtime <= CACHE_TIME:
            cached = True
        else:
            cached = False
    except OSError:
        cached = False
    if not cached:
        try:
            subprocess.check_output(
                [
                    SIMC_BINARY,
                    "armory={},{}".format(realm, character),
                    "html={}".format(output_file),
                    "threads={}".format(multiprocessing.cpu_count() / 2),
                    "calculate_scale_factors=1",
                    "json={}".format(output_json)
                ]
            )
        except subprocess.CalledProcessError:
            return "There was an error running simc"
    with open(output_file, 'r') as file_handle:
        sim_html = file_handle.read()
    return sim_html

if __name__ == "__main__":
    SIMIT.run(host='0.0.0.0', debug=True)
