from app.model import Contest, ContestClass, Contestant, Pilot, Task

import requests
from datetime import datetime


def check_naviter_time():
    time_url = 'http://api.soaringspot.com/v1/time'
    r = requests.get(time_url)
    server_time = datetime.strptime(r.headers['X-Server-Time'], '%A, %d-%b-%Y %H:%M:%S %Z')
    local_time = datetime.utcnow()
    time_delta = (local_time - server_time).total_seconds()

    if time_delta > 300:
        raise Exception('Local time and server time differ too much')


def get_naviter_auth_string(client_id, secret):
    import hashlib
    import hmac
    import ssl
    import random
    import base64

    nonce = base64.b64encode(ssl.RAND_bytes(random.randint(12, 30))).decode('utf-8')
    created = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

    data = nonce + created + client_id
    signature = base64.b64encode(hmac.new(secret.encode('utf-8'), msg=data.encode('utf-8'), digestmod=hashlib.sha256).digest()).decode('utf-8')
    auth_string = 'http://api.soaringspot.com/v1/hmac/v1 ClientID="{0}", Signature="{1}", Nonce="{2}", Created="{3}"' \
        .format(client_id, signature, nonce, created)

    return auth_string


def get_naviter_document(url, client_id, secret):
    from hal_codec import HALCodec

    auth_string = get_naviter_auth_string(client_id, secret)
    r = requests.get(url, headers={'Authorization': auth_string})
    codec = HALCodec()
    document = codec.load(r.text.encode('utf-8'))

    return document


def document_to_objects(document, client_id, secret):
    objects = list()
    for item in document.items():
        if item[0] == "contests":
            for contest_row in item[1]:
                contest_dict = {'category': contest_row['category'],
                                'country': contest_row['country'],
                                'end_date': datetime.strptime(contest_row['end_date'], "%Y-%m-%d"),
                                'featured': contest_row['featured'],
                                'name': contest_row['name'],
                                'start_date': datetime.strptime(contest_row['start_date'], "%Y-%m-%d"),
                                'time_zone': contest_row['time_zone']}
                contest = Contest(**contest_dict)

                for contest_class_row in contest_row['classes']:
                    contest_class_dict = {'category': contest_class_row['category'],
                                          'type': contest_class_row['type']}
                    contest_class = ContestClass(**contest_class_dict)
                    contest_class.contest = contest
                    objects.append(contest_class)

                    contestants_doc = get_naviter_document(contest_class_row.links['contestants'].url, client_id, secret)
                    print(contestants_doc)
                    if 'code' in contestants_doc and contestants_doc['code'] == 404:
                        print("No task")
                    else:
                        for contestant_row in contestants_doc['contestants']:
                            contestant_dict = {'aircraft_model': contestant_row['aircraft_model'],
                                               'aircraft_registration': contestant_row['aircraft_registration'],
                                               'club': contestant_row['club'] if 'club' in contestant_row else None,
                                               'contestant_number': contestant_row['contestant_number'],
                                               'handicap': contestant_row['handicap'],
                                               'name': contestant_row['name'],
                                               'not_competing': contestant_row['not_competing'],
                                               'pure_glider': contestant_row['pure_glider'],
                                               'sponsors': contestant_row['sponsors'] if 'sponsors' in contestant_row else None}
                            contestant = Contestant(**contestant_dict)
                            contestant.contest_class = contest_class

                            for pilot_row in contestant_row['pilot']:
                                pilot_dict = {'civl_id': pilot_row['civl_id'],
                                              'email': pilot_row['email'],
                                              'first_name': pilot_row['first_name'],
                                              'igc_id': pilot_row['igc_id'],
                                              'last_name': pilot_row['last_name'],
                                              'nationality': pilot_row['nationality']}
                                pilot = Pilot(**pilot_dict)
                                pilot.contestant = contestant

                            objects.append(pilot)

                    tasks_doc = get_naviter_document(contest_class_row.links['tasks'].url, client_id, secret)
                    print(tasks_doc)
                    if 'code' in tasks_doc and tasks_doc['code'] == 404:
                        print("No task")
                    else:
                        for task_row in tasks_doc['tasks']:
                            task_dict = {'images': task_row['images'],
                                         'no_start': datetime.strptime(task_row['no_start'], "%Y-%m-%dT%H:%M:%S"),
                                         'result_status': task_row['result_status'],
                                         'start_on_entry': task_row['start_on_entry'],
                                         'task_date': task_row['task_date'],
                                         'task_distance': task_row['task_distance'],
                                         'task_distance_max': task_row['task_distance_max'],
                                         'task_distance_min': task_row['task_distance_min'],
                                         'task_duration': task_row['task_duration'],
                                         'task_number': task_row['task_number'],
                                         'task_type': task_row['task_type'],
                                         'task_value': task_row['task_value']}
                            task = Task(**task_dict)
                            task.contest_class = contest_class
                            objects.append(task)

                    objects.append(contestant)

                objects.append(contest)
    return objects