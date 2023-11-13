@app.route("/data/<start>")
def data (start): 
    session = Session(engine)
    output = [
       func.min(Measurement.tobs), 
       func.max(Measurement.tobs), 
       func.avg(Measurement.tobs)]
    data_filter = session.query(*output).\
    filter(Measurement.date >= start).all()
    session.close()
    data_mod = list(np.ravel(output))
    return jsonify(data_mod)