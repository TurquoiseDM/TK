import csv
from SPARQL_utils import *
from utils import *


def get_info_from_s(prop, wde):
    header_list = ["s", "sLabel", "st_num", "typeLabel", "quantity", "unitLabel", "time", "st_temp"]
    skip = True
    error_list = []
    csv_path="./type_top10/"+prop+".csv"
    with open(csv_path, mode="r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        s_list=[]
        all_data=[]
        for row in reader:
            if (row["s"] == "http://www.wikidata.org/entity/Q155"):
                skip = False
            if skip:
                # print("skip " + row["ID"])
                continue
            s_list.append(row["s"].replace("http://www.wikidata.org/entity/", ""))

        s_list=list(set(s_list))
        slide_len = len(s_list) // 1000
        for i in range(0, len(s_list), slide_len):
            list_sparql = " ".join(["wd:" + my_item for my_item in
                                    s_list[i:i + slide_len]])
            my_sparql = """
                SELECT ?s ?sLabel ?st_num ?typeLabel ?quantity ?unitLabel ?time ?st_temp
                WHERE {
                VALUES ?s{"""+list_sparql+"""} 
                ?s <http://wikiba.se/ontology#statements> ?st_num. 
                ?s p:""" + prop + """ ?st_temp.
                OPTIONAL{
                ?st_temp pq:P585 ?time. 
                }
                ?st_temp psv:""" + prop + """ ?st. 
                ?st wikibase:quantityAmount ?quantity; 
                     wikibase:quantityUnit ?unit. 
                ?s wdt:P31 ?type. 
                SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
                 }
                """
            try:
                data_list = wde.query_db(my_sparql)
            except json.decoder.JSONDecodeError as Jde:
                print("json.decoder.JSONDecodeError " + str(i)+" "+str(i + slide_len))
                continue
            all_data+=data_list
            print(str(i)+" finished")
        with open("./data_property_st/" + prop + ".csv", mode="w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, header_list)
            writer.writeheader()
            writer.writerows(all_data)
            print(prop + " saved")


if __name__ == '__main__':
    wde = WDExecutor()
    #get_props_data(wde)
    # get_prop_instance(prop="P8049",wde=wde)
    #get_s2(wde)
    get_info_from_s("P8687",wde)
