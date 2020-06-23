
import mariadb
import json
import requests
from bs4 import BeautifulSoup


def main():
    comp_sci_url = "cs.ubbcluj.ro"
    about_url = "http://www.cs.ubbcluj.ro/despre-facultate/structura/departamentul-de-informatica/"
    db_name = "ubbcluj"

    username = None
    password = None

    json_obj = None
    with open("credentials.json", 'r') as crd_json_fd:
        json_text = crd_json_fd.read()
        json_obj = json.loads(json_text)

    credentials = json_obj["Credentials"]
    username = credentials["username"]
    password = credentials["password"]

    # region connect_to_db
    table_name = "humanoid_entities"
    mariadb_connection = mariadb.connect(user=username, password=password, database=db_name)
    mariadb_cursor = mariadb_connection.cursor()
    # endregion

    # region cache_request
    data = None
    try:
        with open("cached_request.html", 'r', encoding='utf-8') as req_fd:
            data = req_fd.read()
            print("Did not request.")
    except:
        with open("cached_request.html", 'w', encoding='utf-8') as req_fd:
            data = requests.get(about_url).text
            print("Request was sent.")
            req_fd.write(data)
    # endregion cache_request

    soup = BeautifulSoup(data, 'html.parser')
    divs = soup.find_all(attrs={"style": "margin-bottom: 15px; margin-right: 15px; width: 630px; height: 135px;"})

    for line in divs:
        subdiv = line.find_all(attrs={"style": "vertical-align: middle; text-align: left; display: table-cell; padding-left: 12px; padding-right: 12px; height: 133px; width: 503px; border-top: 1px solid #dddddd; border-bottom: 1px solid #dddddd; border-right: 1px solid #dddddd"})

        joined_str = "".join([str(k) for k in subdiv[0].contents])

        fields = joined_str.split("<br/>")
        init_dict = {}

        for field in fields:
            key = field.split(": ")
            if (len(key) > 1):
                if key[0].lstrip() == "Web":
                    parsed_url = BeautifulSoup(key[1], 'html.parser')

                    init_dict[key[0].lstrip()] = parsed_url.find_all('a')[0]["href"]
                else:
                    init_dict[key[0].lstrip()] = key[1].lstrip()

        name = fields[0].split(',')[0]
        title = fields[0].split(',')[1].split("<em>")[1].rstrip("</em>\n") if "<em>" in fields[0] else "EMPTY"

        print(name + ":::" + title)
        print(init_dict)
        print()

        insert_string = "INSERT INTO humanoid_entities SET "
        insert_string += "FullName=\'{0}\', ".format(name)
        insert_string += "Title=\'{0}\', ".format(title)
        insert_string += "eMail=\'{0}\', ".format(init_dict["E-mail"] if "E-mail" in init_dict.keys() else "EMPTY")
        insert_string += "Website=\'{0}\', ".format(init_dict["Web"] if "Web" in init_dict.keys() else "EMPTY")
        insert_string += "Address=\'{0}\', ".format(init_dict["Adresa"] if "Adresa" in init_dict.keys() else "EMPTY")
        insert_string += "Interests=\'{0}\'".format(init_dict["Domenii de interes"] if "Domenii de interes" in init_dict.keys() else "EMPTY")

        try:
            mariadb_cursor.execute(insert_string)
        except mariadb.ProgrammingError as pe:
            print("Error")
            raise pe
        except mariadb.IntegrityError:
            continue

    mariadb_connection.close()


if __name__ == '__main__':
    main()
