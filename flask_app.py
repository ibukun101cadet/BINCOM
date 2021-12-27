from flask import Flask, render_template, request
import sqlite3
import socket
import pandas as pd
import datetime

app= Flask(__name__)
res =0

# conn = sqlite3.connect('csc455_HW3.db')
#
# with open('bincom_test.sql', 'r') as sql_file:
#     conn.executescript(sql_file.read())
#
# conn.close()

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/one/", methods = ['GET', 'POST'])
def quest_1():
    if request.method == 'POST':
        conn = sqlite3.connect("csc455_HW3.db")
        uniquepolid = request.form
        uid = uniquepolid['upi']
        cursor = conn.cursor()

        select_polling_unit_uniqueid = """SELECT polling_unit_uniqueid FROM announced_pu_results"""
        cursor.execute(select_polling_unit_uniqueid)
        idpol = cursor.fetchall()
        ids = [item for t in idpol for item in t]
        
        select_party_abbreviation = """SELECT party_abbreviation FROM announced_pu_results"""
        cursor.execute(select_party_abbreviation)
        partyname = cursor.fetchall()
        names = [item for t in partyname for item in t]
        dicts = {key: [] for key in names}
        for k, v in zip(names, ids):
            dicts[k].append(v)

        keyslist = list(dicts.values())

        select_party_score = """SELECT party_score FROM announced_pu_results"""
        cursor.execute(select_party_score)
        partyscore = cursor.fetchall()
        scores = [item for t in partyscore for item in t]

        dicts2 = {key: [] for key in names}
        for k, v in zip(names, scores):
            dicts2[k].append(v)
            
        vallist = list(dicts2.values())

        oya = []
        shee=[]
        def getindex(inp):
            for i in keyslist:
                if inp in i:
                    index_pos_list = get_index_positions(keyslist, i)
                    for a in list(index_pos_list):
                        shee.append(a)
            return(set(shee))
        def okay(sets, inp):
            for i in sets:
                if inp in i:
                    oya.append([i.index(inp)])
            return(oya)

        def get_index_positions(list_of_elems, element):
            
            index_pos_list = []
            index_pos = 0
            while True:
                try:
                    # Search for item in list from indexPos to the end of list
                    index_pos = list_of_elems.index(element, index_pos)
                    # Add the index position in list
                    index_pos_list.append(index_pos)
                    index_pos += 1
                except ValueError as e:
                    break
            return index_pos_list
        listc = []
        def get_keys_from_value(dicts,val):
            return [k for k, v in dicts.items() if val in v]
        def donezo(oyao):
            for i in oyao:
                listc.append(vallist[i[0]][i[1]])
            return listc

        keys = get_keys_from_value(dicts, uid)
        indexx = getindex(uid)
        yo = okay(keyslist, uid)

        result = [] 
        for i in yo: 
            if i not in result: 
                result.append(i) 
        keys = get_keys_from_value(dicts, uid)
        flat_list = [item for sublist in yo for item in sublist]
        list_c = [[x, y] for x, y in zip(list(indexx),flat_list)]
        doneo = donezo(list_c)

        
        conn.commit()
        cursor.close()

        res = "\n".join("{:} {:}".format(x, y) for x, y in zip(keys,doneo))

        # print(f"{row[2]} = {row[3]}")


    return render_template("q1.html", variable= res)


