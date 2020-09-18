import pickle
import expclass

with open("data.dat", "rb") as f:
    experiidata = pickle.load(f)

el=experiidata.get_explist()
# print(el)
for i in el:
    print(i.get_subject().get_bday())
    # print(type())
