#Script for changing .xml 15 min data to 1 hour
import xml.etree.ElementTree as ET

tree = ET.parse('kaas.xml')
root = tree.getroot()
namespace = "{%s}" % root.tag.split('}')[0][1:]

timeseries_list = []

for timeseries in root.findall(namespace + "TimeSeries"):
    mrid = timeseries.find(namespace + "mRID").text
    business_type = timeseries.find(namespace + "businessType").text

    points = []
    period = timeseries.find(namespace + "Period")
    for point in period.findall(namespace + "Point"):
        position = point.find(namespace + "position").text
        quantity = point.find(namespace + "quantity").text
        points.append(quantity)
    
    #energytype = timeseries.find(namespace + "MktPSRType").find(namespace + "psrType")

    timeseries_data = {
        "mRID": mrid,
        "businessType": business_type,
        "points": points
    }
    timeseries_list.append(timeseries_data)

for ts in timeseries_list:
    print(ts)