@app.route("/two/", methods=['GET', 'POST'])
def quest_2():
    show = False
    if request.method == "POST":
        note = ""
        show = True
        conn = sqlite3.connect("csc455_HW3.db")
        cursor = conn.cursor()
        # print(cursor)

        data = request.form
        lga_num = int(data['lga'])
        # print(type(lga_num))
        select_polling_unit_uniqueid = """SELECT polling_unit_uniqueid FROM announced_pu_results"""
        cursor.execute(select_polling_unit_uniqueid)
        idpol = cursor.fetchall()
        ids = [item for t in idpol for item in t]
        
        select_party_abbreviation = """SELECT party_abbreviation FROM announced_pu_results"""
        cursor.execute(select_party_abbreviation)
        partyname = cursor.fetchall()
        names = [item for t in partyname for item in t]
        dicts = {key: [] for key in names}
        for k, v in zip(names, ids):
            dicts[k].append(v)

        keyslist = list(dicts.values())

        select_party_score = """SELECT party_score FROM announced_pu_results"""
        cursor.execute(select_party_score)
        partyscore = cursor.fetchall()
        scores = [item for t in partyscore for item in t]

        dicts2 = {key: [] for key in names}
        for k, v in zip(names, scores):
            dicts2[k].append(v)
            
        vallist = list(dicts2.values())

        select_uniqueid = """SELECT uniqueid FROM polling_unit"""
        cursor.execute(select_uniqueid)
        uniqueid = cursor.fetchall()

        uniqueids = [item for t in uniqueid for item in t]

        select_lga_id = """SELECT lga_id FROM polling_unit"""
        cursor.execute(select_lga_id)
        lgaid = cursor.fetchall()
        lgaids = [item for t in lgaid for item in t]

        dictlga = {key: [] for key in lgaids}
        for k, v in zip(lgaids, uniqueids):
            dictlga[k].append(v)

        lgaidkeyslists = list(dictlga.keys())

        oyas = []
        sheet =[]
        def getlgaindexes(inp):
            if inp in lgaidkeyslists:
                alist = dictlga.get(inp)
                for i in alist:
                    oyas.append(i)
            return(oyas) 
        lgas = (getlgaindexes(lga_num))
        
        itch = []
        for i in lgas:
            for j in keyslist:
                if str(i) in j:
                    itch.append(keyslist.index(j))
        
        for i in keyslist:
                for j in lgas:
                    if str(j) in i:
                        sheet.append([i.index(str(j))])
                        
    
        flat_list = [item for sublist in sheet for item in sublist]
        list_c = [[x, y] for x, y in zip(itch,flat_list)]
    
        listad =[]
        for i in list_c:
            listad.append(vallist[i[0]][i[1]])

        res = sum(listad)
        if res == 0:
            res = 'Not available'
        
        
        return render_template("q2.html", show=show, res = res)
        

    return render_template("q2.html", show=show)

@app.route("/three/", methods=['GET', 'POST'])
def quest_3():
    show = False
    if request.method == "POST":
        show = True

        data = request.form
        pdp = int(data['pdp'])
        dpp = int(data['dpp'])
        acn = int(data['acn'])
        ppa = int(data['ppa'])
        cdc = int(data['cdc'])
        jp = int(data['jp'])
        anpp = int(data['anpp'])
        labo = int(data['labo'])
        cpp = int(data['cpp'])
        name = data['name']
        date = datetime.datetime.now()
        ip = socket.gethostbyname(socket.gethostname())
        # uniqueid = '29'
        # print(data)
        # print(f"{pdp}, {dpp}, {acn}, {ppa}, {cdc}, {jp}, {anpp}, {labo}, {cpp}")

        conn = sqlite3.connect("csc455_HW3.db")
        cursor = conn.cursor()

        num = 0
        for row in cursor.execute(f"SELECT * FROM announced_pu_results"):
            if num < row[0]:
                num = row[0]
            # print(row[0])
        id = num

        unique = 0
        for row in cursor.execute(f"SELECT * FROM announced_pu_results"):
            if unique < int(row[1]):
                unique = int(row[1])
            # print(row[0])
        uniqueid = unique + 1
        # print(uniqueid)

        mySql_insert_query = f"""INSERT INTO announced_pu_results (result_id, polling_unit_uniqueid,
                    party_abbreviation, party_score, entered_by_user, date_entered, user_ip_address)
                                    VALUES (?, ?, ?, ?, ?, ?, ?)
                                    """

        # cursor.execute(mySql_insert_query)

        records_to_insert = [((id+1), uniqueid, 'PDP', pdp, name, date, ip),
                             ((id+2), uniqueid, 'DPP', dpp, name, date, ip),
                             ((id+3), uniqueid, 'ACN', acn, name, date, ip),
                             ((id+4), uniqueid, 'PPA', ppa, name, date, ip),
                             ((id+5), uniqueid, 'CDC', cdc, name, date, ip),
                             ((id+6), uniqueid, 'JP', jp, name, date, ip),
                             ((id+7), uniqueid, 'ANPP', anpp, name, date, ip),
                             ((id+8), uniqueid, 'LABO', labo, name, date, ip),
                             ((id+9), uniqueid, 'CPP', cpp, name, date, ip)]
        cursor.executemany(mySql_insert_query, records_to_insert)

        polls = cursor.execute(f"SELECT * FROM announced_pu_results WHERE polling_unit_uniqueid = '{uniqueid}'")

        return render_template("q3.html", show=show, polls=polls)

    return render_template("q3.html", show=show)



if __name__ == '__main__':
    app.run(debug=True)

