from multiprocessing import Process
import json
import time
import requests
from datetime import datetime
import pprint

# chainspace

from chainspaceapi import ChainspaceClient

from chainspacecontract.examples.zenroom_petition import contract as petition_contract
from chainspacecontract.examples import zenroom_petition


pp = pprint.PrettyPrinter(indent=4)

results = []

def pp_json(json_str):
    pp.pprint(json.loads(json_str))


def pp_object(obj):
    pp.pprint(obj)


def post_transaction(tx):
    start_tx = datetime.now()
    response = client.process_transaction(tx)
    client_latency = (datetime.now() - start_tx)
    print response.text
    json_response = json.loads(response.text)
    results.append((json_response['success'], response.url, tx['transaction']['methodID'], str(client_latency)))


start_time = datetime.now()

client = ChainspaceClient()

# Write private key into temp file
private_filepath = "/tmp/key.json"
f = open(private_filepath, "w")
f.write("""
{"private":"000000000000000000000000000000005ebdd5fd81b8242bebca178bc655d149e802b729d9dcd0af5cc7bbaf2f63b866"}
""")
f.close()


# set up options, participants, and tally's key
votes = ['YES', 'NO']
#gender = ['ANY', 'M', 'F', 'O']
#age = ['ANY', '0-19', '20-29', '30-39', '40+']
gender = []
age = []
district = ['ANY', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
options = ["%s-%s-%s-%s" % (v, g, a, d) for v in votes for g in gender for a in age for d in district]


init_transaction = zenroom_petition.init()

# pp_object(init_transaction)

post_transaction(init_transaction)

# pp_object(init_transaction)

petition_token = init_transaction['transaction']['outputs'][0]

print "\nCreate the petition\n"
tx_create_petition = petition_contract.create_petition((petition_token,), None, None, options, '/tmp/key.json')
post_transaction(tx_create_petition)
petition_root = tx_create_petition['transaction']['outputs'][1]


print "\nFirst signature\n"
tx_add_signature_1 = petition_contract.add_signature((petition_root,), None, None, "YES")
post_transaction(tx_add_signature_1)
signature_1 = tx_add_signature_1['transaction']['outputs'][0]

print "\nSecond signature\n"
tx_add_signature_2 = petition_contract.add_signature((signature_1,), None, None, "NO")
post_transaction(tx_add_signature_2)
signature_2 = tx_add_signature_2['transaction']['outputs'][0]

print "\nThird signature\n"
tx_add_signature_3 = petition_contract.add_signature((signature_2,), None, None, "YES")
post_transaction(tx_add_signature_3)
signature_3 = tx_add_signature_3['transaction']['outputs'][0]


# Tally the results
tx_tally = petition_contract.tally((signature_3,), None, None, '/tmp/key.json')

post_transaction(tx_tally)

pp_object(tx_tally)

end_time = datetime.now()

print "\n\nSUMMARY:\n"
all_ok = True
for result in results:
    print "RESULT: " + str(result)
    if not (result[0] == 'True'):
        all_ok = False

print "\n\nRESULT OF ALL CONTRACT CALLS: " + str(all_ok) + "\n"
print "Time Taken " + str(datetime.now() - start_time) + "\n\n"
